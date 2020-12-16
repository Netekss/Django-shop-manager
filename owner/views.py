from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages

from .forms import CreateUserForm
from .models import User

def check_if_owner(request):
    return request.user.user.user_type == User.OWNER

def check_if_seller(request):
    return request.user.user.user_type == User.SELLER

def check_if_warehouseman(request):
    return request.user.user.user_type == User.WAREHOUSEMAN

# owner menu
def index(request):
    user = User.objects.get(name=request.user)
    if str(user.user_type) == "owner":
        pass
    elif str(user.user_type) == "seller":
        messages.error(request, 'access denied')
        return redirect('seller_index')
    elif str(user.user_type) == "warehouseman":
        messages.error(request, 'access denied')
        return redirect('warehouse_index')

    return render(request, "owner/index.html")


# auth
def register_page(request):
    form = CreateUserForm()

    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data['username']
            user_type = form.cleaned_data['user_type']
            user_type2 = form.cleaned_data['user_type2']

            User.objects.create(
                user=user,
                name=user.username,
                user_type=user_type,
                user_type2=user_type2,
            )

            messages.success(request, f'Created user {username}')
            return redirect('owner_index')
        else:
            print(form.errors)

    context = {
        'form': form,
    }

    return render(request, "owner/register.html", context)


def login_page(request):
    if request.user.is_authenticated:
        return render(request, 'warehouse/index.html')

    else:
        if request.method == "POST":
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request,
                                username=username,
                                password=password,
                                )

            if user is not None:
                login(request, user)

                if str(User.objects.get(name=username).user_type) == "seller":
                    return redirect('seller_index')
                elif str(User.objects.get(name=username).user_type) == "warehouseman":
                    return redirect('warehouse_index')
                elif str(User.objects.get(name=username).user_type) == "owner":
                    return redirect('owner_index')

    context = {}

    return render(request, "owner/login.html", context)


def logout_page(request):
    logout(request)
    return redirect('login')
