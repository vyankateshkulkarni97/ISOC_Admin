from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib import messages
from .forms import UserRegistrationForm, CustomUserLoginForm
from ISOC_Security.models import ISOC_User
from django.contrib.auth import get_user_model
from django.contrib import messages
from cryptography.fernet import Fernet
from django.conf import settings
from rest_framework.decorators import api_view

def encrypt_data(data):
    fernet = Fernet(settings.ENCRYPTION_KEY.encode())
    encrypted_data = fernet.encrypt(data.encode())
    return encrypted_data.decode()

def decrypt_data(encrypted_data):
    fernet = Fernet(settings.ENCRYPTION_KEY.encode())
    decrypted_data = fernet.decrypt(encrypted_data.encode())
    return decrypted_data.decode()

User = get_user_model()

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            decrypt_email = decrypt_data(form.cleaned_data['email'])
            decrypt_password = decrypt_data(form.cleaned_data['password'])

            user = ISOC_User.objects.create_user(
                username=form.cleaned_data['username'],
                email=decrypt_email,
                password=decrypt_password  
            ) 
            Encrypt_mail = encrypt_data(user.email)
            print("Encrypt Email:", Encrypt_mail)
            Encrypt_password = encrypt_data(user.password)
            print("Encrypt Password:", Encrypt_password)

            user.set_password(Encrypt_password)
            user.save()

            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect('login')
        else:
            messages.error(request, "Registration failed. Please correct the errors.")
    else:
        form = UserRegistrationForm()
    
    return render(request, 'user_register.html', {'form': form})

# @api_view(['POST'])
# def user_login(request):
#     if request.method == 'POST':
#         form = CustomUserLoginForm(request.POST)  # Use CustomUserLoginForm here

#         if form.is_valid():
#             user = form.get_user()
#             if user is not None:
#                 login(request, user)
#                 return redirect("home")
#             else:
#                 messages.error(request, 'Invalid username or password.')
#         else:
#             messages.error(request, 'Invalid username or password.')
#     else:
#         form = CustomUserLoginForm()

#     return render(request, 'user_login.html', {'form': form})


from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework import status
import logging

logger = logging.getLogger(__name__)

@api_view(['POST'])
def user_login(request):
    username = request.data.get('loginid')
    password = request.data.get('password')
    print('this is username :- ', username)
    print('this is password :- ', password)
    

    logger.info(f'Login attempt for username: {username}')

    user = authenticate(username=username, password=password)
    if user : #is not None
        logger.info('Login successful')
        return Response({'message': 'Login successful'}, status=status.HTTP_200_OK)
    
    logger.warning('Invalid credentials')
    return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)


def user_logout(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect('login')