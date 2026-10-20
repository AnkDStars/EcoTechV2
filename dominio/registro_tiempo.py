from datetime import date


class RegistroTiempo:
    def __init__(self, empleado, proyecto, horas: float,
                 descripcion: str = "", fecha: date | None = None):
        self.fecha = fecha or date.today()   # público
        self._empleado = empleado            # protegido
        self._proyecto = proyecto            # protegido (objeto con .nombre)
        self.descripcion = descripcion
        self.registrar(horas)

    def registrar(self, horas: float) -> None:
        # Invariante: horas en (0, 24]
        if not 0 < horas <= 24:
            raise ValueError("Las horas deben estar entre 0 y 24.")
        self.__horas = horas

    def get_horas(self) -> float:
        return self.__horas

    def __str__(self) -> str:
        return (f"[{self.fecha}] {self._empleado.nombre} - "
                f"{self._proyecto.nombre}: {self.__horas} h")