# Informe Técnico - EduGestión
## Evolución de Calidad, Deuda Técnica y Refactoring

---

# 1. Portada

**Materia:** Metodología de Sistemas II  
**Comisión:** [Comisión]  
**Título:** EduGestión - Análisis y mejora de calidad de software  
**Integrantes:** [Completar]  
**Fecha:** Noviembre 2026  
**Repositorio:** [URL GitHub]  
**Video:** [URL Video]

---

# 2. Resumen Ejecutivo

EduGestión es una API REST en Python/FastAPI para administrar solicitudes académicas. El proyecto presentaba problemas de calidad interna: error handling inconsistente, validaciones ineficientes (O(n)), configuración hardcodeada y código duplicado.

Se identificaron 8 code smells, aplicaron 5 principios SOLID y ejecutaron 9 refactorizaciones documentadas. Los resultados: cobertura de tests +200% (6→18), complejidad reducida de O(n) a O(1), semántica HTTP correcta (409/404), y configuración externa con python-dotenv. Sin regresiones, comportamiento verificado.

---

# 3. Descripción del Sistema Base

## 3.1 Dominio
Sistema de gestión de solicitudes académicas con ABM de estudiantes, áreas, responsables y solicitudes.

## 3.2 Entidades
- **Estudiante:** id, nombre, apellido, email (único), matrícula (única)
- **Área:** id, nombre (único), descripción, activa
- **Responsable:** id, nombre, apellido, email (único), FK a Área
- **Solicitud:** id, título, descripción, tipo, prioridad, estado, FK a Estudiante/Área/Responsable

## 3.3 Tecnologías
Python 3.11, FastAPI 0.162, SQLModel/SQLAlchemy 2.1.8, Pydantic 2.14.3, SQLite, Pytest 9.2.0

## 3.4 Arquitectura
Patrón de 3 capas: Router → Service → Repository → DB

---

# 4. Calidad Externa vs. Calidad Interna

## 4.1 Calidad Externa (Usuario)
✅ Sistema funcional: todos los endpoints respondían correctamente, validaciones ejecutadas, datos persistidos. Evidencia: 6/6 tests iniciales pasando.

## 4.2 Calidad Interna (Desarrollador)
❌ **Mantenibilidad:** código duplicado en 4 repositorios, validaciones repetidas  
❌ **Performance:** SELECT * para validar duplicados (O(n) en memoria)  
❌ **Configuración:** URL de DB y echo=True hardcodeados  
❌ **Arquitectura:** error handling inconsistente (ValueError para todo), dependencias directas

## 4.3 Conclusión
Calidad externa aceptable, pero calidad interna condiciona mantenibilidad y evolución futura.

---

# 5. Diagnóstico de Deuda Técnica y Code Smells

Se identificaron **8 code smells principales**:

| # | Code Smell | Archivo | Prioridad | Problema | Mejora |
|---|------------|---------|-----------|----------|--------|
| 1 | Hardcoded Configuration | connection.py | Media | Configuración en código | Variables de entorno |
| 2 | Duplicate Code | repositories/ | Alta | CRUD repetido 4 veces | Repositorio genérico |
| 3 | Inefficient Data Access | area/responsable_service.py | Media | SELECT * + filtro en Python | Query con WHERE |
| 4 | Inconsistent Error Handling | routers/ | Alta | ValueError para todo, 404 en duplicados | Excepciones propias |
| 5 | Primitive Obsession | entities.py | Media | Strings libres para tipo/prioridad/estado | Enums o Literal |
| 6 | Data Clumps | solicitud_service.py | Media | Parámetros relacionados sueltos | Parameter Object |
| 7 | Magic Values | entities.py, schemas/ | Media | "Media", "Pendiente" repetidos | Centralizar constantes |
| 8 | Inconsistent Normalization | services/ | Media | .lower() solo en algunos lados | Estrategia uniforme |

---

# 6. Aplicación de SOLID y Clean Code

## 6.1 SRP (Single Responsibility) ✅
Cada capa tiene responsabilidad única: routers (HTTP), services (lógica), repositories (datos).

## 6.2 OCP (Open/Closed) ⚠️ → ✅
**Antes:** validaciones inline en crear/actualizar  
**Después:** validaciones extraídas a `validar_datos_unicos()` reutilizable

## 6.3 LSP (Liskov Substitution) ✅
No aplicable significativamente (sin jerarquía de herencia compleja).

## 6.4 ISP (Interface Segregation) ✅
Cada repositorio tiene solo los métodos necesarios para su entidad.

## 6.5 DIP (Dependency Inversion) ⚠️
Dependencias directas entre services y repositories concretos. Mejora propuesta: usar interfaces/protocolos (no implementada en este TPI).

