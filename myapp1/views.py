from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import CustomUserCreationForm, AuthenticationForm #Añadido
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError, transaction
from .forms import TaskForm, CommentForm
from .models import Task, ComicsMangas,Rating, Comments, CartItem, Order, ItemsOrder
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST, require_http_methods
from django.http import JsonResponse
from django.contrib import messages


from django.http import HttpResponseRedirect, HttpResponse
from django.conf import settings
from paypalcheckoutsdk.orders import OrdersCreateRequest
from paypalcheckoutsdk.core import PayPalHttpClient, SandboxEnvironment, LiveEnvironment

import json
from django.http.response import JsonResponse        
def hola(request):
    return render(request, template_name= 'paypal.html') 
    
def cart_pay(request, total_price):
   pass

def home(request):
    return render(request, 'home.html')

def cart_total(request):
    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(user=request.user)
        cart_total = sum(item.comic.price_bs * item.quantity for item in cart_items)
    else:
        cart_total = 0
    
    return {'cart_total': cart_total}

def get_cart_total(request):
    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(user=request.user)
        cart_total = sum(item.comic.price_bs * item.quantity for item in cart_items)
    else:
        cart_total = 0
    
    return JsonResponse({'cart_total': cart_total})

#Login nuevo
# Vista para el formulario de registro
def signup_new(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['password1'] == form.cleaned_data['password2']:
                try:
                    user = form.save(commit=False)
                    user.full_name = form.cleaned_data['full_name']
                    user.birth_date = form.cleaned_data['birth_date']
                    user.save()
                    #login(request, user)
                    return redirect('signin_new')
                except IntegrityError:
                    return render(request, 'signup_new.html', {'form': form, 'error': 'User already exists'})
            else:
                return render(request, 'signup_new.html', {'form': form, 'error': 'Passwords do not match'})
    else:
        form = CustomUserCreationForm()
    return render(request, 'signup_new.html', {'form': form})


# Vista para el formulario de inicio de sesión
def signin_new(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                return redirect('comics_mangas')
        else:
            error_message = "Username or password is incorrect"
            return render(request, 'signin_new.html', {'form': form, 'error_message': error_message})
    else:
        form = AuthenticationForm()
    return render(request, 'signin_new.html', {'form': form})

# Login de formulario
def signup(request): 
    if request.method == 'GET':
        form = CustomUserCreationForm()  # Crea una instancia del formulario sin datos del usuario
        return render(request, 'signup.html', {'form': form})
    else: 
        form = CustomUserCreationForm(request.POST)  # Crea una instancia del formulario con los datos del usuario
        if form.is_valid():  # Verifica si el formulario es válido
            if form.cleaned_data['password1'] == form.cleaned_data['password2']:  # Verifica si las contraseñas coinciden
                try:
                    # Registra el usuario
                    user = form.save(commit=False)  # Guarda el usuario pero no lo persiste en la base de datos aún
                    user.full_name = form.cleaned_data['full_name']  # Asigna el nombre completo del formulario al usuario
                    user.birth_date = form.cleaned_data['birth_date']  # Asigna la fecha de nacimiento del formulario al usuario
                    user.save()  # Ahora sí guarda el usuario con los campos adicionales
                    login(request, user)
                    #messages.success(request, '¡Usuario registrado correctamente! Bienvenido a nuestra plataforma.')
                    return redirect('tasks')
                except IntegrityError:
                    #messages.success(request, 'User already exists')
                    return render(request, 'signup.html', {
                        'form': form,
                        "error": 'User already exists'})
            else:
                return render(request, 'signup.html', {
                    'form': form,
                    'error': 'Passwords do not match'})
        else:
          # Si hay errores de validación, los pasamos al contexto para mostrarlos en la plantill
          errors = form.errors.as_data()  # Obtener los errores del formulario
          error_messages = []  # Lista para almacenar los mensajes de error
          for field, field_errors in errors.items():  # Iterar sobre los errores de cada campo
              for error in field_errors:  # Iterar sobre los errores asociados con cada campo
                  error_messages.append(f"{field}: {error}")  # Agregar cada mensaje de error a la lista
        #return render(request, 'signup.html', {'form': form, 'errors': error_messages, 'success_message': '¡Usuario registrado correctamente! Bienvenido a nuestra plataforma.'})

        return render(request, 'signup.html', {'form': form, 'errors': form.errors})
    
# Iniciar Sesión
def signin (request):
    if request.method == 'GET':
        return render(request, 'signin.html',{
            'form': AuthenticationForm()})
    else: 
        user = authenticate(
            request,
            username=request.POST['username'],
            password=request.POST['password'])
        if user is None:
            return render(request, 'signin.html',{
            'form': AuthenticationForm,
            'error': 'Username or password is incorrect'
            })
        else: 
            
            login(request, user)
            return redirect('tasks')  
        

# Index de la pagina de tareas o comics 
@login_required  
def tasks(request):
    tasks = Task.objects.filter(User=request.user, datecompleted__isnull = True) #Devuelve los registros del modelo Task
    return render(request, 'task.html', {'tasks': tasks})

# Index de la pagina de tareas completadas 
@login_required 
def tasks_completed(request):
    tasks = Task.objects.filter(User=request.user, datecompleted__isnull = False).order_by('-datecompleted') #Devuelve los registros del modelo Task
    return render(request, 'task.html', {'tasks': tasks})

# Logout o Cerrar Sesión
@login_required
def signout (request):
    logout(request)
    return redirect ('home')  

# Crear Tareas
@login_required
def create_task (request):
    if request.method == 'GET':
        return render(request, 'create_task.html',{
            'form': TaskForm
        })
    else:
        try:
            form= TaskForm(request.POST)
            new_task = form.save(commit=False)
            new_task.User = request.user
            new_task.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'create_task.html',{
            'form': TaskForm,
            'error': 'Please provide valida data'
        })
            
        return render(request, 'task.html',{
            'form': TaskForm
            })
    
# Mostrar detalles de tarea
@login_required    
def task_detail (request, task_id):
    if request.method == 'GET':
        task = get_object_or_404(Task, pk=task_id, User=request.user)
        form= TaskForm(instance=task)
        return render(request, 'task_detail.html',{'tasks': task, 'form': form})
    else:
        try:
            task = get_object_or_404(Task, pk=task_id, User=request.user)
            form=TaskForm(request.POST, instance=task)
            form.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'task_detail.html',{'tasks': task, 'form': form, 'error': 'Error updating task'})      

