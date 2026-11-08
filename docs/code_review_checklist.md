# Code review - checklist

**Proyecto:** EduGestión  
**Fecha:** 07/11/2026  
**Alcance:** revisión del código actual enfocada en organización, validaciones,
persistencia, manejo de errores, refactorizaciones y pruebas.

**Criterio:** `[x]` cumple según el código revisado; `[ ]` es una mejora
pendiente. El feedback describe la evidencia observada y la acción correctiva
indica un siguiente paso concreto.

| Estado | Criterio | Feedback objetivo | Acción correctiva |
|---|---|---|---|
| [x] | El código está organizado por responsabilidades. | Routers, servicios, repositorios, esquemas y modelos están separados en paquetes. | Mantener el flujo router → servicio → repositorio y evitar agregar reglas de negocio a los routers. |
| [x] | Se extrajeron validaciones repetidas de estudiantes. | `validar_datos_unicos()` se usa tanto al crear como al actualizar estudiantes. | Mantener una única implementación de estas validaciones y conservar pruebas para creación y actualización. |
| [x] | Las búsquedas de email y matrícula de estudiantes son específicas. | El repositorio consulta por email o matrícula, sin listar todos los estudiantes. | Aplicar el mismo enfoque a las búsquedas de duplicados de áreas y responsables. |
| [x] | Las referencias de solicitud se agrupan en un objeto. | `SolicitudReferencias` reúne estudiante, área y responsable y se valida desde el servicio. | Reutilizar este objeto en futuras operaciones que requieran validar el conjunto de referencias. |
| [x] | Los valores predeterminados están centralizados. | Prioridad y estado inicial se definen en `app/core/constants.py`. | Usar esas constantes en nuevos esquemas y servicios; definir valores permitidos si el dominio lo requiere. |
| [x] | La inicialización usa el ciclo de vida de FastAPI. | `app/main.py` inicializa la base mediante `lifespan`. | Mantener la inicialización dentro de `lifespan` y evitar volver a `on_event("startup")`. |
| [x] | Hay pruebas para operaciones CRUD y algunas validaciones. | `tests/test_main.py` cubre los cuatro recursos y algunos casos negativos. | Ampliar la suite para verificar cada acción correctiva y ejecutar pytest antes de cerrar cambios. |
| [ ] | Los errores se convierten a respuestas HTTP coherentes. | Los routers capturan `ValueError` con códigos diferentes; por ejemplo, duplicados al actualizar estudiante responden `404`. | Definir excepciones diferenciadas para “no encontrado” y “duplicado”; mapearlas de forma uniforme y actualizar pruebas de códigos HTTP. |
| [ ] | Las validaciones de duplicados usan búsquedas específicas en todas las entidades. | Áreas y responsables recorren todos los registros para encontrar nombres o emails repetidos. | Agregar métodos de consulta específicos en sus repositorios y utilizarlos desde los servicios. |
| [ ] | La configuración de base de datos está fuera del código. | `DATABASE_URL` y `echo=True` están fijados en `app/database/connection.py`. | Leer URL y logging desde variables de entorno, conservar un valor local predeterminado y documentar cómo configurarlos. |
| [ ] | Se redujo la duplicación CRUD entre repositorios. | Los repositorios repiten patrones de alta, listado, actualización y borrado. | Evaluar una función o repositorio base para operaciones realmente comunes, manteniendo explícitas las consultas específicas; cubrirlo con pruebas. |
| [ ] | Los valores de tipo, prioridad y estado están restringidos. | Aunque hay constantes predeterminadas, los esquemas aceptan cadenas arbitrarias para estas categorías. | Acordar los valores válidos con el equipo y validarlos con enumeraciones o tipos restringidos en los esquemas/modelos. |

## Conclusión del review

El proyecto tiene una estructura clara y aplicó refactorizaciones concretas:
extracción de validaciones, consultas específicas para estudiantes, agrupación
de referencias, centralización de valores predeterminados y uso de `lifespan`.
Las acciones correctivas prioritarias son unificar el mapeo de errores HTTP y
evitar recorrer colecciones completas para validar duplicados. Luego pueden
abordarse la configuración, la duplicación CRUD y la restricción de categorías.

Las pruebas existentes verifican funcionalidades principales, pero conviene
agregar casos que aseguren los códigos HTTP deseados para duplicados y recursos
inexistentes. Los resultados deben presentarse con el comando de pruebas
ejecutado y no solo con cifras de informes anteriores.
