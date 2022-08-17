from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth import login
from django.contrib import messages
from django.urls import reverse
from liberaction.users.models import Address, User
from liberaction.users.forms import UserCreationForm, UserEditForm, AddressForm

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('core:index')
    else:
        form = UserCreationForm()

    context = {
        'title': 'Registration',
        'form': form,
        'gender_choices': User.GENDER_CHOICES,
    }
    return render(request, 'users/register.html', context)

def perfil(request):
    user = request.user
    if not user.is_authenticated:
        return Http404()    
    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Perfil alterado com sucesso!')
            return redirect('perfil')
    else:
        form = UserEditForm(instance=user)

    context = {
        'user': user,
        'form': form,
    }
    return render(request, 'users/perfil.html', context)

# Addresses
@login_required(login_url='/users/login/')
def user_addresses(request, user_pk):
    user = get_object_or_404(User, pk=user_pk)
    context = {
        'title': 'Meus Endereços',
        'user': user,
        'addresses': user.get_all_addresses(),
    }
    return render(request, 'users/user_addresses.html', context)

@login_required(login_url='/users/login/')
def create_address(request):
    if request.method == 'POST':
        form = AddressForm(request.POST, initial={'user': request.user.pk})
        if form.is_valid():
            form.save()
            messages.success(request, 'Endereço adicionado com sucesso.')
            return redirect('user_addresses', request.user.pk)
    else:
        form = AddressForm(initial={'user': request.user.pk})
    
    context = {
        'title': 'Adicionar novo endereço',
        'form_action': reverse('create_address'),
        'form': form,
    }
    return render(request, 'users/address_form.html', context)

@login_required(login_url='/users/login/')
def update_address(request, pk):
    address = get_object_or_404(Address, pk=pk)
    if request.method == 'POST':
        form = AddressForm(request.POST, instance=address)
        if form.is_valid():
            form.save()
            messages.success(request, 'Endereço alterado com sucesso.')
            return redirect('user_addresses', request.user.pk)
    else:
        form = AddressForm(instance=address)
    
    context = {
        'title': 'Alterar endereço',
        'form_action': reverse('update_address', kwargs={'pk': address.pk}),
        'form': form,
    }
    return render(request, 'users/address_form.html', context)

@login_required(login_url='/users/login/')
def delete_address(request, pk):
    address = get_object_or_404(Address, pk=pk)
    if request.method == 'POST':
        address.delete()
        return redirect('user_addresses', request.user.pk)
    else:
        raise Http404('Página inválida.')