# Poner dato como hecho
@login_required     
def complete_task(request, task_id):
    task= get_object_or_404(Task, pk=task_id, User=request.user)
    if request.method == 'POST':
        task.datecompleted = timezone.now()
        task.save()
        return redirect('tasks') 

#Borrar tarea
@login_required   
def delete_task(request, task_id):
    task= get_object_or_404(Task, pk=task_id, User=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('tasks')
    
from django.contrib.auth.models import User
#Carrito
@login_required 
def add_to_cart(request):
    return render(request, 'add_to_cart.html')

def comics_mangas(request):
    comics_mangas = ComicsMangas.objects.all()
    if request.user.is_authenticated:
        cart_item_ids = request.user.cartitem_set.values_list('comic_id', flat=True)
    else:
        cart_item_ids = []  # Si el usuario no está autenticado, establecer cart_item_ids como una lista vacía

    return render(request, 'comics_mangas.html', {'comics_mangas': comics_mangas, 'cart_item_ids': cart_item_ids})

@login_required
def comics_mangas_detail(request, comic_manga_id):
    if request.user.is_authenticated:
        cart_item_ids = request.user.cartitem_set.values_list('comic_id', flat=True)
    else:
        cart_item_ids = []  # Si el usuario no está autenticado, establecer cart_item_ids como una lis
    comic_manga = get_object_or_404(ComicsMangas, pk=comic_manga_id)
    user_rating = Rating.objects.filter(user=request.user, product=comic_manga).first()
    rating_values = [1, 2, 3, 4, 5]
    comments = Comments.objects.filter(product=comic_manga, approved=True)
    user_rating_value = user_rating.value if user_rating else None
    for comment in comments:
        comment.user_rating = Rating.objects.filter(user=comment.user, product=comic_manga).first()

    context = {
        'comic_manga': comic_manga,
        'comments': comments,
        'user_rating_value': user_rating_value,
        'rating_values': rating_values,
        'user_rating': user_rating,
        'cart_item_ids': cart_item_ids   }
    return render(request, 'comics_mangas_detail.html', context)

@login_required
def add_comment(request, comic_manga_id):
    if request.method == 'POST':
        comment_text = request.POST.get('comment')
        comic_manga = get_object_or_404(ComicsMangas, pk=comic_manga_id)
        # Crea el comentario
        comment = Comments.objects.create(user=request.user, product=comic_manga, review_comment=comment_text)
        # Redirection de vuelta a la página de detalle del cómic o manga
        return redirect('comics_mangas_detail', comic_manga_id=comic_manga_id)
    # Si no es una solicitud POST, redirige a la página de detalle del cómic o manga
    return redirect('comics_mangas_detail', comic_manga_id=comic_manga_id)

def load_more_comments(request, comic_manga_id):
    next_index = int(request.GET.get('next_index', 0))
    comic_manga = get_object_or_404(ComicsMangas, pk=comic_manga_id)
    
    # Obtener solo los comentarios aprobados relacionados con el cómic o manga
    comments = Comments.objects.filter(product=comic_manga, approved=True)[next_index:next_index+4]
    
    # Obtener las calificaciones para cada comentario
    comments_data = []
    for comment in comments:
        user_rating = Rating.objects.filter(user=comment.user, product=comic_manga).first()
        comment_data = {
            'publication_date': comment.publication_date.strftime('%Y-%m-%d %H:%M:%S'),
            'user': comment.user.username,
            'review_comment': comment.review_comment,
            'user_rating_value': user_rating.value if user_rating else None,
        }
        comments_data.append(comment_data)
    
    return JsonResponse({'comments': comments_data})


@login_required
def submit_rating(request, comic_manga_id):
    if request.method == 'POST':
        rating_value = int(request.POST.get('rating'))
        if rating_value >= 1 and rating_value <= 5:
            comic_manga = get_object_or_404(ComicsMangas, pk=comic_manga_id)
            # Buscar si ya existe una calificación del usuario para este producto
            existing_rating = Rating.objects.filter(user=request.user, product=comic_manga).first()
            if existing_rating:
                # Si ya existe una calificación, actualizarla
                existing_rating.value = rating_value
                existing_rating.save()
            else:
                # Si no existe una calificación, crear una nueva
                Rating.objects.create(user=request.user, product=comic_manga, value=rating_value)
            # Redirigir de vuelta a la página de detalle del cómic o manga
            return redirect('comics_mangas_detail', comic_manga_id=comic_manga_id)
    # En caso de que la solicitud no sea POST o la calificación sea inválida, redirigir a la página de inicio
    return redirect('comics_mangas_detail', comic_manga_id=comic_manga_id)



@login_required
def cart_view(request):
    # Obtener los elementos del carrito del usuario actual que no están en ninguna orden
    cart_items = CartItem.objects.filter(user=request.user)
    
    # Calcular el precio total de los elementos en el carrito
    total_price = sum(item.comic.price_bs * item.quantity for item in cart_items)
    
    # Calcular el total de productos en el carrito
    total_products = sum(item.quantity for item in cart_items)
    
    return render(request, 'cart.html', {'cart_items': cart_items, 'total_price': total_price, 'total_products': total_products})

@login_required
@transaction.atomic
def add_to_cart_inline(request, product_id):
    # Verificar si el usuario está autenticado
    if not request.user.is_authenticated:
        return JsonResponse({'success': False, 'error': 'Debe iniciar sesión para agregar productos al carrito'})
    # Obtener el producto
    product = get_object_or_404(ComicsMangas, pk=product_id)
    # Verificar si el producto está en stock
    if product.stock <= 0:
        return JsonResponse({'success': False, 'error': 'Producto agotado'})
    # Verificar si el producto ya está en el carrito
    cart_item, created = CartItem.objects.get_or_create(user=request.user, comic=product)

    if not created:
        # Si el objeto ya existe en el carrito, verificar si hay suficiente stock
        if cart_item.quantity >= product.stock:
            return JsonResponse({'success': False, 'error': 'No hay suficiente stock disponible'})
        else:
            # Incrementar la cantidad en el carrito y reducir el stock del producto
            cart_item.quantity += 1
            if product.stock > 0:  # Verificar si hay suficiente stock
                product.stock -= 1
            else:
                return JsonResponse({'success': False, 'error': 'No hay suficiente stock disponible'})
    else:
        # Si el objeto es nuevo en el carrito, la cantidad será 1
        cart_item.quantity = 1
        product.stock -= 1
    # Guardar los cambios en el producto y el carrito
    product.save()
    cart_item.save()
    # Calcular el nuevo precio total de la orden
    order_total_price = sum(item.comic.price_bs * item.quantity for item in request.user.cartitem_set.all())
    # Indicar que el producto se agregó correctamente al carrito
    return JsonResponse({'success': True, 'message': 'Producto agregado al carrito', 'order_total_price': order_total_price})

@login_required
@transaction.atomic
@require_http_methods(["DELETE"])
def remove_from_cart(request, item_id):
    try:
        cart_item = CartItem.objects.get(pk=item_id, user=request.user)
        # Incrementar el stock del producto al eliminar el elemento del carrito
        cart_item.comic.stock += cart_item.quantity
        cart_item.comic.save()
        cart_item.delete()
        
        # Obtener la cantidad total de elementos en el carrito
        cart_items = CartItem.objects.filter(user=request.user)
        cart_item_count = cart_items.count()
        
        # Obtener el precio total actualizado de la orden
        order_total_price = sum(item.comic.price_bs * item.quantity for item in cart_items)
        
        # Calcular la cantidad total de productos en el carrito
        total_products = sum(item.quantity for item in cart_items)
        
        return JsonResponse({'success': True, 'message': 'Producto eliminado del carrito correctamente', 'cart_item_count': cart_item_count, 'order_total_price': order_total_price, 'total_products': total_products})
    except CartItem.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'El producto no existe en el carrito'})


