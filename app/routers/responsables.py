from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from app.core.exceptions import RecursoDuplicadoError, RecursoNoEncontradoError
from app.database.connection import get_session
from app.schemas.responsable import (
    ResponsableCreate,
    ResponsableResponse,
    ResponsableUpdate,
)
from app.services import responsable_service


router = APIRouter(
    prefix="/responsables",
    tags=["Responsables"]
)


@router.post(
    "/",
    response_model=ResponsableResponse,
    status_code=status.HTTP_201_CREATED
)
def crear_responsable(
    datos: ResponsableCreate,
    session: Annotated[Session, Depends(get_session)]
):
    try:
        return responsable_service.crear_responsable(session, datos)
    except RecursoDuplicadoError as error:
        raise HTTPException(status_code=409, detail=str(error))
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))


@router.get("/", response_model=list[ResponsableResponse])
def obtener_responsables(
    session: Annotated[Session, Depends(get_session)]
):
    return responsable_service.obtener_responsables(session)


@router.get("/{responsable_id}", response_model=ResponsableResponse)
def obtener_responsable(
    responsable_id: int,
    session: Annotated[Session, Depends(get_session)]
):
    try:
        return responsable_service.obtener_responsable_por_id(
            session,
            responsable_id
        )
    except RecursoNoEncontradoError as error:
        raise HTTPException(status_code=404, detail=str(error))


@router.put("/{responsable_id}", response_model=ResponsableResponse)
def actualizar_responsable(
    responsable_id: int,
    datos: ResponsableUpdate,
    session: Annotated[Session, Depends(get_session)]
):
    try:
        return responsable_service.actualizar_responsable(
            session,
            responsable_id,
            datos
        )
    except RecursoNoEncontradoError as error:
        raise HTTPException(status_code=404, detail=str(error))
    except RecursoDuplicadoError as error:
        raise HTTPException(status_code=409, detail=str(error))


@router.delete("/{responsable_id}")
def eliminar_responsable(
    responsable_id: int,
    session: Annotated[Session, Depends(get_session)]
):
    try:
        return responsable_service.eliminar_responsable(
            session,
            responsable_id
        )
    except RecursoNoEncontradoError as error:
        raise HTTPException(status_code=404, detail=str(error))