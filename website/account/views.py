from django.shortcuts import render, redirect
from django.contrib import messages
from catalog.models import Sex, Category, Product
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from django.contrib.auth.models import User
from django.contrib.auth import logout
from account.forms import RegistrationForm, EditProfileForm, RemoveUser


# make this block of code a global function so it doesnt need to be repeated everytime
mcata = Sex.objects.get(sex_selection='m').category_set.all()
wcata = Sex.objects.get(sex_selection='w').category_set.all()
cat_context = {'mcata': mcata, 'wcata': wcata}
######################################################################################


def register(request):
    """page the user sees when registering"""
    # Get the request
    if request.method == 'POST':
        form = RegistrationForm(request.POST)                                                       # Get the register form
        if form.is_valid():                                                                         # If the datas in form are valid
            form.save()
            return redirect('/accounts')
    else:
        form = RegistrationForm()                                                                   # Show the form again
        context = {'form': form}                                                                    # Put the form in a context
        context.update(cat_context)                                                                 # Add some cat_context to the new context
        return render(request, 'account/registration.html', context)                                # Direct the to the website with context


def profile(request):
    """profile overview page
    This is what the user sees when he's already signed in"""
    context = {'user': request.user}
    context.update(cat_context)
    return render(request, 'account/Profile.html', context)


def index(request):
    """Account overview when the user is not signed in"""
    context = cat_context
    return render(request, 'account/index.html', context)


def edit_profile(request):
    """profile editing page"""
    # Get the request
    if request.method == "POST":
        # Edit profile form
        form = EditProfileForm(request.POST, instance=request.user)

        if form.is_valid():                                                                           # IF the form is valid
            form.save()                                                                               # Save the form
            return redirect('/accounts/profile')
    else:
        form = EditProfileForm(instance=request.user)
        context={'form': form}
        context.update(cat_context)
        return render(request,'account/edit_profile.html', context)


def change_password(request):
    """password changing page"""
    # Same idea with edit profile but only change the form

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
    """function that delete the user from being exist"""
    # Get the user
    u = User.objects.get(username=request.user)
    u.delete() # Deleted boy git gud plz
    return render(request, 'catalog/index.html')


def logout_view(request):
    """Function that logout the user"""
    logout(request)
    return redirect('/catalog')