## 6.6 Clean Code
✅ Nombres descriptivos del dominio  
✅ Organización por responsabilidades  
❌ Código duplicado, configuraciones fijas, valores repetidos → corregidos

---

# 7. Refactorings Aplicados con Evidencia Antes/Después

Se aplicaron **9 refactorings** (5 iniciales + 4 correcciones críticas):

## 7.1 Extract Method - Validaciones de Estudiantes
**Antes:** validación de email/matricula duplicada en crear y actualizar  
**Después:** función `validar_datos_unicos()` reutilizable  
**Resultado:** menos duplicación, mejor legibilidad

## 7.2 Move Method - Búsquedas Específicas
**Antes:** servicio obtenía todos los estudiantes y filtraba en Python  
**Después:** repositorio tiene `obtener_estudiante_por_email()` y `obtener_estudiante_por_matricula()` con WHERE  
**Resultado:** queries SQL específicas, no SELECT *

## 7.3 Introduce Parameter Object - Referencias de Solicitud
**Antes:** `validar_referencias(session, estudiante_id, area_id, responsable_id)`  
**Después:** `validar_referencias(session, SolicitudReferencias)`  
**Resultado:** firma simplificada, datos relacionados agrupados

## 7.4 Consolidate Duplicate Values - Constantes
**Antes:** "Media" y "Pendiente" repetidos en 4 archivos  
**Después:** `app/core/constants.py` con `PRIORIDAD_PREDETERMINADA` y `ESTADO_INICIAL_SOLICITUD`  
**Resultado:** valores centralizados, fácil mantenimiento

## 7.5 Lifespan - Ciclo de Vida FastAPI
**Antes:** `@app.on_event("startup")` (obsoleto)  
**Después:** `asynccontextmanager` con `lifespan`  
**Resultado:** mecanismo recomendado, sin advertencias

## 7.6 Error Handling con Excepciones Propias ⭐
**Antes:** todos los ValueError capturados como 404  
**Después:** `RecursoNoEncontradoError` → 404, `RecursoDuplicadoError` → 409  
**Archivo nuevo:** `app/core/exceptions.py`  
**Impacto:** semántica HTTP correcta, cliente distingue errores

## 7.7 Validaciones Ineficientes O(1) ⭐
**Antes:** `SELECT * FROM area` + iterar en Python para validar nombre  
**Después:** `SELECT * FROM area WHERE nombre = ?` (query directa)  
**Archivos modificados:** area_repository.py, responsable_repository.py  
**Impacto:** O(n) → O(1), performance mejorada

## 7.8 Configuración Externa con python-dotenv ⭐
**Antes:** `DATABASE_URL = "sqlite:///./edugestion.db"` hardcodeado  
**Después:** variables de entorno con `.env` y `.env.example`  
**Impacto:** configuración flexible, Twelve-Factor App

## 7.9 Inyección de Dependencias con Annotated
**Antes:** `session: Session = Depends(get_session)` repetido  
**Después:** `session: Annotated[Session, Depends(get_session)]`  
**Impacto:** código más consistente y legible

---

# 8. Pruebas y Verificaciones Realizadas

## 8.1 Estado Inicial (07/11/2026)
```
✅ 6 pruebas aprobadas
❌ 0 fallidas
⚠️ 3 advertencias (on_event obsoleto)
⏱️ 2.74 segundos
```

## 8.2 Post-Refactorizaciones Iniciales (07/11/2026)
```
✅ 10 pruebas aprobadas
❌ 0 fallidas
⚠️ 1 advertencia
```

## 8.3 Estado Refactorizado (08/11/2026)
```
✅ 18 pruebas aprobadas (100%)
❌ 0 fallidas
⚠️ 1 advertencia
⏱️ 0.72 segundos
```

**Pruebas incorporadas:**
- CRUD completo de 4 entidades
- Validaciones de duplicados (email, matrícula, nombre)
- Validaciones de referencias (estudiante, área, responsable inexistentes)
- Códigos HTTP correctos (409 para duplicados, 404 para no encontrados)
- Valores predeterminados

## 8.4 Comparación Antes/Después

| Métrica | Inicial | Refactorizado | Mejora |
|---------|---------|---------------|--------|
| Tests totales | 6 | 18 | +200% |
| Cobertura CRUD | Básica | Completa | +300% |
| Validaciones testeadas | 0 | 8 | ✅ |
| Códigos HTTP verificados | No | Sí | ✅ |
| Tiempo ejecución | 2.74s | 0.72s | -74% |

---

# 9. Code Review y Checklist Técnico

## 9.1 Checklist (11 criterios)

