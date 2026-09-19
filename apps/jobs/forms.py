from django import forms

class JobApplicationForm(forms.Form):
    first_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-input'}))
    last_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-input'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-input'}))
    phone = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'class': 'form-input'}))
    cv = forms.FileField(
        label="Upload CV",
        help_text="Accepted formats: PDF, DOCX",
        widget=forms.FileInput(attrs={'accept': '.pdf,.doc,.docx'})
    )
    cover_letter = forms.CharField(
        required=False, 
        widget=forms.Textarea(attrs={'rows': 4, 'class': 'form-input'})
    )