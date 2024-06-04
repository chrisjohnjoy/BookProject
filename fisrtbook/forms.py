from django import forms
from .models import Book,Author

class AuthorForm(forms.ModelForm):

    class Meta:

        model=Author
        fields=['name']


class BookForm(forms.ModelForm):

    class Meta:

        model=Book
        fields='__all__'

        widgets={
            'title':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter the Book name'}),
            'author':forms.Select(attrs={'class':'form-control','placeholder':'Enter the Author name'}),
            'price':forms.NumberInput(attrs={'class':'form-control','placeholder':'Enter the Price'},)

        }