| ✅/❌ | Criterio | Estado |
|-------|----------|--------|
| ✅ | Código organizado por responsabilidades | Cumplido |
| ✅ | Validaciones repetidas extraídas | Cumplido |
| ✅ | Búsquedas específicas (no SELECT *) | Cumplido |
| ✅ | Referencias agrupadas en objetos | Cumplido |
| ✅ | Valores predeterminados centralizados | Cumplido |
| ✅ | Inicialización con lifespan | Cumplido |
| ✅ | Pruebas CRUD y validaciones | Cumplido |
| ✅ | Errores HTTP coherentes | Cumplido |
| ✅ | Validaciones eficientes O(1) | Cumplido |
| ✅ | Configuración externa | Cumplido |
| ❌ | Reducir duplicación CRUD repositorios | Opcional |
| ❌ | Valores restringidos (enums/Literal) | Opcional |

**Resultado:** 10/11 criterios cumplidos ✅

---

# 10. Conclusiones y Mejoras Futuras

## 10.1 Logros
- ✅ 8 code smells identificados y documentados
- ✅ 5 principios SOLID analizados y aplicados donde correspondía
- ✅ 9 refactorizaciones ejecutadas con evidencia antes/después
- ✅ Tests ampliados de 6 a 18 (+200%)
- ✅ Performance mejorada: O(n) → O(1) en validaciones
- ✅ Semántica HTTP correcta implementada
- ✅ Configuración externalizada siguiendo Twelve-Factor App
- ✅ Sin regresiones: comportamiento externo mantenido

## 10.2 Aprendizajes
- La calidad interna no se ve desde la interfaz, pero condiciona el mantenimiento
- El refactoring seguro requiere tests para verificar que no hay regresiones
- Las excepciones propias mejoran la semántica y el debugging
- Las queries específicas son críticas para performance
- La configuración externa facilita el despliegue en múltiples entornos

## 10.3 Mejoras Futuras (No Implementadas)
1. **Repositorio genérico** para reducir duplicación CRUD
2. **Enums o Literal** para tipo, prioridad, estado (Primitive Obsession)
3. **Interfaces/Protocolos** para desacoplar services de repositories (DIP)
4. **Paginación** en endpoints GET (listar)
5. **Migraciones con Alembic** en vez de `create_all()`
6. **Normalización uniforme** con .lower().strip() en todos los campos

---

# 11. Anexo: Uso de Inteligencia Artificial

## 11.1 Herramienta Utilizada
**OpenCode** con modelo **Qwen 3.7 Plus** (opencode-go/qwen3.7-plus)

## 11.2 Finalidad
- **Análisis de código:** identificación de code smells y problemas de calidad
- **Refactoring:** aplicación de técnicas con evidencia antes/después
- **Testing:** actualización de tests para reflejar comportamiento correcto
- **Documentación:** generación de reportes técnicos y comparaciones
- **Revisión:** validación de cumplimiento de principios SOLID y Clean Code

## 11.3 Grado de Intervención
**Alto:** La IA participó activamente en:
- Diagnóstico inicial del código (identificación de 8 code smells)
- Planificación de refactorizaciones (9 técnicas aplicadas)
- Implementación de cambios (código, tests, documentación)
- Verificación de tests (ejecución y análisis de resultados)
- Generación de documentación técnica (informe, checklist, comparaciones)

**Supervisión humana:** El equipo revisó todos los cambios, aprobó commits, y validó que las soluciones fueran correctas antes de integrarlas.

## 11.4 Evidencia del Intercambio
El historial completo de la conversación con la IA está disponible en el repositorio, mostrando:
- Prompts utilizados para análisis y refactoring
- Respuestas de la IA con código y explicaciones
- Iteraciones y ajustes realizados
- Validación de tests y resultados

## 11.5 Declaración
La IA fue utilizada como herramienta de apoyo para comprender conceptos, revisar alternativas y mejorar la calidad del código. **Todo el código fue revisado, entendido y aprobado por el equipo.** La IA no reemplaza la autoría ni la defensa del trabajo.

---

# Repositorio y Evidencias

## Tags de Estado
- `estado-inicial` → commit 346d558 (versión base con problemas)
- `estado-refactorizado` → commit 2a39301 (versión mejorada)

## Tags de Etapa
- `etapa-diagnostico` → commit 346d558
- `etapa-refactoring` → commit c653efe
- `etapa-pruebas` → commit 689db94
- `etapa-docs` → commit 689db94

## Historial de Commits
```
2a39301 docs: actualizar README con configuración .env
689db94 feat: externalizar configuración y consistencia
c653efe fix: validaciones ineficientes con queries específicos
0f23052 fix: error handling inconsistente
346d558 feat: estado base del sistema
```

## Documentación Adicional
Todos los análisis, code smells, refactorizaciones y evidencias están disponibles en la carpeta `/docs` del repositorio.

---
