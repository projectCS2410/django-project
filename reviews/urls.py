from django.urls import path
from . import views  # ОБЯЗАТЕЛЬНО: точка означает "текущая папка"

urlpatterns = [
    path('', views.ItemListView.as_view(), name='item_list'),
    path('<int:pk>/', views.ItemDetailView.as_view(), name='item_detail'),
    path('search/advanced/', views.AdvancedSearchView.as_view(), name='advanced_search'),
]