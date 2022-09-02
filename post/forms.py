from django import forms
from post.models import *

class NewPostForm(forms.ModelForm):
    picture= forms.ImageField(widget= forms.FileInput
                            (attrs={'class':'file-input'}), required=True)
    caption= forms.CharField(max_length=1500,
                            widget= forms.Textarea
                            (attrs={'class':'textarea is-medium', 'placeholder': 'Caption'}), required=True)
    tags= forms.CharField(max_length=200,
                            widget= forms.TextInput
                            (attrs={'class':'input is-medium', 'placeholder': 'Tags'}), required=True)

    class Meta:
        model = Post
        fields = {
            'picture', 'caption', 'tags'
        }