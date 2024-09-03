from django.http import HttpResponse
from django.shortcuts import render, redirect
from accounts.forms import UserForm
from accounts.models import User
from django.contrib import messages


def register_user(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            # Create user, using the form
            # user = form.save(commit=False)
            # user.set_password(form.cleaned_data['password'])
            # user.role = User.CUSTOMER
            # user.save()

            # Create user, using create_user method
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User.objects.create(first_name=first_name, last_name=last_name,
                                       username=username, email=email, password=password
                                       )
            user.role = User.CUSTOMER
            user.save()
            messages.success(request, 'your account has been registered successfully!   ')
            return redirect('registerUser')  # an error cause me to learn the function of redirect,
        else:
            messages.error(request, 'There are some problems in your form data   ')
            print('*'*20, 'errors', '*'*20)
            print('invalid form')
            print(form.errors)
            print(form.non_field_errors)
    else:
        form = UserForm()


    context = {
            'form': form
    }

    print('form is not valid')
    return render(request, 'accounts/registerUser.html', context)



