from django import forms

class PostForm(forms.Form):
    post = forms.CharField(label="", widget=forms.Textarea(attrs={'placeholder': 'What do you want to post about?'}))
    

