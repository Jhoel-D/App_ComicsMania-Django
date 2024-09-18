import math

# Función que evalúa f(x) a partir de la entrada del usuario
def f(x, func_str):
    return eval(func_str)

# Función que evalúa la derivada f'(x) a partir de la entrada del usuario
def df(x, deriv_str):
    return eval(deriv_str)

# Implementación del método de Newton-Raphson
def newton_raphson(func_str, deriv_str, x0, tol, max_iter):
    error = float('inf')  # Error inicial
    iter_count = 0  # Contador de iteraciones
    x = x0  # Valor inicial

    # Bucle iterativo del método de Newton-Raphson
    while error > tol and iter_count < max_iter:
        # Cálculo del nuevo valor de x
        x_new = x - f(x, func_str) / df(x, deriv_str)
        # Calcular el error
        error = abs(x_new - x)
        # Actualizar el valor de x
        x = x_new
        iter_count += 1
        print(f"Iteración: {iter_count}, x: {x}, Error: {error}")

    # Condición para verificar si se alcanzó la convergencia
    if error <= tol:
        print(f"\nConvergencia lograda en {iter_count} iteraciones. Raíz aproximada: {x}")
    else:
        print(f"\nNo se logró convergencia después de {max_iter} iteraciones.")

    return x

# Ejemplo de ejecución
func_str = input("Ingresa la función f(x) en formato Python (por ejemplo, 'x**3 - 2*x**2 + 3'): ")
deriv_str = input("Ingresa la derivada f'(x) en formato Python (por ejemplo, '3*x**2 - 4*x'): ")
x0 = float(input("Ingresa el valor inicial x0: "))
tol = float(input("Ingresa la tolerancia (por ejemplo, 1e-6): "))
max_iter = int(input("Ingresa el número máximo de iteraciones: "))

# Ejecutar el método
raiz = newton_raphson(func_str, deriv_str, x0, tol, max_iter)
print(f"Raíz aproximada: {raiz}")
