from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Task
from .models import ComicsMangas, Comments, Categories, CategoryType, Genres, Publisher, Themes, Languages, Rating, CartItem, Order, ItemsOrder, Author, CustomUser

#Poner header en admin
admin.site.site_header = "Fantasy ComicsMania" #Poner Nombre Principal en el admin
admin.site.index_title = "Administrador" #Poner Nombre de la sección
admin.site.site_title = "Fantasy ComicsMania" #Poner Nombre de la página
class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('email', 'first_name', 'last_name', 'birth_date')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    list_display = ('username', 'email', 'first_name', 'last_name', 'birth_date', 'is_staff')
    search_fields = ('username', 'email', 'fist_name', 'last_name', 'birth_date')
    ordering = ('username',)

# Desregistrar el modelo User (si lo estás usando) y registrar CustomUser
#admin.site.unregister(User)  # Asegúrate de que realmente necesites esto
admin.site.register(CustomUser, UserAdmin)  # Cambia User por CustomUser
#Registrar TASKS
#admin.site.register(Task)

#Registrar Comics
class ComicsMangasAdmin(admin.ModelAdmin):
    # Autocompletado para ForeignKey
    autocomplete_fields = ['publisher']  # Permite buscar en el campo de editorial (ForeignKey)
    # Campos en los que quieres habilitar la búsqueda
    search_fields = ['title', 'publisher__description', 'author__name']  # Búsqueda por título, editorial y autor
    # Filtros en la barra lateral
    list_filter = ['category', 'publisher', 'genre']  # Filtro por categoría, editorial y género
    # Campos a mostrar en la lista principal
    list_display = ['title', 'publisher', 'price_bs', 'stock', 'volume']  # Campos que se mostrarán en la lista
    # Número de ítems por página
    list_per_page = 100  # Número de elementos por página en el admin
    # Funcionalidad adicional: Mostrar relaciones ManyToMany (en este caso, los autores y temas)
    filter_horizontal = ('author', 'theme', 'category')  # Facilita la gestión de campos many-to-many
# Registrar el modelo con el admin personalizado
admin.site.register(ComicsMangas, ComicsMangasAdmin)

# Configuración del modelo Publisher en el admin para permitir búsqueda
class PublisherAdmin(admin.ModelAdmin):
    search_fields = ['description']  # Permite la búsqueda por nombre de editorial
admin.site.register(Publisher, PublisherAdmin)

#Registrar Cemetaries
class CommentsAdmin(admin.ModelAdmin):
    # Habilitar búsqueda por el nombre de usuario y el título del producto
    search_fields = ['user__username', 'product__title', 'review_comment']  # Permitir búsqueda por nombre de usuario y título del producto

    # Filtros para la barra lateral
    #list_filter = ['user', 'product', 'approved', 'publication_date']  # Filtrar por usuario, producto, aprobado y fecha de publicación

    # Campos a mostrar en la lista principal
    list_display = ['user', 'product', 'review_comment', 'publication_date', 'approved']  # Campos que se mostrarán en la lista

    # Número de elementos por página
    list_per_page = 100  # Configura cuántos ítems se mostrarán por página

# Registrar el modelo Comments con el admin personalizado
admin.site.register(Comments, CommentsAdmin)

# Registrar el modelo Rating con el admin personalizado
class RatingAdmin(admin.ModelAdmin):
    # Habilitar autocompletado para ForeignKeys (usuario y producto)
    autocomplete_fields = ['user', 'product']  # Permitir búsqueda autocompletada para user y product
    # Campos para habilitar la búsqueda en la vista de lista del admin
    search_fields = ['user__username', 'product__title', 'value']  # Búsqueda por nombre de usuario, título de producto y valor
    
    # Filtros para la barra lateral
    #list_filter = ['value', 'product', 'user']  # Filtros por valor, producto y usuario
    # Campos a mostrar en la lista principal
    list_display = ['user', 'product', 'value', 'publication_date']  # Mostrar estos campos en la lista
    # Número de elementos por página
    list_per_page = 100  # Configura cuántos ítems se mostrarán por página
# Registrar el modelo Rating con el admin personalizado
admin.site.register(Rating, RatingAdmin)

admin.site.register(Categories)
admin.site.register(Genres)
admin.site.register(Themes)
admin.site.register(CategoryType)
admin.site.register(Languages)
admin.site.register(CartItem)
admin.site.register(Order)
admin.site.register(ItemsOrder)
admin.site.register(Author)