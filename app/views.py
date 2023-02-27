from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.views import View
from .forms import  UserLoginForm , AddUserForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView, ListView, DeleteView, UpdateView, CreateView
from django.utils.decorators import method_decorator
from app.models import MyUser
from django.core.mail import send_mail
from django.urls import reverse, reverse_lazy
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin

class HomeView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('/userlist/')
        return redirect('/login/')

# @method_decorator(login_required, name='dispatch')   
# class RegisterView(View):
#     def get(self, request):
#         form = AddUserForm()
#         return render(request, "app/add_user.html", context={"register_form": form})

#     def post(self, request):
#         form = AddUserForm(request.POST)
#         if form.is_valid():
#             username = form.cleaned_data.get('username')
#             email = form.cleaned_data.get('email')
#             address = form.cleaned_data.get('address')
#             qualification = form.cleaned_data.get('qualification')
#             password = form.cleaned_data.get('password1')
#             user = MyUser.objects.create_user(email, username, address, qualification, password=password)
#             self.send_mail(user)
#             messages.success(request, "User added.")
#             return redirect("/dashboard/")
#         messages.warning(
#             request, "Unsuccessful registration. Invalid data or Username already exists.")
#         form = AddUserForm()
#         return render(request, "app/add_user.html", context={"register_form": form})
    
#     def send_mail(self, user):
#         subject = 'User Added'
#         message = f'User {user.username} added successfully'
#         from_email = str(settings.EMAIL_HOST_USER)
#         to_mail = User.objects.filter(is_staff=True).first().email
#         print(to_mail)
#         recipient_list = [to_mail,]
#         print(subject, message, from_email, recipient_list)
#         send_mail(subject, message, from_email, recipient_list, fail_silently=False)

class LoginRequestView(View):
    def get(self, request):
        form = UserLoginForm()
        return render(request, template_name="app/login.html", context={"login_form": form})

    def post(self, request, *args, **kwargs):
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("app:home")
            else:
                messages.warning(request, "Invalid username or password!!!")
                form = UserLoginForm()
                return render (request, 'app/login.html', context={"login_form":form})
        else:
            messages.warning(request, "Invalid username or password!!!")
            form = UserLoginForm()
            return render (request, 'app/login.html', context={"login_form":form})


class LogoutRequestView(View):
    def get(self, request):
        logout(request)
        messages.info(request, "You have successfully logged out.")
        return redirect("app:home")
    
# @method_decorator(login_required, name='dispatch')
# class DashboardView(View, LoginRequiredMixin):
#     def get(self, request):
#         if request.user.is_authenticated:
#             users = User.objects.filter(is_staff=False)
#             return render(request, "app/home.html",context={"users":users} )

class UserList(ListView, LoginRequiredMixin): 
    model = MyUser 

class UserDetail(DetailView, LoginRequiredMixin):
    model = MyUser

class UserDelete(DeleteView, LoginRequiredMixin):
    model = MyUser
    success_url = reverse_lazy('app:user_list')
    success_message = "User deleted successfully"
    template_name = 'app/myuser_confirm_delete.html'

class UserEdit(UpdateView, LoginRequiredMixin):
    model = MyUser
    fields = '__all__'
    success_url = reverse_lazy('app:user_list')
    success_message = "User updated successfully"
    template_name = 'app/update_user.html'

class UserCreate(CreateView, LoginRequiredMixin):
    model = MyUser
    fields = '__all__'
    success_url = reverse_lazy('app:user_list')
    success_message = "User created successfully"
    template_name = 'app/myuser_form.html'

    def form_valid(self, form):
        self.object = form.save(False)
        self.object.save()
        self.send_mail(self.object)
        return HttpResponseRedirect(self.get_success_url())

    def send_mail(self, user):
        subject = 'User Added'
        message = f'User {user.name} added successfully'
        from_email = str(settings.EMAIL_HOST_USER)
        to_mail = User.objects.filter(is_staff=True).first().email
        recipient_list = [to_mail,]
        print(subject, message, from_email, recipient_list)
        send_mail(subject, message, from_email, recipient_list, fail_silently=False)