@login_required
@transaction.atomic
@require_POST
def increase_quantity(request, item_id):
    try:
        cart_item = CartItem.objects.get(pk=item_id, user=request.user)
        # Verificar si hay suficiente stock disponible antes de aumentar la cantidad
        if cart_item.comic.stock > 0:
            cart_item.quantity += 1
            cart_item.comic.stock -= 1
            cart_item.comic.save()
            cart_item.save()
            
            # Obtener la cantidad total de elementos en el carrito
            cart_item_count = request.user.cartitem_set.count()
            
            # Obtener el precio total actualizado de la orden
            order_total_price = sum(item.comic.price_bs * item.quantity for item in request.user.cartitem_set.all())
            
            # Calcular la cantidad total de productos en el carrito
            total_products = sum(item.quantity for item in request.user.cartitem_set.all())
            
            return JsonResponse({'success': True, 'message': 'Cantidad aumentada en el carrito', 'quantity': cart_item.quantity, 'order_total_price': order_total_price, 'cart_item_count': cart_item_count, 'total_products': total_products})
        else:
            return JsonResponse({'success': False, 'error': 'No hay suficiente stock disponible'})
    except CartItem.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'El producto no existe en el carrito'})
    

@login_required
@transaction.atomic
@require_POST
def decrease_quantity(request, item_id):
    try:
        cart_item = CartItem.objects.get(pk=item_id, user=request.user)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.comic.stock += 1
            cart_item.comic.save()
            cart_item.save()
        
        
        # Obtener el precio total actualizado de la orden
        order_total_price = sum(item.comic.price_bs * item.quantity for item in request.user.cartitem_set.all())
        
        # Calcular la cantidad total de elementos en el carrito
        cart_item_count = request.user.cartitem_set.count()
        
        # Calcular la cantidad total de productos en el carrito
        total_products = sum(item.quantity for item in request.user.cartitem_set.all())
        
        return JsonResponse({'success': True, 'message': 'Cantidad disminuida en el carrito', 'quantity': cart_item.quantity if hasattr(cart_item, 'quantity') else 0, 'order_total_price': order_total_price, 'cart_item_count': cart_item_count, 'total_products': total_products})
    except CartItem.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'El producto no existe en el carrito'})


