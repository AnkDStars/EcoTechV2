from datetime import date
from .persona import Persona
from .registro_tiempo import RegistroTiempo


class Empleado(Persona):
    """Un empleado de EcoTech. Registra su tiempo en proyectos."""

    def __init__(self, id_empleado: str, nombre: str, direccion: str,
                 telefono: str, email: str, fecha_contrato: date,
                 salario: float):
        """Crea el empleado sin registros y sin departamento asignado."""
        super().__init__(nombre, direccion, telefono, email)
        self.__id_empleado = id_empleado
        self.set_fecha_contrato(fecha_contrato)
        self.set_salario(salario)
        self._registros = []        # cardinalidad 1..* -> lista
        self._departamento = None   # cardinalidad 0..1 -> puede ser None

    @property
    def id_empleado(self) -> str:
        """Devuelve el identificador del empleado."""
        return self.__id_empleado

    @property
    def departamento(self):
        """Devuelve el departamento del empleado, o None si no tiene."""
        return self._departamento

    @property
    def fecha_contrato(self) -> date:
        """Devuelve la fecha de contrato del empleado."""
        return self.__fecha_contrato

    @property
    def salario(self) -> float:
        """Devuelve el salario del empleado."""
        return self.__salario

    def set_salario(self, valor: float) -> None:
        """Cambia el salario; debe ser mayor a 0."""
        if valor <= 0:
            raise ValueError("El salario debe ser mayor a 0.")
        self.__salario = valor

    def set_fecha_contrato(self, valor: date) -> None:
        """Cambia la fecha de contrato; no puede ser futura."""
        if valor > date.today():
            raise ValueError("La fecha de contrato no puede ser futura.")
        self.__fecha_contrato = valor

    def consultar_salario(self) -> float:
        """Devuelve el salario del empleado."""
        return self.__salario

    def actualizar_datos(self, nuevo_telefono: str, nuevo_email: str) -> None:
        """Actualiza teléfono y email validando ambos."""
        self.set_telefono(nuevo_telefono)
        self.set_email(nuevo_email)

    def asignar_departamento(self, departamento) -> None:
        """Asocia al empleado con un departamento (None lo desasocia)."""
        self._departamento = departamento

    def registrar_horas(self, proyecto, horas: float, descripcion: str) -> None:
        """Agrega un registro de tiempo del empleado en un proyecto."""
        self._registros.append(RegistroTiempo(self, proyecto, horas, descripcion))

    def listar_registros(self) -> list[RegistroTiempo]:
        """Devuelve una copia de los registros de tiempo del empleado."""
        return list(self._registros)

    def total_horas(self) -> float:
        """Calcula y devuelve el total de horas registradas."""
        return sum(r.get_horas() for r in self._registros)

    def describir(self) -> str:
        """Describe al empleado, su departamento y sus horas."""
        depto = self._departamento.nombre if self._departamento else "sin departamento"
        return (f"Empleado {self.__id_empleado} - {self.nombre} <{self.email}> | "
                f"{depto} | contratado el {self.__fecha_contrato} | "
                f"{self.total_horas()} h registradas")