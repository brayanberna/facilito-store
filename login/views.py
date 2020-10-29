from django.shortcuts import render
from django.shortcuts import redirect

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth import authenticate

#from django.contrib.auth.models import User
from users.models import User
from products.models import Product

from .forms import RegisterForm

from django.http import HttpResponseRedirect

# Create your views here.
def index(request):
  products = Product.objects.all().order_by('-id')
  return render(request,'index.html', {
    'message': 'Listado de productos',
    'title': 'Productos',
    'products': products
  })
  
def login_view(request):
  if request.user.is_authenticated:
    return redirect('index')
  #print(request.method)
  if request.method == 'POST':
    username = request.POST['username']
    password = request.POST['password']
    #username1 = request.POST.get('username')
    #password1 = request.POST.get('password')

    user = authenticate(username=username, password=password) # Retorna None en caso de no validar
    if user:
      login(request, user)
      print("Usuario autenticado")
      messages.success(request, 'Bienvenido {}'.format(user.username))

      if request.GET.get('next'):
        return HttpResponseRedirect(request.GET['next'])
      return redirect('index')
    else:
      print("Usuario no autenticado")
      messages.error(request, 'Usuario o contraseña no validos')
  print("Adios!!")
  return render(request, 'users/login.html')

def logout_view(request):
  logout(request)
  messages.success(request, 'Sesión cerrada exitosamente')
  return redirect('login')

def register(request):
  if request.user.is_authenticated:
    return redirect('index')

  form = RegisterForm(request.POST or None)

  if request.method == 'POST' and form.is_valid():

    user = form.save()
    if user:
      login(request, user)
      messages.success(request, 'Usuario creado exitosamente')
      return redirect('index')

  return render(request, 'users/register.html', {'form': form})

