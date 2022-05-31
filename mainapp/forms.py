from django import forms

from mainapp.models import SNPosts, SNSections


class SNPostForm(forms.ModelForm):
    class Meta:
        model = SNPosts
        fields = ('name', 'text', 'image', 'short_desc', 'description', 'is_active')


    # def __init__(self, *args, **kwargs):
    #     super(SNUserLoginForm, self).__init__(*args, **kwargs)
    #     for field_name, field in self.fields.items():
    #         field.widget.attrs['class'] = 'form-control'
    #         field.help_text = ''


# class SNUserRegisterForm(UserCreationForm):
#     class Meta:
#         model = SNUser
#         fields = ('username', 'first_name', 'last_name', 'avatar', 'email', 'age', 'password1', 'password2')
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         for field_name, field in self.fields.items():
#             field.widget.attrs['class'] = 'form-control'
#             field.help_text = ''
#
#     def save(self, *args, **kwargs):
#         user = super().save(*args, **kwargs)
#         user.is_active = True
#         user.save()
#         return user


# class SNUserEditForm(UserChangeForm):
#     class Meta:
#         model = SNUser
#         fields = ('username', 'first_name', 'last_name', 'patronymic', 'avatar', 'email', 'age',)
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         for field_name, field in self.fields.items():
#             field.widget.attrs['class'] = 'form-control'
#             field.help_text = ''
#             if field_name == 'password':
#                 field.widget = forms.HiddenInput()
#
#
# class SNUserProfileEditForm(forms.ModelForm):
#     class Meta:
#         model = SNUserProfile
#         exclude = ('user',)
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         for field_name, field in self.fields.items():
#             field.widget.attrs['class'] = 'form-control'
#             field.help_text = ''


