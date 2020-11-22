from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='seller_index'),
    # order
    path('create-new-order/', views.create_order, name='new_order'),
    path('delete-order/<int:order_id>/', views.delete_order, name='delete_order'),
    path('order-details/<int:order_id>/', views.order_details, name='order_details'),
    path('change-open-status/<int:order_id>/', views.change_open_status, name='change_open_status'),
    path('change_paid_status/<int:order_id>/', views.change_paid_status, name='change_paid_status'),
    path('change_send_status/<int:order_id>/', views.change_send_status, name='change_send_status'),
    # product
    path('add-to-order/<int:product_id>/', views.add_to_order, name='add_to_order'),
    path('display-product/<int:product_id>/', views.display_product_info, name='order_product_info'),
    path('remove-from-order/<int:product_id>/<int:order_id>/', views.remove_from_order, name='remove_from_order'),
    path('increase-quantity/<int:product_id>/<int:order_id>/', views.increase_quantity, name='increase_quantity'),
    path('reduce-quantity/<int:product_id>/<int:order_id>/', views.reduce_quantity, name='reduce_quantity'),
    # category
    path('category-products/<int:category_id>/', views.category_products, name='order_category_products'),
]
