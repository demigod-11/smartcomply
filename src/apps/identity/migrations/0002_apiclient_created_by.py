import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("identity", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="apiclient",
            name="created_by",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="created_clients",
                to="identity.apiclient",
            ),
        ),
        migrations.AddIndex(
            model_name="apiclient",
            index=models.Index(
                fields=["created_by", "-created_at"],
                name="api_clients_created_0f8e2a_idx",
            ),
        ),
    ]
