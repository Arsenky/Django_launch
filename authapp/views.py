from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView
from django.views.generic.edit import CreateView
from django.contrib import messages
from authapp import models 
from django.views.generic import TemplateView 
from django.http import HttpResponseRedirect
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
import os.path
from django.contrib.auth import get_user_model
from authapp import forms
from django.contrib.auth.mixins import UserPassesTestMixin 
from django.views.generic import UpdateView


class CustomLoginView(LoginView):
    def form_valid(self,form): 
        ret=super().form_valid(form) 
        message = _("Login success!<br>Hi, %(username)s") % { 
        "username":self.request.user.get_full_name() 
        if self.request.user.get_full_name() 
        else self.request.user.get_username() } 
        
        messages.add_message(self.request,messages.INFO,mark_safe(message)) 
        return ret 
        
    def form_invalid(self,form): 
        for _unused, msg in form.error_messages.items(): 
            messages.add_message( self.request, messages.WARNING, 
            mark_safe(f"Something goes worng:<br>{msg}"), 
            ) 
            return self.render_to_response(self.get_context_data(form=form))
    
class CustomLogoutView(LogoutView):

    def dispatch(self, request, *args, **kwargs): 
        messages.add_message(self.request, messages.INFO, _("See you later!")) 
        return super().dispatch(request, *args, **kwargs)

class RegisterView(CreateView): 
    model = get_user_model() 
    form_class = forms.CustomUserCreationForm 
    success_url = reverse_lazy("mainapp:main_page")


class ProfileEditView(UserPassesTestMixin, UpdateView): 
    model = get_user_model() 
    form_class = forms.CustomUserChangeForm 
    
    def test_func(self): 
        return True if self.request.user.pk == self.kwargs.get("pk") else False 
        
    def get_success_url(self): 
        return reverse_lazy("authapp:profile_edit", args=[self.request.user.pk])

# class ProfileEditView(LoginRequiredMixin, TemplateView): 
#     template_name = "registration/profile_edit.html" 
#     login_url = reverse_lazy("authapp:login") 

#     def post(self, request, *args, **kwargs): 
#         try:
#             if request.POST.get("username"): 
#                 request.user.username =request.POST.get("username") 
#             if request.POST.get("first_name"): 
#                 request.user.first_name =request.POST.get("first_name") 
#             if request.POST.get("last_name"): 
#                 request.user.last_name =request.POST.get("last_name") 
#             if request.POST.get("age"): 
#                 request.user.age =request.POST.get("age") 
#             if request.POST.get("email"): 
#                 request.user.email =request.POST.get("email") 
#             if request.FILES.get("avatar"): 
#                 if request.user.avatar and os.path.exists( request.user.avatar.path ): 
#                     os.remove(request.user.avatar.path) 
#                 request.user.avatar =request.FILES.get("avatar") 
#             request.user.save() 
#             messages.add_message(request,messages.INFO,_("Saved!")) 

#         except Exception as exp: 
#             messages.add_message( request, messages.WARNING, mark_safe(f"Something goes worng:<br>{exp}"), ) 

#         return HttpResponseRedirect(reverse_lazy("authapp:profile_edit"))