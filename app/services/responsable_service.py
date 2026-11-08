from sqlmodel import Session

from app.core.exceptions import RecursoDuplicadoError, RecursoNoEncontradoError
from app.models import Area, Responsable
from app.repositories import responsable_repository
from app.schemas.responsable import (
    ResponsableCreate,
    ResponsableUpdate,
)


def crear_responsable(
    session: Session,
    datos: ResponsableCreate
):
    area = session.get(Area, datos.area_id)

    if area is None:
        raise RecursoNoEncontradoError("No existe el área seleccionada.")

    responsable_existente = responsable_repository.obtener_responsable_por_email(
        session,
        datos.email
    )

    if responsable_existente is not None:
        raise RecursoDuplicadoError("Ya existe un responsable con ese email.")

    nuevo_responsable = Responsable(
        nombre=datos.nombre,
        apellido=datos.apellido,
        email=datos.email,
        area_id=datos.area_id,
    )

    return responsable_repository.crear_responsable(
        session,
        nuevo_responsable
    )


def obtener_responsables(session: Session):
    return responsable_repository.obtener_responsables(session)


def obtener_responsable_por_id(
    session: Session,
    responsable_id: int
):
    responsable = responsable_repository.obtener_responsable_por_id(
        session,
        responsable_id
    )

    if responsable is None:
        raise RecursoNoEncontradoError("No se encontró el responsable solicitado.")

    return responsable


def actualizar_responsable(
    session: Session,
    responsable_id: int,
    datos: ResponsableUpdate
):
    responsable = obtener_responsable_por_id(
        session,
        responsable_id
    )

    nuevos_datos = datos.model_dump(exclude_unset=True)

    if "area_id" in nuevos_datos:
        area = session.get(Area, nuevos_datos["area_id"])

        if area is None:
            raise RecursoNoEncontradoError("No existe el área seleccionada.")

    if "email" in nuevos_datos:
        responsable_existente = responsable_repository.obtener_responsable_por_email(
            session,
            nuevos_datos["email"],
            excluir_id=responsable_id
        )

        if responsable_existente is not None:
            raise RecursoDuplicadoError("Ese email ya está registrado.")

    return responsable_repository.actualizar_responsable(
        session,
        responsable,
        nuevos_datos
    )


def eliminar_responsable(
    session: Session,
    responsable_id: int
):
    responsable = obtener_responsable_por_id(
        session,
        responsable_id
    )

    responsable_repository.eliminar_responsable(
        session,
        responsable
    )

    return {"mensaje": "Responsable eliminado correctamente."}