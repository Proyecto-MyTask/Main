import json
import hashlib
from datetime import datetime
import logging
import os

logging.basicConfig(
    filename='logfile.txt',  # Nombre del archivo donde se guardarán los logs
    level=logging.DEBUG,     # Nivel de log (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format='%(asctime)s - %(levelname)s - %(message)s',  # Formato del log
    datefmt='%Y-%m-%d %H:%M:%S'  # Formato de la fecha
)

def menu():
    logging.info("Aplicación iniciada correctamente.")
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
        print("4. Consultar tarea por titulo")
        print("5. Buscar tarea por filtro")
        print("6. Marcar Tarea ")
        print("7. Archivar tareas completadas")
        print("8. Consultar tareas archivadas")
        print("9. Ver tareas no archivadas")
        print("10. Salir")
        
        opcion = input("Seleccione una opción: ")
        
        if opcion == '10':
            print("Saliendo...")
            break

        elif opcion == '1':
            nombre_tarea = input("Ingrese titulo tarea: ")
            descripcion = input("Ingrese la descripcion: ")
            fecha_vencimiento = input("Ingrese fecha de vencimiento formato (dd/mm/yyyy): ")
            etiqueta = input("Ingrese etiqueta: ")
            crear_tarea(nombre_tarea,descripcion,fecha_vencimiento,etiqueta,estado='pendiente')

        elif opcion == '2':
            eliminar_tarea()

        elif opcion == '3':
            actualizar_tarea()
        
        elif opcion == '4':
            nombre_tarea = input("Ingrese titulo tarea: ")
            consultar_tarea(nombre_tarea)

        elif opcion == '5':
            print("\n1. Buscar por fecha de vencimiento")
            print("2. Buscar por etiquetas")
            print("3. Buscar por estado de la tarea")

            opcion_filtro = input("Seleccione una opción: ")

            if opcion_filtro == '1':
                fecha_de_partida = input("\nFecha desde la que quiere empezar a buscar, dejar vacio si no esta este limite (dd/mm/yyyy): ")
                fecha_de_termino = input("Fecha hasta la que quiere buscar, dejar vacio si no esta este limite (dd/mm/yyyy): ")
                filtrar_por_fecha(fecha_de_partida, fecha_de_termino)

            elif opcion_filtro == '2':
                etiqueta = input("\nIndique etiqueta que busca: ")
                filtrar_por_etiqueta(etiqueta)

            elif opcion_filtro == '3':
                estado = input("\nIndique estado que busca (pendiente, en progreso, completada o atrasada): ")
                filtrar_por_estado(estado)


        elif opcion == "6":
            titulo = input("Ingrese el título de la tarea: ")
            nuevo_estado = input("Ingrese el nuevo estado ('en progreso' o 'completada'): ")
            marcar_tarea(titulo, nuevo_estado)

        elif opcion == '7':
            archivar_tareas()
        
        elif opcion == '8':
            consultar_tareas_archivadas()
        
        elif opcion == '9':
            ver_tareas_no_archivadas()

        else:
            print("Opción no válida. Intente de nuevo.")
            logging.warning("Opción no válida. Intente de nuevo.")

def registrar_usuario(nombre_usuario, contraseña, archivo_json='usuarios.json'):
    usuarios = {}
    
    # Leer usuarios existentes del archivo JSON
    try:
        with open(archivo_json, 'r') as archivo:
            usuarios = json.load(archivo)
    except FileNotFoundError as e:
        logging.error(f"Error: No se encontró el archivo '{archivo_json}")
        pass
    except json.JSONDecodeError as e:
        logging.error(f"Error: No se pudo decodificar el archivo JSON '{archivo_json}")
        pass
    except Exception as e:
        logging.error("Error inesperado")
        pass
        
    # Verificar si el usuario ya existe
    if nombre_usuario in usuarios:
        print("El nombre de usuario ya existe. Intente con otro.")
        logging.warning("El nombre de usuario ya existe. Intente con otro.")
        return False
    
    # Guardar el nuevo usuario con la contraseña encriptada
    usuarios[nombre_usuario] = encriptar_contraseña(contraseña)
    
    try:
        with open(archivo_json, 'w') as archivo:
            json.dump(usuarios, archivo)
    except FileNotFoundError as e:
        logging.error(f"Error: No se encontró el archivo '{archivo_json}")
        return False
    except PermissionError as e:
        logging.error(f"Error: No tienes permisos para escribir en el archivo '{archivo_json}'")
        return False
    except json.JSONDecodeError as e:
        logging.error(f"Error: No se pudo decodificar el archivo JSON '{archivo_json}")
        return False
    except Exception as e:
        logging.error("Error inesperado")
        return False
    
    print("Usuario registrado exitosamente.")
    logging.info("Usuario registrado")
    return True

