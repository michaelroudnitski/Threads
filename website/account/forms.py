from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm


class RegistrationForm(UserCreationForm):

    # Email
    email = forms.EmailField(required=True)

    # Show the some specific things in the registeration form
    class Meta:
        model = User
        fields ={
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2',
        }

    # Function that save the change to the main database
    def save(self, commit=True):
        user= super(RegistrationForm, self).save(commit=False)              # Call the user object
        user.first_name = self.cleaned_data['first_name']                   # Change the first name
        user.last_name = self.cleaned_data['last_name']                     # Change the last name
        user.email = self.cleaned_data['email']                             # Change the first name

        # commit
        if commit:
            user.save()

        return user


class EditProfileForm(UserChangeForm):

    # Show the some specific things in the edit profile form
    class Meta:
        model = User
        fields = {
            'email',
            'first_name',
            'last_name',
            'password',
        }


class RemoveUser(forms.Form):
    # Show the username in the remove user form
    class Meta:
        model = User
        fields = {'username',
                  }
