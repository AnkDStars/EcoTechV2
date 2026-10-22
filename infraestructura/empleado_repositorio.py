from infraestructura.conexion import obtener_conexion


class EmpleadoRepositorio:
    """Guarda y recupera empleados; traduce entre objetos del dominio y filas."""

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