# Quick Module Updater DZ

Modulo para Odoo 17 Community que agrega un acceso rapido en la barra superior para buscar y actualizar modulos instalados sin entrar al menu de Aplicaciones.

Esta pensado para desarrollo y soporte, cuando necesitas actualizar un modulo con frecuencia mientras trabajas en Odoo.

## Que hace

- Agrega un widget en el systray de Odoo.
- Permite buscar modulos instalados por nombre.
- Actualiza un modulo desde el mismo widget.
- Permite marcar modulos como favoritos para tenerlos a la mano.
- Guarda un historial basico de las actualizaciones realizadas desde el widget.

## Requisitos

- Odoo 17 Community Edition.
- Acceso de administrador en Odoo.

## Instalacion

1. Copia la carpeta `quick_module_updater_dz` dentro de tu ruta de addons.
2. Reinicia el servidor de Odoo.
3. Actualiza la lista de aplicaciones.
4. Busca `Quick Module Updater DZ` e instala el modulo.

## Uso

1. Entra a Odoo con un usuario administrador.
2. Abre el widget desde la barra superior.
3. Busca el modulo que quieres actualizar.
4. Presiona `Actualizar`.

Si marcas un modulo como favorito, aparecera al abrir el widget. Los favoritos se guardan en el navegador actual.

## Notas

- El widget solo se muestra a usuarios administradores.
- Solo permite actualizar modulos ya instalados.
- Antes de usarlo en produccion, conviene probar el flujo de actualizacion en una base de respaldo o en un entorno de prueba.

## Estructura

```text
quick_module_updater_dz/
|-- controllers/
|-- data/
|-- models/
|-- security/
|-- static/
|-- views/
|-- __init__.py
|-- __manifest__.py
```

## Licencia

LGPL-3
