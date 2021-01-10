from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    # path('admin/', admin.site.urls),
    path('', views.index, name='shop'),
    path('about/', views.about, name='about'),
    path('contact/', views.contactus, name='contactUs'),
    path('tracker/', views.tracker, name='tracker'),
    path('search/', views.search, name='search'),
    path('productview/<int:id>', views.productview, name='product'),
    path('checkout/', views.checkout, name='checkout'),
    path('HandleReqst/', views.HandleReqst, name='HandleReqst'),
]
