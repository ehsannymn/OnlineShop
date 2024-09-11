# Some special functionalities
from django.core.exceptions import PermissionDenied


def detect_user(user):
    if user.role == 1:
        redirect_url = 'vendorDashboard'
        return redirect_url
    elif user.role == 2:
        redirect_url = 'customerDashboard'
        return redirect_url
    elif user.role is None and user.is_superuser:
        redirect_url = '/admin'
        return redirect_url


# Restrict the vendor from accessing customer page
def check_role_vendor(user):
    if user.role == 1:
        return True
    else:
        raise PermissionDenied


# Restrict the customer from accessing vendor page
def check_role_customer(user):
    if user.role == 2:
        return True
    else:
        raise PermissionDenied
