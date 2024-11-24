from django import forms
from .models import Listing, Bid, Comment


class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = [
            'category',
            'title',
            'description',
            'starting_bid',
            'image_url',
        ]
        widgets = {
            'category': forms.TextInput(attrs={
                'class': 'form-control form-style', 
                'placeholder': 'Category'
            }),
            'title': forms.TextInput(attrs={
                'class': 'form-control form-style', 
                'placeholder': 'Title'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control form-style', 
                'placeholder': 'Description'
            }),
            'starting_bid': forms.NumberInput(attrs={
                'class': 'form-control form-style', 
                'placeholder': '£0.00'
            }),
            'image_url': forms.URLInput(attrs={
                'class': 'form-control form-style', 
                'placeholder': 'https://www.example.com/image.jpg'
            }),
        }


class BidForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = ['bid_amount']
        labels = { 'bid_amount': False }
        widgets = {
            'bid_amount': forms.NumberInput(attrs={
                'class': 'form-control form-style',
                'placeholder': 'Bid',
            }), 
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        labels = { 'content': False }
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control form-style',
                'placeholder': 'Leave a comment...',
                'rows': 4,
            }), 
        }