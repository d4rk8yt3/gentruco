import os
from flask import Flask, request, render_template
import random

app = Flask(__name__)

# Función para cargar los números existentes desde un archivo
def load_existing_numbers(filename):
    try:
        with open(filename, 'r') as file:
            return set(file.read().splitlines())
    except FileNotFoundError:
        return set()

# Función para guardar números en un archivo
def save_numbers(filename, numbers):
    with open(filename, 'a') as file:
        for number in numbers:
            file.write(f"{number}\n")

# Función para generar números únicos
def generate_numbers(area_code, num_digits, num_count, existing_numbers):
    generated_numbers = set()
    while len(generated_numbers) < num_count:
        number = ''.join(random.choices('0123456789', k=num_digits))
        full_number = f"+{area_code}{number}"
        if full_number not in existing_numbers:
            generated_numbers.add(full_number)
            existing_numbers.add(full_number)
    return generated_numbers

# Ruta principal para mostrar y procesar el formulario
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        area_code = request.form['area_code']
        num_digits = int(request.form['num_digits'])
        num_count = int(request.form['num_count'])
        filename = "generated_numbers.txt"

        # Cargar números existentes y generar nuevos
        existing_numbers = load_existing_numbers(filename)
        numbers = generate_numbers(area_code, num_digits, num_count, existing_numbers)
        save_numbers(filename, numbers)

        return render_template('index.html', numbers=numbers)

    return render_template('index.html', numbers=[])

# Esta es la sección modificada para permitir que Railway o cualquier otro servicio
# asigne el puerto automáticamente
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  # Railway asigna automáticamente un puerto
    app.run(host='0.0.0.0', port=port)
