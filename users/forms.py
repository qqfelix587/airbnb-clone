from django import forms

# from django.contrib.auth.forms import UserCreationForm
# ; 'auth.User' has been swapped for 'users.User 오류로 해결 안됨
from . import models


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    # clean_... 해당 field의 값을 하나하나 확인하는 용도로 쓰임.
    def clean(self):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        try:
            user = models.User.objects.get(username=email)
            if user.check_password(password):

                # check_password는 hashed한 password의 값 확인
                return self.cleaned_data
            else:
                self.add_error("password", forms.ValidationError("Password is wrong"))
        except models.User.DoesNotExist:
            self.add_error("email", forms.ValidationError("User does not exist"))


class SignUpForm(forms.ModelForm):
    # https://docs.djangoproject.com/en/4.0/topics/forms/modelforms/
    class Meta:
        model = models.User
        fields = ("first_name", "last_name", "email", "birthdate")
        # models form은 기본적으로 추가된 field에 대해 clean 과정을 진행하나,
        # 아래 password_confirm 이나 이미 존재하는 사용자를 찾는 과정 등 customizing이 필요한 경우에는 clean_<field_name> method를 사용
        # 따라서 signupform에서는 일반적으로 잘 사용하지 않음.

    password = forms.CharField(widget=forms.PasswordInput)
    # User model은 암호화된 password를 갖고 있으므로 이는 field에 넣지 않음.
    password1 = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    def clean_email(self):
        email = self.cleaned_data.get("email")
        try:
            models.User.objects.get(email=email)
            raise forms.ValidationError("User already exists with that email")
        except models.User.DoesNotExist:
            return email

    def clean_password1(self):

        password = self.cleaned_data.get("password")
        password1 = self.cleaned_data.get("password1")

        if password != password1:
            raise forms.ValidationError("Password confirmation does not match")
        else:
            return password

    def save(self, *args, **kwargs):

        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        user = super().save(commit=False)
        # commit=False :  create but don't save to the DB
        user.username = email
        user.set_password(password)
        user.save()
