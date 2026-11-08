
from sqlmodel import Session

from app.core.exceptions import RecursoDuplicadoError, RecursoNoEncontradoError
from app.models import Estudiante
from app.repositories import estudiante_repository
from app.schemas.estudiante import (
    EstudianteCreate,
    EstudianteUpdate,
)


def validar_datos_unicos(
    session: Session,
    email: str | None = None,
    matricula: str | None = None,
    estudiante_id: int | None = None,
):
    if email is not None:
        estudiante = estudiante_repository.obtener_estudiante_por_email(
            session,
            email,
            excluir_id=estudiante_id,
        )

        if estudiante is not None:
            raise RecursoDuplicadoError("Ese email ya está registrado.")

    if matricula is not None:
        estudiante = estudiante_repository.obtener_estudiante_por_matricula(
            session,
            matricula,
            excluir_id=estudiante_id,
        )

        if estudiante is not None:
            raise RecursoDuplicadoError("Esa matrícula ya está registrada.")


def crear_estudiante(session: Session, datos: EstudianteCreate):
    validar_datos_unicos(
        session,
        email=datos.email,
        matricula=datos.matricula,
    )

    nuevo_estudiante = Estudiante(
        nombre=datos.nombre,
        apellido=datos.apellido,
        email=datos.email,
        matricula=datos.matricula,
    )

    return estudiante_repository.crear_estudiante(
        session,
        nuevo_estudiante
    )


def obtener_estudiantes(session: Session):
    return estudiante_repository.obtener_estudiantes(session)


def obtener_estudiante_por_id(session: Session, estudiante_id: int):
    estudiante = estudiante_repository.obtener_estudiante_por_id(
        session,
        estudiante_id
    )

    if estudiante is None:
        raise RecursoNoEncontradoError("No se encontró el estudiante solicitado.")

    return estudiante


def actualizar_estudiante(
    session: Session,
    estudiante_id: int,
    datos: EstudianteUpdate
):
    estudiante = obtener_estudiante_por_id(session, estudiante_id)

    nuevos_datos = datos.model_dump(exclude_unset=True)

    if "email" in nuevos_datos or "matricula" in nuevos_datos:
        validar_datos_unicos(
            session,
            email=nuevos_datos.get("email"),
            matricula=nuevos_datos.get("matricula"),
            estudiante_id=estudiante_id,
        )

    return estudiante_repository.actualizar_estudiante(
        session,
        estudiante,
        nuevos_datos
    )


def eliminar_estudiante(session: Session, estudiante_id: int):
    estudiante = obtener_estudiante_por_id(session, estudiante_id)

    estudiante_repository.eliminar_estudiante(session, estudiante)

    return {"mensaje": "Estudiante eliminado correctamente."}
