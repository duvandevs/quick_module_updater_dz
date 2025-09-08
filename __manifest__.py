# -*- coding: utf-8 -*-
{
    'name': 'Quick Module Updater DZ',
    'version': '17.0.1.0.1',
    'category': 'Technical',
    'summary': 'Actualiza módulos rápidamente desde la barra superior de Odoo',
    'description': """
Quick Module Updater DZ
========================

Este módulo añade un widget de actualización rápida en la barra superior de Odoo 17.

Características principales:
----------------------------
* Widget dropdown en la barra superior para actualizar módulos
* Lista de todos los módulos instalados
* Agrega los módulos a favoritos
* Muestra siempre los módulos favoritos primero
* Actualización con un solo clic
* Notificaciones de éxito/error
* Búsqueda y filtros rápidos

Desarrollado por: DZ
    """,
    'author': 'DZ Development',
    'website': 'https://github.com/dz',
    'license': 'LGPL-3',
    'depends': [
        'base',
        'web',
        'mail',
    ],
    'data': [
        'security/ir.model.access.csv',
        #'views/assets.xml',
        'views/update_log_views.xml',
        'data/ir_cron.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'quick_module_updater_dz/static/src/components/module_updater/module_updater.js',
            'quick_module_updater_dz/static/src/components/module_updater/module_updater.xml',
            'quick_module_updater_dz/static/src/components/module_updater/module_updater.scss',
        ],
    },
    'images': ['static/description/icon.png'],
    'installable': True,
    'application': False,
    'auto_install': False,
}
