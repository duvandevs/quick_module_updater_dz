# -*- coding: utf-8 -*-

import time
import logging
from odoo import http, _
from odoo.http import request
from odoo.exceptions import AccessError, UserError

_logger = logging.getLogger(__name__)


class ModuleUpdaterController(http.Controller):
    
    @http.route('/module_updater_dz/search_module', type='json', auth='user')
    def search_module(self, search_term):
        """Busca módulos por nombre"""
        try:
            # Verificar permisos de administrador
            if not request.env.user.has_group('base.group_system'):
                raise AccessError(_('Solo los administradores pueden usar esta función.'))
            
            Module = request.env['ir.module.module'].sudo()
            
            # Buscar módulos instalados que coincidan con el término de búsqueda
            domain = [
                ('state', '=', 'installed'),
                '|', '|',
                ('name', 'ilike', search_term),
                ('shortdesc', 'ilike', search_term),
                ('summary', 'ilike', search_term)
            ]
            
            modules = Module.search(domain, limit=10)
            
            module_list = []
            for module in modules:
                module_info = {
                    'id': module.id,
                    'name': module.name,
                    'display_name': module.shortdesc or module.name,
                    'version': module.installed_version or '1.0',
                    'summary': module.summary or '',
                    'author': module.author or 'Unknown',
                    'category': module.category_id.name if module.category_id else 'Uncategorized',
                }
                module_list.append(module_info)
            
            return {
                'success': True,
                'modules': module_list
            }
            
        except Exception as e:
            _logger.error(f"Error buscando módulo: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'modules': []
            }
    
    @http.route('/module_updater_dz/get_favorite_modules', type='json', auth='user')
    def get_favorite_modules(self, module_ids):
        """Obtiene información de módulos específicos por sus IDs"""
        try:
            if not request.env.user.has_group('base.group_system'):
                return {'success': False, 'modules': []}
            
            if not module_ids:
                return {'success': True, 'modules': []}
            
            Module = request.env['ir.module.module'].sudo()
            
            # Convertir IDs a enteros si vienen como strings
            try:
                module_ids = [int(mid) for mid in module_ids]
            except (ValueError, TypeError):
                _logger.error(f"Invalid module IDs: {module_ids}")
                return {'success': False, 'modules': []}
            
            modules = Module.browse(module_ids)
            module_list = []
            
            for module in modules:
                if module.exists() and module.state == 'installed':
                    module_info = {
                        'id': module.id,
                        'name': module.name,
                        'display_name': module.shortdesc or module.name,
                        'version': module.installed_version or '1.0',
                        'summary': module.summary or '',
                        'author': module.author or 'Unknown',
                        'category': module.category_id.name if module.category_id else 'Uncategorized',
                    }
                    module_list.append(module_info)
            
            return {
                'success': True,
                'modules': module_list
            }
            
        except Exception as e:
            _logger.error(f"Error obteniendo módulos favoritos: {str(e)}")
            return {
                'success': False,
                'modules': []
            }
    
    @http.route('/module_updater_dz/update_module', type='json', auth='user')
    def update_module(self, module_id):
        """Actualiza un módulo específico"""
        try:
            # Verificar permisos
            if not request.env.user.has_group('base.group_system'):
                raise AccessError(_('Solo los administradores pueden actualizar módulos.'))
            
            start_time = time.time()
            
            Module = request.env['ir.module.module'].sudo()
            UpdateLog = request.env['module.update.log'].sudo() if 'module.update.log' in request.env else None
            
            # Buscar el módulo
            module = Module.browse(module_id)
            if not module.exists():
                raise UserError(_('Módulo no encontrado.'))
            if module.state != 'installed':
                raise UserError(_('Solo se pueden actualizar módulos instalados.'))
            
            module_name = module.shortdesc or module.name
            version_before = module.latest_version or module.installed_version
            
            # Crear registro de log si el modelo existe
            log = None
            if UpdateLog:
                try:
                    log = UpdateLog.create_log(
                        module_name,
                        module.name,
                        version_before
                    )
                except Exception:
                    _logger.exception("No se pudo crear el log de actualización")
            
            try:
                # Actualizar lista de módulos disponibles
                Module.update_list()
                
                # Ejecutar actualización inmediata
                module.button_immediate_upgrade()
                module = Module.browse(module.id)
                
                # Calcular duración
                duration = time.time() - start_time
                
                # Actualizar log con éxito si existe
                if log:
                    try:
                        log.mark_success(
                            module.installed_version or module.latest_version,
                            duration
                        )
                    except Exception:
                        _logger.exception("No se pudo marcar como exitoso el log de actualización")
                
                return {
                    'success': True,
                    'message': _('Módulo %s actualizado exitosamente.') % module_name,
                    'version': module.installed_version or module.latest_version,
                    'duration': duration
                }
                
            except Exception as update_error:
                # Registrar error si existe el log
                if log:
                    try:
                        duration = time.time() - start_time
                        log.mark_error(str(update_error), duration)
                    except Exception:
                        _logger.exception("No se pudo marcar como fallido el log de actualización")
                raise
                
        except AccessError as e:
            return {
                'success': False,
                'error': str(e)
            }
        except UserError as e:
            return {
                'success': False,
                'error': str(e)
            }
        except Exception as e:
            _logger.error(f"Error actualizando módulo: {str(e)}")
            return {
                'success': False,
                'error': _('Error al actualizar el módulo: %s') % str(e)
            }
    
    @http.route('/module_updater_dz/get_modules', type='json', auth='user')
    def get_installed_modules(self):
        """Obtiene todos los módulos instalados (mantenido por compatibilidad)"""
        try:
            if not request.env.user.has_group('base.group_system'):
                return {'modules': [], 'updates_count': 0, 'total_count': 0}
            
            Module = request.env['ir.module.module'].sudo()
            modules = Module.search([('state', '=', 'installed')])
            
            module_list = []
            for module in modules:
                module_info = {
                    'id': module.id,
                    'name': module.name,
                    'display_name': module.shortdesc or module.name,
                    'version': module.installed_version or '1.0',
                    'state': 'updated',
                    'application': module.application,
                }
                module_list.append(module_info)
            
            return {
                'modules': module_list,
                'updates_count': 0,
                'total_count': len(module_list)
            }
            
        except Exception as e:
            _logger.error(f"Error obteniendo módulos: {str(e)}")
            return {
                'modules': [],
                'updates_count': 0,
                'total_count': 0
            }
