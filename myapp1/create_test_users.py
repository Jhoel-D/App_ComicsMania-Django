import os
import sys
import django
from django.contrib.auth import get_user_model
from datetime import date

# Agrega la ruta de tu proyecto al path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))  # Esto agrega la carpeta PROY-SOFT al path

# Configuración del entorno de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ProyComicsmania.settings')  # Asegúrate de que sea el nombre correcto
django.setup()

# Obtén el modelo de usuario personalizado
User = get_user_model()

# Función para crear usuarios de prueba
def create_test_users():
    # Generar usuarios desde user006 hasta user150
    for i in range(6, 151):
        username = f'user{i:03}'  # Formato user006, user007, etc.
        email = f'{username}@example.com'  # Asignar un email único
        password = 'password123'  # Contraseña más segura
        full_name = f'Nombre Completo {i}'  # Nombre completo genérico
        birth_date = date(2000, 1, 1)  # Puedes personalizar la fecha de nacimiento

        # Crear el usuario
        user = User(
            username=username,
            email=email,
            full_name=full_name,  # Asignar el nombre completo
            birth_date=birth_date,  # Asignar la fecha de nacimiento
            is_active=True,  # El usuario estará activo
            is_staff=False,  # No será un miembro del staff
        )

        # Establecer la contraseña
        user.set_password(password)

        # Guardar el usuario en la base de datos
        user.save()

    print("Usuarios creados con éxito.")

if __name__ == '__main__':
    create_test_users()
