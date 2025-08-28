from enum import Enum
import logging
import argparse
import json
from datetime import datetime as dt
from pathlib import Path


# Logger de eventos
logging.basicConfig(format='[%(levelname)s] %(message)s', level=logging.WARNING)
logger = logging.getLogger(__name__)

# Archivo para almacenar tareas
archivo_tareas = 'tasks.json'

# Formato para fechas
formato_fechas = '%y-%m-%d %H:%M:%S'
# formato_fechas = '%y-%m-%d'


class Status(Enum):
	TODO = 'todo'
	IN_PROGRESS = 'in_progress'
	DONE = 'done'

class TaskList:
	def __init__(self, archivo:str):
		self.tasks:list[dict] = []
		self.archivo:str = archivo
		self.last_id:int = 0
		if not Path(self.archivo).exists():
			self.save_tasks()
		self.load_tasks()

	def load_tasks(self):
		logger.debug('Cargando archivo de tareas')
		with open(self.archivo, 'r') as archivo:
			contenido = json.load(archivo)
		self.last_id = contenido['last_id']
		self.tasks = contenido['tasks']

	def save_tasks(self):
		logger.debug(f'Guardando archivo de tareas {self.last_id}')
		contenido = {'last_id': self.last_id, 'tasks': self.tasks}
		with open(self.archivo, 'w') as archivo:
			json.dump(contenido, archivo, indent=4)

	def add_task(self, description):
		self.last_id += 1
		status = Status.TODO.value
		created = dt.now().timestamp()
		updated = created
		logger.debug(f'Agregando tarea: ID={self.last_id} description={description}')
		self.tasks.append({'id': self.last_id, 'description': description, 'status': status, 'createdAt': created, 'updatedAt': updated})
		self.save_tasks()

	def delete_task(self, task_id):
		logger.debug(f'Eliminando tarea: ID={task_id}')
		deleted:bool = False
		for task in self.tasks:
			if task['id'] == task_id:
				self.tasks.remove(task)
				deleted = True
		if deleted:
			logger.info(f'Se eliminó la tarea ID={task_id}')
			self.save_tasks()
		else:
			logger.info(f'No se encontró la tarea ID={task_id}')

	def list_tasks(self, status=None):
		logger.debug(f'Listando tareas: status={status}')
		if status == 'all':
			return self.tasks
		return [task for task in self.tasks if task['status'] == status]

	def update_task(self, id:int, description:str) -> bool:
		for task in self.tasks:
			if task['id'] == id:
				task['description'] = description
				task['updatedAt'] = dt.now().timestamp()
				self.save_tasks()
				logger.info(f'Se editó la tarea con id={id}')
				return True
		logger.info(f'No se encontró la tarea con id={id}')
		return False

	def mark_status(self, id:int, status:str) -> bool:
		for task in self.tasks:
			logger.debug(task)
			if task['id'] == id:
				task['status'] = status
				task['updatedAt'] = dt.now().timestamp()
				logger.info(f'Tarea id={id} marcada como {status}')
				self.save_tasks()
				return True

		logger.info(f'No existe la tarea con id={id}')
		return False


task_list = TaskList(archivo_tareas)


def add_task(args) -> None:
	"""Agrega una tarea a la lista"""
	task_list.add_task(args.description)


def list_tasks(args) -> None:
	"""Lista las tareas"""
	tasks = task_list.list_tasks(args.status)
	longitud = len(str(task_list.last_id)) + 2 # Calcular el largo del número más grande
	print(f' {"ID": ^{longitud}}   {"CREATED": ^{len(formato_fechas)}}   {"UPDATED": ^{len(formato_fechas)}}   STATUS   DESCRIPTION')
	for i in tasks:
		created = dt.fromtimestamp(i["createdAt"]).strftime(formato_fechas)
		updated = dt.fromtimestamp(i["updatedAt"]).strftime(formato_fechas)
		status = ' '
		status = '.' if i['status'] == 'in_progress' else status
		status = 'X' if i['status'] == 'done' else status
		print(f' {(i["id"]):>{longitud}}   {created}   {updated}   {f"[{status}]":^6}   {i["description"]}')


def delete_task(args) -> None:
	"""Elimina una tarea"""
	task_list.delete_task(args.id)


def edit_task(args) -> None:
	"""Editar la descripción de una tarea"""
	task_list.update_task(args.id, args.description)

def mark_done(args) -> None:
	"""Marca una tarea como realizada"""
	task_list.mark_status(args.id, Status.DONE.value)


def mark_in_progress(args) -> None:
	"""Marca una tarea como en progreso"""
	task_list.mark_status(args.id, Status.IN_PROGRESS.value)


def mark_todo(args) -> None:
	"""Marca una tarea como a realizar"""
	task_list.mark_status(args.id, Status.TODO.value)

def main():
	# Parser de argumentos
	parser = argparse.ArgumentParser(prog='TaskApp')
	subparsers = parser.add_subparsers(dest='command', help='Subcomandos disponibles')
	# Subcomando add
	add_parser = subparsers.add_parser('add', help='Agregar una tarea')
	add_parser.add_argument('description', type=str, action='store', help='Descripción de la tarea')
	add_parser.set_defaults(func=add_task)
	# Subcomando delete
	delete_parser = subparsers.add_parser('delete', help='Eliminar una tarea')
	delete_parser.add_argument('id', type=int, action='store', help='ID de la tarea a eliminar')
	delete_parser.set_defaults(func=delete_task)
	# Subcomando edit
	edit_parser = subparsers.add_parser('edit', help='Editar la descripción de una tarea')
	edit_parser.add_argument('id', type=int, action='store', help='ID de la tarea a editar')
	edit_parser.add_argument('description', type=str, action='store', help='Nueva descripción de la tarea')
	edit_parser.set_defaults(func=edit_task)
	# Subcomando list
	list_parser = subparsers.add_parser('list', help='Listar tareas')
	list_parser.add_argument('status', choices=['all', 'todo', 'done', 'in_progress'], action='store', help='Estado de las tareas a listar')
	list_parser.set_defaults(func=list_tasks)
	# Subcomando mark-done
	mark_done_parser = subparsers.add_parser('mark-done', help='Marcar tarea como realizada')
	mark_done_parser.add_argument('id', type=int, action='store', help='ID de la tarea a marcar')
	mark_done_parser.set_defaults(func=mark_done)
	# Subcomando mark-todo
	mark_todo_parser = subparsers.add_parser('mark-todo', help='Marcar tarea como a realizar')
	mark_todo_parser.add_argument('id', type=int, action='store', help='ID de la tarea a marcar')
	mark_todo_parser.set_defaults(func=mark_todo)
	# Subcomando mark-done
	mark_in_progress_parser = subparsers.add_parser('mark-in-progress', help='Marcar tarea como en progreso')
	mark_in_progress_parser.add_argument('id', type=int, action='store', help='ID de la tarea a marcar')
	mark_in_progress_parser.set_defaults(func=mark_in_progress)
	# # Subcomando info
	# info_parser = subparsers.add_parser('info', help='Muestra la información de una tarea específica')
	# info_parser.add_argument('id', type=int, action='store', help='ID de la tarea a mostrar')
	# info_parser.set_defaults(func=info_task)
	# Parsear argumentos
	args = parser.parse_args()
	logger.debug(f'Args: {args}')

	# Ejecutar comando ingresado por argumentos
	if hasattr(args, 'func'):
		args.func(args)
	else:
		parser.print_help()


if __name__ == "__main__":
	main()