@login_required
@transaction.atomic
@require_POST
def clear_cart(request):
    try:
        # Obtener los elementos del carrito del usuario actual
        cart_items = CartItem.objects.filter(user=request.user)
        
        # Iterar sobre los elementos del carrito y devolver el stock de cada producto
        for cart_item in cart_items:
            cart_item.comic.stock += cart_item.quantity
            cart_item.comic.save()
        
        # Eliminar todos los elementos del carrito del usuario actual
        cart_items.delete()
        
        # Obtener la cantidad total de elementos en el carrito (que ahora será 0)
        cart_item_count = 0
        
        # Precio total de la orden (que ahora será 0)
        order_total_price = 0
        
        # Calcular la cantidad total de productos en el carrito
        total_products = 0
        
        return JsonResponse({'success': True, 'message': 'Carrito vaciado correctamente', 'cart_item_count': cart_item_count, 'order_total_price': order_total_price, 'total_products': total_products})
    except CartItem.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Error al vaciar el carrito'})


from django.db import transaction
@login_required
@transaction.atomic
def create_order(request):
    if request.method == 'POST':
        try:
            # Obtener los elementos del carrito del usuario actual
            cart_items = CartItem.objects.filter(user=request.user)
            
            # Verificar si hay elementos en el carrito
            if not cart_items:
                return JsonResponse({'success': False, 'error': 'El carrito está vacío'})
            
            # Calcular el precio total de la orden
            total_price = sum(item.comic.price_bs * item.quantity for item in cart_items)
            
            # Crear una nueva instancia de Order y guardar los datos en la base de datos
            with transaction.atomic():
                order = Order.objects.create(
                    user=request.user,
                    total_price=total_price,
                    status='Pendiente',
                    shipping_address=request.POST.get('shipping_address', ''),
                    first_name=request.POST.get('first_name', ''),
                    last_name=request.POST.get('last_name', ''),
                    zone=request.POST.get('zone', ''),
                    city=request.POST.get('city', ''),
                    country=request.POST.get('country', ''),
                    shipping_method=request.POST.get('shipping_method', 0),
                    payment_method=request.POST.get('payment_method', '')
                )
                
                # Agregar los elementos del carrito a la orden
                order.items.add(*[ItemsOrder.objects.create(
                    user=request.user,
                    comic=cart_item.comic,
                    quantity=cart_item.quantity,
                ) for cart_item in cart_items])
                
                # Limpiar el carrito
                cart_items.delete()
            
            # Redirigir al usuario a la página de detalles de la orden recién creada
            return redirect('order_detail', order_id=order.id)
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    else:
        # Si la solicitud no es POST, mostrar un error o redirigir a la página de inicio
        return JsonResponse({'success': False, 'error': 'Método no permitido'})
    
