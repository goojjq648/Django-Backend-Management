from django import forms

class BaseModelLabelForm(forms.ModelForm):
    def render_field_with_label(self, field_name):
        field = self[field_name]

        widget_attrs = self.fields[field_name].widget.attrs
        field_name_value = widget_attrs.get('name', field_name)  # 如果沒有配置 id，就使用字段名作為 id
        show_alert = widget_attrs.get('data-alert', False)  # 默認不生成 alert
        error_html = ""
        if show_alert == "true":
            error_html = f'<div id="alert_{field_name_value}" class="text-danger"></div>'

        # 自動生成 label 和 field
        return f'''
            <div class="mb-3" data-field="{field_name}">
                <label for="{field.id_for_label}" class="form-label">{field.label}</label>
                {field}
                {error_html}
            </div>
        '''
    
    # 通用方法：渲染所有字段
    def render_all_fields(self):
        rendered_fields = ""
        for field_name in self.fields:
            rendered_fields += self.render_field_with_label(field_name)
        return rendered_fields