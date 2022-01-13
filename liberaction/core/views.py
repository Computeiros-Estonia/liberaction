from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import redirect, render
from .models import Album, Picture, Product, Review
from .forms import ProductForm

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
        form = ProductForm(request.POST, request.FILES, initial={'owner': request.user.id})
        if form.is_valid():
            product = form.save()
            messages.success(request, 'Produto adicionado com sucesso!')
            if request.FILES:
                album = Album.objects.create(product=product)
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
        form = ProductForm(initial={'owner': request.user.id})
    
    context = {
        'title': 'Cadastro de Produto',
        'form': form
    }
    return render(request, 'core/create_product.html', context)


def product_details(request, pk):
    context = {
        'product': Product.objects.get(id=pk),
    }
    return render(request, 'core/product.html', context)