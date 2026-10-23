from abc import ABC, abstractmethod


class Persona(ABC):
    """Clase abstracta: datos personales comunes a toda persona de EcoTech."""

    def __init__(self, nombre: str, direccion: str, telefono: str, email: str):
        """Crea la persona validando nombre, teléfono y email."""
        self.set_nombre(nombre)
        self.__direccion = direccion
        self.set_telefono(telefono)
        self.set_email(email)

    @property
    def nombre(self) -> str:
        """Devuelve el nombre de la persona."""
        return self.__nombre

    @property
    def direccion(self) -> str:
        """Devuelve la dirección de la persona."""
        return self.__direccion

    @property
    def telefono(self) -> str:
        """Devuelve el teléfono de la persona."""
        return self.__telefono

    @property
    def email(self) -> str:
        """Devuelve el email de la persona."""
        return self.__email

    def set_nombre(self, valor: str) -> None:
        """Cambia el nombre; no puede estar vacío."""
        if not valor or not valor.strip():
            raise ValueError("El nombre no puede estar vacío.")
        self.__nombre = valor.strip()

    def set_telefono(self, valor: str) -> None:
        """Cambia el teléfono; solo dígitos, mínimo 8."""
        digitos = valor.replace("+", "").replace(" ", "")
        if not digitos.isdigit() or len(digitos) < 8:
            raise ValueError("Teléfono inválido: solo dígitos, mínimo 8.")
        self.__telefono = valor

    def set_email(self, valor: str) -> None:
        """Cambia el email; debe contener @ y un dominio con punto."""
        if "@" not in valor or "." not in valor.split("@")[-1]:
            raise ValueError("Email inválido.")
        self.__email = valor

    @abstractmethod
    def describir(self) -> str:
        """Cada tipo de persona se describe a su manera."""

    def __str__(self) -> str:
        """Devuelve la descripción de la persona."""
        return self.describir()