from sqlmodel import Session, select

from app.models import Solicitud


def crear_solicitud(session: Session, solicitud: Solicitud):
    session.add(solicitud)
    session.commit()
    session.refresh(solicitud)
    return solicitud


def obtener_solicitudes(session: Session):
    sentencia = select(Solicitud)
    return session.exec(sentencia).all()


def obtener_solicitud_por_id(session: Session, solicitud_id: int):
    return session.get(Solicitud, solicitud_id)


def actualizar_solicitud(
    session: Session,
    solicitud: Solicitud,
    nuevos_datos: dict
):
    for campo, valor in nuevos_datos.items():
        setattr(solicitud, campo, valor)

    session.add(solicitud)
    session.commit()
    session.refresh(solicitud)
    return solicitud


def eliminar_solicitud(session: Session, solicitud: Solicitud):
    session.delete(solicitud)
    session.commit()