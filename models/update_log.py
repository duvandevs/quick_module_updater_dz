# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime


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
    def get_pending_updates_count(self):
        """Cuenta los módulos con actualizaciones pendientes"""
        Module = self.env['ir.module.module']
        return Module.search_count([
            ('state', '=', 'installed'),
            ('latest_version', '!=', False)
        ])


class ModuleFavorite(models.Model):
    _name = 'module.favorite'
    _description = 'Módulos Favoritos'
    _order = 'sequence, name'
    _rec_name = 'display_name'
    
    module_id = fields.Many2one('ir.module.module', 'Módulo', required=True, ondelete='cascade')
    name = fields.Char('Nombre Técnico', related='module_id.name', store=True)
    display_name = fields.Char('Nombre', related='module_id.shortdesc', store=True)
    user_id = fields.Many2one('res.users', 'Usuario', default=lambda self: self.env.user, required=True)
    sequence = fields.Integer('Secuencia', default=10)
    color = fields.Integer('Color', default=0)
    last_used = fields.Datetime('Último Uso')
    use_count = fields.Integer('Veces Usado', default=0)
    notes = fields.Text('Notas')
    
    _sql_constraints = [
        ('unique_user_module', 'UNIQUE(user_id, module_id)', 'Este módulo ya está en tus favoritos')
    ]
    
    @api.model
    def toggle_favorite(self, module_id):
        """Agrega o quita un módulo de favoritos"""
        existing = self.search([
            ('user_id', '=', self.env.user.id),
            ('module_id', '=', module_id)
        ])
        
        if existing:
            existing.unlink()
            return {'added': False, 'message': 'Módulo removido de favoritos'}
        else:
            self.create({
                'module_id': module_id,
                'user_id': self.env.user.id
            })
            return {'added': True, 'message': 'Módulo agregado a favoritos'}
    
    def mark_used(self):
        """Marca el favorito como usado"""
        self.write({
            'last_used': fields.Datetime.now(),
            'use_count': self.use_count + 1
        })
    
    @api.model
    def get_user_favorites(self):
        """Obtiene los favoritos del usuario actual"""
        favorites = self.search([('user_id', '=', self.env.user.id)])
        result = []
        for fav in favorites:
            module = fav.module_id
            result.append({
                'id': module.id,
                'favorite_id': fav.id,
                'name': module.name,
                'display_name': module.shortdesc or module.name,
                'version': module.installed_version or '1.0',
                'summary': module.summary or '',
                'color': fav.color,
                'use_count': fav.use_count,
                'last_used': fav.last_used.strftime('%Y-%m-%d %H:%M') if fav.last_used else None,
                'notes': fav.notes or ''
            })
        return result