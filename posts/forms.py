from django import forms
from .models import Post, Comment


class PostForm(forms.ModelForm):
    title = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': '제목을 입력하세요'
            }
        ),
    )
    select1_content = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': '선택지 1',
            }
        ),
    )
    select2_content = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': '선택지 2',
            }
        ),
    )
    image1 = forms.ImageField(
        widget=forms.FileInput(
            attrs={
                'class': 'form-control',
            }
        ),
    )
    image2 = forms.ImageField(
        widget=forms.FileInput(
            attrs={
                'class': 'form-control',
            }
        ),
    )
    class Meta:
        model = Post
        fields = ('title', 'select1_content', 'image1', 'select2_content', 'image2',)