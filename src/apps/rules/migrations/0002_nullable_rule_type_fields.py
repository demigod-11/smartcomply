from django.db import migrations, models


def null_irrelevant_rule_fields(apps, schema_editor):
    Rule = apps.get_model("rules", "Rule")
    Rule.objects.filter(rule_type="LARGE_TRANSACTION").update(
        frequency_limit=None,
        window_hours=None,
    )
    Rule.objects.filter(rule_type="HIGH_FREQUENCY").update(amount_threshold=None)


class Migration(migrations.Migration):
    dependencies = [
        ("rules", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="rule",
            name="frequency_limit",
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="rule",
            name="window_hours",
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.RunPython(null_irrelevant_rule_fields, migrations.RunPython.noop),
    ]