def iniciar_sesion(nombre_usuario, contraseña, archivo_json='usuarios.json'):
    try:
        if os.path.getsize(archivo_json) == 0: 
            logging.warning("Archivo vacio, tiene que registrarse")
            return False
        with open(archivo_json, 'r') as archivo:
            usuarios = json.load(archivo)
    except FileNotFoundError as e:
        logging.error(f"Error: No se encontró el archivo '{archivo_json}")
        return False
    except json.JSONDecodeError as e:
        logging.error(f"Error: No se pudo decodificar el archivo JSON '{archivo_json}")
        return False
    except Exception as e:
        logging.error("Error inesperado")
        return False

    
    if nombre_usuario in usuarios:
        contraseña_encriptada = encriptar_contraseña(contraseña)
        if usuarios[nombre_usuario] == contraseña_encriptada:
            print("Inicio de sesión exitoso.")
            logging.info("Usuario ha iniciado sesión")
            return True
        else:
            print("Contraseña incorrecta.")
            logging.warning("Contraseña incorrecta")
            return False
    else:
        print("El usuario no existe.")
        logging.warning("Usuario no existe.")
        return False

def encriptar_contraseña(contraseña):
    return hashlib.sha256(contraseña.encode()).hexdigest()


def crear_tarea(titulo, descripcion,fecha_vencimiento, etiqueta, estado, archivo_json='tareas.json'):
    tareas = cargar_datos()
    tarea_agregar = {'titulo':titulo,'descripcion':descripcion, 'fecha_vencimiento':fecha_vencimiento, 'etiqueta':etiqueta, 'estado':estado}
    tareas["tareas_activas"].append(tarea_agregar)
    

    try:
        with open(archivo_json, 'w') as archivo:
            json.dump(tareas, archivo)
        logging.info("Tarea creada")
    except FileNotFoundError as e:
        logging.error(f"Error: No se encontró el archivo '{archivo_json}")
    except PermissionError as e:
        logging.error(f"Error: No tienes permisos para escribir en el archivo '{archivo_json}'")
    except json.JSONDecodeError as e:
        logging.error(f"Error: No se pudo decodificar el archivo JSON '{archivo_json}")
    except Exception as e:
        logging.error("Error inesperado")

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

    try:
        with open(archivo_json, 'w') as archivo:
            json.dump(tareas, archivo)
    except FileNotFoundError as e:
        logging.error(f"Error: No se encontró el archivo '{archivo_json}")
    except PermissionError as e:
        logging.error(f"Error: No tienes permisos para escribir en el archivo '{archivo_json}'")
    except json.JSONDecodeError as e:
        logging.error(f"Error: No se pudo decodificar el archivo JSON '{archivo_json}")
    except Exception as e:
        logging.error("Error inesperado")

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

    try:
        with open(archivo_json, 'w') as archivo:
            json.dump(tareas, archivo)
    except FileNotFoundError as e:
        logging.error(f"Error: No se encontró el archivo '{archivo_json}")
    except PermissionError as e:
        logging.error(f"Error: No tienes permisos para escribir en el archivo '{archivo_json}'")
    except json.JSONDecodeError as e:
        logging.error(f"Error: No se pudo decodificar el archivo JSON '{archivo_json}")
    except Exception as e:
        logging.error("Error inesperado")

def consultar_tarea(titulo):
    datos = cargar_datos()
    tareas_activas = datos['tareas_activas']
    tareas_archivadas = datos['tareas_archivadas']

    tareas_activas = [tareas for tareas in tareas_activas if tareas['titulo'].find(titulo) != -1]

    if not tareas_activas:
        logging.info("No hay tareas activas con dicho titulo")
    else:
        print('\nTareas activas filtradas por titulo:')
        for tarea in tareas_activas:
            print('\nTarea: '+ tarea['titulo'])
            print('Descripcion: '+ tarea['descripcion'])
            print('Fecha vencimiento: '+ tarea['fecha_vencimiento'])
            print('Etiqueta: '+ tarea['etiqueta'])
            print('Estado: '+ tarea['estado'])
    
    tareas_archivadas = [tareas for tareas in tareas_archivadas if tareas['titulo'].find(titulo) != -1]
    
    if not tareas_archivadas:
        logging.info("No hay tareas archivadas con dicha titulo")
    else:
        print('\nTareas archivadas filtradas por titulo:')
        for tarea in tareas_archivadas:
            print('\nTarea: '+ tarea['titulo'])
            print('Descripcion: '+ tarea['descripcion'])
            print('Fecha vencimiento: '+ tarea['fecha_vencimiento'])
            print('Etiqueta: '+ tarea['etiqueta'])
            print('Estado: '+ tarea['estado'])

