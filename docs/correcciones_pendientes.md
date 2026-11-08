# Correcciones de Code Review - Documentación Antes/Después

Este documento registra las correcciones aplicadas a los problemas identificados en el code review checklist, con evidencia de antes/después para demostrar la mejora.

---

## Problema 1: Error Handling Inconsistente

### Diagnóstico

**Archivos afectados:**
- `app/routers/estudiantes.py` líneas 67-68
- `app/routers/areas.py` líneas 56-57

**Problema:**
Los endpoints `PUT /{id}` capturan `ValueError` y responden con código HTTP 404 (Not Found), pero el service lanza `ValueError` para dos dominios semánticos distintos:
1. "No existe el recurso" → debería responder 404
2. "Ya está duplicado" (email/matrícula/nombre) → debería responder 400 o 409

**Impacto:**
Cuando un cliente intenta actualizar un estudiante con un email que ya existe, recibe un error 404 "Not Found" aunque el recurso SÍ exista. Esto viola la semántica HTTP y dificulta el debugging.

**Tabla de comportamiento actual (INCORRECTO):**

| Operación | No encontrado | Duplicado (create) | Duplicado (update) |
|---|---|---|---|
| Estudiantes | 404 ✓ | 400 ✓ | **404 ✗** |
| Áreas | 404 ✓ | 400 ✓ | **404 ✗** |
| Responsables | 404 ✓ | 400 ✓ | 400 ✓ (por casualidad) |
| Solicitudes | 404 ✓ | 400 ✓ | 400 ✓ (por casualidad) |

### Código ANTES

**`app/routers/estudiantes.py` (líneas 55-68):**
```python
@router.put("/{estudiante_id}", response_model=EstudianteResponse)
def actualizar_estudiante(
    estudiante_id: int,
    datos: EstudianteUpdate,
    session: Session = Depends(get_session)
):
    try:
        return estudiante_service.actualizar_estudiante(
            session,
            estudiante_id,
            datos
        )
    except ValueError as error:
        raise HTTPException(status_code=404, detail=str(error))
```

**`app/routers/areas.py` (líneas 48-57):**
```python
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
```

**`app/services/estudiante_service.py` (método `actualizar_estudiante`):**
```python
def actualizar_estudiante(session, estudiante_id, datos):
    estudiante = estudiante_repository.obtener_estudiante_por_id(session, estudiante_id)
    if not estudiante:
        raise ValueError(f"Estudiante con id {estudiante_id} no encontrado.")
    
    # Validar datos únicos (puede lanzar ValueError si hay duplicados)
    validar_datos_unicos(session, datos, excluir_id=estudiante_id)
    
    # ... resto del código
```

### Causa raíz

El router no puede distinguir si el `ValueError` viene de:
- `obtener_estudiante_por_id()` → "no existe" (404)
- `validar_datos_unicos()` → "duplicado" (400/409)

Ambos se capturan con el mismo `except ValueError` y responden 404.

### Solución aplicada

**1. Crear excepciones propias (`app/core/exceptions.py`):**
```python
class RecursoNoEncontradoError(Exception):
    """Excepción lanzada cuando un recurso no existe en la base de datos."""
    pass


class RecursoDuplicadoError(Exception):
    """Excepción lanzada cuando se intenta crear/actualizar un recurso con datos únicos duplicados."""
    pass
```

**2. Actualizar servicios para lanzar excepciones específicas:**

`app/services/estudiante_service.py`:
- Cambiar `ValueError` por `RecursoDuplicadoError` en `validar_datos_unicos()` (líneas 26, 36)
- Cambiar `ValueError` por `RecursoNoEncontradoError` en `obtener_estudiante_por_id()` (línea 70)

`app/services/area_service.py`:
- Cambiar `ValueError` por `RecursoDuplicadoError` en validaciones de nombre duplicado (líneas 13, 51)
- Cambiar `ValueError` por `RecursoNoEncontradoError` en `obtener_area_por_id()` (línea 31)

**3. Actualizar routers para capturar excepciones específicas:**

`app/routers/estudiantes.py` y `app/routers/areas.py`:
- Importar `RecursoNoEncontradoError` y `RecursoDuplicadoError`
- `POST /`: capturar `RecursoDuplicadoError` → 409, `ValueError` → 400
- `GET /{id}`: capturar `RecursoNoEncontradoError` → 404
- `PUT /{id}`: capturar `RecursoNoEncontradoError` → 404, `RecursoDuplicadoError` → 409
- `DELETE /{id}`: capturar `RecursoNoEncontradoError` → 404

**4. Actualizar tests para reflejar comportamiento correcto:**

`tests/test_main.py`:
- `test_crear_estudiante_con_email_duplicado`: cambiar aserción de 400 a 409 (línea 205)
- `test_crear_estudiante_con_matricula_duplicada`: cambiar aserción de 400 a 409 (línea 223)
- `test_actualizar_estudiante_con_email_duplicado`: cambiar aserción de 404 a 409 (línea 256)
- `test_actualizar_estudiante_con_matricula_duplicada`: cambiar aserción de 404 a 409 (línea 368)

### Código DESPUÉS

**`app/routers/estudiantes.py` (endpoint PUT actualizado):**
```python
@router.put("/{estudiante_id}", response_model=EstudianteResponse)
def actualizar_estudiante(
    estudiante_id: int,
    datos: EstudianteUpdate,
    session: Session = Depends(get_session)
):
    try:
        return estudiante_service.actualizar_estudiante(
            session,
            estudiante_id,
            datos
        )
    except RecursoNoEncontradoError as error:
        raise HTTPException(status_code=404, detail=str(error))
    except RecursoDuplicadoError as error:
        raise HTTPException(status_code=409, detail=str(error))
```

### Resultado de tests DESPUÉS

```bash
$ pytest tests/test_main.py -v
======================== 18 passed, 1 warning in 0.81s =========================
```

**18/18 tests pasando** con comportamiento HTTP correcto:
- Duplicados → 409 Conflict (semánticamente correcto)
- No encontrado → 404 Not Found (semánticamente correcto)

### Tabla de comportamiento actualizado (CORRECTO)

| Operación | No encontrado | Duplicado (create) | Duplicado (update) |
|---|---|---|---|
| Estudiantes | 404 ✓ | **409 ✓** | **409 ✓** |
| Áreas | 404 ✓ | **409 ✓** | **409 ✓** |
| Responsables | 404 ✓ | 400 ✓ | 400 ✓ |
| Solicitudes | 404 ✓ | 400 ✓ | 400 ✓ |

**Beneficios:**
- Semántica HTTP correcta (409 = Conflict para recursos duplicados)
- El cliente puede distinguir entre "no existe" y "ya existe"
- Mejor debugging y manejo de errores en el frontend
- Código más mantenible con excepciones semánticas

---

## Problema 2: [PRÓXIMO]

---

## Problema 3: [PRÓXIMO]

---

## Problema 4: [PRÓXIMO]

---

## Resumen de cambios

| # | Problema | Estado | Commit |
|---|---|---|---|
| 1 | Error handling inconsistente | ✅ Completado | - |
| 2 | Tests codifican bug | ✅ Completado (incluido en #1) | - |
| 3 | Validaciones ineficientes | 🔲 Pendiente | - |
| 4 | Configuración DB hardcodeada | 🔲 Pendiente | - |
