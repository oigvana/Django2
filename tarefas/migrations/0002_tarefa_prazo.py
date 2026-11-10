from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("tarefas", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="tarefa",
            name="prazo",
            field=models.DateField(blank=True, null=True),
        ),
    ]
