from django import forms
from books.models import Book


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = '__all__'  # ⬅️ 让 Django 自动获取所有字段
        widgets = {
            'ReleaseDate': forms.DateInput(attrs={'type': 'date'})  # ✅ 只改 `widget`
        }

