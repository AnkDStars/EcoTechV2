from datetime import date

from dominio.empleado import Empleado
from infraestructura.conexion import obtener_conexion


class EmpleadoRepositorio:
    """Guarda y recupera empleados; traduce entre objetos del dominio y filas."""

    # Texto fijo de la consulta: nunca lleva datos del usuario (esos van con ?).
    _SELECT = """SELECT p.rut, p.nombre, p.direccion, p.telefono, p.email,
                        e.fecha_ingreso, e.sueldo_base
                 FROM empleado e JOIN persona p ON p.rut = e.rut"""

    @staticmethod
    def _fila_a_empleado(fila):
        """Convierte una fila de la base en un objeto Empleado del dominio."""
        return Empleado(
            id_empleado=fila[0],
            nombre=fila[1],
            direccion=fila[2],
            telefono=fila[3],
            email=fila[4],
            fecha_contrato=date.fromisoformat(fila[5]),
            salario=fila[6],
        )

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
        sql = self._SELECT + " WHERE e.rut = ?"
        with obtener_conexion() as conn:
            fila = conn.execute(sql, (rut,)).fetchone()
        return self._fila_a_empleado(fila) if fila else None

    def listar(self, nombre_contiene=None):
        """Devuelve una lista de empleados; si hay filtro, solo los que lo contienen."""
        sql = self._SELECT
        params = []
        if nombre_contiene:
            sql += " WHERE p.nombre LIKE ?"
            params.append(f"%{nombre_contiene}%")
        with obtener_conexion() as conn:
            filas = conn.execute(sql, params).fetchall()
        return [self._fila_a_empleado(f) for f in filas]