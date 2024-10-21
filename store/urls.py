from django.urls import path,include
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('login',views.login_user,name='login'),
    path('logout',views.logout_user,name='logout'),
   path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('register',views.reg,name='register'),
    path('product/<slug:slug>/', views.product_detail, name='productd'),
    path('category/<slug:slug>/', views.cat, name='cat'),
    path('cart',views.view_cart,name='cart'),
    path('cart/update/<int:cart_item_id>/', views.update_cart, name='update_cart'),
    path('cart/remove/<int:cart_item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout_view, name='checkout'),
    path('success/', views.done, name='success')
]