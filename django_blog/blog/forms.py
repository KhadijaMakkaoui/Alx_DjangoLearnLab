from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Comment, Post
from taggit.forms import TagWidget

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
    
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'tags']  # Add 'tags' to the fields
        widgets = {
            'tags': TagWidget(),  # Use the TagWidget to render the tags field
        }

    def save(self, commit=True):
        post = super().save(commit=False)
        tags = self.cleaned_data['tags']
        if commit:
            post.save()
            if tags:
                tag_list = [Tag.objects.get_or_create(name=tag.strip())[0] for tag in tags.split(',')]
                post.tags.set(tag_list)
        return post