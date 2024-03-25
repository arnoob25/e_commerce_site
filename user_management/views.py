"""views for authentication"""
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse, reverse_lazy
from .forms import BuyerSignUpForm, MerchantSignUpForm
from .models import BuyerInfo, MerchantInfo, UserInfo


def signup(request):
    """sign the user up"""
    if request.method == 'POST':
        user_type = request.POST.get('user_type')
        if user_type == 'buyer':
            form = BuyerSignUpForm(request.POST)
        else:
            form = MerchantSignUpForm(request.POST)

        if form.is_valid():
            user = form.save()
            if user_type == 'buyer':
                BuyerInfo.objects.create(  # pylint: disable=no-member
                    user=user)
            else:
                store_name = form.cleaned_data.get('store_name')
                MerchantInfo.objects.create(  # pylint: disable=no-member
                    user=user, store_name=store_name)

            return redirect(reverse_lazy('account:login'))
    else:
        buyer_form = BuyerSignUpForm()
        merchant_form = MerchantSignUpForm()
    return render(request, 'signup.html',
                  {'buyer_form': buyer_form, 'merchant_form': merchant_form})


def login_view(request):
    """log the user in"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)

            user_info = UserInfo.objects.get(  # pylint: disable=no-member
                user=user)  
            if user_info.user_type == 'buyer':
                return redirect('products:list')
            else:
                return redirect('products:m-list')
        else:
            # Return an 'invalid login' error message.
            return render(request, 'login.html', {'error': 'Invalid username or password'})
    else:
        return render(request, 'login.html')


@login_required
def logout_view(request):
    """log the user out"""
    logout(request)
    return redirect(reverse('products:list'))
