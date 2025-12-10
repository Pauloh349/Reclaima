from django import forms
from .models import LostItem, FoundItem, Category


class LostItemForm(forms.ModelForm):
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    date_lost = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )

    class Meta:
        model = LostItem
        fields = [
            'title', 'category', 'description', 'location',
            'date_lost', 'brand', 'color', 'model',
            'reporter_name', 'reporter_email', 'reporter_phone', 'reward', 'image'
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., iPhone 12, Black Wallet'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Describe the item in detail...'
            }),
            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Downtown Mall, Central Station'
            }),
            'brand': forms.TextInput(attrs={'class': 'form-control'}),
            'color': forms.TextInput(attrs={'class': 'form-control'}),
            'model': forms.TextInput(attrs={'class': 'form-control'}),
            'reporter_name': forms.TextInput(attrs={'class': 'form-control'}),
            'reporter_email': forms.EmailInput(attrs={'class': 'form-control'}),
            'reporter_phone': forms.TextInput(attrs={'class': 'form-control'}),
            'reward': forms.NumberInput(attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image:
            content_type = image.content_type
            if not content_type.startswith('image/'):
                raise forms.ValidationError('Uploaded file is not an image.')
            if image.size > 5 * 1024 * 1024:
                raise forms.ValidationError('Image file too large ( > 5MB ).')
        return image


class SearchForm(forms.Form):
    search = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search items...'
        })
    )

    category = forms.ModelChoiceField(
        required=False,
        queryset=Category.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    location = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Location...'
        })
    )

    date_from = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )

    date_to = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )


class FoundItemForm(forms.ModelForm):
    date_found = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )

    class Meta:
        model = FoundItem
        fields = [
            'title', 'category', 'description', 'location',
            'date_found', 'finder_name', 'finder_email', 'finder_phone', 'image'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'finder_name': forms.TextInput(attrs={'class': 'form-control'}),
            'finder_email': forms.EmailInput(attrs={'class': 'form-control'}),
            'finder_phone': forms.TextInput(attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image:
            content_type = image.content_type
            if not content_type.startswith('image/'):
                raise forms.ValidationError('Uploaded file is not an image.')
            if image.size > 5 * 1024 * 1024:
                raise forms.ValidationError('Image file too large ( > 5MB ).')
        return image