def cargar_datos(archivo_json='tareas.json'):
    try:
        with open(archivo_json, 'r') as archivo:
            return json.load(archivo)
    except FileNotFoundError as e:
        logging.error(f"Error: No se encontró el archivo '{archivo_json}")
        return {"tareas_activas": [], "tareas_archivadas": []} 
    except json.JSONDecodeError as e:
        logging.error(f"Error: No se pudo decodificar el archivo JSON '{archivo_json}")
        return {"tareas_activas": [], "tareas_archivadas": []}
    except Exception as e:
        logging.error("Error inesperado")
        return {"tareas_activas": [], "tareas_archivadas": []}
        

def guardar_datos(datos, archivo_json='tareas.json'):
    try:
        with open(archivo_json, 'w') as archivo:
            json.dump(datos, archivo, indent=4)
    except FileNotFoundError as e:
        logging.error(f"Error: No se encontró el archivo '{archivo_json}")
    except PermissionError as e:
        logging.error(f"Error: No tienes permisos para escribir en el archivo '{archivo_json}'")
    except json.JSONDecodeError as e:
        logging.error(f"Error: No se pudo decodificar el archivo JSON '{archivo_json}")
    except Exception as e:
        logging.error(f"Error inesperado")

def marcar_tarea(titulo, nuevo_estado, archivo_json='tareas.json'):
    datos = cargar_datos(archivo_json)
    
    # Buscar tarea por título y cambiar el estado
    for tarea in datos['tareas_activas']:
        if tarea['titulo'] == titulo:
            tarea['estado'] = nuevo_estado
            print(f"Tarea '{titulo}' marcada como {nuevo_estado}.")
            guardar_datos(datos, archivo_json)
            return
    
    logging.warning(f"Tarea con título '{titulo}' no encontrada.")
    print(f"Tarea con título '{titulo}' no encontrada.")

def archivar_tareas(archivo_json='tareas.json'):
    datos = cargar_datos(archivo_json)
    
    tareas_completadas = [tarea for tarea in datos['tareas_activas'] if tarea['estado'] == 'completada']
    
    if not tareas_completadas:
        # print("No hay tareas completadas para archivar.")
        logging.warning("No hay tareas completadas para archivar.")
        return
    
    # Mover tareas completadas a la sección de tareas archivadas
    datos['tareas_archivadas'].extend(tareas_completadas)
    
    # Eliminar tareas completadas de las tareas activas
    datos['tareas_activas'] = [tarea for tarea in datos['tareas_activas'] if tarea['estado'] != 'completada']
    
    guardar_datos(datos, archivo_json)
    # print("Tareas completadas archivadas exitosamente.")
    logging.info("Tareas completadas archivadas exitosamente.")

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
        logging.info("No hay tareas activas.")
        # print("No hay tareas activas.")
        return
    
    print("Tareas No Archivadas:")
    for tarea in datos['tareas_activas']:
        print(f"- {tarea['titulo']} (estado: {tarea['estado']}, descripcion: {tarea['descripcion']}, vencimiento: {tarea['fecha_vencimiento']}, etiqueta: {tarea['etiqueta']})")

