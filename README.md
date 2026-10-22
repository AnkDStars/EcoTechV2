# EcoTech

Proyecto de clases en Python traducidas desde UML, con persistencia en SQLite.
Se corre con: `python main.py`

Líder de Proyecto: Oscar Guzmán

## Decisiones de diseño (C08)

| Decisión | La nuestra |
| --- | --- |
| ¿Se borra de verdad? | DELETE real. Al eliminar un empleado también se borra su fila en `persona`. |
| ¿Qué pasa con los hijos? | Los registros de tiempo se borran en cascada con el empleado (`ON DELETE CASCADE`). Un departamento con empleados no se puede borrar. |
| ¿Quién asigna el id? | El programa: el RUT del empleado y el código del departamento. |