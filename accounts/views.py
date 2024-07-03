from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotAllowed, JsonResponse
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth import update_session_auth_hash
from django.template.response import TemplateResponse
from django.views import View

# Create your views here.

class Register(View):

    def get(self, request, *args, **kwargs):
        return TemplateResponse(request, 'accounts/register.html')

    def post(self, request, *args, **kwargs):

        password1 = request.POST.get('password1', '')
        password2 = request.POST.get('password2', '')
        username = request.POST.get('username', '')
        email = request.POST.get('email', '')
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')

        context = {'username': [], 'password1': [], 'password2': [], 'email': [], 'username_value': username,
                   'email_value': email, 'first_name_value': first_name, 'last_name_value': last_name}

        if password1 != password2:
            context['password1'].append("The two password fields didn't match")
            context['password2'].append("The two password fields didn't match")

        if len(password1) < 8:
            context['password1'].append("This password is too short. It must contain at least 8 characters")
        if password1 is None:
            context['password1'].append("This field is required")

        if len(password2) < 8:
            context['password2'].append("This password is too short. It must contain at least 8 characters")
        if password2 is None:
            context['password2'].append("This field is required")

        if username is None:
            context['username'].append("This field is required")

        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            pass
        else:
            context['username'].append("A user with that username already exists")

        try:
            validate_email(email)
        except ValidationError:
            context['email'].append("Enter a valid email address")
        else:
            pass

        if len(context['username']) > 0 or len(context['password1']) > 0 or len(context['password2']) > 0 or len(
                context['email']) > 0:
            return TemplateResponse(request, 'accounts/register.html',
                                    context=context)
        else:
            User.objects.create_user(username=username, password=password1, email=email, first_name=first_name,
                                     last_name=last_name)

            return HttpResponseRedirect('/accounts/login/')

    HttpResponseNotAllowed(['GET', 'POST'])


class Login(View):

    def get(self, request, *args, **kwargs):
        return TemplateResponse(request, 'accounts/login.html')

    def post(self, request, *args, **kwargs):
        username = request.POST.get('username')
        password = request.POST.get('password')

        context = {'errors': [], "username_value": username}

        if user := authenticate(username=username, password=password):
            login(request, user)
            return HttpResponseRedirect('/accounts/profile/view/')
        else:
            context['errors'].append('Username or password is invalid')
            return TemplateResponse(request, 'accounts/login.html', context=context)

    HttpResponseNotAllowed(['GET', 'POST'])


class Logout(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return HttpResponseRedirect('/accounts/login/')

    HttpResponseNotAllowed(['GET'])


class ProfileView(View):
    def get(self, request, *args, **kwargs):

        if request.user.is_authenticated:
            user = request.user

            data = {"id": user.id, "username": user.username, "email": user.email, "first_name": user.first_name,
                    "last_name": user.last_name}
            return JsonResponse(data)
        else:
            return HttpResponse('401 UNAUTHORIZED ', status=401)

    HttpResponseNotAllowed(['GET'])


class EditProfile(View):

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            user = request.user

            context = {'email_value': user.email, 'first_name_value': user.first_name,
                       'last_name_value': user.last_name}
            return TemplateResponse(request, 'accounts/edit_profile.html',
                                    context=context)
        else:
            return HttpResponse('401 UNAUTHORIZED ', status=401)

    def post(self, request, *args, **kwargs):

        if request.user.is_authenticated:
            user = request.user

            # updated values
            password1 = request.POST.get('password1', '')
            password2 = request.POST.get('password2', '')
            email = request.POST.get('email', '')
            first_name = request.POST.get('first_name', '')
            last_name = request.POST.get('last_name', '')

            user.first_name = first_name
            user.last_name = last_name

            context = {'password1': [], 'password2': [], 'email': [],
                       'email_value': email, 'first_name_value': first_name, 'last_name_value': last_name}

            try:
                validate_email(email)
            except ValidationError:
                context['email'].append("Enter a valid email address")
            else:
                user.email = email

            if password1 != password2:
                context['password1'].append("The two password fields didn't match")
                context['password2'].append("The two password fields didn't match")

            if (password1 is None or password1 is "") and (password2 is None or password2 is ""):
                pass
            if 1 <= len(password1) < 8:
                context['password1'].append("This password is too short. It must contain at least 8 characters")
            if 1 <= len(password2) < 8:
                context['password2'].append("This password is too short. It must contain at least 8 characters")
            else:
                user.set_password(str(password1))

            if len(context['password1']) > 0 or len(context['password2']) > 0 or len(context['email']) > 0:
                return TemplateResponse(request, 'accounts/edit_profile.html',
                                        context=context)
            else:
                user.save()
                update_session_auth_hash(request, user)
                return HttpResponseRedirect('/accounts/profile/view/')

        else:
            return HttpResponse('401 UNAUTHORIZED ', status=401)

    HttpResponseNotAllowed(['GET', 'POST'])
