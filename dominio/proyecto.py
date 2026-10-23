class Proyecto:
    """Proyecto en el que los empleados registran horas."""

    def __init__(self, id_proyecto: int, nombre: str):
        """Crea el proyecto validando su nombre."""
        self.__id_proyecto = id_proyecto
        self.set_nombre(nombre)

    @property
    def id_proyecto(self) -> int:
        """Devuelve el identificador del proyecto."""
        return self.__id_proyecto

    @property
    def nombre(self) -> str:
        """Devuelve el nombre del proyecto."""
        return self.__nombre

    def set_nombre(self, valor: str) -> None:
        """Cambia el nombre; no puede estar vacío."""
        if not valor or not valor.strip():
            raise ValueError("El nombre del proyecto no puede estar vacío.")
        self.__nombre = valor.strip()

    def __str__(self) -> str:
        """Devuelve la descripción del proyecto."""
        return f"Proyecto {self.__id_proyecto} - {self.__nombre}"