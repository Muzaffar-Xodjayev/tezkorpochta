from datetime import datetime

from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin,BaseUserManager


class MyAccountManager(BaseUserManager):
    def create_user(self, first_name, last_name, phone_number, password=None):
        if not phone_number:
            raise ValueError('User must have an phone number')

        user = self.model(
            phone_number=phone_number,
            first_name=first_name,
            last_name=last_name,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, first_name, last_name, phone_number, password):
        user = self.create_user(
            phone_number=phone_number,
            first_name=first_name,
            last_name=last_name,
            password=password,
        )
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=250,verbose_name="Ism")
    last_name = models.CharField(max_length=250,verbose_name="Familiya")
    phone_number = models.CharField(max_length=50,unique=True,verbose_name="Telefon raqam")
    phone_verify = models.BooleanField(default=False,verbose_name="Telefon raqam tekshirish")

    # required
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superadmin = models.BooleanField(default=False)

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = MyAccountManager()

    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return self.phone_number

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, add_lable):
        return self.is_admin

    class Meta:
        verbose_name = "Foydalanuvchilar"
        verbose_name_plural = "Foydalanuvchilar"

class Code(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE, verbose_name="Foydalanuvchi")
    code = models.CharField(max_length=10,unique=True)

    def __str__(self):
        return self.code

    class Meta:
        verbose_name = "Bir martalik parollar"
        verbose_name_plural = "Bir martalik parollar"


class Order(models.Model):
    status = (
        ("Kutilmoqda","Kutilmoqda"),
        ("Yo'lda","Yo'lda"),
        ("Arxivlandi","Arxivlandi")
    )
    sender_person_phone_number = models.ForeignKey(Account, on_delete=models.CASCADE,verbose_name="Jo'natuvchi Shahsning tel raqami")
    sender_person_name = models.CharField(max_length=250,verbose_name="Jo'natuvchi Shahsning ismi")
    product_name = models.CharField(max_length=500,verbose_name="Mahsulot nomi")
    product_weight = models.CharField(max_length=250,verbose_name="Mahsulotning o'girligi")
    product_price = models.CharField(max_length=500,verbose_name="Mahsulotning narxi")
    address = models.TextField(verbose_name="Manzil")
    client_name = models.CharField(max_length=500, verbose_name="Oluvchi shahsning ismi")
    client_phone_number = models.CharField(max_length=50,verbose_name="Oluvchi shahsning tel raqami")
    product_status = models.CharField(max_length=50,choices=status,verbose_name="Mahsulotning Holati")

    def __str__(self):
        return self.product_name

    class Meta:
        verbose_name = "Buyurtmalar"
        verbose_name_plural = "Buyurtmalar"

class Done_Jobs(models.Model):
    title = models.CharField(max_length=500)
    img = models.ImageField(upload_to="Jobs")
    content = models.TextField()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Bajarilgan ishlar"
        verbose_name_plural = "Bajarilgan ishlar"
