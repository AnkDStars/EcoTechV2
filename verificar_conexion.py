from infraestructura.conexion import ErrorDeConexion, obtener_conexion


def insertar_persona(rut: str, nombre: str) -> None:
    """Inserta una persona; los datos van aparte con ?, nunca concatenados."""
    with obtener_conexion() as conn:
        conn.execute(
            "INSERT INTO persona (rut, nombre) VALUES (?, ?)",
            (rut, nombre),
        )


def listar_personas() -> list:
    """Devuelve todas las personas como (rut, nombre)."""
    with obtener_conexion() as conn:
        return conn.execute("SELECT rut, nombre FROM persona").fetchall()


def main():
    """Inserta una fila, la lee y prueba que un RUT repetido avisa sin caerse."""
    listar_personas()   # si falta el .env o la base, falla aquí, al arrancar

    try:
        insertar_persona("12345678-9", "Ana Rojas")
        print("Fila insertada.")
    except ErrorDeConexion as e:
        print(f"Aviso: {e}")

    for fila in listar_personas():
        print(fila)

    # Prueba del RUT duplicado: debe avisar, no caerse.
    try:
        insertar_persona("12345678-9", "Ana Rojas")
    except ErrorDeConexion as e:
        print(f"Aviso (esperado): {e}")


if __name__ == "__main__":
    try:
        main()
    except ErrorDeConexion as e:
        print(f"Error de configuración: {e}")