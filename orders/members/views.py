from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

from .forms import RegisterUserForm

from orders.settings import EMAIL_HOST_USER

# Create your views here.

def login_user(request):

    if request.method == 'POST':

        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
            # Redirect to a success page.
            ...
        else:
            messages.success(request, 'Ошибка входа! Попробуйте снова.')
            return redirect('login')
            # Return an 'invalid login' error message.
            ...
    else:
        return render(request, 'authenticate/login.html', {})
    

def logout_user(request):
    logout(request)
    messages.success(request, 'Выход выполнен.')
    return redirect('home')


def register_user(request):

    if request.method == 'POST':
        
        form = RegisterUserForm(request.POST)
        
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']

            user = authenticate(username=username, password=password)

            login(request, user)

            messages.success(request, 'Регистрация выполнена.')

            send_mail(
                subject='Подтверждение регистрации',
                message=f'{username}, ваша регистрация подтверждена',
                from_email=EMAIL_HOST_USER,
                recipient_list=[user.email],
            )

            return redirect('home')
        
    else:
        form = RegisterUserForm()


    return render(request, 'authenticate/register_user.html', {'form':form})

def reset_password(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        try:
            user = get_user_model().objects.get(username=username)
        except User.DoesNotExist:
            # обработка ошибки, если пользователь с таким именем не существует
            return HttpResponse('Пользователь с таким именем не существует')

        # генерация нового пароля
        import random
        import string
        new_password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
        user.set_password(new_password)
        user.save()

        # отправка нового пароля на email пользователя
        subject = 'Восстановление пароля'
        message = f'Ваш новый пароль: {new_password}'
        from_email = 'noreply@example.com'
        to_email = user.email
        send_mail(subject, message, from_email, [to_email])
        messages.success(request, 'Новый пароль был отправлен на вашу почту.')
        return redirect('login')
    
    else:
        return render(request, 'authenticate/reset_password.html')