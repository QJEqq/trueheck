from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.IndexView.as_view() , name='index'),
    path('catalog/', views.CatalogView.as_view() , name='catalog_all'),
    path('catalog/<slug:brand_slug>/', views.CatalogView.as_view() , name='catalog_by_brand'),
    path('car/<slug:slug>/', views.CarDetailView.as_view() , name='car_detail'),
    
]
