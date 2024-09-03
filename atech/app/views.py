from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import *
from .forms import *
from django.db.models import Q
from .models import Product, Category, Brand, Color
from .forms import AdvancedSearchForm
from .models import Product, Cart

def home(request):
    search_form = SearchForm(request.GET)
    advanced_search_form = AdvancedSearchForm(request.GET)
    products = Product.objects.all()
    categories = Category.objects.all()

    if search_form.is_valid():
        product_name = search_form.cleaned_data.get('product_name')
        if product_name:
            products = products.filter(product_name__icontains=product_name)

    if advanced_search_form.is_valid():
        product_name = advanced_search_form.cleaned_data.get('product_name')
        min_price = advanced_search_form.cleaned_data.get('min_price')
        max_price = advanced_search_form.cleaned_data.get('max_price')
        category = advanced_search_form.cleaned_data.get('category')
        brand = advanced_search_form.cleaned_data.get('brand')
        color = advanced_search_form.cleaned_data.get('color')

        if product_name:
            products = products.filter(product_name__icontains=product_name)
        if min_price:
            products = products.filter(price__gte=min_price)
        if max_price:
            products = products.filter(price__lte=max_price)
        if category:
            products = products.filter(category__in=category).distinct()
        if brand:
            products = products.filter(brand__in=brand).distinct()
        if color:
            products = products.filter(color__in=color).distinct()

    return render(request, 'base.html', {
        'search_form': search_form,
        'advanced_search_form': advanced_search_form,
        'products': products,
        'categories': categories,
    })


def category_view(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    products = Product.objects.filter(category=category)
    search_form = SearchForm(request.GET)
    advanced_search_form = AdvancedSearchForm(request.GET)
    categories = Category.objects.all() 

    if search_form.is_valid():
        product_name = search_form.cleaned_data.get('product_name')
        if product_name:
            products = products.filter(product_name__icontains=product_name)

    if advanced_search_form.is_valid():
        product_name = advanced_search_form.cleaned_data.get('product_name')
        price = advanced_search_form.cleaned_data.get('price')
        brand = advanced_search_form.cleaned_data.get('brand')
        color = advanced_search_form.cleaned_data.get('color')

        if product_name:
            products = products.filter(product_name__icontains=product_name)
        if price:
            products = products.filter(price=price)
        if brand:
            products = products.filter(brand__in=brand).distinct()
        if color:
            products = products.filter(color__in=color).distinct()

    return render(request, 'category_view.html', {
        'category': category,
        'products': products,
        'search_form': search_form,
        'advanced_search_form': advanced_search_form,
        'categories': categories, 
    })

def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    search_form = SearchForm(request.GET) 
    advanced_search_form = AdvancedSearchForm(request.GET)
    categories = Category.objects.all()
    return render(request, 'product_detail.html', {
        'product': product,
        'search_form': search_form,
        'advanced_search_form': advanced_search_form,
        'categories': categories,
    })

def search_view(request):
    form = SearchForm(request.GET)
    products = Product.objects.none()
    search_form = SearchForm(request.GET)
    advanced_search_form = AdvancedSearchForm(request.GET)
    categories = Category.objects.all()

    if form.is_valid():
        product_name = form.cleaned_data.get('product_name')
        if product_name:
            products = Product.objects.filter(product_name__icontains=product_name)

    return render(request, 'search_results.html', {
        'products': products,
        'form': form,
        'search_form': search_form,
        'advanced_search_form': advanced_search_form,
        'categories': categories,
    })

def advanced_search_view(request):
    advanced_search_form = AdvancedSearchForm(request.GET)
    products = Product.objects.all()
    categories = Category.objects.all() 


    if advanced_search_form.is_valid():
            product_name = advanced_search_form.cleaned_data.get('product_name')
            min_price = advanced_search_form.cleaned_data.get('min_price')
            max_price = advanced_search_form.cleaned_data.get('max_price')
            category = advanced_search_form.cleaned_data.get('category')
            brand = advanced_search_form.cleaned_data.get('brand')
            color = advanced_search_form.cleaned_data.get('color')

            if product_name:
                products = products.filter(product_name__icontains=product_name)
            if min_price is not None:
                products = products.filter(price__gte=min_price)
            if max_price is not None:
                products = products.filter(price__lte=max_price)
            if category:
                products = products.filter(category__in=category)
            if brand:
                products = products.filter(brand__in=brand)
            if color:
                products = products.filter(color__in=color)

            return render(request, 'search_results.html', {
                'products': products,
                'search_form': SearchForm(), 
                'advanced_search_form': advanced_search_form,
                'categories': categories,
            })

def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    cart = request.session.get('cart', {})

    if str(product_id) in cart:
        cart[str(product_id)] += 1 
    else:
        cart[str(product_id)] = 1

    request.session['cart'] = cart

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', reverse('home')))


def view_cart(request):
    search_form = SearchForm(request.GET)
    advanced_search_form = AdvancedSearchForm(request.GET)
    
    categories = Category.objects.all()

    cart = request.session.get('cart', {})
    products = Product.objects.filter(id__in=cart.keys())
    cart_items = []

    for product in products:
        cart_items.append({
            'product': product,
            'quantity': cart[str(product.id)],
            'total_price': product.price * cart[str(product.id)]
        })

    context = {
        'cart_items': cart_items,
        'total_cart_price': sum(item['total_price'] for item in cart_items),
        'search_form': search_form,
        'advanced_search_form': advanced_search_form,
        'categories': categories,
    }
    
    return render(request, 'cart.html', context)



def increase_quantity(request, product_id):
    cart = request.session.get('cart', {})

    if str(product_id) in cart:
        cart[str(product_id)] += 1
        request.session['cart'] = cart

    return redirect('view_cart')

def decrease_quantity(request, product_id):
    cart = request.session.get('cart', {})

    if str(product_id) in cart:
        if cart[str(product_id)] > 1:
            cart[str(product_id)] -= 1
        else:
            del cart[str(product_id)]
        request.session['cart'] = cart

    return redirect('view_cart')

def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})

    if str(product_id) in cart:
        del cart[str(product_id)]
        request.session['cart'] = cart

    return redirect('view_cart')


def checkout_view(request):
    search_form = SearchForm(request.GET)
    advanced_search_form = AdvancedSearchForm(request.GET)

    cart_items = request.session.get('cart_items', []) 
    total_cart_price = sum(item['price'] * item['quantity'] for item in cart_items)

    context = {
        'search_form': search_form,
        'advanced_search_form': advanced_search_form,
        'cart_items': cart_items,
        'total_cart_price': total_cart_price,
    }

    return render(request, 'checkout.html', context)