/** @odoo-module **/

import { Component, useState, onWillStart, onMounted, useRef } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { _t } from "@web/core/l10n/translation";

export class ModuleUpdaterWidget extends Component {
    static template = "quick_module_updater_dz.ModuleUpdaterWidget";
    static props = {};
    
    setup() {
        this.rpc = useService("rpc");
        this.notification = useService("notification");
        this.action = useService("action");
        this.user = useService("user");
        
        this.searchInputRef = useRef("searchInput");
        
        this.state = useState({
            searchTerm: "",
            allModules: [], // Todos los módulos para mostrar
            favoriteIds: [], // IDs de favoritos guardados en localStorage
            isLoading: false,
            dropdownOpen: false,
            showNoResults: false,
            favoritesLoaded: false, // Flag para saber si ya cargamos los favoritos
        });
        
        // Bind methods
        this.updateModule = this.updateModule.bind(this);
        this.onSearchInput = this.onSearchInput.bind(this);
        this.onKeyDown = this.onKeyDown.bind(this);
        this.toggleDropdown = this.toggleDropdown.bind(this);
        this.toggleFavorite = this.toggleFavorite.bind(this);
        this.onDropdownOpen = this.onDropdownOpen.bind(this);
        
        onWillStart(async () => {
            try {
                this.isAdmin = await this.user.hasGroup("base.group_system");
                // Cargar IDs de favoritos desde localStorage
                this.loadFavoriteIds();
            } catch (error) {
                console.error("Error checking admin rights:", error);
                this.isAdmin = false;
            }
        });
        
        onMounted(() => {
            const dropdownElement = this.searchInputRef.el?.closest('.dropdown');
            if (dropdownElement) {
                dropdownElement.addEventListener('shown.bs.dropdown', this.onDropdownOpen);
            }
        });
    }
    
    onDropdownOpen() {
        // Cargar módulos favoritos cuando se abre el dropdown
        if (!this.state.favoritesLoaded) {
            this.loadFavoriteModules();
        }
        // Focus automático
        setTimeout(() => {
            if (this.searchInputRef.el) {
                this.searchInputRef.el.focus();
            }
        }, 100);
    }
    
    loadFavoriteIds() {
        // Cargar solo los IDs de favoritos desde localStorage
        const stored = localStorage.getItem('module_favorites_dz');
        if (stored) {
            try {
                const ids = JSON.parse(stored);
                // Asegurarse de que sean números
                this.state.favoriteIds = ids.map(id => typeof id === 'string' ? parseInt(id) : id);
                console.log("Favoritos cargados desde localStorage:", this.state.favoriteIds);
            } catch (e) {
                console.error("Error parsing favorites:", e);
                this.state.favoriteIds = [];
            }
        } else {
            this.state.favoriteIds = [];
        }
    }
    
    saveFavorites() {
        // Guardar IDs de favoritos en localStorage
        localStorage.setItem('module_favorites_dz', JSON.stringify(this.state.favoriteIds));
        console.log("Favoritos guardados en localStorage:", this.state.favoriteIds);
    }
    
    async toggleFavorite(moduleId) {
        // Asegurarse de que moduleId sea un número
        moduleId = typeof moduleId === 'string' ? parseInt(moduleId) : moduleId;
        
        const index = this.state.favoriteIds.indexOf(moduleId);
        
        if (index > -1) {
            // Quitar de favoritos
            this.state.favoriteIds.splice(index, 1);
            // Quitar de la lista si no hay búsqueda activa
            if (!this.state.searchTerm) {
                this.state.allModules = this.state.allModules.filter(m => m.id !== moduleId);
            }
        } else {
            // Agregar a favoritos
            this.state.favoriteIds.push(moduleId);
            // Si el módulo está en los resultados, actualizarlo
            const module = this.state.allModules.find(m => m.id === moduleId);
            if (module) {
                module.is_favorite = true;
            }
        }
        
        // Actualizar el estado de favorito en todos los módulos mostrados
        this.state.allModules.forEach(m => {
            m.is_favorite = this.state.favoriteIds.includes(m.id);
        });
        
        // Guardar en localStorage
        this.saveFavorites();
        
        // Forzar re-render
        this.state.allModules = [...this.state.allModules];
    }
    
    toggleDropdown() {
        this.state.dropdownOpen = !this.state.dropdownOpen;
        if (this.state.dropdownOpen) {
            this.state.searchTerm = "";
            this.state.allModules = [];
            this.state.showNoResults = false;
            this.state.favoritesLoaded = false;
        }
    }
    
