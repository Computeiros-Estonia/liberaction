from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import redirect, render
from .models import Album, Picture, BaseProduct, Product
from .forms import BaseProductForm, ProductForm

def index(request):
    user = request.user
    products = Product.objects.all()

    context = {
        'products': products,
    }
    return render(request, 'core/index.html', context)

@login_required(login_url='/users/login/')
def create_product(request):
    if request.method == 'POST':
        base_form = BaseProductForm(request.POST, request.FILES, prefix='base', initial={'owner': request.user.id})
        product_form = ProductForm(request.POST, prefix='product')
        if base_form.is_valid():
            base_product = base_form.save()
            product_form = ProductForm(request.POST, initial={'base': base_product}, prefix='product')
            if product_form.is_valid():
                product_form.save()
                messages.success(request, 'Produto adicionado com sucesso!')
                if request.FILES:
                    album = Album.objects.create(base_product=base_product)
                    try:
                        files = request.FILES.getlist('images')
                        i=0
                        for img in files:
                            Picture.objects.create(img=img, index=i, album=album)
                            i+=1
                        return redirect('core:create_product')
                    except Exception as e:
                        messages.error(request, 'Falha ao fazer o upload das fotos.')
                        album.delete()
            else:
                messages.error(request, 'Falha ao criar produto.')
                base_product.delete()

    else:
        base_form = BaseProductForm(prefix='base', initial={'owner': request.user.id})
        product_form = ProductForm(prefix='product')
    
    context = {
        'title': 'Cadastro de Produto',
        'base_form': base_form,
        'product_form': product_form,
    }
    return render(request, 'core/create_product.html', context)


def product_details(request, pk):
    context = {
        'product': Product.objects.get(id=pk),
    }
    return render(request, 'core/product.html', context)