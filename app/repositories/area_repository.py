from sqlmodel import Session, select

from app.models import Area


def crear_area(session: Session, area: Area):
    session.add(area)
    session.commit()
    session.refresh(area)
    return area


def obtener_areas(session: Session):
    sentencia = select(Area)
    return session.exec(sentencia).all()


def obtener_area_por_id(session: Session, area_id: int):
    return session.get(Area, area_id)


def obtener_area_por_nombre(session: Session, nombre: str, excluir_id: int | None = None):
    sentencia = select(Area).where(Area.nombre == nombre)
    
    if excluir_id is not None:
        sentencia = sentencia.where(Area.id != excluir_id)
    
    return session.exec(sentencia).first()


def actualizar_area(
    session: Session,
    area: Area,
    nuevos_datos: dict
):
    for campo, valor in nuevos_datos.items():
        setattr(area, campo, valor)

    session.add(area)
    session.commit()
    session.refresh(area)
    return area


def eliminar_area(session: Session, area: Area):
    session.delete(area)
    session.commit()