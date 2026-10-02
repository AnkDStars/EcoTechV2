from .empleado import Empleado


class Departamento:
    def __init__(self, id_departamento: str, nombre: str, gerente_asignado: str):
        self.__id_departamento = id_departamento
        self.set_nombre(nombre)
        self._gerente_asignado = gerente_asignado   # protegido
        self._empleados = []

    @property
    def nombre(self) -> str:
        return self.__nombre

    def set_nombre(self, valor: str) -> None:
        if not valor or not valor.strip():
            raise ValueError("El nombre del departamento no puede estar vacío.")
        self.__nombre = valor.strip()

    def asignar_empleado(self, empleado: Empleado) -> None:
        if empleado in self._empleados:
            raise ValueError("El empleado ya está en el departamento.")
        self._empleados.append(empleado)

    def remover_empleado(self, id_empleado: str) -> None:
        for e in self._empleados:
            if e.id_empleado == id_empleado:
                self._empleados.remove(e)
                return
        raise ValueError(f"No existe el empleado {id_empleado}.")

    def listar_empleados(self) -> list[Empleado]:
        return list(self._empleados)   # copia: protege la lista interna

    def __str__(self) -> str:
        return (f"Departamento {self.__id_departamento} - {self.__nombre} "
                f"(gerente: {self._gerente_asignado}, "
                f"{len(self._empleados)} empleados)")