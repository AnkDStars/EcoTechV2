from datetime import date
from .persona import Persona
from .registro_tiempo import RegistroTiempo


class Empleado(Persona):
    def __init__(self, id_empleado: str, nombre: str, direccion: str,
                 telefono: str, email: str, fecha_contrato: date,
                 salario: float):
        super().__init__(nombre, direccion, telefono, email)
        self.__id_empleado = id_empleado
        self.set_fecha_contrato(fecha_contrato)
        self.set_salario(salario)
        self._registros = []

    @property
    def id_empleado(self) -> str:
        return self.__id_empleado

    def set_salario(self, valor: float) -> None:
        if valor <= 0:
            raise ValueError("El salario debe ser mayor a 0.")
        self.__salario = valor

    def set_fecha_contrato(self, valor: date) -> None:
        if valor > date.today():
            raise ValueError("La fecha de contrato no puede ser futura.")
        self.__fecha_contrato = valor

    def consultar_salario(self) -> float:
        return self.__salario

    def actualizar_datos(self, nuevo_telefono: str, nuevo_email: str) -> None:
        self.set_telefono(nuevo_telefono)
        self.set_email(nuevo_email)

    def registrar_horas(self, proyecto, horas: float, descripcion: str) -> None:
        self._registros.append(RegistroTiempo(self, proyecto, horas, descripcion))

    def total_horas(self) -> float:
        return sum(r.get_horas() for r in self._registros)

    def describir(self) -> str:
        return (f"Empleado {self.__id_empleado} - {self.nombre} <{self.email}> | "
                f"contratado el {self.__fecha_contrato} | "
                f"{self.total_horas()} h registradas")