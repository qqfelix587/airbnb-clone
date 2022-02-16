import uuid
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.mail import send_mail
from django.utils.html import strip_tags
from django.shortcuts import reverse
from django.template.loader import render_to_string

# Create your models here.
class User(AbstractUser):
    """Custom User Model"""

    GENDER_MALE = "male"
    GENDER_FEMALE = "female"
    GENDER_OTHER = "other"
    GENDER_CHOICES = (
        (GENDER_MALE, "Male"),
        (GENDER_FEMALE, "Female"),
        (GENDER_OTHER, "Other"),
    )
    LANGUAGE_ENGLISH = "en"
    LANGUAGE_KOREAN = "kr"
    LANGUAGE_CHOICES = (
        (LANGUAGE_ENGLISH, "English"),
        # 앞 부분은 db로 가고, 뒷부분은 form으로 감
        (LANGUAGE_KOREAN, "Korean"),
    )
    CURRENCY_USD = "usd"
    CURRENCY_KRW = "krw"
    CURRENCY_CHOICES = (
        (CURRENCY_USD, "USD"),
        (CURRENCY_KRW, "KRW"),
    )
    LOGIN_EMAIL = "email"
    LOGIN_KAKAO = "kakao"
    LOGIN_GITHUB = "github"

    LOGIN_CHOICES = (
        (LOGIN_EMAIL, "Email"),
        (LOGIN_GITHUB, "Github"),
        (LOGIN_KAKAO, "Kakao"),
    )

    avatar = models.ImageField(upload_to="avatars", blank=True)
    # null is for db, blank is for form
    gender = models.CharField(choices=GENDER_CHOICES, max_length=10, blank=True)
    bio = models.TextField(blank=True)
    birthdate = models.DateField(blank=True, null=True)
    language = models.CharField(
        choices=LANGUAGE_CHOICES, max_length=2, blank=True, default=LANGUAGE_KOREAN
    )
    currency = models.CharField(
        choices=CURRENCY_CHOICES, max_length=3, blank=True, default=CURRENCY_KRW
    )
    superhost = models.BooleanField(default=False)

    # django ORM에 의해 sql query로 바뀌어서 db 에게 명령 수행
    # 이를 통해 models.py 내의 모든 것들을 djaango가 알아서 db table에 넣어줌.

    email_verified = models.BooleanField(default=False)
    email_secret = models.CharField(max_length=120, default="", blank=True)

    login_method = models.CharField(
        max_length=50, choices=LOGIN_CHOICES, default=LOGIN_EMAIL
    )

    def get_absolute_url(self):
        # get_absolute_url을 사용하지 않아도 url의 인자값을 넘겨 사용할 수 있으나,
        # 이 함수를 사용할 시 관리자 페이지에서 "view on site" 버튼을 통해 해당되는 실제화면을 볼 수 있다.
        return reverse("users:profile", kwargs={"pk": self.pk})

    def verify_email(self):
        # verify의 경우 곳곳에서 사용될 수 있으므로 model에 정의
        if self.email_verified is False:
            secret = uuid.uuid4().hex[:20]
            self.email_secret = secret
            html_message = render_to_string(
                "emails/verify_email.html", {"secret": secret}
            )
            send_mail(
                "Verify Airbnb Account",
                strip_tags(html_message),
                settings.EMAIL_FROM,
                [self.email],
                fail_silently=False,
                html_message=html_message,
            )
            self.save()
