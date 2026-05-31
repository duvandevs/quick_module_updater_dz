# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ModuleUpdateLog(models.Model):
    _name = 'module.update.log'
    _description = 'Registro de actualizaciones de módulos'
    _order = 'create_date desc'
    _rec_name = 'module_name'

    module_name = fields.Char('Nombre del Módulo', required=True)
    module_technical_name = fields.Char('Nombre Técnico', required=True)
    version_before = fields.Char('Versión Anterior')
    version_after = fields.Char('Versión Nueva')
    user_id = fields.Many2one('res.users', 'Usuario', default=lambda self: self.env.user)
    state = fields.Selection([
        ('success', 'Exitoso'),
        ('error', 'Error'),
        ('in_progress', 'En Progreso')
    ], string='Estado', default='in_progress')
    error_message = fields.Text('Mensaje de Error')
    duration = fields.Float('Duración (segundos)')
    dependencies_updated = fields.Text('Dependencias Actualizadas')
    
    @api.model
    def create_log(self, module_name, technical_name, version_before=None):
        """Crea un nuevo registro de actualización"""
        return self.create({
            'module_name': module_name,
            'module_technical_name': technical_name,
            'version_before': version_before,
            'state': 'in_progress'
        })
    
    def mark_success(self, version_after, duration, dependencies=None):
        """Marca la actualización como exitosa"""
        self.write({
            'state': 'success',
            'version_after': version_after,
            'duration': duration,
            'dependencies_updated': dependencies
        })
        
    def mark_error(self, error_message, duration):
        """Marca la actualización como fallida"""
        self.write({
            'state': 'error',
            'error_message': error_message,
            'duration': duration
        })
        
    @api.model
    def get_recent_updates(self, limit=10):
        """Obtiene las actualizaciones recientes"""
        return self.search([], limit=limit)
    
    @api.model
    def get_pending_updates_count(self, refresh=False):
        """Cuenta los módulos con actualizaciones pendientes"""
        Module = self.env['ir.module.module'].sudo()
        if refresh:
            Module.update_list()

        modules = Module.search([('state', '=', 'installed')])
        return len(modules.filtered(
            lambda module: (
                module.latest_version
                and module.installed_version
                and module.latest_version != module.installed_version
            )
        ))
