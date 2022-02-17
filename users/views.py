from gc import get_objects
import os
import requests
from django.contrib.auth.views import PasswordChangeView
from django.views.generic import FormView, DetailView, UpdateView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate, login, logout
from django.core.files.base import ContentFile
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from . import forms, models, mixins


class LoginView(mixins.LoggedOutOnlyView, FormView):
    template_name = "users/login.html"
    form_class = forms.LoginForm
    success_url = reverse_lazy("core:home")
    # 이것대신에 next query에 담긴 정보를 바탕으로 본래 접근하고자 했던 곳으로 가게 할 수 있음(get_success_url이용)

    def form_valid(self, form):
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=email, password=password)

        if user is not None:
            login(self.request, user)
            return redirect(reverse("core:home"))
        return super().form_valid(form)

    # def get_success_url(self):
    #     next_arg = self.request.GET.get("next")
    #     if next_arg is not None:
    #         return next_arg
    #     else:
    #         return reverse("core:home")
    # 작동안함 이유찾기 -> accessmixin에 get_success_url func없음


def log_out(request):
    messages.info(request, f"See you later {request.user.first_name}")
    logout(request)
    return redirect(reverse("core:home"))


class SignUpView(FormView):
    template_name = "users/signup.html"
    form_class = forms.SignUpForm
    success_url = reverse_lazy("core:home")
    initial = {}

    def form_valid(self, form):
        form.save()
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=email, password=password)
        if user is not None:
            login(self.request, user)
        user.verify_email()
        return super().form_valid(form)


def complete_verification(request, key):
    try:
        user = models.User.objects.get(email_secret=key)
        user.email_verified = True
        user.email_secret = ""
        user.save()
    except models.User.DoesNotExist:
        pass
    return redirect(reverse("core:home"))


def github_login(request):
    client_id = os.environ.get("GH_ID")
    redirect_uri = "http://127.0.0.1:8000/users/login/github/callback"
    return redirect(
        f"https://github.com/login/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&scope=read:user"
    )


class GithubException(Exception):
    pass


def github_callback(request):
    client_id = os.environ.get("GH_ID")
    client_secret = os.environ.get("GH_SECRET")
    code = request.GET.get("code")
    try:
        if code is not None:
            result = requests.post(
                f"https://github.com/login/oauth/access_token?client_id={client_id}&client_secret={client_secret}&code={code}",
                headers={"Accept": "application/json"},
            )
            token_json = result.json()
            error = token_json.get("error", None)
            if error is not None:
                raise GithubException("Can't get access token from github")
            else:
                access_token = token_json.get("access_token")
                profile_request = requests.get(
                    "https://api.github.com/user",
                    headers={
                        "Authorization": f"token {access_token}",
                        "Accept": "application/json",
                    },
                )

                profile_json = profile_request.json()
                username = profile_json.get("login", None)
                if username is not None:
                    name = profile_json.get("name")
                    email = profile_json.get("email")
                    bio = profile_json.get("bio")
                    print(name, email, bio)
                    if name is None:
                        name = username
                    if email is None:
                        raise GithubException("Can't get your profile")

                    try:
                        user = models.User.objects.get(email=email)
                        if user.login_method != models.User.LOGIN_GITHUB:
                            raise GithubException(
                                f"Please log in with: {user.login_method}"
                            )
                    except models.User.DoesNotExist:
                        user = models.User.objects.create(
                            email=email,
                            first_name=name,
                            username=email,
                            bio=bio,
                            login_method=models.User.LOGIN_GITHUB,
                            email_verified=True,
                        )
                        user.set_unusable_password()
                        user.save()
                    login(request, user)
                    messages.success(request, f"Welcome back {user.first_name}")
                    return redirect(reverse("core:home"))
                else:
                    raise GithubException("Can't get your information.")
        else:
            raise GithubException()
    except GithubException as e:
        messages.error(request, e)
        return redirect(reverse("users:login"))


def kakao_login(request):
    client_id = os.environ.get("KAKAO_ID")
    redirect_uri = "http://127.0.0.1:8000/users/login/kakao/callback"
    return redirect(
        f"https://kauth.kakao.com/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code&scope=account_email,profile_nickname,profile_image"
    )


class KakaoException(Exception):
    pass