@login_required
@transaction.atomic
def cancel_order(request, order_id):
    try:
        # Obtener la orden con el ID proporcionado y perteneciente al usuario actual
        order = get_object_or_404(Order, id=order_id, user=request.user)
        
        # Devolver el stock de los comics asociados a la orden
        for item in order.items.all():
            item.comic.stock += item.quantity
            item.comic.save()
            
        # Eliminar la orden y los ItemsOrder asociados serán eliminados automáticamente debido a la ForeignKey
        order.delete()
        
        return JsonResponse({'success': True, 'message': 'Orden cancelada correctamente'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


@login_required
def order_detail(request, order_id):
    # Obtener la orden con el ID proporcionado
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    if request.method == 'POST':
        form_type = request.POST.get('form_type')
        if form_type == 'update-form':
            # Actualizar los detalles faltantes de la orden con los datos proporcionados en la solicitud
            order.shipping_address = request.POST.get('shipping_address')
            order.first_name = request.POST.get('first_name')
            order.last_name = request.POST.get('last_name')
            order.zone = request.POST.get('zone')
            order.city = request.POST.get('city')
            order.country = request.POST.get('country')
            # Obtener el costo del método de envío seleccionado y sumarlo al total_price
            
            shipping_method_cost = int(request.POST.get('shipping_method', 0))
            if not order.shipping_cost_applied:
               order.total_price += shipping_method_cost
               order.shipping_cost_applied = True
               order.shipping_method_cost = shipping_method_cost  # Guardar el costo del método de envío
            else:
                # Restar el costo del envío anterior al total_price antes de sumar el nuevo costo
                order.total_price -= order.shipping_method_cost
                order.total_price += shipping_method_cost
                order.shipping_method_cost = shipping_method_cost  # Actualizar el costo del método de envío
        # Guardar la orden actualizada
            # Guardar la orden actualizada
            order.save()
            
            # Redirigir al usuario a la página de detalles de la orden
            return HttpResponseRedirect(request.path)
        elif form_type == 'payment-form':
            order.payment_method = request.POST.get('payment_method')
            order.status = "Pagado"
            order.save()
            return HttpResponseRedirect(request.path)

    # Si no es una solicitud POST o no se proporcionó un form_type válido, Renderizar la página de detalles de la orden
    return render(request, 'order_detail.html', {'order': order})    
@login_required
def order_list(request, status=None):
    # Filtrar por usuario
    user = request.user
    # Si se proporciona un estado, filtrar por usuario y estado
    if status:
        orders = Order.objects.filter(user=user, status=status)
    else:
        # Si no se proporciona un estado, obtener todas las órdenes del usuario
        orders = Order.objects.filter(user=user)
    # Verifica en el servidor si las órdenes son correctas (opcional, solo para depuración)
    print(f"Usuario: {user}, Órdenes: {orders}")
    return render(request, 'order_list.html', {'orders': orders})

def orders_by_status(request, status):
    orders = Order.objects.filter(status=status)
    return render(request, 'order_list.html', {'orders': orders})
