from .empleado import Empleado


class Departamento:
    """Unidad de EcoTech que agrupa empleados y tiene un gerente asignado."""

    def __init__(self, id_departamento: str, nombre: str, gerente_asignado: str):
        """Crea el departamento sin empleados."""
        self.__id_departamento = id_departamento
        self.set_nombre(nombre)
        self._gerente_asignado = gerente_asignado   # protegido
        self._empleados = []                        # cardinalidad 1..* -> lista

    @property
    def id_departamento(self) -> str:
        """Devuelve el código del departamento."""
        return self.__id_departamento

    @property
    def gerente_asignado(self) -> str:
        """Devuelve el nombre del gerente asignado."""
        return self._gerente_asignado

    @property
    def nombre(self) -> str:
        """Devuelve el nombre del departamento."""
        return self.__nombre

    def set_nombre(self, valor: str) -> None:
        """Cambia el nombre; no puede estar vacío."""
        if not valor or not valor.strip():
            raise ValueError("El nombre del departamento no puede estar vacío.")
        self.__nombre = valor.strip()

    def asignar_empleado(self, empleado: Empleado) -> None:
        """Agrega un empleado al departamento y lo conecta de vuelta."""
        if empleado in self._empleados:
            raise ValueError("El empleado ya está en el departamento.")
        self._empleados.append(empleado)
        empleado.asignar_departamento(self)

    def remover_empleado(self, id_empleado: str) -> None:
        """Quita un empleado por su id y lo desasocia del departamento."""
        for e in self._empleados:
            if e.id_empleado == id_empleado:
                self._empleados.remove(e)
                e.asignar_departamento(None)
                return
        raise ValueError(f"No existe el empleado {id_empleado}.")

    def listar_empleados(self) -> list[Empleado]:
        """Devuelve una copia de la lista de empleados."""
        return list(self._empleados)   # copia: protege la lista interna

    def __str__(self) -> str:
        """Devuelve el departamento en una línea legible."""
        return (f"Departamento {self.__id_departamento} - {self.__nombre} "
                f"(gerente: {self._gerente_asignado}, "
                f"{len(self._empleados)} empleados)")