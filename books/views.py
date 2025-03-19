import os

from django.conf import settings
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import JsonResponse, HttpResponse
from django.contrib import messages
from django.template import loader
from django.template.loader import render_to_string
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime, timedelta

from books.forms import BookForm
from .models import Book, BorrowInfo, Comment
import json


@login_required
def book_list2(request):
    category = request.GET.get('category', "All Books")
    books = Book.objects.all()
    if category and category != "All Books":
        books = books.filter(category=category)

    categories = Book.objects.exclude(category__isnull=True).exclude(category="").values_list('category',
                                                                                              flat=True).distinct()
    book_comments = {book.BookID: Comment.objects.filter(BookID=book).order_by('-CommentTime')[:2] for book in books}

    return render(request, 'books/book_list.html', {
        'books': books,
        'categories': categories,
        'current_category': category,
        "user": request.user,
        "book_comments": book_comments
    })


@login_required
def book_detail_api(request, book_id):
    book = get_object_or_404(Book, pk=book_id)

    data = {
        "BookName": book.BookName,
        "Publisher": book.Publisher,
        "Category": book.category,
        "ReleaseDate": book.ReleaseDate.strftime('%Y-%m-%d'),
        "Amount": book.Amount,
        "InStock": book.InStock,
        "Status": book.Status,
        "Description": book.description,
    }

    return JsonResponse(data)


@login_required
def book_detail(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    comments = Comment.objects.filter(BookID=book).order_by('-CommentTime')[:2]  # 取最新的2筆

    return render(request, 'book_detail.html', {'book': book, 'comments': comments})


@login_required
@csrf_exempt
def add_comment(request):
    if request.method == "POST":
        data = json.loads(request.body)
        book_id = data.get("book_id")

        if not book_id or not isinstance(book_id, int):
            return JsonResponse({"message": "Invalid book ID"}, status=400)

        content = data.get("content", "").strip()  # 避免空評論
        if not content:
            return JsonResponse({"message": "Comment cannot be empty"}, status=400)

        try:
            book = Book.objects.get(pk=book_id)
            Comment.objects.create(
                BookID=book,
                BorrowUserID=request.user,
                Comment=content
            )
            return JsonResponse({"message": "Comment added successfully!"})
        except Book.DoesNotExist:
            return JsonResponse({"message": "Book not found!"}, status=404)


@login_required
@csrf_exempt
def borrow_book(request):
    if request.method == "POST":
        data = json.loads(request.body)
        book_id = data.get("book_id")
        user = request.user

        if not user.is_authenticated:
            return JsonResponse({"success": False, "message": "Please log in first!"}, status=403)

        book = get_object_or_404(Book, pk=book_id)

        if book.InStock <= 0:
            return JsonResponse({"success": False, "message": "This book is out of stock!"}, status=400)

        borrow_time = datetime.now()
        return_time = borrow_time + timedelta(days=30)

        borrow_record = BorrowInfo.objects.create(
            BookID=book,
            BorrowUserID=user,
            BorrowTime=borrow_time,
            ReturnTime=return_time,
            Status="Borrowed"
        )

        book.InStock -= 1
        book.save()

        return JsonResponse({
            "success": True,
            "message": f"You have successfully borrowed '{book.BookName}'. Please return it by {return_time.strftime('%Y-%m-%d %H:%M:%S')}.",
            "borrow_user_id": user.user_id
        })

    return JsonResponse({"success": False, "message": "Invalid request"}, status=400)


@login_required
def my_borrowed_books(request):
    borrowed_books = BorrowInfo.objects.filter(BorrowUserID=request.user).select_related("BookID")
    return render(request, "books/my_borrowed_books.html", {"borrowed_books": borrowed_books})


@login_required
def return_book(request, borrow_id):
    if request.method == "POST":
        borrow_info = get_object_or_404(BorrowInfo, Number=borrow_id, BorrowUserID=request.user)

        if borrow_info.Status == "Borrowed":
            borrow_info.Status = "Returned"
            borrow_info.ActualReturnTime = timezone.now()
            borrow_info.save()

            book = borrow_info.BookID
            book.InStock += 1
            book.save()

            messages.success(request, f'《{book.BookName}》 success return！')
        else:
            messages.warning(request, f'《{borrow_info.BookID.BookName}》 already return。')

    return redirect('my_borrowed_books')


@login_required
def book_list(request):
    query = request.GET.get("q", "").strip()
    books = Book.objects.all()

    if query:
        books = books.filter(BookName__icontains=query)

    return render(request, "books/book_list.html", {"books": books, "query": query})


# def get_book_details(request, book_id):
#     try:
#         book = Book.objects.get(pk=book_id)
#         comments = Comment.objects.filter(BookID=book).order_by("-CommentTime")[:3]

#         comments_data = [
#             {"user": comment.BorrowUserID.username, "content": comment.Comment}
#             for comment in comments
#         ]

#         data = {
#             "BookName": book.BookName,
#             "Publisher": book.Publisher,
#             "Category": book.Category,
#             "ReleaseDate": book.ReleaseDate.strftime("%Y-%m-%d"),
#             "InStock": book.InStock,
#             "Status": "Available" if book.InStock > 0 else "Out of Stock",
#             "Description": book.Description,
#             "Comments": comments_data
#         }
#         return JsonResponse(data)

#     except Book.DoesNotExist:
#         return JsonResponse({"error": "Book not found"}, status=404)

@login_required
def get_book_comments(request, book_id):
    try:
        book = Book.objects.get(pk=book_id)
        comments = Comment.objects.filter(BookID=book).order_by('-CommentTime')[:3]

        comment_data = [
            {"user": comment.BorrowUserID.username, "content": comment.Comment,
             "time": comment.CommentTime.strftime('%Y-%m-%d %H:%M')}
            for comment in comments
        ]

        return JsonResponse({"success": True, "book": book.BookName, "comments": comment_data})

    except Book.DoesNotExist:
        return JsonResponse({"success": False, "error": "Book not found"})


@login_required
def history_view(request):
    # 获取用户的借阅历史
    borrow_history = BorrowInfo.objects.filter(
        BorrowUserID=request.user
    ).order_by('-BorrowTime')

    # 获取用户的评论历史
    comment_history = Comment.objects.filter(
        BorrowUserID=request.user
    ).order_by('-CommentTime')

    context = {
        'borrow_history': borrow_history,
        'comment_history': comment_history
    }

    return render(request, 'books/history.html', context)


@login_required
@csrf_exempt
def manage_book(request):
    if request.user.role != 'teacher':
        return redirect('book_list2')

    if request.method == "POST":
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})

    books = Book.objects.all().order_by('-BookID')
    paginator = Paginator(books, 10)
    page = request.GET.get('page')
    books = paginator.get_page(page)

    # 获取所有不重复的分类
    categories = Book.objects.values_list('category', flat=True).distinct()

    return render(request, 'books/manage_books.html', {
        'books': books,
        'categories': categories
    })


