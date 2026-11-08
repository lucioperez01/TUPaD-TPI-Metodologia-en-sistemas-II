
from sqlmodel import Session, select

from app.models import Estudiante


def crear_estudiante(session: Session, estudiante: Estudiante):
    session.add(estudiante)
    session.commit()
    session.refresh(estudiante)
    return estudiante


def obtener_estudiantes(session: Session):
    sentencia = select(Estudiante)
    return session.exec(sentencia).all()


def obtener_estudiante_por_id(session: Session, estudiante_id: int):
    return session.get(Estudiante, estudiante_id)


def obtener_estudiante_por_email(
    session: Session,
    email: str,
    excluir_id: int | None = None
):
    sentencia = select(Estudiante).where(Estudiante.email == email)

    if excluir_id is not None:
        sentencia = sentencia.where(Estudiante.id != excluir_id)

    return session.exec(sentencia).first()


def obtener_estudiante_por_matricula(
    session: Session,
    matricula: str,
    excluir_id: int | None = None
):
    sentencia = select(Estudiante).where(
        Estudiante.matricula == matricula
    )

    if excluir_id is not None:
        sentencia = sentencia.where(Estudiante.id != excluir_id)

    return session.exec(sentencia).first()


def actualizar_estudiante(
    session: Session,
    estudiante: Estudiante,
    nuevos_datos: dict
):
    for campo, valor in nuevos_datos.items():
        setattr(estudiante, campo, valor)

    session.add(estudiante)
    session.commit()
    session.refresh(estudiante)
    return estudiante


def eliminar_estudiante(session: Session, estudiante: Estudiante):
    session.delete(estudiante)
    session.commit()
