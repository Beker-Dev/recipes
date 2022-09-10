from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.http import HttpResponse
from django.shortcuts import redirect


@method_decorator(
    login_required(login_url='authors:login', redirect_field_name='next'),
    name='dispatch'
)
class Logout(View):
    def post(self, *args, **kwargs):
        username_logged_in = self.request.user.username
        username_in_form = self.request.POST.get('username')

        if username_logged_in != username_in_form:
            return HttpResponse(status=401)
        else:
            logout(self.request)
            return redirect('authors:login')
