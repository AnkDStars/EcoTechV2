from datetime import date

from dominio.departamento import Departamento
from dominio.empleado import Empleado
from infraestructura.conexion import obtener_conexion

# Consultas completas: cada una es una sola constante de texto fijo.
# Los datos del usuario viajan siempre aparte, como parámetros (?).
_SQL_OBTENER = """
    SELECT p.rut, p.nombre, p.direccion, p.telefono, p.email,
           e.fecha_ingreso, e.sueldo_base,
           d.id, d.nombre, d.gerente_asignado
    FROM empleado e
    JOIN persona p ON p.rut = e.rut
    LEFT JOIN departamento d ON d.id = e.departamento_id
    WHERE e.rut = ?
"""

_SQL_LISTAR = """
    SELECT p.rut, p.nombre, p.direccion, p.telefono, p.email,
           e.fecha_ingreso, e.sueldo_base,
           d.id, d.nombre, d.gerente_asignado
    FROM empleado e
    JOIN persona p ON p.rut = e.rut
    LEFT JOIN departamento d ON d.id = e.departamento_id
"""

_SQL_LISTAR_FILTRO = """
    SELECT p.rut, p.nombre, p.direccion, p.telefono, p.email,
           e.fecha_ingreso, e.sueldo_base,
           d.id, d.nombre, d.gerente_asignado
    FROM empleado e
    JOIN persona p ON p.rut = e.rut
    LEFT JOIN departamento d ON d.id = e.departamento_id
    WHERE p.nombre LIKE '%' || ? || '%'
"""


class EmpleadoRepositorio:
    """Guarda y recupera empleados; traduce entre objetos del dominio y filas."""

    @staticmethod
    def _fila_a_empleado(fila):
        """Convierte una fila de la base en un Empleado (con su departamento, si tiene)."""
        empleado = Empleado(
            id_empleado=fila[0],
            nombre=fila[1],
            direccion=fila[2],
            telefono=fila[3],
            email=fila[4],
            fecha_contrato=date.fromisoformat(fila[5]),
            salario=fila[6],
        )
        if fila[7] is not None:   # cardinalidad 0..1: solo si tiene departamento
            empleado.asignar_departamento(Departamento(fila[7], fila[8], fila[9]))
        return empleado

    def guardar(self, empleado):
        """Inserta al empleado en persona y empleado, dentro de una sola transacción."""
        departamento = empleado.departamento
        departamento_id = departamento.id_departamento if departamento else None
        with obtener_conexion() as conn:
            conn.execute(
                """INSERT INTO persona (rut, nombre, direccion, telefono, email)
                   VALUES (?, ?, ?, ?, ?)""",
                (empleado.id_empleado, empleado.nombre, empleado.direccion,
                 empleado.telefono, empleado.email),
            )
            conn.execute(
                """INSERT INTO empleado (rut, fecha_ingreso, sueldo_base, departamento_id)
                   VALUES (?, ?, ?, ?)""",
                (empleado.id_empleado, empleado.fecha_contrato.isoformat(),
                 empleado.salario, departamento_id),
            )
        return empleado

    def obtener(self, rut):
        """Devuelve el empleado con ese rut, o None si no existe."""
        with obtener_conexion() as conn:
            fila = conn.execute(_SQL_OBTENER, (rut,)).fetchone()
        return self._fila_a_empleado(fila) if fila else None

    def listar(self, nombre_contiene=None):
        """Devuelve una lista de empleados; si hay filtro, solo los que lo contienen."""
        with obtener_conexion() as conn:
            if nombre_contiene:
                filas = conn.execute(_SQL_LISTAR_FILTRO, (nombre_contiene,)).fetchall()
            else:
                filas = conn.execute(_SQL_LISTAR).fetchall()
        return [self._fila_a_empleado(f) for f in filas]

    def actualizar(self, empleado):
        """Actualiza los datos del empleado; devuelve cuántas filas cambiaron."""
        departamento = empleado.departamento
        departamento_id = departamento.id_departamento if departamento else None
        with obtener_conexion() as conn:
            conn.execute(
                """UPDATE persona
                   SET nombre = ?, direccion = ?, telefono = ?, email = ?
                   WHERE rut = ?""",
                (empleado.nombre, empleado.direccion, empleado.telefono,
                 empleado.email, empleado.id_empleado),
            )
            cur = conn.execute(
                """UPDATE empleado
                   SET fecha_ingreso = ?, sueldo_base = ?, departamento_id = ?
                   WHERE rut = ?""",
                (empleado.fecha_contrato.isoformat(), empleado.salario,
                 departamento_id, empleado.id_empleado),
            )
        return cur.rowcount

    def eliminar(self, rut):
        """Borra al empleado (y en cascada sus registros) y su fila en persona."""
        with obtener_conexion() as conn:
            cur = conn.execute("DELETE FROM empleado WHERE rut = ?", (rut,))
            conn.execute("DELETE FROM persona WHERE rut = ?", (rut,))
        return cur.rowcount > 0