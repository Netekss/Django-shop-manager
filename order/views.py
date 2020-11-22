import random

from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test, login_required
from django.core.exceptions import ObjectDoesNotExist

from owner.models import User
from warehouse.models import Item, Category
from .models import OrderItem, Order
from .forms import RawSearchOrder


def user_check(request):
    user = User.objects.get(name=request.user)
    return str(user.user_type) == "seller" or str(user.user_type) == "owner"


@login_required(login_url='login')
def index(request):
    user = User.objects.get(name=request.user)
    if str(user.user_type) == "seller" or str(user.user_type) == "owner":
        pass
    elif str(user.user_type) == "warehouseman":
        messages.error(request, 'access denied')
        return redirect('warehouse_index')

    # open order
    open_order = Order.objects.filter(open_status=True)

    # waiting orders
    waiting_orders = Order.objects.filter(waiting_status=True)

    # categories
    categories = Category.objects.all()

    paginator = Paginator(categories, 4)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # search
    search_form = RawSearchOrder()
    if request.method == "POST":
        search_form = RawSearchOrder(request.POST)
        if search_form.is_valid():
            expected_order_id = search_form.cleaned_data['order_id']
            try:
                expected_order = Order.objects.get(order_id=expected_order_id)
                return redirect('order_details', order_id=expected_order.id)
            except ObjectDoesNotExist:
                messages.error(request, f"Cant find order with id: {expected_order_id}")

    context = {'open_order': open_order,
               'waiting_orders': waiting_orders,
               'categories': page_obj,
               'search_form': search_form
               }

    return render(request, "order/index.html", context)


# order
def create_unique_order_id():
    """Function witch creating new unique order_id"""
    numbers = []
    for i in range(48, 58):
        numbers.append(chr(i))

    def create_id():
        order_id = "order#"
        for i in range(5):
            x = random.choice(numbers)
            order_id += x
        return order_id

    while True:
        new_order_id = create_id()
        id_exists = Order.objects.filter(order_id=new_order_id)

        if not bool(id_exists):
            break
    return new_order_id


@login_required(login_url='login')
@user_passes_test(user_check, login_url='login')
def create_order(request):
    open_status_check = Order.objects.filter(open_status=True)
    if len(open_status_check) == 1:
        messages.error(request, f"You have one active order: {open_status_check[0]}")
        return redirect('seller_index')
    else:
        new_order_id = create_unique_order_id()
        Order.objects.create(order_id=new_order_id)
        messages.success(request, f"New order created! ID: {new_order_id}")
        return redirect('seller_index')


@login_required(login_url='login')
@user_passes_test(user_check, login_url='login')
def delete_order(request, order_id):
    order = Order.objects.get(id=order_id)
    products = OrderItem.objects.filter(order_id=order.order_id)

    if len(products) > 0:
        messages.error(request, 'Cannot delete order, because order still have products.')
    else:
        order.delete()
        messages.success(request, f'Order "{order.order_id}" deleted')
    return redirect('seller_index')


@login_required(login_url='login')
@user_passes_test(user_check, login_url='login')
def order_details(request, order_id):
    order = Order.objects.get(pk=order_id)
    order_items = OrderItem.objects.filter(order_id=order.order_id)
    waiting_orders = Order.objects.filter(waiting_status=True)

    # search
    search_form = RawSearchOrder()
    if request.method == "POST":
        search_form = RawSearchOrder(request.POST)
        if search_form.is_valid():
            expected_order_id = search_form.cleaned_data['order_id']
            try:
                expected_order = Order.objects.get(order_id=expected_order_id)
                return redirect('order_details', order_id=expected_order.id)
            except ObjectDoesNotExist:
                messages.error(request, f"Cant find order with id: {expected_order_id}")

    context = {
        'order': order,
        'order_items': order_items,
        'waiting_orders': waiting_orders,
        'search_form': search_form,
    }
    return render(request, "order/order_details.html", context)


@login_required(login_url='login')
@user_passes_test(user_check, login_url='login')
def change_open_status(request, order_id):
    order = Order.objects.get(id=order_id)

    if order.open_status:
        order.open_status = False
        order.waiting_status = True
        order.save()
        messages.info(request, 'Changed order status to: waiting')

    elif not order.open_status:
        open_status_check = Order.objects.filter(open_status=True)

        if open_status_check.exists():
            messages.error(request, 'You have to close active order to change this status!')
        else:
            order.waiting_status = False
            order.open_status = True
            order.save()
            messages.success(request, 'Changed order status to: open')

    return redirect('order_details', order_id=order_id)


