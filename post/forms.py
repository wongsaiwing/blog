from django import forms
from .models import Post

# allow users publish posts using forms
class PostForm(forms.ModelForm):
    
    class Meta:
        model = Post
        fields = ('title', 'body', 'tags')