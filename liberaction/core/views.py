from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from .models import Album, Picture, Product, Service
from .forms import ProductForm, ServiceForm

def index(request):
    products = Product.objects.all()
    pop_produts = sorted(products, key=lambda p: p.get_review_avg_score(), reverse=True)

    context = {
        'products': products,
        'pop_produts': pop_produts,
    }
    return render(request, 'core/index.html', context)


def handle_prod_pics(request, product, file_list):
    album = Album.objects.create(base_product=product)
    try:
        i=0
        for img in file_list:
            Picture.objects.create(img=img, index=i, album=album)
            i+=1
    except Exception as e:
        messages.error(request, 'Falha ao fazer o upload das fotos.')
        album.delete()


@login_required(login_url='/users/login/')
def create_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save()
            if request.FILES:
                album = Album.objects.create(base_product=product)
                try:
                    files = request.FILES.getlist('imgs')
                    i=0
                    for img in files:
                        Picture.objects.create(img=img, index=i, album=album)
                        i+=1
                except Exception as e:
                    messages.error(request, 'Falha ao fazer o upload das fotos.')
                    album.delete()
            messages.success(request, 'Produto adicionado com sucesso!')
            return redirect('core:index')
    else:
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
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            product = form.save()
            if request.FILES:
                album = Album.objects.create(base_product=product)
                try:
                    files = request.FILES.getlist('imgs')
                    i=0
                    for img in files:
                        Picture.objects.create(img=img, index=i, album=album)
                        i+=1
                except Exception as e:
                    messages.error(request, 'Falha ao fazer o upload das fotos.')
                    album.delete()
            messages.success(request, 'Produto alterado com sucesso.')
            return redirect(reverse('core:product', kwargs={'pk':product.pk}))
    else:
        form = ProductForm(instance=product)

    context = {
        'title': 'Editar Produto',
        'product': product,
        'form': form,
    }
    return render(request, 'core/edit_product.html', context)


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
        form = ServiceForm(request.POST)
        if form.is_valid():
            service = form.save()
            if request.FILES:
                files = request.FILES.getlist('imgs')
                handle_prod_pics(request, service, files)
            messages.success(request, 'Serviço adicionado com sucesso!')
            return redirect('core:index')
    else:
        form = ServiceForm()

    context = {
        'title': 'Cadastro de Serviço',
        'form': form,
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
    service = get_object_or_404(Service, pk=pk)
    if request.method == 'POST':
        form = ServiceForm(request.POST, instance=service)
        if form.is_valid():
            service = form.save()
            if request.FILES:
                files = request.FILES.getlist('imgs')
                handle_prod_pics(request, service, files)
            messages.success(request, 'Serviço alterado com sucesso.')
            return redirect(reverse('core:service', kwargs={'pk':service.pk}))
    else:
        form = ServiceForm(instance=service)

    context = {
        'title': 'Editar Serviço',
        'service': service,
        'form': form,
    }
    return render(request, 'core/edit_service.html', context)

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
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        request.user.favorites.add(product)
        messages.success(request, 'Produto adicionado aos seus favoritos.')
        return redirect(reverse('core:product', kwargs={'pk': pk}))

@login_required(login_url='/users/login/')
def remove_from_favorites(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        request.user.favorites.remove(product)
        messages.success(request, 'Produto removido dos seus favoritos.')
        return redirect(reverse('core:product', kwargs={'pk': pk}))
