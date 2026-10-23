from dominio.departamento import Departamento
from infraestructura.conexion import obtener_conexion


class DepartamentoRepositorio:
    """Guarda y recupera departamentos; traduce entre objetos y filas."""

    # Texto fijo de la consulta: nunca lleva datos del usuario (esos van con ?).
    _SELECT = "SELECT id, nombre, gerente_asignado FROM departamento"

    @staticmethod
    def _fila_a_departamento(fila):
        """Convierte una fila de la base en un objeto Departamento del dominio."""
        return Departamento(
            id_departamento=fila[0],
            nombre=fila[1],
            gerente_asignado=fila[2],
        )

    def guardar(self, departamento):
        """Inserta el departamento en la base."""
        with obtener_conexion() as conn:
            conn.execute(
                "INSERT INTO departamento (id, nombre, gerente_asignado) VALUES (?, ?, ?)",
                (departamento.id_departamento, departamento.nombre,
                 departamento.gerente_asignado),
            )
        return departamento

    def obtener(self, id_departamento):
        """Devuelve el departamento con ese id, o None si no existe."""
        sql = self._SELECT + " WHERE id = ?"
        with obtener_conexion() as conn:
            fila = conn.execute(sql, (id_departamento,)).fetchone()
        return self._fila_a_departamento(fila) if fila else None

    def listar(self, nombre_contiene=None):
        """Devuelve los departamentos; si hay filtro, solo los que lo contienen."""
        sql = self._SELECT
        params = []
        if nombre_contiene:
            sql += " WHERE nombre LIKE ?"
            params.append(f"%{nombre_contiene}%")
        with obtener_conexion() as conn:
            filas = conn.execute(sql, params).fetchall()
        return [self._fila_a_departamento(f) for f in filas]

    def actualizar(self, departamento):
        """Actualiza nombre y gerente; devuelve cuántas filas cambiaron."""
        with obtener_conexion() as conn:
            cur = conn.execute(
                "UPDATE departamento SET nombre = ?, gerente_asignado = ? WHERE id = ?",
                (departamento.nombre, departamento.gerente_asignado,
                 departamento.id_departamento),
            )
        return cur.rowcount

    def eliminar(self, id_departamento):
        """Borra el departamento; si tiene empleados, la base lo impide (error)."""
        with obtener_conexion() as conn:
            cur = conn.execute("DELETE FROM departamento WHERE id = ?", (id_departamento,))
        return cur.rowcount > 0