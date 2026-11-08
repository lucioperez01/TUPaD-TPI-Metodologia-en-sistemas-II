# Informe Técnico - EduGestión
## Evolución profesional de un sistema existente: calidad, deuda técnica, refactoring y revisión técnica

---

# 1. Portada

**Materia:** Metodología de Sistemas II  
**Comisión:** [Comisión]  
**Título del trabajo:** EduGestión - Análisis y mejora de calidad de software  
**Integrantes:**
- [Integrante 1]
- [Integrante 2]  
- [Integrante 3]
- [Integrante 4]

**Fecha:** Noviembre 2026  
**Repositorio:** [URL del repositorio GitHub]  
**Video de defensa:** [URL del video]

---

# 2. Resumen Ejecutivo

EduGestión es una API REST desarrollada en Python con FastAPI para administrar solicitudes académicas y sus entidades relacionadas (estudiantes, áreas, responsables). El proyecto presentaba una arquitectura funcional pero con problemas de calidad interna: manejo inconsistente de errores HTTP, validaciones ineficientes que cargaban todos los registros en memoria, configuración hardcodeada y código duplicado.

Se realizó un diagnóstico exhaustivo identificando 8 code smells principales, aplicando principios SOLID y Clean Code. Se ejecutaron 5 refactorizaciones documentadas (Extract Method, Move Method, Introduce Parameter Object, Consolidate Duplicate Values, y migración a lifespan) más 4 correcciones críticas adicionales (error handling con excepciones propias, validaciones O(1) con queries SQL específicas, configuración externa con python-dotenv, y tests actualizados).

Los resultados muestran mejora del 200% en cobertura de tests (de 6 a 18), reducción de complejidad algorítmica de O(n) a O(1) en validaciones, semántica HTTP correcta (409 para duplicados, 404 para no encontrados), y configuración flexible siguiendo Twelve-Factor App. El comportamiento externo se mantuvo sin regresiones, verificando la calidad del refactoring seguro aplicado.

**Palabras clave:** refactoring, code smells, SOLID, Clean Code, calidad de software, deuda técnica, pruebas automatizadas.

---

# 3. Descripción del Sistema Base

## 3.1 Dominio y Alcance

EduGestión es un sistema de gestión de solicitudes académicas que permite:

- **Gestión de estudiantes:** alta, baja, modificación y consulta con validación de email y matrícula únicos
- **Gestión de áreas administrativas:** ABM con validación de nombres únicos
- **Gestión de responsables:** ABM con validación de email único y asociación a áreas
- **Gestión de solicitudes:** registro con clasificación por tipo, prioridad y estado, asignación de responsable

## 3.2 Actores y Casos de Uso

**Actores:**
- Estudiantes (inician solicitudes)
- Responsables de área (gestionan solicitudes)
- Administradores del sistema

**Casos de uso principales:**
1. Registrar nueva solicitud académica
2. Cambiar estado de solicitud (Pendiente → En Proceso → Resuelta/Rechazada)
3. Asignar responsable a una solicitud
4. Buscar y filtrar solicitudes por diversos criterios
5. Listar reportes básicos de solicitudes

## 3.3 Entidades Principales

| Entidad | Atributos | Relaciones |
|---------|-----------|------------|
| **Estudiante** | id, nombre, apellido, email (único), matrícula (única) | Inicia solicitudes |
| **Área** | id, nombre (único), descripción, activa | Tiene responsables |
| **Responsable** | id, nombre, apellido, email (único), FK a Área | Gestiona solicitudes |
| **Solicitud** | id, título, descripción, tipo, prioridad, estado, fecha_creación | FK a Estudiante, Área, Responsable |

## 3.4 Tecnologías Utilizadas

| Capa | Tecnología | Versión |
|------|------------|---------|
| Lenguaje | Python | 3.11 |
| Framework web | FastAPI | 0.162.0 |
| Servidor HTTP | Uvicorn | 0.54.0 |
| ORM / Modelado | SQLModel (sobre SQLAlchemy 2.1.8) | 0.0.48 |
| Validación | Pydantic v2 | 2.14.3 |
| Base de datos | SQLite | - |
| Testing | Pytest + httpx TestClient | 9.2.0 |

