from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from .models import Album, BaseProduct, Picture, Product, Service
from .forms import BaseProductForm, ProductForm, ServiceForm

def index(request):
    base_products = BaseProduct.objects.all()
    popular_bp = sorted(base_products, key=lambda p: p.get_review_avg_score(), reverse=True)

    context = {
        'base_products': base_products,
        'popular_bp': popular_bp,
    }
    return render(request, 'core/index.html', context)

@login_required(login_url='/users/login/')
def create_product(request):
    if request.method == 'POST':
        # base_form = BaseProductForm(request.POST, request.FILES, prefix='base', initial={'owner': request.user.id})
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save()
            messages.success(request, 'Produto adicionado com sucesso!')
            if request.FILES:
                album = Album.objects.create(base_product=product.base_product)
                try:
                    files = request.FILES.getlist('imgs')
                    i=0
                    for img in files:
                        Picture.objects.create(img=img, index=i, album=album)
                        i+=1
                    return redirect('core:create_product')
                except Exception as e:
                    messages.error(request, 'Falha ao fazer o upload das fotos.')
                    album.delete()
    else:
        # base_form = BaseProductForm(prefix='base', initial={'owner': request.user.id})
        form = ProductForm()
    
    context = {
        'title': 'Cadastro de Produto',
        'form': form,
    }
    return render(request, 'core/create_product.html', context)

def product_details(request, pk):
    try:
        context = {
            'product': Product.objects.get(id=pk),
        }
        return render(request, 'core/product_page_model.html', context)
    except Product.DoesNotExist:
        raise Http404('Produto não encontrado')

@login_required(login_url='/users/login/')
def edit_product(request, pk):
    try:
        product = Product.objects.get(pk=pk)
        if request.method == 'POST':
            base_form = BaseProductForm(request.POST, prefix='base', instance=product.base)
            prod_form = ProductForm(request.POST, prefix='prod', instance=product)
            if base_form.is_valid() and prod_form.is_valid():
                base_form.save()
                prod_form.save()
                messages.success(request, 'Produto alterado com sucesso.')
                return redirect(reverse('core:product', kwargs={'pk':product.pk}))
        else:
            base_form = BaseProductForm(instance=product.base, prefix='base')
            prod_form = ProductForm(instance=product, prefix='prod')
    
        context = {
            'title': 'Editar Produto',
            'product': product,
            'base_form': base_form,
            'prod_form': prod_form,
        }
        return render(request, 'core/edit_product.html', context)
    except Product.DoesNotExist:
        raise Http404('Product not found.')

@login_required(login_url='/users/login/')
def delete_product(request, pk):
    try:
        product = Product.objects.get(pk=pk)
        product.delete()
        return redirect('core:index')
    except Product.DoesNotExist:
        raise Http404('Produto não encontrado')

@login_required(login_url='/users/login/')
def create_service(request):
    if request.method == 'POST':
        base_form = BaseProductForm(request.POST, request.FILES, prefix='base', initial={'owner': request.user.id})
        service_form = ServiceForm(request.POST, prefix='service')
        if base_form.is_valid():
            base_product = base_form.save()
            service_form = ServiceForm(request.POST, initial={'base': base_product}, prefix='service')
            if service_form.is_valid():
                service_form.save()
                messages.success(request, 'Serviço adicionado com sucesso!')
                if request.FILES:
                    album = Album.objects.create(base_product=base_product)
                    try:
                        files = request.FILES.getlist('imgs')
                        i=0
                        for img in files:
                            Picture.objects.create(img=img, index=i, album=album)
                            i+=1
                    except Exception as e:
                        messages.error(request, 'Falha ao fazer o upload das fotos.')
                        album.delete()
                return redirect('core:index')
            else:
                messages.error(request, 'Falha ao criar serviço.')
                base_product.delete()
    else:
        base_form = BaseProductForm(prefix='base', initial={'owner': request.user.id})
        service_form = ServiceForm(prefix='service')

    context = {
        'title': 'Cadastro de Serviço',
        'base_form': base_form,
        'service_form': service_form,
    }
    return render(request, 'core/create_service.html', context)

def service_details(request, pk):
    try:
        context = {
            'service': Service.objects.get(id=pk),
        }
        return render(request, 'core/service.html', context)
    except Service.DoesNotExist:
        raise Http404('Serviço não encontrado')

@login_required(login_url='/users/login/')
def edit_service(request, pk):
    try:
        service = Service.objects.get(pk=pk)
        if request.method == 'POST':
            base_form = BaseProductForm(request.POST, prefix='base', instance=service.base)
            service_form = ServiceForm(request.POST, prefix='prod', instance=service)
            if base_form.is_valid() and service_form.is_valid():
                base_form.save()
                service_form.save()
                messages.success(request, 'Serviço alterado com sucesso.')
                return redirect(reverse('core:service', kwargs={'pk':service.pk}))
        else:
            base_form = BaseProductForm(instance=service.base, prefix='base')
            service_form = ServiceForm(instance=service, prefix='prod')
    
        context = {
            'title': 'Editar Serviço',
            'service': service,
            'base_form': base_form,
            'service_form': service_form,
        }
        return render(request, 'core/edit_service.html', context)
    except Product.DoesNotExist:
        raise Http404('Product not found.')

@login_required(login_url='/users/login/')
def delete_service(request, pk):
    try:
        service = Service.objects.get(pk=pk)
        service.delete()
        messages.success(request, 'Serviço deletado com sucesso.')
        return redirect('core:index')
    except Service.DoesNotExist:
        raise Http404('Serviço não encontrado')


@login_required(login_url='/users/login/')
def service_vs_product_redirection(request):
    return render(request, 'core/sp_redirection.html')


# Favorites
@login_required(login_url='/users/login/')
def favorites(request):
    context = {
        'title': 'Meus favoritos',
        'user': request.user,
    }
    return render(request, 'core/favorites.html', context)

@login_required(login_url='/users/login/')
def add_to_favorites(request, pk):
    product = get_object_or_404(BaseProduct, pk=pk)
    if request.method == 'POST':
        request.user.favorites.add(product)
        messages.success(request, 'Produto adicionado aos seus favoritos.')
        return redirect(reverse('core:product', kwargs={'pk': pk}))

@login_required(login_url='/users/login/')
def remove_from_favorites(request, pk):
    product = get_object_or_404(BaseProduct, pk=pk)
    if request.method == 'POST':
        request.user.favorites.remove(product)
        messages.success(request, 'Produto removido dos seus favoritos.')
        return redirect(reverse('core:product', kwargs={'pk': pk}))
