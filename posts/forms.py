from django import forms
from .models import Post, Image

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['text', ]

class ImageForm(forms.ModelForm):
    image = forms.ImageField(label='image')
    class Meta:
        model = Image
        fields = ['image', ]