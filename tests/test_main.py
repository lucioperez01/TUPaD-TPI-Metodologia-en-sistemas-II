
def test_inicio(client):
    respuesta = client.get("/")
    assert respuesta.status_code == 200
    assert respuesta.json()["mensaje"] == "Bienvenido a EduGestión"


def test_verificar_estado(client):
    respuesta = client.get("/health")
    assert respuesta.status_code == 200
    assert respuesta.json()["estado"] == "activo"


def test_listar_estudiantes(client):
    respuesta = client.get("/estudiantes/")
    assert respuesta.status_code == 200
    assert isinstance(respuesta.json(), list)


def test_listar_areas(client):
    respuesta = client.get("/areas/")
    assert respuesta.status_code == 200
    assert isinstance(respuesta.json(), list)


def test_listar_responsables(client):
    respuesta = client.get("/responsables/")
    assert respuesta.status_code == 200
    assert isinstance(respuesta.json(), list)


def test_listar_solicitudes(client):
    respuesta = client.get("/solicitudes/")
    assert respuesta.status_code == 200
    assert isinstance(respuesta.json(), list)


def test_crud_estudiantes(client):
    datos = {
        "nombre": "Juan",
        "apellido": "Perez",
        "email": "juan.perez@test.com",
        "matricula": "EST001"
    }

    crear = client.post("/estudiantes/", json=datos)
    assert crear.status_code == 201
    estudiante_id = crear.json()["id"]

    consultar = client.get(f"/estudiantes/{estudiante_id}")
    assert consultar.status_code == 200
    assert consultar.json()["nombre"] == "Juan"

    actualizar = client.put(
        f"/estudiantes/{estudiante_id}",
        json={"nombre": "Juan Carlos"}
    )
    assert actualizar.status_code == 200
    assert actualizar.json()["nombre"] == "Juan Carlos"

    eliminar = client.delete(f"/estudiantes/{estudiante_id}")
    assert eliminar.status_code == 200

    verificar = client.get(f"/estudiantes/{estudiante_id}")
    assert verificar.status_code == 404


def test_crud_areas(client):
    datos = {
        "nombre": "Secretaria de Prueba",
        "descripcion": "Area utilizada para pruebas"
    }

    crear = client.post("/areas/", json=datos)
    assert crear.status_code == 201
    area_id = crear.json()["id"]

    consultar = client.get(f"/areas/{area_id}")
    assert consultar.status_code == 200

    actualizar = client.put(
        f"/areas/{area_id}",
        json={"nombre": "Secretaria Actualizada"}
    )
    assert actualizar.status_code == 200
    assert actualizar.json()["nombre"] == "Secretaria Actualizada"

    eliminar = client.delete(f"/areas/{area_id}")
    assert eliminar.status_code == 200

    verificar = client.get(f"/areas/{area_id}")
    assert verificar.status_code == 404


def test_crud_responsables(client):
    area = client.post(
        "/areas/",
        json={
            "nombre": "Area para Responsable",
            "descripcion": "Area de prueba"
        }
    )
    assert area.status_code == 201
    area_id = area.json()["id"]

    datos = {
        "nombre": "Maria",
        "apellido": "Gonzalez",
        "email": "maria.prueba@test.com",
        "area_id": area_id
    }

    crear = client.post("/responsables/", json=datos)
    assert crear.status_code == 201
    responsable_id = crear.json()["id"]

    consultar = client.get(f"/responsables/{responsable_id}")
    assert consultar.status_code == 200

    actualizar = client.put(
        f"/responsables/{responsable_id}",
        json={"nombre": "Maria Elena"}
    )
    assert actualizar.status_code == 200
    assert actualizar.json()["nombre"] == "Maria Elena"

    eliminar = client.delete(f"/responsables/{responsable_id}")
    assert eliminar.status_code == 200

    verificar = client.get(f"/responsables/{responsable_id}")
    assert verificar.status_code == 404


def test_crud_solicitudes(client):
    estudiante = client.post(
        "/estudiantes/",
        json={
            "nombre": "Pedro",
            "apellido": "Lopez",
            "email": "pedro.prueba@test.com",
            "matricula": "EST002"
        }
    )
    assert estudiante.status_code == 201
    estudiante_id = estudiante.json()["id"]

    area = client.post(
        "/areas/",
        json={
            "nombre": "Area de Solicitudes",
            "descripcion": "Area para pruebas"
        }
    )
    assert area.status_code == 201
    area_id = area.json()["id"]

    datos = {
        "titulo": "Solicitud de prueba",
        "descripcion": "Descripcion de la solicitud de prueba",
        "tipo": "Academica",
        "prioridad": "Media",
        "estudiante_id": estudiante_id,
        "area_id": area_id
    }

    crear = client.post("/solicitudes/", json=datos)
    assert crear.status_code == 201
    solicitud_id = crear.json()["id"]

    consultar = client.get(f"/solicitudes/{solicitud_id}")
    assert consultar.status_code == 200

    actualizar = client.put(
        f"/solicitudes/{solicitud_id}",
        json={"titulo": "Solicitud actualizada"}
    )
    assert actualizar.status_code == 200
    assert actualizar.json()["titulo"] == "Solicitud actualizada"

    eliminar = client.delete(f"/solicitudes/{solicitud_id}")
    assert eliminar.status_code == 200

    verificar = client.get(f"/solicitudes/{solicitud_id}")
    assert verificar.status_code == 404


