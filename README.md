# EduGestión

EduGestión es una API para administrar solicitudes académicas y las entidades
relacionadas con ellas: estudiantes, áreas y responsables. El proyecto está
desarrollado con FastAPI, SQLModel y SQLite.

## Funcionalidades

- ABM (alta, baja, modificación y consulta) de estudiantes, áreas,
  responsables y solicitudes.
- Validación de datos de entrada mediante esquemas Pydantic.
- Validación de referencias: una solicitud debe pertenecer a un estudiante y
  un área existentes; el responsable, si se informa, también debe existir y
  pertenecer al área seleccionada.
- Documentación interactiva de la API generada por FastAPI.

## Tecnologías

- Python 3.11 (versión utilizada en las pruebas documentadas).
- FastAPI y Uvicorn.
- SQLModel/SQLAlchemy con SQLite.
- Pytest para las pruebas automatizadas.

Las versiones instalables se encuentran fijadas en `requirements.txt`.

## Instalación en Windows

Desde la carpeta raíz del proyecto, ejecutar en PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Si PowerShell no permite activar el entorno virtual, se puede invocar
directamente el ejecutable de `.venv\Scripts\python.exe` en los comandos
siguientes.

## Ejecución

```powershell
python -m uvicorn app.main:app --reload
```

La API queda disponible normalmente en `http://127.0.0.1:8000`.

- Documentación interactiva: `http://127.0.0.1:8000/docs`
- Documentación alternativa: `http://127.0.0.1:8000/redoc`
- Verificación de estado: `http://127.0.0.1:8000/health`

La aplicación crea las tablas al iniciar. Actualmente la URL de SQLite está
definida en `app/database/connection.py` como `sqlite:///./edugestion.db`, y
el registro SQL está habilitado con `echo=True`. Por lo tanto, la configuración
no se obtiene de variables de entorno todavía. La base local se crea en la
carpeta desde la que se inicia Uvicorn.

## Endpoints principales

| Recurso | Rutas |
|---|---|
| Estudiantes | `/estudiantes/` |
| Áreas | `/areas/` |
| Responsables | `/responsables/` |
| Solicitudes | `/solicitudes/` |

Cada recurso ofrece operaciones `GET` para listar y consultar por identificador,
`POST` para crear, `PUT` para actualizar y `DELETE` para eliminar. Consultar
`/docs` para ver los parámetros, esquemas y respuestas de cada operación.

La raíz `/` devuelve un mensaje de bienvenida y `/health` informa el estado
del servicio.

## Pruebas

Con el entorno virtual activo, ejecutar:

```powershell
python -m pytest tests/test_main.py -v
```

Las pruebas usan una base SQLite en memoria y reemplazan la dependencia de
sesión de la aplicación para mantener aislados los datos de prueba. Los
resultados pueden variar si cambia el conjunto de pruebas; ejecutar el comando
para obtener el resultado vigente.

## Estructura del proyecto

```text
app/
  core/          Constantes compartidas
  database/      Motor, sesiones y creación de tablas
  models/        Entidades persistidas
  repositories/  Acceso a datos
  routers/       Endpoints HTTP
  schemas/       Validación de entrada y salida
  services/      Reglas de negocio
tests/           Pruebas automatizadas
docs/            Diagnósticos y documentación de refactorizaciones
```

El flujo habitual de una operación es: **router → servicio → repositorio →
base de datos**. Los esquemas validan la información que entra y sale de la API.

## Calidad y mejoras identificadas

El diagnóstico y el checklist de revisión se encuentran en `docs/`. Entre las
mejoras ya reflejadas en el código están el uso de `lifespan` para el inicio de
FastAPI, la extracción de validaciones de estudiante, las búsquedas específicas
de email y matrícula de estudiantes, la agrupación de referencias de solicitudes
y la centralización de algunos valores predeterminados.

El code review también registra oportunidades pendientes: externalizar la
configuración de base de datos, uniformar el mapeo de errores HTTP, evitar
consultas completas para validar nombres de áreas y emails de responsables y
reducir la duplicación CRUD entre repositorios.