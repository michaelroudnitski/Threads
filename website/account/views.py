from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from catalog.models import Sex

mcata = Sex.objects.get(sex_selection='m').category_set.all()
wcata = Sex.objects.get(sex_selection='w').category_set.all()
cat_context = {'mcata': mcata, 'wcata': wcata}

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/account')

        else:
            form = UserCreationForm()
            context = {'form': form}
            context.update(cat_context)
            return render(request, 'account/registration_warning.html', context=context)
    else:
        form = UserCreationForm()
        context = {'form': form}
        context.update(cat_context)
        return render(request, 'account/registration.html', context=context)


def index(request):
    context = cat_context
    return render(request, 'account/index.html', context)
