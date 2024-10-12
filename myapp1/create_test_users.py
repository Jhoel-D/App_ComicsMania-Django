# import os
# import sys
# import django
# from django.contrib.auth import get_user_model
# from datetime import date

# # Agrega la ruta de tu proyecto al path
# sys.path.append(os.path.join(os.path.dirname(__file__), '..'))  # Esto agrega la carpeta PROY-SOFT al path

# # Configuración del entorno de Django
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ProyComicsmania.settings')  # Asegúrate de que sea el nombre correcto
# django.setup()

# # Obtén el modelo de usuario personalizado
# User = get_user_model()

# # Función para crear usuarios de prueba
# def create_test_users():
#     # Generar usuarios desde user006 hasta user150
#     for i in range(6, 151):
#         username = f'user{i:03}'  # Formato user006, user007, etc.
#         email = f'{username}@example.com'  # Asignar un email único
#         password = 'password123'  # Contraseña más segura
#         full_name = f'Nombre Completo {i}'  # Nombre completo genérico
#         birth_date = date(2000, 1, 1)  # Puedes personalizar la fecha de nacimiento

#         # Crear el usuario
#         user = User(
#             username=username,
#             email=email,
#             full_name=full_name,  # Asignar el nombre completo
#             birth_date=birth_date,  # Asignar la fecha de nacimiento
#             is_active=True,  # El usuario estará activo
#             is_staff=False,  # No será un miembro del staff
#         )

#         # Establecer la contraseña
#         user.set_password(password)

#         # Guardar el usuario en la base de datos
#         user.save()

#     print("Usuarios creados con éxito.")

# if __name__ == '__main__':
#     create_test_users()
#USER CREADO 
# import csv
# import mysql.connector

# # Configura tu conexión a la base de datos
# db_config = {
#     'user': '',
#     'password': '',  # Cambia esto si tienes una contraseña
#     'host': '',
#     'port': '',  # Asegúrate de usar el puerto correcto
#     'database': ''
# }

# # Lee el archivo CSV
# csv_file_path = 'myapp1/user2.csv'  # Asegúrate de que la ruta sea correcta

# # Conéctate a la base de datos
# conn = mysql.connector.connect(**db_config)
# cursor = conn.cursor()

# # Abre el archivo CSV y procesa cada fila
# with open(csv_file_path, 'r', encoding='utf-8') as archivo:
#     lector = csv.DictReader(archivo, delimiter=';')
    
#     for fila in lector:
#         username = fila['username']  # Ajusta esto al nombre de la columna en tu CSV
#         new_id = fila['id']  # Ajusta esto al nombre de la columna en tu CSV
#         print(f"Actualizando ID para usuario: {username} a {new_id}")

#         # Ejecuta la consulta de actualización
#         try:
#             cursor.execute(
#                 "UPDATE myapp1_customuser SET id = %s WHERE username = %s",
#                 (new_id, username)
#             )
#             print(f"ID actualizado para {username} a {new_id}.")
#         except mysql.connector.Error as err:
#             print(f"Error al actualizar {username}: {err}")

# # Guarda los cambios y cierra la conexión
# conn.commit()
# cursor.close()
# conn.close()

# print("Actualización completa.")
#Corregir el ID con mysql y numpy instalando (pip install mysql-connector-python  )