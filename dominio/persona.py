from abc import ABC, abstractmethod


class Persona(ABC):
    """Clase abstracta: datos personales comunes."""

    def __init__(self, nombre: str, direccion: str, telefono: str, email: str):
        self.set_nombre(nombre)
        self.__direccion = direccion
        self.set_telefono(telefono)
        self.set_email(email)

    @property
    def nombre(self) -> str:
        return self.__nombre

    @property
    def direccion(self) -> str:
        return self.__direccion

    @property
    def telefono(self) -> str:
        return self.__telefono

    @property
    def email(self) -> str:
        return self.__email

    def set_nombre(self, valor: str) -> None:
        if not valor or not valor.strip():
            raise ValueError("El nombre no puede estar vacío.")
        self.__nombre = valor.strip()

    def set_telefono(self, valor: str) -> None:
        digitos = valor.replace("+", "").replace(" ", "")
        if not digitos.isdigit() or len(digitos) < 8:
            raise ValueError("Teléfono inválido: solo dígitos, mínimo 8.")
        self.__telefono = valor

    def set_email(self, valor: str) -> None:
        if "@" not in valor or "." not in valor.split("@")[-1]:
            raise ValueError("Email inválido.")
        self.__email = valor

    @abstractmethod
    def describir(self) -> str:
        """Cada tipo de persona se describe a su manera."""

    def __str__(self) -> str:
        return self.describir()