import json

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

def ver_tareas_no_archivadas(archivo_json='tareas.json'):
    datos = cargar_datos(archivo_json)
    
    if not datos['tareas_activas']:
        print("No hay tareas activas.")
        return
    
    print("Tareas No Archivadas:")
    for tarea in datos['tareas_activas']:
        print(f"- {tarea['titulo']} (estado: {tarea['estado']}, vencimiento: {tarea['fecha_vencimiento']}, etiqueta: {tarea['etiqueta']})")

def consultar_tareas_archivadas(archivo_json='tareas.json'):
    datos = cargar_datos(archivo_json)
    
    if not datos['tareas_archivadas']:
        print("No hay tareas archivadas.")
        return
    
    print("Tareas Archivadas:")
    for tarea in datos['tareas_archivadas']:
        print(f"- {tarea['titulo']} (vencimiento: {tarea['fecha_vencimiento']}, etiqueta: {tarea['etiqueta']})")

def menu():
    while True:
        print("\n--- Menú de Tareas ---")
        print("1. Marcar tarea")
        print("2. Consultar tareas activas")
        print("3. Consultar tareas archivadas")
        print("4. Salir")
        
        opcion = input("Seleccione una opción: ")
        
        if opcion == '1':
            titulo = input("Ingrese el título de la tarea: ")
            nuevo_estado = input("Ingrese el nuevo estado ('en progreso' o 'completada'): ")
            marcar_tarea(titulo, nuevo_estado)
            if nuevo_estado == "completada":
                archivar_tareas()
        
        elif opcion == '2':
            ver_tareas_no_archivadas()
        
        elif opcion == '3':
            consultar_tareas_archivadas()
        
        elif opcion == '4':
            print("Saliendo...")
            break
        
        else:
            print("Opción no válida. Intente de nuevo.")

# Ejecutar el menú
menu()

