
from sqlmodel import Session

from app.core.constants import ESTADO_INICIAL_SOLICITUD
from app.models import Area, Estudiante, Responsable, Solicitud
from app.repositories import solicitud_repository
from app.schemas.referencias import SolicitudReferencias
from app.schemas.solicitud import SolicitudCreate, SolicitudUpdate


def validar_referencias(
    session: Session,
    referencias: SolicitudReferencias
):
    estudiante = session.get(Estudiante, referencias.estudiante_id)

    if estudiante is None:
        raise ValueError("No existe el estudiante seleccionado.")

    area = session.get(Area, referencias.area_id)

    if area is None:
        raise ValueError("No existe el área seleccionada.")

    if referencias.responsable_id is not None:
        responsable = session.get(
            Responsable,
            referencias.responsable_id
        )

        if responsable is None:
            raise ValueError("No existe el responsable seleccionado.")

        if responsable.area_id != referencias.area_id:
            raise ValueError(
                "El responsable no pertenece al área seleccionada."
            )


def crear_solicitud(session: Session, datos: SolicitudCreate):
    referencias = SolicitudReferencias(
        estudiante_id=datos.estudiante_id,
        area_id=datos.area_id,
        responsable_id=datos.responsable_id,
    )

    validar_referencias(session, referencias)

    nueva_solicitud = Solicitud(
        titulo=datos.titulo,
        descripcion=datos.descripcion,
        tipo=datos.tipo,
        prioridad=datos.prioridad,
        estado=ESTADO_INICIAL_SOLICITUD,
        estudiante_id=datos.estudiante_id,
        area_id=datos.area_id,
        responsable_id=datos.responsable_id,
    )

    return solicitud_repository.crear_solicitud(
        session,
        nueva_solicitud
    )


def obtener_solicitudes(session: Session):
    return solicitud_repository.obtener_solicitudes(session)


def obtener_solicitud_por_id(session: Session, solicitud_id: int):
    solicitud = solicitud_repository.obtener_solicitud_por_id(
        session,
        solicitud_id
    )

    if solicitud is None:
        raise ValueError("No se encontró la solicitud solicitada.")

    return solicitud


def actualizar_solicitud(
    session: Session,
    solicitud_id: int,
    datos: SolicitudUpdate
):
    solicitud = obtener_solicitud_por_id(session, solicitud_id)

    nuevos_datos = datos.model_dump(exclude_unset=True)

    referencias = SolicitudReferencias(
        estudiante_id=nuevos_datos.get(
            "estudiante_id",
            solicitud.estudiante_id
        ),
        area_id=nuevos_datos.get(
            "area_id",
            solicitud.area_id
        ),
        responsable_id=nuevos_datos.get(
            "responsable_id",
            solicitud.responsable_id
        ),
    )

    validar_referencias(session, referencias)

    return solicitud_repository.actualizar_solicitud(
        session,
        solicitud,
        nuevos_datos
    )


def eliminar_solicitud(session: Session, solicitud_id: int):
    solicitud = obtener_solicitud_por_id(session, solicitud_id)

    solicitud_repository.eliminar_solicitud(session, solicitud)

    return {"mensaje": "Solicitud eliminada correctamente."}
