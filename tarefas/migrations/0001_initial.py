from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Tarefa",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("titulo", models.CharField(max_length=120)),
                ("descricao", models.TextField(blank=True)),
                ("prioridade", models.CharField(choices=[("baixa", "Baixa"), ("media", "Média"), ("alta", "Alta")], default="media", max_length=5)),
                ("concluida", models.BooleanField(default=False)),
                ("criada_em", models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