    async loadFavoriteModules() {
        if (this.state.favoriteIds.length === 0) {
            this.state.allModules = [];
            this.state.favoritesLoaded = true;
            return;
        }
        
        this.state.isLoading = true;
        try {
            const result = await this.rpc("/module_updater_dz/get_favorite_modules", {
                module_ids: this.state.favoriteIds,
            });
            
            if (result.success) {
                const favoriteModules = result.modules || [];
                // Marcar todos como favoritos
                favoriteModules.forEach(m => {
                    m.is_favorite = true;
                });
                
                // Solo mostrar los módulos que siguen estando instalados
                this.state.allModules = favoriteModules;
                
                // Si algún favorito ya no existe, limpiarlo
                if (favoriteModules.length < this.state.favoriteIds.length) {
                    const existingIds = favoriteModules.map(m => m.id);
                    this.state.favoriteIds = this.state.favoriteIds.filter(id => 
                        existingIds.includes(id)
                    );
                    this.saveFavorites();
                }
                
                this.state.favoritesLoaded = true;
            }
        } catch (error) {
            console.error("Error loading favorite modules:", error);
            this.state.favoritesLoaded = true;
        } finally {
            this.state.isLoading = false;
        }
    }
    
    async onSearchInput(ev) {
        const searchValue = ev.target.value.trim();
        this.state.searchTerm = searchValue;
        
        if (!searchValue) {
            // Si no hay búsqueda, recargar favoritos
            this.state.favoritesLoaded = false;
            await this.loadFavoriteModules();
            this.state.showNoResults = false;
            return;
        }
        
        if (searchValue.length < 2) {
            return;
        }
        
        await this.searchModules(searchValue);
    }
    
    async searchModules(searchTerm) {
        this.state.isLoading = true;
        this.state.showNoResults = false;
        
        try {
            const result = await this.rpc("/module_updater_dz/search_module", {
                search_term: searchTerm,
            });
            
            if (result.success) {
                let searchResults = result.modules || [];
                
                // Marcar cuáles son favoritos basándose en localStorage
                searchResults.forEach(m => {
                    m.is_favorite = this.state.favoriteIds.includes(m.id);
                });
                
                // Ordenar: favoritos primero
                searchResults.sort((a, b) => {
                    if (a.is_favorite && !b.is_favorite) return -1;
                    if (!a.is_favorite && b.is_favorite) return 1;
                    return 0;
                });
                
                this.state.allModules = searchResults;
                this.state.showNoResults = searchResults.length === 0;
            } else {
                this.state.allModules = [];
                this.state.showNoResults = true;
            }
        } catch (error) {
            console.error("Error searching modules:", error);
            this.state.allModules = [];
            this.state.showNoResults = true;
        } finally {
            this.state.isLoading = false;
        }
    }
    
    async updateModule(moduleId, moduleName) {
        this.state.isLoading = true;
        
        try {
            const result = await this.rpc("/module_updater_dz/update_module", {
                module_id: moduleId,
            });
            
            if (result.success) {
                this.notification.add(_t(`Módulo ${moduleName} actualizado correctamente`), {
                    type: "success",
                    sticky: false,
                });
                
                // Recargar después de 2 segundos
                setTimeout(() => {
                    window.location.reload();
                }, 2000);
            } else {
                this.notification.add(
                    _t(`Error al actualizar ${moduleName}: `) + (result.error || "Error desconocido"),
                    {
                        type: "danger",
                        sticky: false,
                    }
                );
            }
        } catch (error) {
            console.error("Error updating module:", error);
            this.notification.add(_t(`Error al actualizar el módulo ${moduleName}`), {
                type: "danger",
                sticky: false,
            });
        } finally {
            this.state.isLoading = false;
        }
    }
    
    onKeyDown(ev) {
        if (ev.key === 'Enter') {
            const visibleModules = this.state.allModules;
            if (visibleModules.length === 1) {
                const module = visibleModules[0];
                this.updateModule(module.id, module.display_name);
            }
        }
    }
    
    get favoriteModules() {
        // Solo mostrar favoritos cuando no hay búsqueda
        return this.state.allModules.filter(m => m.is_favorite && !this.state.searchTerm);
    }
    
    get searchResultModules() {
        // Mostrar todos los resultados cuando hay búsqueda
        return this.state.searchTerm ? this.state.allModules : [];
    }
}

ModuleUpdaterWidget.template = "quick_module_updater_dz.ModuleUpdaterWidget";

registry.category("systray").add(
    "ModuleUpdaterWidget",
    {
        Component: ModuleUpdaterWidget,
    },
    { sequence: 10 }
);