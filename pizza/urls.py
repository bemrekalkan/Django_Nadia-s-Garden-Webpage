from django.urls import path
from .views import (
    home,
    order,
    pizzas,
    edit_order,
    index,
    pizzas_api,
    pizzas_api_get_update_delete,
    size_api,
)

urlpatterns = [
    path('', home, name='home'), # This is for home page
    path('order/', order, name='order'), # This is for ordering page
    path('pizzas/', pizzas, name='pizzas'),
    path('order/<int:pk>', edit_order, name='edit_order'),
    path('api/', index, name='index'),
    path('api/pizzas/', pizzas_api),
    path('api/pizzas/<int:pk>/', pizzas_api_get_update_delete, name = "detail"),
    path('api/sizes/', size_api),
]