from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from app.database.connection import get_session
from app.schemas.solicitud import (
    SolicitudCreate,
    SolicitudResponse,
    SolicitudUpdate,
)
from app.services import solicitud_service


router = APIRouter(
    prefix="/solicitudes",
    tags=["Solicitudes"]
)


@router.post(
    "/",
    response_model=SolicitudResponse,
    status_code=status.HTTP_201_CREATED
)
def crear_solicitud(
    datos: SolicitudCreate,
    session: Annotated[Session, Depends(get_session)]
):
    try:
        return solicitud_service.crear_solicitud(session, datos)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))


@router.get("/", response_model=list[SolicitudResponse])
def obtener_solicitudes(
    session: Annotated[Session, Depends(get_session)]
):
    return solicitud_service.obtener_solicitudes(session)


@router.get("/{solicitud_id}", response_model=SolicitudResponse)
def obtener_solicitud(
    solicitud_id: int,
    session: Annotated[Session, Depends(get_session)]
):
    try:
        return solicitud_service.obtener_solicitud_por_id(
            session,
            solicitud_id
        )
    except ValueError as error:
        raise HTTPException(status_code=404, detail=str(error))


@router.put("/{solicitud_id}", response_model=SolicitudResponse)
def actualizar_solicitud(
    solicitud_id: int,
    datos: SolicitudUpdate,
    session: Annotated[Session, Depends(get_session)]
):
    try:
        return solicitud_service.actualizar_solicitud(
            session,
            solicitud_id,
            datos
        )
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))


@router.delete("/{solicitud_id}")
def eliminar_solicitud(
    solicitud_id: int,
    session: Annotated[Session, Depends(get_session)]
):
    try:
        return solicitud_service.eliminar_solicitud(
            session,
            solicitud_id
        )
    except ValueError as error:
        raise HTTPException(status_code=404, detail=str(error))