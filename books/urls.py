from django.urls import path
from .views import book_list, book_detail_api, borrow_book, my_borrowed_books, book_list2, get_book_comments, \
    return_book, add_comment, book_detail, history_view, manage_book, edit_book, delete_book, borrow_records, force_return_book

urlpatterns = [
    path('', book_list2, name='book_list2'),
    path('list/', book_list, name='book_list'),
    path('api/<int:book_id>/', book_detail_api, name='book_detail_api'),
    path('api/borrow/', borrow_book, name='borrow_book'),
    path('my_borrowed_books/', my_borrowed_books, name='my_borrowed_books'),
    path('return/<int:borrow_id>/', return_book, name='return_book'),
    path('add_comment/', add_comment, name='add_comment'),
    path('book/<int:book_id>/', book_detail, name='book_detail'),
    path('history/', history_view, name='history'),
    path('manage_book/', manage_book, name='manage_book'),
    path('book_edit/<int:book_id>/', edit_book, name='edit_book'),
    path('book_delete/<int:pk>/', delete_book, name='delete_book'),
    path('api/comments/<int:book_id>/', get_book_comments, name='get_book_comments'),
    path('borrow_records/', borrow_records, name='borrow_records'),
    path('force_return/<int:borrow_id>/', force_return_book, name='force_return_book'),
]
