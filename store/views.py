from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.db import transaction

from .models import Product, Order, OrderItem
from .forms import ProductForm


# ==========================================
# HOME PAGE
# ==========================================

def home(request):

    products = Product.objects.all().order_by('-created_at')

    return render(
        request,
        'store/home.html',
        {
            'products': products
        }
    )


# ==========================================
# PRODUCT LIST + SEARCH
# ==========================================

def product_list(request):

    search_query = request.GET.get('search', '')

    products = Product.objects.all().order_by('-created_at')

    if search_query:

        products = products.filter(
            name__icontains=search_query
        )

    return render(
        request,
        'store/product_list.html',
        {
            'products': products,
            'search_query': search_query,
        }
    )


# ==========================================
# PRODUCT DETAIL
# ==========================================

def product_detail(request, product_id):

    product = get_object_or_404(
        Product,
        id=product_id
    )

    return render(
        request,
        'store/product_detail.html',
        {
            'product': product
        }
    )


# ==========================================
# ADD ORDER
# ==========================================

@login_required
def add_order(request, product_id):

    product = get_object_or_404(
        Product,
        id=product_id
    )

    if request.method == 'POST':

        # --------------------------------------
        # Validate quantity input
        # --------------------------------------

        try:

            quantity = int(
                request.POST.get('quantity', 1)
            )

        except (TypeError, ValueError):

            messages.error(
                request,
                'Invalid quantity.'
            )

            return redirect(
                'product_detail',
                product_id=product.id
            )

        # --------------------------------------
        # Check minimum quantity
        # --------------------------------------

        if quantity < 1:

            messages.error(
                request,
                'Quantity must be at least 1.'
            )

            return redirect(
                'product_detail',
                product_id=product.id
            )

        # --------------------------------------
        # Check available stock
        # --------------------------------------

        if quantity > product.stock:

            messages.error(
                request,
                'Requested quantity is greater than available stock.'
            )

            return redirect(
                'product_detail',
                product_id=product.id
            )

        # --------------------------------------
        # Calculate total price
        # --------------------------------------

        total_price = product.price * quantity

        # --------------------------------------
        # Create order
        # --------------------------------------

        with transaction.atomic():

            order = Order.objects.create(
                user=request.user
            )

            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=quantity,
                total_price=total_price
            )

            # Reduce product stock
            product.stock -= quantity

            product.save()

        # --------------------------------------
        # Success message
        # --------------------------------------

        messages.success(
            request,
            'Your order has been placed successfully.'
        )

        return redirect(
            'product_detail',
            product_id=product.id
        )

    # ------------------------------------------
    # If request is not POST
    # ------------------------------------------

    return redirect(
        'product_detail',
        product_id=product.id
    )


# ==========================================
# MY ORDERS
# ==========================================

@login_required
def my_orders(request):

    orders = Order.objects.filter(
        user=request.user
    ).prefetch_related(
        'items__product'
    ).order_by('-order_date')

    return render(
        request,
        'store/my_orders.html',
        {
            'orders': orders
        }
    )


# ==========================================
# CREATE PRODUCT
# ADMIN / STAFF ONLY
# ==========================================

@staff_member_required
def product_create(request):

    if request.method == 'POST':

        form = ProductForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                'Product added successfully.'
            )

            return redirect(
                'product_list'
            )

    else:

        form = ProductForm()

    return render(
        request,
        'store/product_form.html',
        {
            'form': form,
            'title': 'Add Product'
        }
    )


# ==========================================
# UPDATE PRODUCT
# ADMIN / STAFF ONLY
# ==========================================

@staff_member_required
def product_update(request, product_id):

    product = get_object_or_404(
        Product,
        id=product_id
    )

    if request.method == 'POST':

        form = ProductForm(
            request.POST,
            request.FILES,
            instance=product
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                'Product updated successfully.'
            )

            return redirect(
                'product_list'
            )

    else:

        form = ProductForm(
            instance=product
        )

    return render(
        request,
        'store/product_form.html',
        {
            'form': form,
            'title': 'Edit Product'
        }
    )


# ==========================================
# DELETE PRODUCT
# ADMIN / STAFF ONLY
# ==========================================

@staff_member_required
def product_delete(request, product_id):

    product = get_object_or_404(
        Product,
        id=product_id
    )

    if request.method == 'POST':

        product.delete()

        messages.success(
            request,
            'Product deleted successfully.'
        )

        return redirect(
            'product_list'
        )

    return render(
        request,
        'store/product_confirm_delete.html',
        {
            'product': product
        }
    )


# ==========================================
# USER REGISTRATION
# ==========================================

def register(request):

    if request.method == 'POST':

        form = UserCreationForm(
            request.POST
        )

        if form.is_valid():

            user = form.save()

            messages.success(
                request,
                'Registration successful. You can now login.'
            )

            return redirect(
                'login'
            )

    else:

        form = UserCreationForm()

    return render(
        request,
        'store/register.html',
        {
            'form': form
        }
    )