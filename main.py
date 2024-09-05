import json
import hashlib

def menu():
    while True:
        print("\n--- Menú ---")
        print("1. Registrarse")
        print("2. Iniciar Sesión")
        print("3. Salir")
        print("4. Agregar tarea")
        print("5. Eliminar tarea")
        print("6. Actualizar tarea")
        
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

        elif opcion == '4':
            nombre_tarea = input("Ingrese nombre tarea: ")
            descripcion = input("Ingrese la descripcion: ")
            fecha_vencimiento = input("Ingrese fecha de vencimiento formato (dd/mm/yyyy): ")
            etiqueta = input("Ingrese etiqueta: ")
            crear_tarea(nombre_tarea,descripcion,fecha_vencimiento,etiqueta,estado='Pendiente')

        elif opcion == '5':
            eliminar_tarea()

        elif opcion == '6':
            actualizar_tarea()
        
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


def crear_tarea(titulo, descripcion,fecha_vencimiento, etiqueta, estado, archivo_json='tarea.json'):
    try:
        with open(archivo_json, 'r') as archivo:
            tareas = json.load(archivo)
    except FileNotFoundError:
        print("No hay tareas")
        tareas = []
    except json.JSONDecodeError:
        tareas = []
    tarea_agregar = {'titulo':titulo,'descripcion':descripcion, 'fecha_vencimiento':fecha_vencimiento, 'etiqueta':etiqueta}
    tareas.append(tarea_agregar)

    with open(archivo_json, 'w') as archivo:
        json.dump(tareas, archivo)

def eliminar_tarea(archivo_json='tarea.json'):
    try:
        with open(archivo_json, 'r') as archivo:
            tareas = json.load(archivo)
    except FileNotFoundError:
        print("No hay tareas")
        pass
    except json.JSONDecodeError:
        pass

    iterador = 0
    print("\nSeleccione tarea a eliminar:")
    while(iterador < len(tareas)):
        print('tarea '+ str(iterador + 1) +': ' + str(tareas[iterador]))
        iterador = iterador + 1
    
    tarea_eliminar = input("Ingrese numero de tarea a eliminar\n")
    tareas.pop(int(tarea_eliminar) - 1)

    with open(archivo_json, 'w') as archivo:
        json.dump(tareas, archivo)

def actualizar_tarea(archivo_json='tarea.json'):
    try:
        with open(archivo_json, 'r') as archivo:
            tareas = json.load(archivo)
    except FileNotFoundError:
        print("No hay tareas")
        pass
    except json.JSONDecodeError:
        pass

    iterador = 0
    print("\nSeleccione tarea a actualizar:")
    while(iterador < len(tareas)):
        print('tarea '+ str(iterador + 1) +': ' + str(tareas[iterador]))
        iterador = iterador + 1
    
    tarea_actualizar = input("Ingrese numero de tarea a actualizar\n")
    elemento_actualizar = input("\nIndique que desea actualizar (titulo, descripcion, fecha_vencimiento, etiqueta):")
    tareas[int(tarea_actualizar)-1][elemento_actualizar] = input("Ingrese nuevo valor:")

    with open(archivo_json, 'w') as archivo:
        json.dump(tareas, archivo)
# Ejecutar el menú
menu()

