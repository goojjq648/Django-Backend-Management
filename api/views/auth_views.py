import json
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

from google.auth.transport.requests import Request
from google.oauth2 import id_token
from google.auth import exceptions

from user.models import UserUserprofile
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from api.serializers import UserUserprofileSerializer, UserSerializer

from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken


def get_user_response(user_profile):
    if user_profile is None:
        return None

    tokens = RefreshToken.for_user(user_profile.user)
    user_profile_data = UserUserprofileSerializer(user_profile).data
    if user_profile_data is None or tokens is None:
        return None
    
    user_data = dict(user_profile_data['user'])

    if user_profile_data['google_id'] is not None:
        user_data['googleLinked'] = True
        user_data['avatar_url'] = user_profile.avatar_url
    else:
        user_data['googleLinked'] = False

    return {
        'user': user_data,
        'tokens': {
            'refresh': str(tokens),
            'access': str(tokens.access_token),
        }
    }


class UserLoginViewSet(APIView):
    queryset = UserUserprofile.objects.all()
    serializer_class = UserUserprofileSerializer

    """
    使用者登入
    """

    def post(self, request, *args, **kwargs) -> Response:
        try:
            email = request.data.get('email')
            password = request.data.get('password')

            if not email or not password:
                return Response({'error': '請輸入帳號或密碼'}, status=status.HTTP_400_BAD_REQUEST)

            user = authenticate(request, username=email,
                                password=password)  # 自動處理密碼加密比對

            if user is not None:
                user_profile = UserUserprofile.objects.get(user=user)
                response_data = get_user_response(user_profile)

                if response_data is None:
                    return Response({'error': '使用者登入失敗'}, status=status.HTTP_401_UNAUTHORIZED)

                return Response(response_data, status=status.HTTP_200_OK)
            else:
                return Response({'error': '帳號或密碼錯誤'}, status=status.HTTP_401_UNAUTHORIZED)

        except Exception as e:
            return Response({'error': f"登入失敗:{str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserRegisterViewSet(viewsets.ModelViewSet):
    queryset = UserUserprofile.objects.all()
    serializer_class = UserUserprofileSerializer # 預設使用的serializer
    http_method_names = ['post']  # 限制只開 POST

    """
    使用者註冊後自動登入
    """

    def create(self, request, *args, **kwargs) -> Response:
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user_profile = self.perform_create(serializer)

        response_data = get_user_response(user_profile)

        return Response(response_data, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        user = serializer.save(role='user')
        return user

@csrf_exempt  # 禁用 CSRF 檢查
def google_callback(request) -> JsonResponse:
    data = json.loads(request.body)
    id_token_from_google = data.get('id_token')

    try:
        # 驗證 id_token
        id_info = id_token.verify_oauth2_token(
            id_token_from_google, Request(), settings.GOOGLE_CLIENT_ID)

        google_id = id_info['sub']
        user_email = id_info['email']
        name = id_info.get('name', '')
        avatar_url = id_info.get('picture', '')

        print(
            f'google_id: {google_id} user_email: {user_email} name: {name} avatar_url: {avatar_url}')
        
        # 檢查是否已經存在email，若有直接登入
        if User.objects.filter(email=user_email).exists():
            if UserUserprofile.objects.filter(google_id=google_id).exists() == False:
                # 先擋掉
                return JsonResponse({'error': 'Email已經被註冊過 請先連結google帳號'}, status=400)
                
        # 檢查是否已經存在google_id
        try:
            profile_data = UserUserprofile.objects.get(google_id=google_id)
        except UserUserprofile.DoesNotExist:
            # 創建新使用者
            user_data = {
                'email': user_email,
                'username': f'google_{google_id[:8]}',
                'password': User.objects.make_random_password()
            }

            profile_data = {
                'user': user_data,
                'google_id': google_id,
                'avatar_url': avatar_url,
                'role': 'user'
            }
        
            profile_serializer = UserUserprofileSerializer(data=profile_data)
            profile_serializer.is_valid(raise_exception=True)
            user = profile_serializer.save()
            print(f'Registered user: {user}')  # 印出使用者user
        
        # 使用者登入
        response_data = get_user_response(profile_data)
        if response_data is None:
            return JsonResponse({'error': 'Google Register failed'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
        response_data['message'] = 'Google Register/Login successful'
        response_data['Cross-Origin-Opener-Policy'] = 'same-origin-allow-popups'

        return JsonResponse(response_data, status=status.HTTP_200_OK)

    except ValueError as e:
        print(f'Google error :{e}')
        return JsonResponse({'error': 'Invalid ID Token'}, status=status.HTTP_400_BAD_REQUEST)
    except exceptions.GoogleAuthError:
        return JsonResponse({'the issuer is invalid.'}, status=status.HTTP_400_BAD_REQUEST)
