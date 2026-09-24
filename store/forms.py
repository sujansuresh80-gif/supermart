from django import forms
from .models import Product


class ProductForm(forms.ModelForm):

    class Meta:

        model = Product

        fields = [
            'name',
            'category',
            'description',
            'price',
            'stock',
            'image',
        ]

        widgets = {

            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter product name',
            }),

            'category': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter category',
            }),

            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Enter product description',
                'rows': 5,
            }),

            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter price',
                'step': '0.01',
                'min': '0.01',
            }),

            'stock': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter stock quantity',
                'min': '0',
            }),

            'image': forms.ClearableFileInput(attrs={
                'class': 'form-control',
            }),
        }


    # ==========================================
    # PRICE VALIDATION
    # ==========================================

    def clean_price(self):

        price = self.cleaned_data.get('price')

        if price is None:
            raise forms.ValidationError(
                'Price is required.'
            )

        if price <= 0:
            raise forms.ValidationError(
                'Price must be greater than 0.'
            )

        return price


    # ==========================================
    # STOCK VALIDATION
    # ==========================================

    def clean_stock(self):

        stock = self.cleaned_data.get('stock')

        if stock is None:
            raise forms.ValidationError(
                'Stock is required.'
            )

        if stock < 0:
            raise forms.ValidationError(
                'Stock cannot be negative.'
            )

        return stock


    # ==========================================
    # NAME VALIDATION
    # ==========================================

    def clean_name(self):

        name = self.cleaned_data.get('name')

        if not name or not name.strip():
            raise forms.ValidationError(
                'Product name is required.'
            )

        return name.strip()


    # ==========================================
    # CATEGORY VALIDATION
    # ==========================================

    def clean_category(self):

        category = self.cleaned_data.get('category')

        if not category or not category.strip():
            raise forms.ValidationError(
                'Category is required.'
            )

        return category.strip()