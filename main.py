import json
import hashlib

def menu():
    while True:
        print("\n--- Menú ---")
        print("1. Registrarse")
        print("2. Iniciar Sesión")
        print("3. Salir")
        
        opcion = input("Seleccione una opción: ")
        
        if opcion == '1':
            nombre_usuario = input("Ingrese un nombre de usuario: ")
            contraseña = input("Ingrese una contraseña: ")
            registrar_usuario(nombre_usuario, contraseña)
        
        elif opcion == '2':
            nombre_usuario = input("Ingrese su nombre de usuario: ")
            contraseña = input("Ingrese su contraseña: ")
            iniciar_sesion(nombre_usuario, contraseña)
        
        elif opcion == '3':
            print("Saliendo...")
            break
        
        else:
            print("Opción no válida. Intente de nuevo.")

def registrar_usuario(nombre_usuario, contraseña, archivo_json='usuarios.json'):
    usuarios = {}
    
    # Leer usuarios existentes del archivo JSON
    try:
        with open(archivo_json, 'r') as archivo:
            usuarios = json.load(archivo)
    except FileNotFoundError:
        pass
    
    # Verificar si el usuario ya existe
    if nombre_usuario in usuarios:
        print("El nombre de usuario ya existe. Intente con otro.")
        return False
    
    # Guardar el nuevo usuario con la contraseña encriptada
    usuarios[nombre_usuario] = encriptar_contraseña(contraseña)
    
    with open(archivo_json, 'w') as archivo:
        json.dump(usuarios, archivo)
    
    print("Usuario registrado exitosamente.")
    return True

def iniciar_sesion(nombre_usuario, contraseña, archivo_json='usuarios.json'):
    try:
        with open(archivo_json, 'r') as archivo:
            usuarios = json.load(archivo)
    except FileNotFoundError:
        print("No hay usuarios registrados.")
        return False
    
    if nombre_usuario in usuarios:
        contraseña_encriptada = encriptar_contraseña(contraseña)
        if usuarios[nombre_usuario] == contraseña_encriptada:
            print("Inicio de sesión exitoso.")
            return True
        else:
            print("Contraseña incorrecta.")
            return False
    else:
        print("El usuario no existe.")
        return False

def encriptar_contraseña(contraseña):
    return hashlib.sha256(contraseña.encode()).hexdigest()

# Ejecutar el menú
menu()

