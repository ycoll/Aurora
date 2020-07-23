from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from.models import Product, Category
# Create your views here.


def all_products(request):

    products = Product.objects.all()
    search = None
    categories = None

    if request.GET:
        if 'category' in request.GET:
            categories = request.GET['category'].split(',')
            products = products.filter(category__name__in=categories)
            categories = Category.objects.filter(name__in=categories)

    if request.GET:
        if 's' in request.GET:
            search = request.GET['s']
            if not search:
                messages.error(request, "No search entered")
                return redirect(reverse('products'))

            queries = Q(name__icontains=search) | Q(description__icontains=search)
            products = products.filter(queries)

    context = {
        'products': products,
        'search_term': search,
        'current_categories': categories,
    }

    return render(request, 'products/products.html', context)


def product_detail(request, product_id):

    product = get_object_or_404(Product, pk=product_id)

    context = {
        'product': product,
    }

    return render(request, 'products/product_detail.html', context)

 

