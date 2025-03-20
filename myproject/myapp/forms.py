from django import forms
from .models import Product, DesignRequest
from .models import Product, CustomUser


class ProductForm(forms.ModelForm):
    designer = forms.ChoiceField(choices=[], required=False)  

    class Meta:
        model = Product
        fields = ['name', 'description'] 

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        designers = CustomUser.objects.filter(role='Người thiết kế')
        self.fields['designer'].choices = [(designer.user_id, designer.username) for designer in designers]
        
        if self.instance and self.instance.designer:
            self.fields['designer'].initial = self.instance.designer.user_id

        self.fields['name'].widget.attrs.update({'class': 'form-control'})
        self.fields['description'].widget.attrs.update({'class': 'form-control', 'rows': 3})
        self.fields['designer'].widget.attrs.update({'class': 'form-control'})

from django import forms
from .models import RequestFeedback,ProductFeedback

class RequestFeedbackForm(forms.ModelForm):
    class Meta:
        model = RequestFeedback
        fields = ['content']  

class ProductFeedbackForm(forms.ModelForm):
    class Meta:
        model = ProductFeedback
        fields = ['content']  
        
class DesignRequestForm(forms.ModelForm):
    class Meta:
        model = DesignRequest
        fields = ['description', 'file_path'] 

    file = forms.FileField(required=False, label="Upload file", widget=forms.ClearableFileInput(attrs={
        'class': 'form-control-file'
    }))

    description = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'form-control', 
        'placeholder': 'Enter a description...',
        'rows': 3
    }))

    file_path = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control', 
        'placeholder': 'Enter a file path or URL (optional)',
        'type': 'text'
    }), required=False)


