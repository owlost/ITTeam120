from django.db import models
from django.conf import settings
from datetime import datetime, timedelta

class Book(models.Model):
    STATUS_CHOICES = [
        ("Available", "Available"),
        ("Borrowed", "Borrowed"),
        ("Reserved", "Reserved"),
    ]

    CATEGORY_CHOICES = [
        ("Literature & Fiction", "Literature & Fiction"),
        ("Business & Finance", "Business & Finance"),
        ("Science & Technology", "Science & Technology"),
        ("Children & Teenage", "Children & Teenage"),
        ("Computing & Internet", "Computing & Internet"),
        ("History", "History"),
    ]
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default="Literature & Fiction")

    BookID = models.AutoField(primary_key=True)
    BookName = models.CharField(max_length=255)
    Publisher = models.CharField(max_length=255)
    ReleaseDate = models.DateField()
    Amount = models.IntegerField(default=1)
    InStock = models.IntegerField(default=1)
    Status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Available")
    description = models.TextField(blank=True, null=True)
    cover_image = models.ImageField(upload_to="book_covers/", blank=True, null=True)

    
    def __str__(self):
        return f"{self.BookName} ({self.Status}) - {self.category}"
    
class BorrowInfo(models.Model):
    BORROW_STATUS_CHOICES = [
        ("Borrowed", "Borrowed"),
        ("Returned", "Returned"),
        ("Overdue", "Overdue"),
    ]

    Number = models.AutoField(primary_key=True)
    BookID = models.ForeignKey("Book", on_delete=models.CASCADE, verbose_name="BookID")
    BorrowUserID = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="BorrowUserID"
    )
    BorrowTime = models.DateTimeField(auto_now_add=True, verbose_name="BorrowTime")
    ReturnTime = models.DateTimeField(verbose_name="ReturnTime")
    ActualReturnTime = models.DateTimeField(blank=True, null=True, verbose_name="ActualReturnTime")
    Status = models.CharField(max_length=10, choices=BORROW_STATUS_CHOICES, default="Borrowed", verbose_name="Status")

    def __str__(self):
        return f"{self.BorrowUserID.username} - {self.BookID.BookName} ({self.Status})"
        #return f"Borrow {self.BookID.BookName} by UserID {self.BorrowUserID.user_id} ({self.Status})"
class Comment(models.Model):
    BookID = models.ForeignKey("Book", on_delete=models.CASCADE, verbose_name="BookID")
    BorrowUserID = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="BorrowUserID")
    Comment = models.TextField(verbose_name="Comment")
    CommentTime = models.DateTimeField(auto_now_add=True, verbose_name="CommentTime")

    def __str__(self):
        return f"Comment by {self.BorrowUserID.username} on {self.BookID.BookName}"