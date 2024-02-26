
from django.contrib.auth.models import User
#from django.contrib.auth.models import AbstractUser
from django.db import models  # Importa models de Django
from django.core.validators import MinValueValidator, MaxValueValidator


class Task(models.Model):
    title = models.CharField(max_length=100)
    descripction = models.TextField(blank = True)
    created = models.DateTimeField(auto_now_add=True)
    datecompleted = models.DateTimeField(null=True, blank=True)
    important = models.BooleanField(default=False)
    User = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.title + ' - by '+ self.User.username
    
class Publisher(models.Model): #Editorials
    description = models.CharField(max_length=60, null=True)
    def __str__(self):
        return self.description if self.description else "No description available"

class Themes(models.Model):#Temas
    description = models.CharField(max_length=60, null=True)
    def __str__(self):
        return self.description if self.description else "No description available"

class Languages(models.Model): #Idioms
    description = models.CharField(max_length=60, null=True)
    def __str__(self):
        return self.description if self.description else "No description available"

class Genres(models.Model): #Generis
    description = models.CharField(max_length=60, null=True)
    def __str__(self):
        return self.description if self.description else "No description available"
    

class CategoryType(models.Model): #Typo Category
    description = models.CharField(max_length=45, null=True)
    def __str__(self):
        return self.description if self.description else "No description available"

class Categories(models.Model): #Categories
    description = models.CharField(max_length=60, null=True)
    category_type = models.ForeignKey(CategoryType, on_delete=models.CASCADE)
    def __str__(self):
        return self.description if self.description else "No description available"

class ComicsMangas(models.Model): #Comics Manga
    title = models.CharField(max_length=100, verbose_name="Title")
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE)
    author = models.CharField(max_length=100)
    synopsis = models.TextField(max_length=800, null=True, verbose_name='Synopsis')
    pages = models.IntegerField(null=True)
    format = models.CharField(max_length=40, null=True)
    dimension = models.CharField(max_length=40, null=True)
    color = models.CharField(max_length=30, null=True)
    year_of_release = models.DateField(null=True)
    language = models.ForeignKey(Languages, on_delete=models.CASCADE, null=True)
    audience = models.CharField(max_length=45, null=True)
    price_bs = models.DecimalField(max_digits=10, decimal_places=2)
    volume = models.IntegerField(null=True)
    theme = models.ForeignKey(Themes, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genres, on_delete=models.CASCADE)
    category = models.ForeignKey(Categories, on_delete=models.CASCADE)
    stock = models.IntegerField()
    cover_img = models.ImageField(upload_to='images/', verbose_name='Image', null=True)
    
    
    def __str__(self):
        fila = f"Title: {self.title} - by: {self.author} - Stock: {self.stock}"
        return fila
    def delete(self, using=None, keep_parents=False):
        self.cover_img.storage.delete(self.cover_img.name)
        super().delete()
    

class PaymentMethods(models.Model): #Method de Page
    description = models.CharField(max_length=45, null=True)
    def __str__(self):
        return self.description if self.description else "No description available"

class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comic = models.ForeignKey(ComicsMangas, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

class Order(models.Model):
    DEFAULT_COUNTRY = 'Bolivia'

    COUNTRY_CHOICES = [
        (DEFAULT_COUNTRY, 'Bolivia'),
    ]
    STATUS_CHOICES = [
        ('Pendiente', 'Pendiente'),
        ('En Proceso', 'En Proceso'),
        ('Completado', 'Completado'),
        ('Cancelado', 'Cancelado'),
    ]
    PAYMENT_CHOICES = [
        ('PayPal', 'PayPal'),
        ('Mercado Libre', 'Mercado Libre'),
        ('Otro', 'Otro'),
    ]
    
    BOLIVIAN_DEPARTMENTS = [
        ('LP', 'La Paz'),
        ('CBB', 'Cochabamba'),
        ('SCZ', 'Santa Cruz'),
        ('OR', 'Oruro'),
        ('PT', 'Potosí'),
        ('TJ', 'Tarija'),
        ('CH', 'Chuquisaca'),
        ('BE', 'Beni'),
        ('PD', 'Pando'),
        ('LP', 'El Alto'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(CartItem)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    shipping_address = models.CharField(max_length=255)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    zone = models.CharField(max_length=100)
    city = models.CharField(max_length=100, choices=BOLIVIAN_DEPARTMENTS)
    country = models.CharField(max_length=100, choices=COUNTRY_CHOICES, default=DEFAULT_COUNTRY)
    payment_method = models.CharField(max_length=50, choices=PAYMENT_CHOICES, default='PayPal')
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Pendiente')
    created_at = models.DateTimeField(auto_now_add=True)

class Comments(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(ComicsMangas, on_delete=models.CASCADE, null=True)
    review_comment = models.TextField(blank=True)
    publication_date = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.product.title}"

class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(ComicsMangas, on_delete=models.CASCADE)
    value = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])
    publication_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Rating: {self.value} stars by {self.user.username} for '{self.product.title}'"
    
class Sales(models.Model): #Ventas 
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    sales_date = models.DateTimeField(null=True)
    total_price = models.IntegerField(null=True)
    

class SalesDetail(models.Model): #Detail vents
    sale = models.ForeignKey(Sales, on_delete=models.CASCADE)
    product = models.ForeignKey(ComicsMangas, on_delete=models.CASCADE)
    quantity = models.IntegerField(null=True)
    subtotal = models.IntegerField(null=True)