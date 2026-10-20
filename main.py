from datetime import date
from types import SimpleNamespace

from dominio.departamento import Departamento
from dominio.empleado import Empleado

def main():
    # Un objeto de cada clase
    dep = Departamento("D01", "Operaciones", "Carlos Pérez")
    ana = Empleado("E01", "Ana Rojas", "Av. Siempre Viva 123",
                   "+56912345678", "ana@ecotech.cl",
                   date(2024, 3, 1), 950_000)
    proyecto = SimpleNamespace(nombre="Planta Solar")  # stand-in de Proyecto

    dep.asignar_empleado(ana)                             
    ana.registrar_horas(proyecto, 6, "Instalación de paneles")  
    ana.registrar_horas(proyecto, 4, "Pruebas de conexión")

    # Estado de cada uno
    print(dep)
    print(ana)
    for registro in ana.listar_registros():
        print(registro)
    print(f"Horas registradas: {ana.total_horas()}")


if __name__ == "__main__":
    main()