def filtrar_por_fecha(fecha_inicio, fecha_termino):
    datos = cargar_datos()
    tareas_activas = datos['tareas_activas']
    tareas_archivadas = datos['tareas_archivadas']

    if(fecha_inicio != ''):
        fecha1 = datetime.strptime(fecha_inicio, "%d/%m/%Y")
        tareas_activas = [tareas for tareas in tareas_activas if datetime.strptime(tareas['fecha_vencimiento'], "%d/%m/%Y") >= fecha1]
    if(fecha_termino != ''):
        fecha2 = datetime.strptime(fecha_termino, "%d/%m/%Y")
        tareas_activas = [tareas for tareas in tareas_activas if datetime.strptime(tareas['fecha_vencimiento'], "%d/%m/%Y") <= fecha2]
    
    if not tareas_activas:
        logging.info("No hay tareas activas en dichas fechas")
    else:
        print('\nTareas activas filtradas por fecha:')
        for tarea in tareas_activas:
            print('\nTarea: '+ tarea['titulo'])
            print('Descripcion: '+ tarea['descripcion'])
            print('Fecha vencimiento: '+ tarea['fecha_vencimiento'])
            print('Etiqueta: '+ tarea['etiqueta'])
            print('Estado: '+ tarea['estado'])
    
    if(fecha_inicio != ''):
        fecha1 = datetime.strptime(fecha_inicio, "%d/%m/%Y")
        tareas_archivadas = [tareas for tareas in tareas_archivadas if datetime.strptime(tareas['fecha_vencimiento'], "%d/%m/%Y") >= fecha1]
    if(fecha_termino != ''):
        fecha2 = datetime.strptime(fecha_termino, "%d/%m/%Y")
        tareas_archivadas = [tareas for tareas in tareas_archivadas if datetime.strptime(tareas['fecha_vencimiento'], "%d/%m/%Y") <= fecha2]
    
    if not tareas_archivadas:
        logging.info("No hay tareas archivadas en dichas fechas")
    else:
        print('\nTareas archivadas filtradas por fecha:')
        for tarea in tareas_archivadas:
            print('\nTarea: '+ tarea['titulo'])
            print('Descripcion: '+ tarea['descripcion'])
            print('Fecha vencimiento: '+ tarea['fecha_vencimiento'])
            print('Etiqueta: '+ tarea['etiqueta'])
            print('Estado: '+ tarea['estado'])

def filtrar_por_etiqueta(etiqueta):
    datos = cargar_datos()
    tareas_activas = datos['tareas_activas']
    tareas_archivadas = datos['tareas_archivadas']

    tareas_activas = [tareas for tareas in tareas_activas if tareas['etiqueta'].find(etiqueta) != -1]

    if not tareas_activas:
        logging.info("No hay tareas activas con dicha etiqueta")
    else:
        print('\nTareas activas filtradas por etiqueta:')
        for tarea in tareas_activas:
            print('\nTarea: '+ tarea['titulo'])
            print('Descripcion: '+ tarea['descripcion'])
            print('Fecha vencimiento: '+ tarea['fecha_vencimiento'])
            print('Etiqueta: '+ tarea['etiqueta'])
            print('Estado: '+ tarea['estado'])
    
    tareas_archivadas = [tareas for tareas in tareas_archivadas if tareas['etiqueta'].find(etiqueta) != -1]
    
    if not tareas_archivadas:
        logging.info("No hay tareas archivadas con dicha etiqueta")
    else:
        print('\nTareas archivadas filtradas por etiqueta:')
        for tarea in tareas_archivadas:
            print('\nTarea: '+ tarea['titulo'])
            print('Descripcion: '+ tarea['descripcion'])
            print('Fecha vencimiento: '+ tarea['fecha_vencimiento'])
            print('Etiqueta: '+ tarea['etiqueta'])
            print('Estado: '+ tarea['estado'])

def filtrar_por_estado(estado):
    datos = cargar_datos()
    tareas_activas = datos['tareas_activas']
    tareas_archivadas = datos['tareas_archivadas']

    tareas_activas = [tareas for tareas in tareas_activas if tareas['estado'] == estado]

    if not tareas_activas:
        logging.info("No hay tareas activas con dicho estado")
    else:
        print('\nTareas activas filtradas por estado:')
        for tarea in tareas_activas:
            print('\nTarea: '+ tarea['titulo'])
            print('Descripcion: '+ tarea['descripcion'])
            print('Fecha vencimiento: '+ tarea['fecha_vencimiento'])
            print('Etiqueta: '+ tarea['etiqueta'])
            print('Estado: '+ tarea['estado'])
    
    tareas_archivadas = [tareas for tareas in tareas_archivadas if tareas['estado'] == estado]
    
    if not tareas_archivadas:
        logging.info("No hay tareas archivadas con dicho estado")
    else:
        print('\nTareas archivadas filtradas por estado:')
        for tarea in tareas_archivadas:
            print('\nTarea: '+ tarea['titulo'])
            print('Descripcion: '+ tarea['descripcion'])
            print('Fecha vencimiento: '+ tarea['fecha_vencimiento'])
            print('Etiqueta: '+ tarea['etiqueta'])
            print('Estado: '+ tarea['estado'])
    
# Ejecutar el menú
menu()

