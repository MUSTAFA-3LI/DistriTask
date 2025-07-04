from django.shortcuts import render, redirect
from django.contrib import messages  # For system messages
from django.contrib.auth import authenticate, login as auth_login
from django.core.mail import send_mail #sent mail with otp
from django.utils import timezone
import random
from django.contrib.auth.hashers import make_password

from .models import User
from django.contrib.auth.hashers import check_password, make_password  # For password hashing
import time 


def login(request) :

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)

            if check_password(password, user.password):
                auth_login(request, user)  # ← تسجيل الدخول الرسمي هنا 👌

                # تقدر تسيب الحاجات دي لو بتستخدمها في الجلسة
                request.session['user_id'] = user.id  
                request.session['user_role'] = user.role  
                request.session['user_name'] = f"{user.first_name} {user.last_name}"

                messages.success(request, "Login successful!")

                if user.role == 'manager':
                    return redirect('tasks:manager_tasks')
                elif user.role == 'employee':
                    return redirect('tasks:employee_tasks')
            else:
                messages.error(request, 'Invalid password')
        except User.DoesNotExist:
            messages.error(request, 'User not found')

        return render(request, 'users/login.html')
    
    return render(request, 'users/login.html')


def register(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        category = request.POST.get('category')
        phone_number = request.POST.get('phone_number')
        birthday = request.POST.get('birthday')
        role = request.POST.get('role')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # Check if passwords match
        if password != confirm_password:
            messages.error(request, 'Passwords do not match')
            return render(request, 'users/register.html')  # Reload the register page with error message

        # Check if email is already registered
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists')
            return render(request, 'users/register.html')  # Reload the register page with error message

        # Hash the password before saving
        hashed_password = make_password(password)

        user = User(
            first_name=first_name,
            last_name=last_name,
            category = category,
            email=email,
            phone_number=phone_number,
            birthday=birthday,
            role=role,
            password=hashed_password  # Store hashed password
        )
        user.save()

        messages.success(request, 'Registration successful! You can now login.')
        return redirect('users:login')  # Redirect to login page after successful registration

    return render(request, 'users/register.html')


def change_password(request):
    if request.method == "POST":
        user_id = request.session.get('user_id')  
        old_password = request.POST['old_password']
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']

        user = User.objects.get(id=user_id)

        if not check_password(old_password, user.password):
            messages.error(request, "Old password is incorrect.")
        elif new_password != confirm_password:
            messages.error(request, "New passwords do not match.")
        else:
            user.password = make_password(new_password)
            user.save()
            messages.success(request, "Password updated successfully!")
            return redirect('users:login')  # or any page you want

    return render(request, 'users/change_password.html')




def send_otp(request):
    if request.method == "POST":
        email = request.POST['email']
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, "Email not found.")
            return redirect('users:send_otp')

        otp = str(random.randint(100000, 999999))
        user.reset_otp = otp
        user.otp_expiry = timezone.now() + timezone.timedelta(minutes=10)
        user.save()

        send_mail(
            subject='Your OTP Code',
            message = f"🎉 Ding Ding! You've got an OTP! 🎉\nYour OTP code is: {otp}\nI spent over two weeks writing the code to send this, so please... don't ignore it (⊙_⊙)\nUse it before it disappears like my free time☕",
            from_email='ahmed.h.ramadan.cs@email.com',
            recipient_list=[email],
        )
        messages.success(request, 'OTP sent to your email.')
        return redirect('users:verify_otp')
    
    return render(request, 'users/send_otp.html')


def verify_otp(request):
    if request.method == "POST":
        email = request.POST['email']
        otp = request.POST['otp']
        try:
            user = User.objects.get(email=email, reset_otp=otp)
            if user.otp_expiry < timezone.now():
                messages.error(request, 'OTP expired.')
                return redirect('users:send_otp')
            request.session['reset_user_id'] = user.id
            return redirect('users:reset_password')
        except User.DoesNotExist:
            messages.error(request, 'Invalid OTP.')
    
    return render(request, 'users/verify_otp.html')



def reset_password(request):
    user_id = request.session.get('reset_user_id')
    if not user_id:
        return redirect('users:send_otp')

    if request.method == "POST":
        new_password = request.POST['new_password']
        confirm = request.POST['confirm_password']
        if new_password != confirm:
            messages.error(request, 'Passwords do not match.')
            return redirect('users:reset_password')

        user = User.objects.get(id=user_id)
        user.password = make_password(new_password)
        user.reset_otp = None
        user.otp_expiry = None
        user.save()
        messages.success(request, 'Password reset successful.')
        return redirect('users:login')

    return render(request, 'users/reset_password.html')
