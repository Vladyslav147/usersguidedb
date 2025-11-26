from django.db import models
# Create your models here.
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.html import strip_tags


# Это менеджер модели — объект, который управляет созданием пользователей. ПРОВЕРКА
class CustomUserManager(BaseUserManager):
    #Используется когда обычный человек регистрируется на сайте через форму.
    def create_user(self, email, first_name, last_name, password=None, **extra_fields):
        if not email:
            raise ValueError('Поле email должно быть обезательным')
        email = self.normalize_email(email) # Приводит email к стандартному виду: делает маленькие буквы в домене, убирает лишние пробелы
        user = self.model(email=email, first_name=first_name, last_name=last_name, **extra_fields )
        user.set_password(password)
        user.save(using=self._db)

    #Используется только для создания суперюзеров.
    def create_superuser(self, email, first_name, last_name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True')
        return self.create_user(email, first_name, last_name, password, **extra_fields)
    #create_user → обычная регистрация на сайте
    #create_superuser → регистрация админа через команду в Python

# CustomUser(AbstractUser) — это ОДНА модель для ВСЕХ пользователей Она используется: ✔ и для обычных пользователей ✔ и для суперюзеров (админов)
class CustomUser(AbstractUser):
    email = models.EmailField(unique=True, max_length=66)
    first_name = models.CharField(max_length=66)
    last_name = models.CharField(max_length=66)
    address1 = models.CharField(max_length=128, blank=True, null=True)
    address2 = models.CharField(max_length=128, blank=True, null=True)
    city = models.CharField(max_length=128, blank=True, null=True)
    country = models.CharField(max_length=128, blank=True, null=True)
    province = models.CharField(max_length=128, blank=True, null=True)
    postal_code = models.CharField(max_length=20, blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    marketing_consent1 = models.BooleanField(default=False)
    marketing_consent2 = models.BooleanField(default=False)

    username = models.CharField(max_length=150, unique=True, null=True, blank=True)#сделан необязательным Как это работает: • username теперь не нужен вообще • он может быть пустым (null=True, blank=True)

    objects = CustomUserManager() 

    USERNAME_FIELD = 'email' # Зделать его в место username 
    REQUIRED_FIELDS = ['first_name', 'last_name']
    
    def __str__(self):
        return self.email
