from django import forms
from comments.models import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'email', 'url', 'text']

        wedgets = {
            'name': forms.TextInput(attrs={
                'placeholder': "名字",
            }),
            'emali': forms.TextInput(attrs={
                'placeholder': "邮箱",
            }),
            'url': forms.TextInput(attrs={
                'placeholder': "网址",
            }),
        }


class AddForm(forms.Form):
    a = forms.IntegerField()
    b = forms.IntegerField()
