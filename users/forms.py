from .models import User
from django.contrib.auth.forms import UserCreationForm


class UserRegisterForm(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for item in ['email', 'password1', 'password2']:
            self.fields[item].help_text = None

        self.fields['email'].label = 'Email'
        self.fields['password1'].label = 'Пароль'
        self.fields['password2'].label = 'Повторите пароль'
        # self.fields['gender'].label = 'П'

    class Meta:
        model = User
        fields = ['email', 'password1', 'password2']