## 3.5 Arquitectura del Sistema

El sistema sigue un patrón de 3 capas con separación de responsabilidades:

```
Router (HTTP) → Service (lógica de negocio) → Repository (acceso a datos) → DB
```

**Estructura de directorios:**
```
app/
├── main.py                 # Punto de entrada FastAPI + lifespan
├── core/
│   └── constants.py        # Constantes globales
├── database/
│   └── connection.py       # Engine, sesiones, create_all
├── models/
│   └── entities.py         # 4 modelos SQLModel
├── repositories/           # Acceso a datos (1 por entidad)
├── routers/                # Endpoints HTTP (1 por recurso)
├── schemas/                # DTOs Pydantic (Create/Update/Response)
└── services/               # Reglas de negocio (1 por entidad)
```

## 3.6 Estado Inicial del Sistema

El sistema base funcionaba correctamente desde el punto de vista del usuario (calidad externa), pero presentaba múltiples problemas de calidad interna que serán detallados en las siguientes secciones.

**Enlace al tag `estado-inicial`:** commit 346d558

---

# 4. Calidad Externa vs. Calidad Interna

## 4.1 Calidad Externa (Perspectiva del Usuario)

Desde la perspectiva del usuario, el sistema **funcionaba correctamente**:

- ✅ Todos los endpoints respondían según lo esperado
- ✅ Las validaciones de datos se ejecutaban
- ✅ Las operaciones CRUD completaban exitosamente
- ✅ Los datos se persistían correctamente
- ✅ La documentación interactiva estaba disponible en `/docs`

**Evidencia:** 6/6 tests iniciales pasando (ver sección 8.1)

## 4.2 Calidad Interna (Perspectiva del Desarrollador)

Sin embargo, al analizar la estructura interna del código, se identificaron **múltiples problemas de calidad**:

### Problemas de Mantenibilidad
- **Código duplicado:** operaciones CRUD repetidas en 4 repositorios
- **Validaciones repetidas:** lógica de duplicados copiada en servicios
- **Nombres inconsistentes:** diferentes criterios de normalización (lowercase solo en algunos lados)

### Problemas de Performance
- **Acceso ineficiente a datos:** `SELECT * FROM area` para validar un nombre (O(n) en memoria)
- **Carga innecesaria:** traer 100.000 registros solo para verificar si uno existe

### Problemas de Configuración
- **Hardcoded values:** URL de DB y `echo=True` fijos en el código
- **Falta de flexibilidad:** imposible cambiar entre entornos (dev/test/prod)

### Problemas de Arquitectura
- **Error handling inconsistente:** `ValueError` para todo, sin diferenciar "no encontrado" vs "duplicado"
- **Excepciones genéricas:** el router no puede distinguir el tipo de error
- **Falta de abstracciones:** dependencias directas entre servicios y repositorios concretos

## 4.3 Relación entre Calidad Externa e Interna

| Aspecto | Calidad Externa | Calidad Interna |
|---------|-----------------|-----------------|
| **Funcionalidad** | ✅ Correcta | ✅ Correcta |
| **Mantenibilidad** | No visible | ❌ Baja (código duplicado) |
| **Performance** | Aceptable con pocos datos | ❌ Escalabilidad pobre |
| **Legibilidad** | No evaluable | ⚠️ Parcial (nombres buenos, estructura mejorable) |
| **Evolución futura** | No evaluable | ❌ Difícil (configuración rígida, sin tests) |

**Conclusión:** La calidad externa era aceptable, pero la calidad interna condicionaba fuertemente el costo del cambio y la vida útil del software. Un sistema con buena calidad externa pero mala calidad interna es como un iceberg: lo que se ve funciona, pero lo que no se ve puede hundir el proyecto.

---