from django.shortcuts import render, get_object_or_404, redirect
from .models import Book
from .forms import BookForm  # 确保导入了 BookForm


@login_required
@csrf_exempt
def edit_book(request, book_id):
    if not request.user.role == 'teacher':
        return redirect('book_list2')
    book = get_object_or_404(Book, BookID=book_id)
    if request.method == 'POST':
        print("Received POST request for book_id:", book_id)
        print("POST data:", request.POST)

        try:
            # 直接更新数据库中的记录
            book.BookName = request.POST.get('BookName', book.BookName)
            book.Publisher = request.POST.get('Publisher', book.Publisher)
            book.category = request.POST.get('category', book.category)
            book.ReleaseDate = request.POST.get('ReleaseDate', book.ReleaseDate)
            book.Amount = int(request.POST.get('Amount', book.Amount))
            book.InStock = int(request.POST.get('InStock', book.InStock))
            book.Status = request.POST.get('Status', book.Status)

            book.save()
            return JsonResponse({'success': True})
        except Exception as e:
            print("Error saving book:", str(e))
            return JsonResponse({'success': False, 'errors': str(e)}, status=400)
    else:
        form = BookForm(instance=book)
        return render(request, 'books/edit_book_form_partial.html', {'form': form, 'book': book})


# def edit_book(request, book_id):
#     template = loader.get_template('manage')
#     return HttpResponse(template.render())

@login_required
@csrf_exempt
def delete_book(request, pk):
    if not request.user.role == 'teacher':
        return redirect('book_list2')
    book = get_object_or_404(Book, BookID=pk)
    if request.method == "POST":
        book.delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False}, status=400)


@login_required
def borrow_records(request):
    if not request.user.role == 'teacher':
        return redirect('book_list2')

    # 获取状态过滤参数
    status_filter = request.GET.get('status', 'all')

    # 获取所有借阅记录
    records = BorrowInfo.objects.all().order_by('-BorrowTime')

    # 根据状态过滤记录
    if status_filter != 'all':
        records = records.filter(Status=status_filter)

    # 分页
    page = request.GET.get('page', 1)
    paginator = Paginator(records, 10)  # 每页显示10条记录

    try:
        records = paginator.page(page)
    except PageNotAnInteger:
        records = paginator.page(1)
    except EmptyPage:
        records = paginator.page(paginator.num_pages)

    return render(request, 'books/borrow_records.html', {
        'records': records,
        'status_filter': status_filter
    })


@login_required
@csrf_exempt
def force_return_book(request, borrow_id):
    if not request.user.role == 'teacher':
        return redirect('book_list2')

    if request.method == "POST":
        try:
            borrow_info = get_object_or_404(BorrowInfo, Number=borrow_id)

            if borrow_info.Status == "Borrowed":
                borrow_info.Status = "Returned"
                borrow_info.ActualReturnTime = timezone.now()
                borrow_info.save()

                book = borrow_info.BookID
                book.InStock += 1
                book.save()

                return JsonResponse({
                    'success': True,
                    'message': f'Book "{book.BookName}" has been force returned successfully.'
                })
            else:
                return JsonResponse({
                    'success': False,
                    'message': 'This book has already been returned.'
                }, status=400)
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': str(e)
            }, status=500)

    return JsonResponse({'success': False, 'message': 'Invalid request method'}, status=400)
