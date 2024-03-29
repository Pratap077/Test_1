from django.shortcuts import render, HttpResponseRedirect
from django.contrib import messages
from .forms import SignUpForm, EditUserProfileForm, LoginForm
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm, SetPasswordForm
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash

# Create your views here.
def sign_up(request):
 if request.method == "POST":
  fm = SignUpForm(request.POST)
  if fm.is_valid():
   messages.success(request, 'Account Created Successfully !!') 
   fm.save()
 else: 
  fm = SignUpForm()
 return render(request, 'myapp/signup.html', {'form':fm})

# Login View Function
def user_login(request):
  if not request.user.is_authenticated:
    if request.method == "POST":
      fm = LoginForm(request=request, data=request.POST)
      if fm.is_valid():
        uname = fm.cleaned_data['username']
        upass = fm.cleaned_data['password']
        user = authenticate(username=uname, password=upass)
        if user is not None:
          login(request, user)
          messages.success(request, 'Logged in successfully !!')
          return HttpResponseRedirect('/profile/')
    else: 
      fm = LoginForm()
    return render(request, 'myapp/userlogin.html', {'form':fm})
  else:
    return HttpResponseRedirect('/profile/')

# Profile
def user_profile(request):
  if request.user.is_authenticated:
    if request.method == "POST":
      fm = EditUserProfileForm(request.POST, instance=request.user)
      if fm.is_valid():
        messages.success(request, 'Profile Updated !!!')
        fm.save()
    else:
      fm = EditUserProfileForm(instance=request.user)
    return render(request, 'myapp/profile.html', {'name': request.user, 'form':fm})
  else:
    return HttpResponseRedirect('/login/')

# Logout
def user_logout(request):
  logout(request)
  return HttpResponseRedirect('/login/')

# Change Password with old Password
def user_change_pass(request):
  if request.user.is_authenticated:
    if request.method == "POST":
      fm = PasswordChangeForm(user=request.user, data=request.POST)
      if fm.is_valid():
        fm.save()
        update_session_auth_hash(request, fm.user)
        messages.success(request, 'Password Changed Successfully')
        return HttpResponseRedirect('/profile/')
    else:
      fm = PasswordChangeForm(user=request.user)
    return render(request, 'myapp/changepass.html', {'form':fm})
  else:
    return HttpResponseRedirect('/login/')
