from django.urls import path
from .views import cart, add, remove

app_name = 'carts'

urlpatterns = [
  path('', cart, name='cart'),
  path('agregar', add, name='add'),
  path('eliminar', remove, name='remove'),
]

