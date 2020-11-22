from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name="warehouse_index"),
    # product
    path('create-new-product/', views.create_new_product, name='create_product'),
    path('edit-product/<int:product_id>/', views.edit_product, name='edit_product'),
    path('display-product/<int:product_id>/', views.display_product_info, name='product_info'),
    path('display-products/', views.display_products, name='display_products'),
    path('search-product/', views.search_product, name='search_product'),
    # category
    path('create-new-category/', views.create_new_category, name='create_category'),
    path('display-categories/', views.display_categories, name='display_categories'),
    path('category-products/<int:category_id>/', views.products_in_category, name='category_products'),
    path('search-category/', views.search_category, name='search_category'),
    # order
    path('display-order/<int:order_id>/', views.display_order, name='display_order'),
    path('change-close-status/<int:order_id>/', views.change_close_status, name='change_close_status'),
]
