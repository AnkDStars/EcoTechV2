from datetime import date, timedelta

from dominio.departamento import Departamento
from dominio.empleado import Empleado
from dominio.proyecto import Proyecto
from infraestructura.conexion import ErrorDeIntegridad, ErrorDePersistencia
from infraestructura.departamento_repositorio import DepartamentoRepositorio
from infraestructura.empleado_repositorio import EmpleadoRepositorio

PAYLOAD_INYECCION = "' OR '1'='1"
RUT_DEMO = "12345678-9"
ID_DEPARTAMENTO_DEMO = "D10"


def demo_dominio():
    """Usa las clases del dominio en memoria, sin base de datos (C05)."""
    dep = Departamento("D01", "Operaciones", "Carlos Pérez")
    ana = Empleado("E01", "Ana Rojas", "Av. Siempre Viva 123",
                   "+56912345678", "ana@ecotech.cl",
                   date(2024, 3, 1), 950_000)
    proyecto = Proyecto(1, "Planta Solar")

    dep.asignar_empleado(ana)
    ana.registrar_horas(proyecto, 6, "Instalación de paneles")
    ana.registrar_horas(proyecto, 4, "Pruebas de conexión")

    print(dep)
    print(ana)
    for registro in ana.listar_registros():
        print(registro)
    print(f"Horas registradas: {ana.total_horas()}")


def demo_validaciones():
    """Intenta crear datos inválidos: se rechazan y el programa sigue."""
    print("\n== Validación de entradas ==")
    base = dict(id_empleado="E90", nombre="Luis Soto", direccion="Calle 1",
                telefono="911112222", email="luis@ecotech.cl",
                fecha_contrato=date(2024, 1, 1), salario=800000)
    casos = {
        "nombre vacío": {"nombre": ""},
        "email sin dominio": {"email": "luis@ecotech"},
        "teléfono con letras": {"telefono": "abc12345"},
        "salario negativo": {"salario": -5},
        "fecha de contrato futura": {"fecha_contrato": date.today() + timedelta(days=30)},
    }
    for descripcion, cambio in casos.items():
        try:
            Empleado(**{**base, **cambio})
            print(f"{descripcion}: ACEPTADO (revisar validación)")
        except ValueError as error:
            print(f"{descripcion}: rechazado -> {error}")

    try:
        Empleado(**base).registrar_horas(Proyecto(1, "Planta Solar"), 30, "prueba")
    except ValueError as error:
        print(f"horas fuera de rango: rechazado -> {error}")


def demo_crud():
    """Corre las cuatro operaciones sobre empleados y departamentos (C08)."""
    empleados = EmpleadoRepositorio()
    departamentos = DepartamentoRepositorio()

    # Deja la base sin los datos de la demo para poder repetirla.
    empleados.eliminar(RUT_DEMO)
    departamentos.eliminar(ID_DEPARTAMENTO_DEMO)

    dep = Departamento(ID_DEPARTAMENTO_DEMO, "Demostración", "Carlos Pérez")
    ana = Empleado(RUT_DEMO, "Ana Rojas", "Av. Costanera 123", "+56912345678",
                   "ana@ecotech.cl", date(2024, 3, 1), 950_000)
    dep.asignar_empleado(ana)

    departamentos.guardar(dep)                                    # crear
    empleados.guardar(ana)
    print(empleados.obtener(RUT_DEMO))                            # leer uno
    print(f"Empleados en la base: {len(empleados.listar())}")     # leer varios

    ana.set_salario(1_050_000)
    print(f"Filas actualizadas: {empleados.actualizar(ana)}")     # actualizar
    print(f"Sueldo guardado: {empleados.obtener(RUT_DEMO).salario}")

    try:                                                          # borrado impedido
        departamentos.eliminar(ID_DEPARTAMENTO_DEMO)
    except ErrorDeIntegridad as error:
        print(f"Aviso (esperado): {error}")

    print(f"Empleado eliminado: {empleados.eliminar(RUT_DEMO)}")  # eliminar
    print(f"Departamento eliminado: {departamentos.eliminar(ID_DEPARTAMENTO_DEMO)}")


def prueba_inyeccion():
    """Verifica que el payload ' OR '1'='1 se trata como dato y no como código."""
    empleados = EmpleadoRepositorio()
    departamentos = DepartamentoRepositorio()
    total_antes = len(empleados.listar())

    resultados = {
        "empleados.listar": empleados.listar(nombre_contiene=PAYLOAD_INYECCION),
        "empleados.obtener": empleados.obtener(PAYLOAD_INYECCION),
        "empleados.eliminar": empleados.eliminar(PAYLOAD_INYECCION),
        "departamentos.listar": departamentos.listar(nombre_contiene=PAYLOAD_INYECCION),
        "departamentos.obtener": departamentos.obtener(PAYLOAD_INYECCION),
        "departamentos.eliminar": departamentos.eliminar(PAYLOAD_INYECCION),
    }
    for nombre, resultado in resultados.items():
        veredicto = "OK" if not resultado else "FALLO: concatena"
        print(f"{nombre}: {resultado} -> {veredicto}")

    intactos = len(empleados.listar()) == total_antes
    print(f"Empleados intactos tras eliminar con el payload: {intactos}")


def main():
    """Ejecuta el ciclo completo de principio a fin como un cliente real."""
    print("== Dominio en memoria ==")
    demo_dominio()
    demo_validaciones()
    print("\n== CRUD con la base ==")
    demo_crud()
    print("\n== Prueba de inyección SQL ==")
    prueba_inyeccion()


if __name__ == "__main__":
    try:
        main()
    except ErrorDePersistencia as error:
        print(f"Error de base de datos: {error}")
    except ValueError as error:
        print(f"Dato inválido: {error}")