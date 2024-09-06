import json
import hashlib

def menu():
    while True:
        print("\n--- Bienvenido, favor registrarse o iniciar sesión ---")
        print("1. Registrarse")
        print("2. Iniciar Sesión")
        opcion = input("Seleccione una opción: ")
        
        if opcion == '1':
            nombre_usuario = input("Ingrese un nombre de usuario: ")
            contraseña = input("Ingrese una contraseña: ")
            registrar_usuario(nombre_usuario, contraseña)
        
        elif opcion == '2':
            nombre_usuario = input("Ingrese su nombre de usuario: ")
            contraseña = input("Ingrese su contraseña: ") 
            if iniciar_sesion(nombre_usuario, contraseña):
                break
    while True:
        print("\n--- Menú ---")
        print("1. Agregar tarea")
        print("2. Eliminar tarea")
        print("3. Actualizar tarea")
        print("4. Marcar Tarea ")
        print("5. Archivar tareas completadas")
        print("6. Consultar tareas archivadas")
        print("7. Ver tareas no archivadas")
        print("8. Salir")
        
        opcion = input("Seleccione una opción: ")
        
        if opcion == '8':
            print("Saliendo...")
            break

        elif opcion == '1':
            nombre_tarea = input("Ingrese nombre tarea: ")
            descripcion = input("Ingrese la descripcion: ")
            fecha_vencimiento = input("Ingrese fecha de vencimiento formato (dd/mm/yyyy): ")
            etiqueta = input("Ingrese etiqueta: ")
            crear_tarea(nombre_tarea,descripcion,fecha_vencimiento,etiqueta,estado='pendiente')

        elif opcion == '2':
            eliminar_tarea()

        elif opcion == '3':
            actualizar_tarea()
        
        elif opcion == "4":
            titulo = input("Ingrese el título de la tarea: ")
            nuevo_estado = input("Ingrese el nuevo estado ('en progreso' o 'completada'): ")
            marcar_tarea(titulo, nuevo_estado)

        elif opcion == '5':
            archivar_tareas()
        
        elif opcion == '6':
            consultar_tareas_archivadas()
        
        elif opcion == '7':
            ver_tareas_no_archivadas()

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


def crear_tarea(titulo, descripcion,fecha_vencimiento, etiqueta, estado, archivo_json='tareas.json'):
    tareas = cargar_datos()
    tarea_agregar = {'titulo':titulo,'descripcion':descripcion, 'fecha_vencimiento':fecha_vencimiento, 'etiqueta':etiqueta, 'estado':estado}
    tareas["tareas_activas"].append(tarea_agregar)

    with open(archivo_json, 'w') as archivo:
        json.dump(tareas, archivo)

def eliminar_tarea(archivo_json='tareas.json'):
    tareas = cargar_datos()

    iterador = 0
    print("\nSeleccione tarea a eliminar:")
    while(iterador < len(tareas['tareas_activas'])):
        print('tarea '+ str(iterador + 1) +': ' + str(tareas['tareas_activas'][iterador]))
        iterador = iterador + 1
    while(iterador < len(tareas['tareas_archivadas']) + len(tareas['tareas_activas'])):
        print('tarea '+ str(iterador + 1) +': ' + str(tareas['tareas_archivadas'][iterador - len(tareas['tareas_activas'])]))
        iterador = iterador + 1
    tarea_eliminar = int(input("Ingrese numero de tarea a eliminar\n"))
    if tarea_eliminar-1 < len(tareas['tareas_activas']):
        tareas['tareas_activas'].pop(int(tarea_eliminar) - 1)
    else:
        print(int(tarea_eliminar - len(tareas['tareas_activas'])) - 1)
        tareas['tareas_archivadas'].pop(int(tarea_eliminar - len(tareas['tareas_activas'])) - 1)

    with open(archivo_json, 'w') as archivo:
        json.dump(tareas, archivo)

def actualizar_tarea(archivo_json='tareas.json'):
    tareas = cargar_datos()

    iterador = 0
    print("\nSeleccione tarea a actualizar:")
    while(iterador < len(tareas['tareas_activas'])):
        print('tarea '+ str(iterador + 1) +': ' + str(tareas['tareas_activas'][iterador]))
        iterador = iterador + 1
    
    tarea_actualizar = input("Ingrese numero de tarea a actualizar\n")
    elemento_actualizar = input("\nIndique que desea actualizar (titulo, descripcion, fecha_vencimiento, etiqueta):")
    tareas['tareas_activas'][int(tarea_actualizar)-1][elemento_actualizar] = input("Ingrese nuevo valor:")

    with open(archivo_json, 'w') as archivo:
        json.dump(tareas, archivo)

def cargar_datos(archivo_json='tareas.json'):
    try:
        with open(archivo_json, 'r') as archivo:
            return json.load(archivo)
    except FileNotFoundError:
        return {"tareas_activas": [], "tareas_archivadas": []}

def guardar_datos(datos, archivo_json='tareas.json'):
    with open(archivo_json, 'w') as archivo:
        json.dump(datos, archivo, indent=4)

def marcar_tarea(titulo, nuevo_estado, archivo_json='tareas.json'):
    datos = cargar_datos(archivo_json)
    
    # Buscar tarea por título y cambiar el estado
    for tarea in datos['tareas_activas']:
        if tarea['titulo'] == titulo:
            tarea['estado'] = nuevo_estado
            print(f"Tarea '{titulo}' marcada como {nuevo_estado}.")
            guardar_datos(datos, archivo_json)
            return
    
    print(f"Tarea con título '{titulo}' no encontrada.")

def archivar_tareas(archivo_json='tareas.json'):
    datos = cargar_datos(archivo_json)
    
    tareas_completadas = [tarea for tarea in datos['tareas_activas'] if tarea['estado'] == 'completada']
    
    if not tareas_completadas:
        print("No hay tareas completadas para archivar.")
        return
    
    # Mover tareas completadas a la sección de tareas archivadas
    datos['tareas_archivadas'].extend(tareas_completadas)
    
    # Eliminar tareas completadas de las tareas activas
    datos['tareas_activas'] = [tarea for tarea in datos['tareas_activas'] if tarea['estado'] != 'completada']
    
    guardar_datos(datos, archivo_json)
    print("Tareas completadas archivadas exitosamente.")

def consultar_tareas_archivadas(archivo_json='tareas.json'):
    datos = cargar_datos(archivo_json)
    
    if not datos['tareas_archivadas']:
        print("No hay tareas archivadas.")
        return
    
    print("Tareas Archivadas:")
    for tarea in datos['tareas_archivadas']:
        print(f"- {tarea['titulo']} (vencimiento: {tarea['fecha_vencimiento']}, etiqueta: {tarea['etiqueta']})")

def ver_tareas_no_archivadas(archivo_json='tareas.json'):
    datos = cargar_datos(archivo_json)
    
    if not datos['tareas_activas']:
        print("No hay tareas activas.")
        return
    
    print("Tareas No Archivadas:")
    for tarea in datos['tareas_activas']:
        print(f"- {tarea['titulo']} (estado: {tarea['estado']}, descripcion: {tarea['descripcion']}, vencimiento: {tarea['fecha_vencimiento']}, etiqueta: {tarea['etiqueta']})")


# Ejecutar el menú
menu()

