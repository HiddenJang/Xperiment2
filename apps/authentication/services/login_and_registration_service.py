from django.contrib.auth.models import User
from django.db import utils
from django.contrib.auth import authenticate, login

class EntranceService:
    """Сервис регистрации и авторизации пользователя"""

    def __init__(self, request):
        self.request = request
    
    def registrate_user(self) -> dict:
        """Регистрация пользователя"""

        if self.request.method == 'POST':
            user_login = self.request.POST['login']
            user_password = self.request.POST['password']
            first_name = self.request.POST['name']
            email = self.request.POST['email']
            if not user_login or not user_password or not first_name or not email:
                context = {'text': 'Заполните все поля формы!'}
                return {'result': False, 'page': 'reg_page.html', 'context': context}
            try:
                user = User.objects.create_user(user_login, email, user_password, first_name=first_name)
                user.save()
                return {'result': True, 'page': 'login_page', 'context': {}}
            except utils.IntegrityError:
                context = {'text': 'Данный пользователь уже зарегистрирован!'}
                return {'result': False, 'page': 'reg_page.html', 'context': context}
        else:
            return {'result': False, 'page': 'reg_page.html', 'context': {}}

    def login_user(self) -> dict:
        """Авторизация пользователя"""

        if self.request.user.is_authenticated:
            return {'result': True, 'page': 'scan_page', 'context': {}}
        elif self.request.method == 'POST':
            user_login = self.request.POST['login']
            user_password = self.request.POST['password']
            user = authenticate(self.request, username=user_login, password=user_password)
            if user is None:
                context = {'text': 'Введен неверный логин или пароль!'}
                return {'result': False, 'page': 'login_page.html', 'context': context}
            login(self.request, user)
            return {'result': True, 'page': 'scan_page', 'context': {}}
        else:
            return {'result': False, 'page': 'login_page.html', 'context': {}}
