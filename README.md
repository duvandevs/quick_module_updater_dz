# Quick Module Updater DZ para Odoo 17 CE

## 📋 Descripción

**Quick Module Updater DZ** es un módulo para Odoo 17 Community Edition que agrega un widget de actualización rápida en la barra superior (systray) de Odoo. Permite actualizar módulos instalados con un solo clic, mantener módulos favoritos anclados para acceso inmediato y buscar módulos sin necesidad de navegar a Aplicaciones.

## ✨ Características Principales

### ⭐ **Sistema de Favoritos Anclados**
- Los módulos favoritos aparecen **siempre visibles** al abrir el widget
- No necesitas buscar tus módulos más usados, están anclados al inicio
- Marca/desmarca favoritos con un simple clic en la estrella
- Badge amarillo en el botón principal muestra cantidad de favoritos
- Los favoritos se guardan localmente en tu navegador

### 🔍 **Búsqueda Inteligente con Autofocus**
- **Autofocus automático**: Al abrir el widget, el cursor va directo al campo de búsqueda
- Empieza a escribir inmediatamente sin hacer clic adicional
- Búsqueda en tiempo real (mínimo 2 caracteres)
- Los favoritos no aparecen duplicados en resultados de búsqueda

### 🚀 **Actualización Instantánea**
- Actualiza cualquier módulo con un solo clic
- Sin confirmaciones adicionales para mayor rapidez
- Notificaciones de éxito/error
- Recarga automática después de 2 segundos

### 🎨 **Interfaz Optimizada**
- Widget elegante con gradiente púrpura en la barra superior
- Sección de favoritos con borde amarillo distintivo
- Diseño limpio y minimalista
- Animación sutil en el icono de refresh
- Soporte completo para modo oscuro

## 🚀 Instalación

### Requisitos
- Odoo 17 Community Edition
- Permisos de administrador del sistema

### Pasos de Instalación

1. **Clonar o descargar el módulo**:
   ```bash
   cd /ruta/a/odoo/addons
   git clone https://github.com/tu-usuario/quick_module_updater_dz.git
   ```

2. **Crear la estructura de archivos**:
   ```bash
   mkdir -p quick_module_updater_dz/{models,controllers,security,data,views,static/{description,src/components/module_updater}}
   ```

3. **Copiar todos los archivos** del módulo en sus respectivas ubicaciones

4. **Reiniciar el servidor Odoo**:
   ```bash
   ./odoo-bin -c odoo.conf --dev=all
   ```

5. **Actualizar lista de aplicaciones**:
   - Ir a `Aplicaciones` → `Actualizar lista de aplicaciones`

6. **Instalar el módulo**:
   - Buscar "Quick Module Updater DZ"
   - Click en `Instalar`

## 🎯 Uso

### Flujo de Trabajo Típico

1. **Click en el botón DZ** en la barra superior
2. **Favoritos anclados** aparecen inmediatamente (si tienes)
3. **El cursor se posiciona automáticamente** en el campo de búsqueda
4. **Para actualizar un favorito**: Click directo en su botón "Actualizar"
5. **Para buscar otros módulos**: Simplemente empieza a escribir
6. **Para marcar favorito**: Click en la estrella junto al nombre

### Gestión de Favoritos

#### Agregar a Favoritos
- Busca el módulo deseado
- Click en la **estrella vacía** (⭐) junto al nombre
- El módulo se agrega instantáneamente a la sección de favoritos anclados

#### Usar Favoritos
- Los favoritos aparecen **siempre al inicio** cuando abres el widget
- No necesitas buscarlos, están en la sección amarilla "FAVORITOS"
- Click en "Actualizar" para actualizar directamente

#### Quitar de Favoritos
- Click en la **estrella llena amarilla** (⭐) en cualquier módulo favorito
- El módulo se quita de la sección de favoritos

### Características de Uso

- **Sin búsqueda necesaria**: Los favoritos siempre están visibles
- **Autofocus**: No necesitas hacer clic en el campo de búsqueda
- **Persistencia local**: Los favoritos se guardan en el navegador
- **Badge contador**: Número de favoritos visible en el botón principal
- **Sin duplicados**: Los favoritos no aparecen en resultados de búsqueda

### Atajos de Teclado
- **Enter**: Si hay un solo resultado o un solo favorito, actualiza automáticamente
- **Escribir directamente**: El campo tiene autofocus al abrir

## 🛠️ Estructura Técnica

