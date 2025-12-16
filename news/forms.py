from django import forms
from .models import Post


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ['title', 'text', 'author', 'categories']


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['text'].widget = forms.Textarea(attrs={'rows': 4})
        self.fields['categories'].widget = forms.CheckboxSelectMultiple()
        self.fields['categories'].required = False