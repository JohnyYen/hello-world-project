class_name LibraryProblemContext
extends BaseProblemContext

# --- Datos específicos del problema de la Biblioteca ---
var book_queue: Array = []        # Cola de libros que necesitan ser devueltos o procesados
var bookshelves: Dictionary = {}  # Estanterías con libros disponibles
var borrowed_books: Array = []    # Libros actualmente prestados
var returned_books: Array = []    # Libros que han sido devueltos
var library_catalog: Dictionary = {} # Catálogo de la biblioteca con información de libros

# --- Objetivo del nivel ---
# Ej: {"all_returned": true, "books_sorted": 5}
var level_goal: Dictionary = {}

func _init():
    # Inicializar las propiedades específicas de la biblioteca
    book_queue = []
    bookshelves = {}
    borrowed_books = []
    returned_books = []
    library_catalog = {}
    level_goal = {}


# --- Función específica para verificar el objetivo del nivel de Biblioteca ---
func is_solution_correct() -> bool:
    for goal_key in level_goal.keys():
        match goal_key:
            "all_returned":
                if level_goal[goal_key] and book_queue.size() > 0:
                    print("No se han devuelto todos los libros.")
                    return false
            "min_books_sorted":
                var total_sorted = 0
                for shelf_books in bookshelves.values():
                    total_sorted += shelf_books.size()
                if total_sorted < level_goal[goal_key]:
                    print("No se han ordenado suficientes libros. Actual: " + str(total_sorted) + ", Requerido: " + str(level_goal[goal_key]))
                    return false
            "no_overdue_books":
                var overdue_count = 0
                for book in borrowed_books:
                    if book.get("overdue", false):
                        overdue_count += 1
                if overdue_count > 0:
                    print("Hay libros vencidos que no han sido procesados.")
                    return false
            # Puedes añadir más condiciones de objetivo aquí
            _:
                log("Condición de objetivo desconocida: " + goal_key)
                return false
    print("¡Todos los objetivos del nivel de biblioteca cumplidos!")
    return true