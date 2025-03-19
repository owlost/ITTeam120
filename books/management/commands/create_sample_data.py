from django.core.management.base import BaseCommand
from books.models import Book
from datetime import date

def create_sample_books():
    books_data = [
        {
            'BookName': 'The Great Gatsby',
            'Publisher': 'Scribner',
            'ReleaseDate': date(1925, 4, 10),
            'Amount': 5,
            'InStock': 5,
            'Status': 'Available',
            'category': 'Literature & Fiction',
            'description': 'A story of the fabulously wealthy Jay Gatsby and his love for the beautiful Daisy Buchanan.'
        },
        {
            'BookName': 'Python Programming',
            'Publisher': 'O\'Reilly Media',
            'ReleaseDate': date(2021, 1, 1),
            'Amount': 3,
            'InStock': 3,
            'Status': 'Available',
            'category': 'Computing & Internet',
            'description': 'A comprehensive guide to Python programming language.'
        },
        {
            'BookName': 'The Art of Business',
            'Publisher': 'Harvard Business Review',
            'ReleaseDate': date(2020, 6, 15),
            'Amount': 2,
            'InStock': 2,
            'Status': 'Available',
            'category': 'Business & Finance',
            'description': 'Essential business strategies for modern entrepreneurs.'
        }
    ]
    
    for book_data in books_data:
        Book.objects.create(**book_data)

class Command(BaseCommand):
    help = 'Creates sample books'

    def handle(self, *args, **kwargs):
        create_sample_books()
        self.stdout.write(self.style.SUCCESS('Successfully created sample books')) 