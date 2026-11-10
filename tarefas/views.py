from django.contrib import messages
from django.db.models import Case, IntegerField, Value, When
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import TarefaForm
from .models import Tarefa


def lista_tarefas(request):
    # Desafio: ordenar por prioridade (alta, média, baixa)
    ordem = Case(
        When(prioridade="alta", then=Value(0)),
        When(prioridade="media", then=Value(1)),
        default=Value(2),
        output_field=IntegerField(),
    )
    tarefas = Tarefa.objects.annotate(ordem=ordem).order_by("ordem", "-criada_em")

    # Desafio: busca por título
    q = request.GET.get("q", "").strip()
    if q:
        tarefas = tarefas.filter(titulo__icontains=q)

    # Filtro por status
    status = request.GET.get("status")
    if status == "pendentes":
        tarefas = tarefas.filter(concluida=False)
    elif status == "concluidas":
        tarefas = tarefas.filter(concluida=True)
    else:
        status = "todas"

    # Desafio: totais de pendentes e concluídas
    contexto = {
        "tarefas": tarefas,
        "status": status,
        "q": q,
        "total_pendentes": Tarefa.objects.filter(concluida=False).count(),
        "total_concluidas": Tarefa.objects.filter(concluida=True).count(),
    }
    return render(request, "lista.html", contexto)


def criar_tarefa(request):
    if request.method == "POST":
        form = TarefaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Tarefa criada com sucesso!")
            return redirect("lista_tarefas")
    else:
        form = TarefaForm()
    return render(request, "formulario.html", {"form": form})


def detalhe_tarefa(request, pk):
    tarefa = get_object_or_404(Tarefa, pk=pk)
    return render(request, "detalhe.html", {"tarefa": tarefa})


def editar_tarefa(request, pk):
    tarefa = get_object_or_404(Tarefa, pk=pk)
    if request.method == "POST":
        form = TarefaForm(request.POST, instance=tarefa)
        if form.is_valid():
            form.save()
            messages.success(request, "Tarefa editada com sucesso!")
            return redirect("detalhe_tarefa", pk=tarefa.pk)
    else:
        form = TarefaForm(instance=tarefa)
    return render(request, "formulario.html", {"form": form, "tarefa": tarefa})


@require_POST
def alternar_tarefa(request, pk):
    tarefa = get_object_or_404(Tarefa, pk=pk)
    tarefa.concluida = not tarefa.concluida
    tarefa.save()
    return redirect("detalhe_tarefa", pk=tarefa.pk)


def excluir_tarefa(request, pk):
    tarefa = get_object_or_404(Tarefa, pk=pk)
    if request.method == "POST":
        tarefa.delete()
        messages.success(request, "Tarefa excluída com sucesso!")
        return redirect("lista_tarefas")
    return render(request, "excluir.html", {"tarefa": tarefa})
