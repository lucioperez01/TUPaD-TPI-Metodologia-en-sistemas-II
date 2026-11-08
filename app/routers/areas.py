from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from app.database.connection import get_session
from app.schemas.area import AreaCreate, AreaResponse, AreaUpdate
from app.services import area_service


router = APIRouter(
    prefix="/areas",
    tags=["Áreas"]
)


@router.post(
    "/",
    response_model=AreaResponse,
    status_code=status.HTTP_201_CREATED
)
def crear_area(
    datos: AreaCreate,
    session: Session = Depends(get_session)
):
    try:
        return area_service.crear_area(session, datos)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))


@router.get("/", response_model=list[AreaResponse])
def obtener_areas(
    session: Session = Depends(get_session)
):
    return area_service.obtener_areas(session)


@router.get("/{area_id}", response_model=AreaResponse)
def obtener_area(
    area_id: int,
    session: Session = Depends(get_session)
):
    try:
        return area_service.obtener_area_por_id(session, area_id)
    except ValueError as error:
        raise HTTPException(status_code=404, detail=str(error))


@router.put("/{area_id}", response_model=AreaResponse)
def actualizar_area(
    area_id: int,
    datos: AreaUpdate,
    session: Session = Depends(get_session)
):
    try:
        return area_service.actualizar_area(session, area_id, datos)
    except ValueError as error:
        raise HTTPException(status_code=404, detail=str(error))


@router.delete("/{area_id}")
def eliminar_area(
    area_id: int,
    session: Session = Depends(get_session)
):
    try:
        return area_service.eliminar_area(session, area_id)
    except ValueError as error:
        raise HTTPException(status_code=404, detail=str(error))