#from . import views
from myapp1 import views
from django.urls import path
#for img
from django.conf import settings
from django.conf.urls.static import static
#from django.contrib.staticfiles.urls import static


urlpatterns = [
    path('',views.home, name= 'home' ),
    #login
    path('signup/',views.signup, name= 'signup'),
    path('signin/',views.signin, name= 'signin'),
    path('signin_new/', views.signin_new, name='signin_new'),
    path('signup_new/', views.signup_new, name='signup_new'),
    #Task
    path('tasks/',views.tasks, name= 'tasks'),
    path('tasks/create/',views.create_task, name= 'create_task'),
    path('tasks/<int:task_id>/',views.task_detail, name= 'task_detail'),
    path('tasks/<int:task_id>/complete',views.complete_task, name= 'complete_task'),
    path('tasks/<int:task_id>/delete',views.delete_task, name= 'delete_task'),
    path('tasks_completed/',views.tasks_completed, name= 'tasks_completed'),
    #logout
    path('logout/',views.signout, name= 'logout'),
    
    #Comics_Mangas
    path('comics_mangas/',views.comics_mangas, name= 'comics_mangas'),
    path('comics_mangas/<int:comic_manga_id>/',views.comics_mangas_detail, name= 'comics_mangas_detail'),
    
    #Guardar Calificación
    path('comics_mangas/<int:comic_manga_id>/submit_rating/', views.submit_rating, name='submit_rating'),
    #path("__reload__/", include("django_browser_reload.urls")),
    path('comics_mangas/<int:comic_manga_id>/add_comment/', views.add_comment, name='add_comment'),
    path('load_more_comments/<int:comic_manga_id>/', views.load_more_comments, name='load_more_comments'),
    
    
    
    path('search/', views.search, name='search'),  # Define la URL para la búsqueda
    path('autocomplete_titles/', views.autocomplete_titles, name='autocomplete_titles'),
    #Url para mostrar categorías 
    path('cat_filter/', views.cat_filter, name='cat_filter'),


    #Carrito
    path('add_to_cart/', views.add_to_cart , name= 'add_to_cart'),
    
    path('add_to_cart_inline/<int:product_id>/', views.add_to_cart_inline, name='add_to_cart_inline'),
    
    path('cart/', views.cart_view, name='cart_view'),
    path('remove_from_cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    
    path('increase_quantity/<int:item_id>/', views.increase_quantity, name='increase_quantity'),
    path('decrease_quantity/<int:item_id>/', views.decrease_quantity, name='decrease_quantity'),
    path('clear_cart/', views.clear_cart, name='clear_cart'),
    
    path('recommender/', views.recommender, name='recommender'),
    #Para order
    path('create_order/', views.create_order, name='create_order'),  # URL para crear una orden
    path('orders/', views.order_list, name='order_list'),            # URL para listar órdenes
    #
    path('orders/status/<str:status>/', views.order_list, name='orders_by_status'),  # Lista filtrada por estado
    #
    path('order/<int:order_id>/', views.order_detail, name='order_detail'),  # URL para ver detalles de una orden
    path('orders/<str:status>/', views.orders_by_status, name='orders_by_s'),
    
    path('order/<int:order_id>/cancel/', views.cancel_order, name='cancel_order'),
    
    path('comics_view/', views.comics_view, name= 'comics_view'),
    path('mangas_view/', views.mangas_view, name= 'mangas_view'),
    
    path('get_cart_total/', views.get_cart_total, name='get_cart_total'),
    
    #path('payment_confirmation/<int:order_id>/', views.payment_confirmation, name='payment_confirmation'),
    
 ] #+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# Sirve archivos de medios en modo DEBUG
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

