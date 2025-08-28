# TaskApp: Un Gestor de Tareas por Línea de Comandos

## Descripción

TaskApp es una aplicación de gestión de tareas simple y eficiente basada en la línea de comandos, desarrollada en Python. Permite a los usuarios añadir, listar, editar, eliminar y cambiar el estado de sus tareas de forma rápida y sencilla. Este proyecto es una implementación del primer proyecto del roadmap de backend/python en [roadmap.sh](https://roadmap.sh/projects/task-tracker), sirviendo como una base sólida para entender los fundamentos del desarrollo backend.

## Características

- **Creación de tareas**: Añade nuevas tareas con una descripción.
- **Listado de tareas**: Visualiza todas las tareas o filtra por estado (pendientes, en progreso, completadas).
- **Edición de tareas**: Modifica la descripción de una tarea existente.
- **Eliminación de tareas**: Borra tareas individualmente.
- **Gestión de estados**: Marca tareas como "por hacer", "en progreso" o "completadas".
- **Persistencia de datos**: Las tareas se guardan en un archivo `tasks.json`.

## Instalación

1. **Clona el repositorio** (si aplica, o asegura tener `taskapp.py` y `tasks.json` en el mismo directorio).
2. **Asegúrate de tener Python 3 instalado.**

## Uso

Para usar TaskApp, navega al directorio donde se encuentra `taskapp.py` y ejecuta los comandos con `python taskapp.py [comando] [argumentos]`.

Aquí están los comandos disponibles:

### Añadir una tarea

```bash
python taskapp.py add "Mi nueva tarea"
```

### Listar tareas

Puedes listar todas las tareas o filtrar por estado:

- **Todas las tareas:**
    ```bash
    python taskapp.py list all
    ```
- **Tareas pendientes (`todo`):**
    ```bash
    python taskapp.py list todo
    ```
- **Tareas en progreso (`in_progress`):**
    ```bash
    python taskapp.py list in_progress
    ```
- **Tareas completadas (`done`):**
    ```bash
    python taskapp.py list done
    ```

### Editar una tarea

```bash
python taskapp.py edit 1 "Descripción de la tarea actualizada"
```
Reemplaza `1` con el ID de la tarea que deseas editar.

### Eliminar una tarea

```bash
python taskapp.py delete 1
```
Reemplaza `1` con el ID de la tarea que deseas eliminar.

### Marcar tareas por estado

- **Marcar como completada (`done`):**
    ```bash
    python taskapp.py mark-done 1
    ```
- **Marcar como en progreso (`in_progress`):**
    ```bash
    python taskapp.py mark-in-progress 1
    ```
- **Marcar como por hacer (`todo`):**
    ```bash
    python taskapp.py mark-todo 1
    ```
Reemplaza `1` con el ID de la tarea a actualizar.
