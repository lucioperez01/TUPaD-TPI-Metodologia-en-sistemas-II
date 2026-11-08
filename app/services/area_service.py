from sqlmodel import Session

from app.core.exceptions import RecursoDuplicadoError, RecursoNoEncontradoError
from app.models import Area
from app.repositories import area_repository
from app.schemas.area import AreaCreate, AreaUpdate


def crear_area(session: Session, datos: AreaCreate):
    area_existente = area_repository.obtener_area_por_nombre(session, datos.nombre)
    
    if area_existente is not None:
        raise RecursoDuplicadoError("Ya existe un área con ese nombre.")

    nueva_area = Area(
        nombre=datos.nombre,
        descripcion=datos.descripcion,
    )

    return area_repository.crear_area(session, nueva_area)


def obtener_areas(session: Session):
    return area_repository.obtener_areas(session)


def obtener_area_por_id(session: Session, area_id: int):
    area = area_repository.obtener_area_por_id(session, area_id)

    if area is None:
        raise RecursoNoEncontradoError("No se encontró el área solicitada.")

    return area


def actualizar_area(
    session: Session,
    area_id: int,
    datos: AreaUpdate
):
    area = obtener_area_por_id(session, area_id)
    nuevos_datos = datos.model_dump(exclude_unset=True)

    if "nombre" in nuevos_datos:
        area_existente = area_repository.obtener_area_por_nombre(
            session, 
            nuevos_datos["nombre"], 
            excluir_id=area_id
        )
        
        if area_existente is not None:
            raise RecursoDuplicadoError("Ya existe un área con ese nombre.")

    return area_repository.actualizar_area(
        session,
        area,
        nuevos_datos
    )


def eliminar_area(session: Session, area_id: int):
    area = obtener_area_por_id(session, area_id)

    area_repository.eliminar_area(session, area)

    return {"mensaje": "Área eliminada correctamente."}