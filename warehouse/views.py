from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test, login_required


from owner.models import User
from order.models import Order, OrderItem
from .models import Item, Category
from .forms import NewProductForm, SearchForProduct, NewCategoryForm, SearchForCategory


def user_check(request):
    user = User.objects.get(name=request.user)
    return user.user_type == User.WAREHOUSEMAN or user.user_type == User.OWNER


@login_required(login_url='login')
def index(request):
    # user = User.objects.get(name=request.user)
    user = request.user.user
    if user.user_type == User.SELLER:
        messages.error(request, 'access denied')
        return redirect('seller_index')

    # low quantity
    products = Item.objects.filter(quantity_on_stock__lt=5)

    paginator = Paginator(products, 2)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # orders
    orders = Order.objects.filter(send_status=True)

    context = {
        'low_quantity': page_obj,
        'orders': orders,
    }

    return render(request, 'warehouse/index.html', context)


# product
@login_required(login_url='login')
@user_passes_test(user_check, login_url='login')
def create_new_product(request):
    form = NewProductForm()

    if request.method == "POST":
        form = NewProductForm(request.POST)
        if form.is_valid():
            if Item.objects.filter(title=form.cleaned_data['title']).exists():
                messages.error(request, f'"{form.cleaned_data["title"]}" already on stock')
            else:
                new_product = Item.objects.create(
                    title=form.cleaned_data['title'].title(),
                    category=form.cleaned_data['category'],
                    price=form.cleaned_data['price'],
                    description=form.cleaned_data['description'],
                    quantity_on_stock=form.cleaned_data['quantity_on_stock']
                )
                new_product.save()
                messages.success(request, f'"{form.cleaned_data["title"]}" created')
                return redirect('warehouse_index')

    context = {
        'form': form,
    }

    return render(request, "warehouse/add_new_product.html", context)


@login_required(login_url='login')
@user_passes_test(user_check, login_url='login')
def edit_product(request, product_id):
    product = get_object_or_404(Item, id=product_id)

    form = NewProductForm(request.POST or None, instance=product)

    if form.is_valid():
        messages.success(request, f'Product "{product.title}" edited')
        form.save()
        return redirect('display_products')

    context = {
        'form': form,
        'product': product,
    }
    return render(request, "warehouse/edit_product.html", context)


@login_required(login_url='login')
@user_passes_test(user_check, login_url='login')
def display_products(request):
    try:
        products = Item.objects.all()

        paginator = Paginator(products, 2)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context = {
            'products': page_obj
        }
        return render(request, "warehouse/all_products.html", context)

    except ObjectDoesNotExist:
        messages.error(request, "You haven't any product in warehouse")
        return redirect('warehouse_index')


@login_required(login_url='login')
@user_passes_test(user_check, login_url='login')
def display_product_info(request, product_id):
    product = get_object_or_404(Item, id=product_id)

    context = {
        'product': product
    }

    return render(request, "warehouse/product_info.html", context)


@login_required(login_url='login')
@user_passes_test(user_check, login_url='login')
def search_product(request):
    search_form = SearchForProduct()
    expected_product = []

    if request.method == "POST":
        search_form = SearchForProduct(request.POST)

        if search_form.is_valid():

            # search by title and description
            if search_form.cleaned_data['title'] and search_form.cleaned_data['description']:
                title = search_form.cleaned_data['title']
                description = search_form.cleaned_data['description']
                products = Item.objects.all()

                for product in products:
                    if (title.lower() in str(product).lower()) and (
                            description.lower() in str(product.description).lower()):
                        expected_product.append(product)

            # search by title
            elif search_form.cleaned_data['title']:
                title = search_form.cleaned_data['title']
                products = Item.objects.all()

                for product in products:
                    if title.lower() in str(product).lower():
                        expected_product.append(product)

            # search by description
            elif search_form.cleaned_data['description']:
                description = search_form.cleaned_data['description']
                products = Item.objects.all()

                for product in products:
                    if description.lower() in str(product.description).lower():
                        expected_product.append(product)

            if len(expected_product) == 0:
                messages.error(request, 'Cant find any product')

    context = {
        'search_form': search_form,
        'expected_product': expected_product
    }
    return render(request, 'warehouse/search_for_product.html', context)


# category
@login_required(login_url='login')
@user_passes_test(user_check, login_url='login')
def create_new_category(request):
    form = NewCategoryForm

    if request.method == "POST":
        form = NewCategoryForm(request.POST)
        if form.is_valid():
            if Category.objects.filter(title=form.cleaned_data['title']).exists():
                messages.error(request, f'Category "{form.cleaned_data["title"]}" already exists')
            else:
                new_category = Category.objects.create(
                    title=form.cleaned_data['title']
                )
                new_category.save()
                messages.success(request, f'Category "{form.cleaned_data["title"]}" created')
                return redirect('/warehouse')

    context = {
        'form': form
    }

    return render(request, "warehouse/add_new_category.html", context)


@login_required(login_url='login')
@user_passes_test(user_check, login_url='login')
def display_categories(request):
    try:
        categories = Category.objects.all()

        context = {
            'categories': categories
        }

        return render(request, "warehouse/all_categories.html", context)

    except ObjectDoesNotExist:
        messages.error(request, "You haven't any categories")
        return redirect('warehouse_index')


@login_required(login_url='login')
@user_passes_test(user_check, login_url='login')
def search_category(request):
    search_form = SearchForCategory()

    if request.method == "POST":
        search_form = SearchForCategory(request.POST)
        if search_form.is_valid():
            title = search_form.cleaned_data['title']
            try:
                category = Category.objects.get(title=title)
                return redirect('category_products', category_id=category.id)
            except ObjectDoesNotExist:
                messages.error(request, 'Cant find category')

    context = {
        'search_form': search_form,
    }

    return render(request, 'warehouse/search_for_category.html', context)


@login_required(login_url='login')
@user_passes_test(user_check, login_url='login')
def products_in_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    products = Item.objects.filter(category=category)

    if len(products) > 0:
        context = {
            'products': products
        }
        return render(request, "warehouse/category_products.html", context)
    else:
        messages.error(request, f'No products in category "{category}"')
        return redirect('warehouse_index')


# order
@login_required(login_url='login')
@user_passes_test(user_check, login_url='login')
def display_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    products = OrderItem.objects.filter(order_id=order.order_id)

    context = {
        'order': order,
        'products': products,
    }

    return render(request, 'warehouse/display_order.html', context)


@login_required(login_url='login')
@user_passes_test(user_check, login_url='login')
def change_close_status(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    order.send_status = False
    order.close_status = True
    order.save()

    messages.success(request, f'Order "{order.order_id}" status: Closed')
    return redirect('warehouse_index')
