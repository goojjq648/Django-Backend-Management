from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from google.auth.transport.requests import Request
from google.oauth2 import id_token
import json
from django.conf import settings
from google.auth import exceptions

@csrf_exempt  # 禁用 CSRF 检查
def google_callback(request):
    data = json.loads(request.body)
    id_token_from_google = data.get('id_token')

    try:
        # 驗證 id_token
        id_info = id_token.verify_oauth2_token(
            id_token_from_google, Request(), settings.GOOGLE_CLIENT_ID)

        user_id = id_info['sub']
        user_email = id_info['email']

        # user, created = User.objects.get_or_create(email=user_email)

        response = {'message': 'Login successful', 'user_id': user_id, 'email': user_email}
        response['Cross-Origin-Opener-Policy'] = 'same-origin-allow-popups'

        # 返回用户信息或成功消息
        return JsonResponse(response)

    except ValueError:
        print("id_info:", id_info)
        return JsonResponse({'error': 'Invalid ID Token'}, status=400)
    except exceptions.GoogleAuthError:
        return JsonResponse({'the issuer is invalid.'}, status=400)

