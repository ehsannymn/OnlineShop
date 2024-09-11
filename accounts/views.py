from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse
from django.shortcuts import render, redirect
from accounts.forms import UserForm
from accounts.models import User, UserProfile
from django.contrib import messages

from vendor.forms import VendorForm
from django.contrib import auth

from .utils import detect_user, check_role_vendor, check_role_customer


def register_user(request):
    if request.user.is_authenticated:
        messages.warning(request, 'You are already logged in!')
        return redirect('dashboard')

    elif request.method == 'POST':
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
            user = User.objects.create_user(first_name=first_name, last_name=last_name,
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


def register_vendor(request):

    if request.user.is_authenticated:
        messages.warning(request, 'You are already logged in!')
        return redirect('dashboard')

    elif request.method == "POST":
        # STORE THE DATA and create user
        form = UserForm(request.POST)
        v_form = VendorForm(request.POST, request.FILES)

        if form.is_valid() and v_form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User.objects.create_user(first_name=first_name, last_name=last_name,
                                            username=username, email=email, password=password
                                            )
            user.role = User.VENDOR
            user.save()
            vendor = v_form.save(commit=False)
            vendor.user = user
            user_profile = UserProfile.objects.get(user=user)
            vendor.user_profile = user_profile
            vendor.save()
            messages.success(request, 'vendor is registered successfully! please wait for the approval.')
            return redirect('registerVendor')
        else:
            print('invalid form')
            print('form.errors')

    else:
        form = UserForm()
        v_form = VendorForm()

    context = {
        'form': form,
        'v_form': v_form

    }

    return render(request, 'accounts/registerVendor.html', context)


# Using bootstrap grid system, we can change the columns size in html page: 12 means 100 percent of the width
def login(request):

    if request.user.is_authenticated:
        messages.warning(request, 'You are already logged in!')
        return redirect('myAccount')

    elif request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(email=email, password=password)

        if user is not None:
            auth.login(request, user)
            messages.success(request, 'you are now logged in')
            return redirect('myAccount')
        else:
            messages.error(request, 'invalid login credentials')
            return redirect('login')
    return render(request, 'accounts/login.html')


def logout(request):
    auth.logout(request)
    messages.info(request, 'you are logged out')
    return redirect('login')


@login_required(login_url='login')
def my_account(request):
    user = request.user
    detected_url = detect_user(user)

    return redirect(detected_url)


@login_required(login_url='login')
@user_passes_test(check_role_customer)
def customer_dashboard(request):
    return render(request, 'accounts/customerDashboard.html')


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def vendor_dashboard(request):
    return render(request, 'accounts/vendorDashboard.html')
