from django import forms
from django.contrib.auth import authenticate
from .models import Usuario, Rol, Departamento


class LoginForm(forms.Form):
    """Formulario de login para autenticación de usuarios"""
    username = forms.CharField(
        label='Nombre de usuario',
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese su usuario',
            'autocomplete': 'username'
        })
    )
    password = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese su contraseña',
            'autocomplete': 'current-password'
        })
    )

    def clean(self):
        """Valida las credenciales del usuario"""
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if username and password:
            # Intenta autenticar al usuario
            self.user = authenticate(username=username, password=password)
            if self.user is None:
                raise forms.ValidationError(
                    'Usuario o contraseña incorrectos.'
                )
        return cleaned_data


class CrearUsuarioForm(forms.ModelForm):
    """Formulario para crear nuevos usuarios"""
    password1 = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese una contraseña segura'
        })
    )
    password2 = forms.CharField(
        label='Confirmar contraseña',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirme la contraseña'
        })
    )
    id_rol = forms.ModelChoiceField(
        queryset=Rol.objects.all(),
        label='Rol',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    id_departamento = forms.ModelChoiceField(
        queryset=Departamento.objects.all(),
        label='Departamento',
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Usuario
        fields = ('username', 'email', 'first_name', 'last_name')
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre de usuario'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Correo electrónico'
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Apellido'
            }),
        }

    def clean_password2(self):
        """Valida que las contraseñas coincidan"""
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(
                    'Las contraseñas no coinciden.'
                )
        return password2

    def clean_username(self):
        """Valida que el nombre de usuario sea único"""
        username = self.cleaned_data.get('username')
        if Usuario.objects.filter(username=username).exists():
            raise forms.ValidationError(
                'Este nombre de usuario ya existe.'
            )
        return username

    def clean_email(self):
        """Valida que el email sea único"""
        email = self.cleaned_data.get('email')
        if email and Usuario.objects.filter(email=email).exists():
            raise forms.ValidationError(
                'Este correo ya está registrado.'
            )
        return email

    def save(self, commit=True):
        """Crea el usuario con la contraseña encriptada"""
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        user.id_rol = self.cleaned_data['id_rol']
        user.id_departamento = self.cleaned_data['id_departamento']

        if commit:
            user.save()
        return user
