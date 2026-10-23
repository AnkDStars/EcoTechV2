from dominio.departamento import Departamento
from infraestructura.conexion import obtener_conexion

# Consultas completas: cada una es una sola constante de texto fijo.
# Los datos del usuario viajan siempre aparte, como parámetros (?).
_SQL_OBTENER = """
    SELECT id, nombre, gerente_asignado
    FROM departamento
    WHERE id = ?
"""

_SQL_LISTAR = """
    SELECT id, nombre, gerente_asignado
    FROM departamento
"""

_SQL_LISTAR_FILTRO = """
    SELECT id, nombre, gerente_asignado
    FROM departamento
    WHERE nombre LIKE '%' || ? || '%'
"""


class DepartamentoRepositorio:
    """Guarda y recupera departamentos; traduce entre objetos y filas."""

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
        with obtener_conexion() as conn:
            fila = conn.execute(_SQL_OBTENER, (id_departamento,)).fetchone()
        return self._fila_a_departamento(fila) if fila else None

    def listar(self, nombre_contiene=None):
        """Devuelve los departamentos; si hay filtro, solo los que lo contienen."""
        with obtener_conexion() as conn:
            if nombre_contiene:
                filas = conn.execute(_SQL_LISTAR_FILTRO, (nombre_contiene,)).fetchall()
            else:
                filas = conn.execute(_SQL_LISTAR).fetchall()
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