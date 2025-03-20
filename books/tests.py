from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone
from datetime import datetime, timedelta
import json

from .models import Book, BorrowInfo

User = get_user_model()

class BookModelTest(TestCase):
    """test the core functionality of the Book model"""
    
    def setUp(self):
        """set up the test environment, create a book instance"""
        print("Setting up BookModelTest...")
        self.book = Book.objects.create(
            BookName="test book",
            Publisher="test publisher",
            ReleaseDate=datetime.now().date(),
            Amount=5,
            InStock=5,
            Status="Available",
            category="Literature & Fiction",
            description="this is a test book"
        )
        print("Book created successfully.")
    
    def test_book_creation(self):
        """test the book creation functionality, ensure the book information is correctly stored in the database"""
        print("Running test_book_creation...")
        self.assertEqual(self.book.BookName, "test book")
        self.assertEqual(self.book.Publisher, "test publisher")
        self.assertEqual(self.book.Amount, 5)
        self.assertEqual(self.book.InStock, 5)
        self.assertEqual(self.book.Status, "Available")
        self.assertEqual(self.book.category, "Literature & Fiction")
        print("OK - Book creation test passed!")
    
    def test_book_str_method(self):
        """test the __str__ method of the Book model, ensure it returns the correct format"""
        print("Running test_book_str_method...")
        expected_str = f"test book (Available) - Literature & Fiction"
        self.assertEqual(str(self.book), expected_str)
        print("OK - __str__ method test passed!")

class BookSearchTest(TestCase):
    """test the book search functionality"""
    
    def setUp(self):
        """set up the test environment, create multiple books for search tests"""
        print("Setting up BookSearchTest...")
        Book.objects.create(
            BookName="Python programming",
            Publisher="programming publisher",
            ReleaseDate=datetime.now().date(),
            Amount=3,
            InStock=3,
            Status="Available",
            category="Computing & Internet"
        )
        
        Book.objects.create(
            BookName="Java programming guide",
            Publisher="technology publisher",
            ReleaseDate=datetime.now().date(),
            Amount=2,
            InStock=2,
            Status="Available",
            category="Computing & Internet"
        )
        
        Book.objects.create(
            BookName="novel collection",
            Publisher="literature publisher",
            ReleaseDate=datetime.now().date(),
            Amount=1,
            InStock=1,
            Status="Available",
            category="Literature & Fiction"
        )
        print("Books created successfully.")
        
        # create a test user
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.client.login(username="testuser", password="testpassword")
    
    def test_book_search(self):
        """test the book search functionality, ensure the correct search results are returned"""
        print("Running test_book_search...")
        # use the correct URL name
        response = self.client.get(reverse('book_list2') + '?search=Python')
        self.assertEqual(response.status_code, 200)
        
        # check if the search results contain the expected books
        self.assertContains(response, "Python programming")
        self.assertNotContains(response, "Java programming guide")
        self.assertNotContains(response, "novel collection")
        print("OK - Book search test passed!")
    
    def test_empty_search_results(self):
        """test the handling of empty search results"""
        print("Running test_empty_search_results...")
        # search for a non-existent book
        response = self.client.get(reverse('book_list2') + '?search=non-existent book')
        self.assertEqual(response.status_code, 200)
        
        # ensure the page displays the information of no search results
        self.assertContains(response, "No matching books found")
        print("OK - Empty search results test passed!")

class BookBorrowReturnTest(TestCase):
    """test the book borrowing and returning functionality"""
    
    def setUp(self):
        """set up the test environment, create a book and a user"""
        print("Setting up BookBorrowReturnTest...")
        self.book = Book.objects.create(
            BookName="test borrowing book",
            Publisher="test publisher",
            ReleaseDate=datetime.now().date(),
            Amount=3,
            InStock=3,
            Status="Available",
            category="Literature & Fiction"
        )
        
        self.user = User.objects.create_user(username="borrowuser", password="borrowpass")
        self.client.login(username="borrowuser", password="borrowpass")
        print("Book and user created successfully.")
    
    def test_book_borrowing(self):
        """test the book borrowing functionality, ensure the system correctly updates the inventory and records"""
        print("Running test_book_borrowing...")
        
        # initial inventory before borrowing
        initial_in_stock = self.book.InStock
        
        # send a borrowing request
        response = self.client.post(
            reverse('borrow_book'),
            data=json.dumps({"book_id": self.book.BookID}),
            content_type="application/json"
        )
        
        # refresh the book object
        self.book.refresh_from_db()
        
        # verify the response and database updates
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.book.InStock, initial_in_stock - 1)
        
        # check if the borrowing record is created
        borrow_record = BorrowInfo.objects.filter(BookID=self.book, BorrowUserID=self.user).first()
        self.assertIsNotNone(borrow_record)
        self.assertEqual(borrow_record.Status, "Borrowed")
        print("OK - Book borrowing test passed!")
    
    def test_book_returning(self):
        """test the book returning functionality, ensure the system restores the inventory and updates the borrowing record"""
        print("Running test_book_returning...")
        
        # create a borrowing record first
        borrow_time = timezone.now()
        return_time = borrow_time + timedelta(days=30)
        
        borrow_record = BorrowInfo.objects.create(
            BookID=self.book,
            BorrowUserID=self.user,
            BorrowTime=borrow_time,
            ReturnTime=return_time,
            Status="Borrowed"
        )
        
        # update the book inventory (simulate borrowing)
        self.book.InStock -= 1
        self.book.save()
        
        initial_in_stock = self.book.InStock
        
        # send a return request
        response = self.client.post(reverse('return_book', args=[borrow_record.Number]))
        
        # refresh the data
        self.book.refresh_from_db()
        borrow_record.refresh_from_db()
        
        # verify the response and database updates
        self.assertEqual(response.status_code, 302)  # assume successful redirect
        self.assertEqual(self.book.InStock, initial_in_stock + 1)
        self.assertEqual(borrow_record.Status, "Returned")
        self.assertIsNotNone(borrow_record.ActualReturnTime)
        print("OK - Book returning test passed!") 