```
quick_module_updater_dz/
├── __manifest__.py          # Configuración del módulo
├── __init__.py             # Inicialización
├── models/
│   ├── __init__.py
│   └── update_log.py       # Modelo para historial
├── controllers/
│   ├── __init__.py
│   └── main.py            # Endpoints RPC
├── static/src/
│   └── components/
│       └── module_updater/
│           ├── module_updater.js    # Widget JavaScript
│           ├── module_updater.xml   # Template QWeb
│           └── module_updater.scss  # Estilos CSS
├── views/
│   └── update_log_views.xml # Vistas del historial
├── security/
│   └── ir.model.access.csv # Permisos
└── data/
    └── ir_cron.xml        # Tarea programada
```

## 📊 Almacenamiento de Datos

### Favoritos (localStorage)
- Se guardan en el navegador local del usuario
- No se sincronizan entre dispositivos
- Persisten al cerrar sesión
- Array simple de IDs de módulos

### Historial (Base de datos)
- Registro de todas las actualizaciones realizadas
- Información: módulo, versión, usuario, fecha, duración

## 🎨 Elementos Visuales

| Elemento | Descripción |
|----------|-------------|
| 🔄 DZ | Botón principal del widget con gradiente púrpura |
| Badge amarillo | Contador de módulos favoritos |
| ⭐ Amarilla llena | Módulo marcado como favorito |
| ⭐ Gris vacía | Módulo no favorito (click para agregar) |
| Sección FAVORITOS | Área amarilla con favoritos anclados |
| Campo de búsqueda | Con autofocus automático |

## 💡 Ventajas del Sistema Actual

### Eficiencia Máxima
- **0 clicks para buscar**: Autofocus automático
- **1 click para actualizar favoritos**: Siempre visibles
- **2 clicks total**: Abrir widget + actualizar
- **Sin navegación**: Todo desde la barra superior

### Experiencia de Usuario
- **Favoritos anclados**: No pierdes tiempo buscando módulos frecuentes
- **Autofocus inteligente**: Listo para escribir al instante
- **Sin confirmaciones**: Actualizaciones directas
- **Feedback visual**: Notificaciones claras

### Organización
- **Sección de favoritos**: Claramente separada y destacada
- **Sin duplicados**: Los favoritos no aparecen en búsqueda
- **Visual distintivo**: Borde amarillo para favoritos
- **Badge contador**: Sabes cuántos favoritos tienes

## 🔒 Seguridad

- Solo usuarios con grupo `base.group_system` pueden usar el widget
- Todas las operaciones requieren permisos de administrador
- Registro de auditoría en base de datos
- Favoritos privados por navegador/usuario

## 🔧 Troubleshooting

### El widget no aparece
- Verificar permisos de administrador
- Limpiar caché del navegador (Ctrl+F5)
- Reiniciar servidor Odoo

### Los favoritos no se guardan
- Verificar que localStorage esté habilitado en el navegador
- Verificar permisos del navegador para almacenamiento local
- Probar en modo incógnito para descartar extensiones

### El autofocus no funciona
- Verificar que no haya otras extensiones interfiriendo
- Limpiar caché del navegador
- Verificar compatibilidad del navegador

### Error de compilación CSS
- Reiniciar Odoo con `--dev=all`
- Verificar sintaxis del archivo SCSS
- Si persiste, convertir a CSS simple

## 🚦 Flujo de Uso Recomendado

1. **Primera vez**: 
   - Busca tus módulos más usados
   - Márcalos como favoritos

2. **Uso diario**:
   - Click en el botón DZ
   - Tus favoritos están listos
   - Actualiza con un click

3. **Búsqueda ocasional**:
   - Click en el botón DZ
   - Escribe directamente (autofocus)
   - Actualiza o marca como favorito

## ⚠️ Consideraciones Importantes

- **Los favoritos son locales**: No se comparten entre navegadores o dispositivos
- **Sin confirmación**: Las actualizaciones son inmediatas
- **Recarga automática**: La página se recarga 2 segundos después de actualizar
- **Backup recomendado**: Siempre hacer backup antes de actualizar en producción

## 📝 Changelog

### Versión 17.0.1.0.0 (Actual)
- ✅ Sistema de favoritos con localStorage
- ✅ Favoritos anclados siempre visibles
- ✅ Autofocus automático en campo de búsqueda
- ✅ Badge contador de favoritos
- ✅ Sección visual distintiva para favoritos
- ✅ Sin duplicados en resultados
- ✅ Diseño mejorado con gradientes
- ✅ Animación sutil en icono


## 📄 Licencia

LGPL-3

## 👤 Autor

**DZ Development**
- Website: https://github.com/dz
- Módulo: quick_module_updater_dz

## 🤝 Soporte

Para reportar bugs o solicitar nuevas características, por favor abre un issue en el repositorio de GitHub.

---

**Nota**: Este módulo está optimizado para Odoo 17 CE. El sistema de favoritos anclados y autofocus mejora significativamente la productividad al eliminar clicks y búsquedas innecesarias.