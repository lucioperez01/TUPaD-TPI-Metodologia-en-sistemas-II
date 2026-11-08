class RecursoNoEncontradoError(Exception):
    """Excepción lanzada cuando un recurso no existe en la base de datos."""
    pass


class RecursoDuplicadoError(Exception):
    """Excepción lanzada cuando se intenta crear/actualizar un recurso con datos únicos duplicados."""
    pass
