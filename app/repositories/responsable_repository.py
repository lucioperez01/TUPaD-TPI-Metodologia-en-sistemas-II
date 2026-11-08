from sqlmodel import Session, select

from app.models import Responsable


def crear_responsable(session: Session, responsable: Responsable):
    session.add(responsable)
    session.commit()
    session.refresh(responsable)
    return responsable


def obtener_responsables(session: Session):
    sentencia = select(Responsable)
    return session.exec(sentencia).all()


def obtener_responsable_por_id(
    session: Session,
    responsable_id: int
):
    return session.get(Responsable, responsable_id)


def obtener_responsable_por_email(
    session: Session,
    email: str,
    excluir_id: int | None = None
):
    sentencia = select(Responsable).where(Responsable.email == email)
    
    if excluir_id is not None:
        sentencia = sentencia.where(Responsable.id != excluir_id)
    
    return session.exec(sentencia).first()


def actualizar_responsable(
    session: Session,
    responsable: Responsable,
    nuevos_datos: dict
):
    for campo, valor in nuevos_datos.items():
        setattr(responsable, campo, valor)

    session.add(responsable)
    session.commit()
    session.refresh(responsable)
    return responsable


def eliminar_responsable(
    session: Session,
    responsable: Responsable
):
    session.delete(responsable)
    session.commit()