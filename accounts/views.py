from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import CustomUserCreationForm

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Login successful!")
            user_role = user.role  # 假设角色信息存储在用户的 profile 中
            if user_role == 'teacher':
                return redirect("manage_book")  # Redirect to the new manageBook page for teachers
            else:
                return redirect("book_list")  # Redirect to the book list page for other roles
    else:
            messages.error(request, "Invalid username or password.")
    return render(request, 'accounts/login.html')

def user_register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)  
        if form.is_valid():
            form.save()
            messages.success(request, "Register success! Login now!")
            return redirect('login')
    else:
        form = CustomUserCreationForm() 
    return render(request, 'accounts/register.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('login')
