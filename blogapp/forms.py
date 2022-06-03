from django import forms

from blogapp.models import SNPosts, SNSections


class SNPostForm(forms.ModelForm):
    class Meta:
        model = SNPosts
        fields = ('name', 'text', 'section', 'image', 'user')


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''
