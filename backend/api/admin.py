from django.contrib import admin
from .models import Usuario


@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'nombre', 'apellidos', 'email', 'ciudad',
        'nivel_riesgo', 'created_at', 'google_sheet_synced'
    ]
    list_filter = ['ciudad', 'google_sheet_synced', 'created_at']
    search_fields = ['nombre', 'apellidos', 'email', 'ciudad']
    readonly_fields = ['created_at', 'google_sheet_synced']