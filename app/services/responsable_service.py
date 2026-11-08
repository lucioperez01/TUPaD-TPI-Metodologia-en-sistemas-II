from sqlmodel import Session

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
        raise ValueError("No existe el área seleccionada.")

    responsables = responsable_repository.obtener_responsables(session)

    for responsable in responsables:
        if responsable.email.lower() == datos.email.lower():
            raise ValueError("Ya existe un responsable con ese email.")

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
        raise ValueError("No se encontró el responsable solicitado.")

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
            raise ValueError("No existe el área seleccionada.")

    if "email" in nuevos_datos:
        responsables = responsable_repository.obtener_responsables(session)

        for existente in responsables:
            if existente.id == responsable_id:
                continue

            if existente.email.lower() == nuevos_datos["email"].lower():
                raise ValueError("Ese email ya está registrado.")

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