def kakao_callback(request):
    try:
        code = request.GET.get("code")
        client_id = os.environ.get("KAKAO_ID")
        redirect_uri = "http://127.0.0.1:8000/users/login/kakao/callback"

        token_request = requests.get(
            f"https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={client_id}&redirect_uri={redirect_uri}&code={code}"
        )
        token_json = token_request.json()
        error = token_json.get("error", None)
        if error is not None:
            raise KakaoException("Can't get authorization code from Kakao.")
        access_token = token_json.get("access_token")
        profile_request = requests.get(
            "https://kapi.kakao.com/v2/user/me",
            headers={"Authorization": f"Bearer {access_token}"},
        )

        kakao_account = profile_request.json().get("kakao_account")

        email = kakao_account.get("email", None)
        if email is None:
            raise KakaoException(
                "Please also give me your email(Change your kakao settings)."
            )
        profile_json = kakao_account.get("profile")
        nickname = profile_json.get("nickname")
        profile_image_url = profile_json.get("profile_image_url")
        try:
            user = models.User.objects.get(email=email)
            if user.login_method != models.User.LOGIN_KAKAO:
                raise KakaoException(f"Please log in with {user.login_method}")

        except models.User.DoesNotExist:
            user = models.User.objects.create(
                email=email,
                username=email,
                first_name=nickname,
                login_method=models.User.LOGIN_KAKAO,
                email_verified=True,
            )
            user.set_unusable_password()
            user.save()
            # print(profile_image_url)
            if profile_image_url is not None:
                photo_request = requests.get(profile_image_url)
                user.avatar.save(
                    f"{nickname}-avatar.jpg", ContentFile(photo_request.content)
                )
        login(request, user)
        messages.success(request, f"Welcome back {user.first_name}")
        return redirect(reverse("core:home"))
    except KakaoException as e:
        messages.error(request, e)
        return redirect(reverse("users:login"))


class UserProfileView(DetailView):
    model = models.User
    context_object_name = "user_obj"
    # 이를 설정하지 않을 시 detailveiw는 페이지에 따라 user_obj를 변경하는 문제가 발생 -> 다른 사람의 프로필 접근 가능해짐
    # I think that was a problem which "Django Login" and "DetailView of User" are using same context_object_name "user". So, they could overwrite each other, but Nico changed context_object_name of "DetailView of User" from default "user" to "user_obj" and that solved the problem

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['field_name'] = field_value
    #     return context
    # 위와 같은 방식으로 view에서 특정 값이나 변수를 전달가능


class UpdateProfileView(mixins.LoggedInOnlyView, SuccessMessageMixin, UpdateView):
    model = models.User
    template_name = "users/update-profile.html"
    fields = (
        # "email",
        "first_name",
        "last_name",
        "gender",
        "bio",
        "birthdate",
        "language",
        "currency",
    )
    success_message = "Profile Updated"

    def get_object(self, queryset=None):
        return self.request.user

    # def get_form(self, form_class=None):
    #     form = super().get_form(form_class=form_class)
    #     form.fields["birthdate"].widget.attrs = {"placeholder": "생일"}
    #     form.fields["first_name"].widget.attrs = {"placeholder": "이름"}
    #     form.fields["last_name"].widget.attrs = {"placeholder": "성"}
    #     form.fields["gender"].empty_label = None
    #     return form

    # def form_valid(self, form):
    #     email = form.cleaned_data.get("email")
    #     self.object.username = email
    #     self.object.save()
    #     return super().form_valid(form)
    #  useremail 과 name 변경시 사용


class UpdatePasswordView(
    mixins.LoggedInOnlyView,
    mixins.EmailLoginOnlyView,
    SuccessMessageMixin,
    PasswordChangeView,
):
    template_name = "users/update-password.html"
    success_message = "Password Updated"
    # def get_form(self, form_class=None):
    #     form = super().get_form(form_class=form_class)
    #     form.fields["old_password"].widget.attrs = {"placeholder": "기존 비밀번호"}
    #     form.fields["new_password1"].widget.attrs = {"placeholder": "새 비밀번호"}
    #     form.fields["new_password2"].widget.attrs = {"placeholder": "새 비밀번호 확인"}
    #     return form
    #     placeholder를 원하면 해당 방법 이용

    def get_success_url(self):
        return self.request.user.get_absolute_url()