@login_required(login_url='login')
@user_passes_test(user_check, login_url='login')
def change_paid_status(request, order_id):
    order = Order.objects.get(id=order_id)
    products = OrderItem.objects.filter(order_id=order.order_id)

    if len(products) > 0:
        if order.open_status:
            if not order.paid:
                order.paid = True
                order.save()
                messages.success(request, f'Order "{order.order_id}" paid')
            elif order.paid:
                order.paid = False
                order.save()
                messages.success(request, f'Order "{order.order_id}" unpaid')
        else:
            messages.error(request, 'First you need to change the order status to "open"')
    else:
        messages.error(request, 'Cannot change paid status without items in order.')

    return redirect('order_details', order_id=order_id)


@login_required(login_url='login')
@user_passes_test(user_check, login_url='login')
def change_send_status(request, order_id):
    order = Order.objects.get(id=order_id)

    if order.paid:
        order.open_status = False
        order.waiting_status = False
        order.send_status = True
        order.save()

        messages.success(request, 'Order has been send to warehouse')

    elif not order.paid:
        messages.error(request, 'Order have to be paid before send')

    return redirect('seller_index')


# product
@login_required(login_url='login')
@user_passes_test(user_check, login_url='login')
def display_product_info(request, product_id):
    product = get_object_or_404(Item, id=product_id)

    context = {
        'product': product
    }

    return render(request, 'order/product_info.html', context)


@login_required(login_url='login')
@user_passes_test(user_check, login_url='login')
def add_to_order(request, product_id):
    product = Item.objects.get(pk=product_id)

    try:
        order = Order.objects.get(open_status=True)
        order_id = order.order_id

        if product.quantity_on_stock > 0:
            if OrderItem.objects.filter(item=product, order_id=order_id).exists():
                new_order_item = OrderItem.objects.get(item=product, order_id=order_id)
                new_order_item.quantity += 1
                new_order_item.save()

                product.quantity_on_stock -= 1
                product.save()
                messages.success(request, "Product already in order, quantity increased by one.")
            else:
                item_order_id = f"{product.title}-{order_id}"
                new_order_item = OrderItem.objects.create(item=product, order_id=order_id, item_order_id=item_order_id)
                new_order_item.quantity += 1
                new_order_item.save()

                product.quantity_on_stock -= 1
                product.save()

                order.items.add(new_order_item)
                order.save()
                messages.success(request, f"{product.title} added to order")
        else:
            messages.error(request, f'No more "{product.title}" on stock')
    except ObjectDoesNotExist:
        messages.error(request, 'You have to have open order')

    return redirect('seller_index')


@login_required(login_url='login')
@user_passes_test(user_check, login_url='login')
def increase_quantity(request, product_id, order_id):
    order = Order.objects.get(id=order_id)
    product = OrderItem.objects.get(pk=product_id)
    item = Item.objects.get(title=product.item.title)

    if order.open_status:
        if item.quantity_on_stock > 0:
            product.quantity += 1
            item.quantity_on_stock -= 1
            product.save()
            item.save()
        else:
            messages.error(request, f'No more "{item}" on stock.')
    else:
        messages.error(request, 'First you need to change the order status to "open"')

    return redirect('order_details', order_id=order_id)


@login_required(login_url='login')
@user_passes_test(user_check, login_url='login')
def reduce_quantity(request, product_id, order_id):
    order = Order.objects.get(id=order_id)
    product = OrderItem.objects.get(pk=product_id)
    item = Item.objects.get(title=product.item.title)

    if order.open_status:
        if product.quantity < 1:
            product.delete()
            messages.success(request, f'Removed from order "{item}"')
        else:
            product.quantity -= 1
            item.quantity_on_stock += 1
            product.save()
            item.save()
    else:
        messages.error(request, 'First you need to change the order status to "open"')

    return redirect('order_details', order_id=order_id)


@login_required(login_url='login')
@user_passes_test(user_check, login_url='login')
def remove_from_order(request, product_id, order_id):
    order = Order.objects.get(id=order_id)
    product = OrderItem.objects.get(pk=product_id)
    product_to_remove = OrderItem.objects.get(item_order_id=product)

    if order.open_status:
        item = Item.objects.get(title=product.item.title)
        item.quantity_on_stock += product_to_remove.quantity
        item.save()

        product_to_remove.delete()
        messages.success(request, f'Product "{item.title}" removed from order.')
    else:
        messages.error(request, 'First you need to change the order status to "open"')

    return redirect('order_details', order_id=order_id)


# category
@login_required(login_url='login')
@user_passes_test(user_check, login_url='login')
def category_products(request, category_id):
    products = Item.objects.filter(category=category_id)

    context = {
        'products': products
    }

    return render(request, 'order/category_products.html', context)
