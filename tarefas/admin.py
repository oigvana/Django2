from django.contrib import admin

from .models import Tarefa


@admin.register(Tarefa)
class TarefaAdmin(admin.ModelAdmin):
    list_display = ["titulo", "prioridade", "concluida", "criada_em"]
    list_filter = ["prioridade", "concluida"]
    search_fields = ["titulo"]
    list_per_page = 20
    readonly_fields = ["criada_em"]
    fieldsets = [
        ("Informações da tarefa", {"fields": ["titulo", "descricao", "prioridade", "prazo"]}),
        ("Status", {"fields": ["concluida", "criada_em"]}),
    ]
