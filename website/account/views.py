from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from catalog.models import Sex, Category, Product
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth import logout

mcata = Sex.objects.get(sex_selection='m').category_set.all()
wcata = Sex.objects.get(sex_selection='w').category_set.all()
cat_context = {'mcata': mcata, 'wcata': wcata}

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/accounts')

        else:
            form = UserCreationForm()
            context = {'form': form}
            context.update(cat_context)
            return render(request, 'account/registration_warning.html', context)
    else:
        form = UserCreationForm()
        context = {'form': form}
        context.update(cat_context)
        return render(request, 'account/registration.html', context)

def profile(request):
    context = {'user': request.user}
    context.update(cat_context)
    return render(request, 'account/Profile.html', context)

def edit_profile(request):
    if request.method == "POST":
        form = UserChangeForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            return redirect('/accounts/profile')
    else:
        form = UserChangeForm(instance=request.user)
        context={'form': form}
        context.update(cat_context)
        return render(request,'account/edit_profile.html', context)

def logout_view(request):
    logout(request)
    return redirect('/catalog')

def index(request):
    context = cat_context
    return render(request, 'account/index.html', context)
