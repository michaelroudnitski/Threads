from django.shortcuts import render, redirect
from django.contrib import messages
from catalog.models import Sex, Category, Product
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from django.contrib.auth.models import User
from django.contrib.auth import logout
from account.forms import RegistrationForm, EditProfileForm, RemoveUser

mcata = Sex.objects.get(sex_selection='m').category_set.all()
wcata = Sex.objects.get(sex_selection='w').category_set.all()
cat_context = {'mcata': mcata, 'wcata': wcata}

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/accounts')
    else:
        form = RegistrationForm()
        context = {'form': form}
        context.update(cat_context)
        return render(request, 'account/registration.html', context)

def profile(request):
    context = {'user': request.user}
    context.update(cat_context)
    return render(request, 'account/Profile.html', context)

def edit_profile(request):
    if request.method == "POST":
        form = EditProfileForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            return redirect('/accounts/profile')
    else:
        form = EditProfileForm(instance=request.user)
        context={'form': form}
        context.update(cat_context)
        return render(request,'account/edit_profile.html', context)

def change_password(request):
    if request.method == "POST":
        form = PasswordChangeForm(data=request.POST, user=request.user)

        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('/accounts/profile')
    else:
        form = PasswordChangeForm(user=request.user)

        context={'form': form}
        context.update(cat_context)
        return render(request,'account/change_password.html', context)

def del_user(request):
    u = User.objects.get(username=request.user)
    u.delete()
    return render(request, 'catalog/index.html')


def logout_view(request):
    logout(request)
    return redirect('/catalog')

def index(request):
    context = cat_context
    return render(request, 'account/index.html', context)

