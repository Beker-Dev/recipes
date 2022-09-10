from django.views import View
from django.contrib import messages
from django.shortcuts import render, redirect, reverse
from authors.forms.register_form import RegisterForm


class Register(View):
    def get(self, *args, **kwargs):
        register_form_data = self.request.session.get('register_form_data')
        form = RegisterForm(register_form_data)
        form_action = reverse('authors:register')
        return render(self.request, 'authors/pages/register.html', {'form': form, 'form_action': form_action})

    def post(self, *args, **kwargs):
        post = self.request.POST
        self.request.session['register_form_data'] = post
        form = RegisterForm(post)

        if form.is_valid():
            author = form.save(commit=False)
            author.set_password(author.password)
            author.save()
            messages.success(self.request, 'Usuário registrado com sucesso!')
            del self.request.session['register_form_data']
            return redirect('authors:login')
        else:
            messages.error(self.request, 'Há erros no formulário, verifique e envie novamente!')
            return redirect('authors:register')
