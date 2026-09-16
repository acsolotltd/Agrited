from django import forms

class BulkEmailForm(forms.Form):
    subject = forms.CharField(
        max_length=255, 
        required=True, 
        widget=forms.TextInput(attrs={'class': 'vTextField', 'style': 'width: 100%;'})
    )
    message = forms.CharField(
        required=True, 
        widget=forms.Textarea(attrs={'rows': 10, 'class': 'vLargeTextField', 'style': 'width: 100%;'})
    )