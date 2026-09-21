from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0002_remove_project_name_project_title_alter_project_link"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="project",
            options={"ordering": ["id"]},
        ),
        migrations.AlterField(
            model_name="project",
            name="description",
            field=models.TextField(blank=True),
        ),
    ]
