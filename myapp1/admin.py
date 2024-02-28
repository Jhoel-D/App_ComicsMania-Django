from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Task
from .models import ComicsMangas, Comments, Categories, CategoryType, Genres, Publisher, Themes, Languages, Rating, CartItem, Order, ItemsOrder

class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('email', 'full_name', 'birth_date')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    list_display = ('username', 'email', 'full_name', 'birth_date', 'is_staff')
    search_fields = ('username', 'email', 'full_name', 'birth_date')
    ordering = ('username',)

admin.site.unregister(User)
admin.site.register(User, UserAdmin)

#Registrar TASKS
admin.site.register(Task)

#Registrar Comics
admin.site.register(ComicsMangas)


#Registrar Cemetaries
admin.site.register(Comments)
admin.site.register(Rating)
admin.site.register(Categories)
admin.site.register(Genres)
admin.site.register(Publisher)
admin.site.register(Themes)
admin.site.register(CategoryType)
admin.site.register(Languages)
admin.site.register(CartItem)
admin.site.register(Order)
admin.site.register(ItemsOrder)

