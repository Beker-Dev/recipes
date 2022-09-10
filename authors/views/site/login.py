from django.views import View
from django.contrib import messages
from django.shortcuts import render, redirect, reverse
from authors.forms.login_form import LoginForm
from django.contrib.auth import login, authenticate


class Login(View):
    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('authors:dashboard')
        else:
            form = LoginForm()
            form_action = reverse('authors:login')
            return render(self.request, 'authors/pages/login.html', {'form': form, 'form_action': form_action})

    def post(self, *args, **kwargs):
        post = self.request.POST
        form = LoginForm(post)
        if form.is_valid():
            username = form.cleaned_data.get('username', '')
            password = form.cleaned_data.get('password', '')
            authenticated_user = authenticate(username=username, password=password)

            if authenticated_user is not None:
                login(self.request, authenticated_user)
                messages.success(self.request, 'Login realizado com sucesso!')
                return redirect('authors:dashboard')

        messages.error(self.request, 'Usuário ou Senha invalidos')
        return redirect('authors:login')
