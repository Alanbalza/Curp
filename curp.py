import random
import qrcode

# Función para generar el primer dígito de la homoclave
def generar_primer_digito(fecha_nacimiento):
    # Obtener el año de nacimiento
    anio = int(fecha_nacimiento[:4])

    # Determinar si el año es hasta 1999 o a partir de 2000
    if anio <= 1999:
        return str(random.randint(0, 9))  # Para fechas de nacimiento hasta el año 1999 (0-9)
    else:
        return random.choice('A')  # Para fechas de nacimiento a partir del año 2000 (A-Z)

# Función para calcular el segundo dígito verificador del CURP
def calcular_digito_verificador(curp_sin_verificador):
    # Cálculo del dígito verificador según el algoritmo oficial

    # Lista de caracteres válidos para el cálculo del dígito verificador
    caracteres_validos = '0123456789ABCDEFGHIJKLMNÑOPQRSTUVWXYZ'

    # Diccionario de equivalencias para la conversión de letras a números
    equivalencias = {char: index for index, char in enumerate(caracteres_validos)}

    # Coeficientes para calcular el dígito verificador
    coeficientes = [3, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1]

    # Suma de productos de cada carácter por su respectivo coeficiente
    suma = sum(coef * equivalencias[char] for coef, char in zip(coeficientes, curp_sin_verificador))

    # Obtener residuo de la suma
    residuo = suma % 10

    # Calcular el dígito verificador
    if residuo == 0:
        return '0'
    else:
        return str(10 - residuo)

# Función para generar una CURP válida
def generar_curp(nombre, apellido_paterno, apellido_materno, fecha_nacimiento, sexo, estado):
    curp = ''

    # Primer letra del apellido paterno (en mayúsculas)
    curp += apellido_paterno[0].upper()

    # Primera vocal del apellido paterno (en mayúsculas)
    for letra in apellido_paterno[1:]:
        if letra.upper() in 'AEIOU':
            curp += letra.upper()
            break

    # Primer letra del apellido materno
    curp += apellido_materno[0]

    # Primer letra del nombre
    curp += nombre[0]

    # Año de nacimiento (últimos dos dígitos)
    curp += fecha_nacimiento[2:4]  # Se toman los últimos dos dígitos del año

    # Mes de nacimiento
    mes = fecha_nacimiento[5:7]
    curp += mes

    # Día de nacimiento
    curp += fecha_nacimiento[8:10]  # Se toman los dos últimos dígitos del día

    # Sexo
    curp += sexo

    # Entidad federativa de nacimiento
    curp += estado

    # Primer consonante interna del apellido paterno
    for letra in apellido_paterno[1:]:
        if letra.upper() not in 'AEIOU':
            curp += letra.upper()
            break

    # Primer consonante interna del apellido materno
    for letra in apellido_materno[1:]:
        if letra.upper() not in 'AEIOU':
            curp += letra.upper()
            break

    # Primer consonante interna del nombre
    for letra in nombre[1:]:
        if letra.upper() not in 'AEIOU':
            curp += letra.upper()
            break

    # Generar el primer dígito de la homoclave
    primer_digito = generar_primer_digito(fecha_nacimiento)

    # Agregar primer dígito a la CURP
    curp += primer_digito

    # Calcular el segundo dígito verificador
    segundo_digito_verificador = calcular_digito_verificador(curp)

    # Agregar segundo dígito verificador a la CURP
    curp += segundo_digito_verificador

    return curp

# Solicitar datos al usuario
nombre = input("Ingrese su nombre: ")
apellido_paterno = input("Ingrese su apellido paterno: ")
apellido_materno = input("Ingrese su apellido materno: ")
fecha_nacimiento = input("Ingrese su fecha de nacimiento (AAAA-MM-DD): ")
sexo = input("Ingrese su sexo (H o M): ")
estado = input("Ingrese la clave de su entidad federativa de nacimiento (dos letras en mayúsculas): ")

# Generar CURP
curp_generada = generar_curp(nombre, apellido_paterno, apellido_materno, fecha_nacimiento, sexo, estado)
print("La CURP generada es:", curp_generada)

# Generar el código QR de la CURP generada
qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=10,
    border=4,
)
qr.add_data(curp_generada)
qr.make(fit=True)

# Crear una imagen del código QR
img = qr.make_image(fill_color="black", back_color="white")

# Guardar el código QR como un archivo PNG
img_file = "curp_qr.png"
img.save(img_file)

print("Se ha generado el código QR de la CURP y se ha guardado como:", img_file)
