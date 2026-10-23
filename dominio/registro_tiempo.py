from datetime import date


class RegistroTiempo:
    """Horas que un empleado dedicó a un proyecto en una fecha."""

    def __init__(self, empleado, proyecto, horas: float,
                 descripcion: str = "", fecha: date | None = None):
        """Crea el registro; las horas deben estar entre 0 y 24."""
        self.fecha = fecha or date.today()   # público
        self._empleado = empleado            # protegido
        self._proyecto = proyecto            # protegido (objeto con .nombre)
        self.descripcion = descripcion
        self.registrar(horas)

    def registrar(self, horas: float) -> None:
        """Fija las horas del registro respetando la invariante (0, 24]."""
        if not 0 < horas <= 24:
            raise ValueError("Las horas deben estar entre 0 y 24.")
        self.__horas = horas

    def get_horas(self) -> float:
        """Devuelve las horas registradas."""
        return self.__horas

    def __str__(self) -> str:
        """Devuelve el registro en una línea legible."""
        return (f"[{self.fecha}] {self._empleado.nombre} - "
                f"{self._proyecto.nombre}: {self.__horas} h")