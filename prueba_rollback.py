from datetime import date

from dominio.departamento import Departamento
from dominio.empleado import Empleado
from infraestructura.conexion import ErrorDeIntegridad, ErrorDePersistencia, obtener_conexion
from infraestructura.empleado_repositorio import EmpleadoRepositorio

RUT_PRUEBA = "99999999-9"


def contar_personas() -> int:
    """Cuenta las filas de persona con el RUT de la prueba (consulta parametrizada)."""
    with obtener_conexion() as conn:
        return conn.execute(
            "SELECT COUNT(*) FROM persona WHERE rut = ?", (RUT_PRUEBA,)
        ).fetchone()[0]


def main():
    """Fuerza que falle la segunda escritura de guardar() y verifica el rollback."""
    # El departamento D99 nunca se guarda en la base, así que la llave foránea
    # empleado.departamento_id -> departamento.id va a fallar en el 2.º INSERT.
    departamento_inexistente = Departamento("D99", "Inexistente", "Nadie")
    empleado = Empleado(RUT_PRUEBA, "Prueba Rollback", "Calle 1", "+56911112222",
                        "prueba@ecotech.cl", date(2024, 1, 1), 800_000)
    departamento_inexistente.asignar_empleado(empleado)

    print(f"Filas en persona antes:   {contar_personas()}")
    try:
        EmpleadoRepositorio().guardar(empleado)
    except ErrorDeIntegridad as error:
        print(f"Fallo esperado: {error}")
    print(f"Filas en persona despues: {contar_personas()}")


if __name__ == "__main__":
    try:
        main()
    except ErrorDePersistencia as error:
        print(f"Error de base de datos: {error}")