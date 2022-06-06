from django import forms

from authapp.models import SNUser
from blogapp.models import SNPosts, SNSections


class SNPostForm(forms.ModelForm):

    class Meta:
        model = SNPosts
        fields = ('name', 'text', 'section', 'image')

    # user = forms.ModelChoiceField(
    #     queryset=SNUser.objects.all(),
    #     widget=forms.HiddenInput(),
    #     label='Автор',
    #     required=False,
    # )
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''