# PRUEBAS ADICIONALES DE VALIDACIONES Y REFACTORIZACIONES


def test_crear_estudiante_con_email_duplicado(client):
    datos = {
        "nombre": "Juan",
        "apellido": "Perez",
        "email": "duplicado@test.com",
        "matricula": "EST100"
    }

    primera = client.post("/estudiantes/", json=datos)
    segunda = client.post(
        "/estudiantes/",
        json={**datos, "matricula": "EST101"}
    )

    assert primera.status_code == 201
    assert segunda.status_code == 409


def test_crear_estudiante_con_matricula_duplicada(client):
    datos = {
        "nombre": "Juan",
        "apellido": "Perez",
        "email": "juan1@test.com",
        "matricula": "EST200"
    }

    primera = client.post("/estudiantes/", json=datos)
    segunda = client.post(
        "/estudiantes/",
        json={**datos, "email": "juan2@test.com"}
    )

    assert primera.status_code == 201
    assert segunda.status_code == 409


def test_actualizar_estudiante_con_email_duplicado(client):
    primero = client.post(
        "/estudiantes/",
        json={
            "nombre": "Juan",
            "apellido": "Perez",
            "email": "juan3@test.com",
            "matricula": "EST300"
        }
    )

    segundo = client.post(
        "/estudiantes/",
        json={
            "nombre": "Maria",
            "apellido": "Lopez",
            "email": "maria3@test.com",
            "matricula": "EST301"
        }
    )

    segundo_id = segundo.json()["id"]

    respuesta = client.put(
        f"/estudiantes/{segundo_id}",
        json={"email": "juan3@test.com"}
    )

    assert primero.status_code == 201
    assert segundo.status_code == 201
    assert respuesta.status_code == 409


def test_crear_solicitud_con_estudiante_inexistente(client):
    area = client.post(
        "/areas/",
        json={"nombre": "Area Test Referencia"}
    )

    respuesta = client.post(
        "/solicitudes/",
        json={
            "titulo": "Solicitud de prueba",
            "descripcion": "Descripcion de prueba",
            "tipo": "Academica",
            "estudiante_id": 9999,
            "area_id": area.json()["id"]
        }
    )

    assert area.status_code == 201
    assert respuesta.status_code == 400


def test_crear_solicitud_con_area_inexistente(client):
    estudiante = client.post(
        "/estudiantes/",
        json={
            "nombre": "Pedro",
            "apellido": "Lopez",
            "email": "pedro999@test.com",
            "matricula": "EST999"
        }
    )

    respuesta = client.post(
        "/solicitudes/",
        json={
            "titulo": "Solicitud de prueba",
            "descripcion": "Descripcion de prueba",
            "tipo": "Academica",
            "estudiante_id": estudiante.json()["id"],
            "area_id": 9999
        }
    )

    assert estudiante.status_code == 201
    assert respuesta.status_code == 400


def test_valores_predeterminados_solicitud(client):
    estudiante = client.post(
        "/estudiantes/",
        json={
            "nombre": "Carlos",
            "apellido": "Gomez",
            "email": "carlos999@test.com",
            "matricula": "EST998"
        }
    )

    area = client.post(
        "/areas/",
        json={"nombre": "Area Valores Predeterminados"}
    )

    respuesta = client.post(
        "/solicitudes/",
        json={
            "titulo": "Solicitud predeterminada",
            "descripcion": "Comprobacion de valores predeterminados",
            "tipo": "Academica",
            "estudiante_id": estudiante.json()["id"],
            "area_id": area.json()["id"]
        }
    )

    assert respuesta.status_code == 201
    assert respuesta.json()["prioridad"] == "Media"
    assert respuesta.json()["estado"] == "Pendiente"


def test_actualizar_estudiante_con_matricula_duplicada(client):
    primero = client.post(
        "/estudiantes/",
        json={
            "nombre": "Juan",
            "apellido": "Perez",
            "email": "juan4@test.com",
            "matricula": "EST400"
        }
    )

    segundo = client.post(
        "/estudiantes/",
        json={
            "nombre": "Maria",
            "apellido": "Lopez",
            "email": "maria4@test.com",
            "matricula": "EST401"
        }
    )

    segundo_id = segundo.json()["id"]

    respuesta = client.put(
        f"/estudiantes/{segundo_id}",
        json={"matricula": "EST400"}
    )

    assert primero.status_code == 201
    assert segundo.status_code == 201
    assert respuesta.status_code == 409


def test_crear_solicitud_con_responsable_inexistente(client):
    estudiante = client.post(
        "/estudiantes/",
        json={
            "nombre": "Laura",
            "apellido": "Gomez",
            "email": "laura999@test.com",
            "matricula": "EST997"
        }
    )

    area = client.post(
        "/areas/",
        json={"nombre": "Area Responsable Inexistente"}
    )

    respuesta = client.post(
        "/solicitudes/",
        json={
            "titulo": "Solicitud de prueba",
            "descripcion": "Prueba de responsable inexistente",
            "tipo": "Academica",
            "estudiante_id": estudiante.json()["id"],
            "area_id": area.json()["id"],
            "responsable_id": 9999
        }
    )

    assert estudiante.status_code == 201
    assert area.status_code == 201
    assert respuesta.status_code == 400
