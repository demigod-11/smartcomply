from django.conf import settings
from django.core.management.base import BaseCommand

from apps.identity.models import ApiClient
from apps.rules.models import Rule


class Command(BaseCommand):
    help = "Seed bootstrap API client and sample monitoring rules."

    def handle(self, *args, **options):
        key_hash = ApiClient.hash_key(settings.BOOTSTRAP_API_KEY)
        client, created = ApiClient.objects.get_or_create(
            name="platform-admin",
            defaults={
                "key_hash": key_hash,
                "scopes": ["api_clients:write", "api_clients:read", "api_clients:manage"],
            },
        )
        if created:
            self.stdout.write(self.style.SUCCESS("Created API client: platform-admin"))
        else:
            self.stdout.write("API client already exists: platform-admin")

        rules = [
            {
                "name": "Large Transaction Rule",
                "rule_type": Rule.RuleType.LARGE_TRANSACTION,
                "amount_threshold": 10000,
            },
            {
                "name": "High Frequency Rule",
                "rule_type": Rule.RuleType.HIGH_FREQUENCY,
                "frequency_limit": 5,
                "window_hours": 24,
            },
        ]

        for rule_data in rules:
            _, created = Rule.objects.get_or_create(
                name=rule_data["name"],
                defaults={**rule_data, "is_active": True},
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"Created rule: {rule_data['name']}"))
            else:
                self.stdout.write(f"Rule already exists: {rule_data['name']}")

        self.stdout.write(self.style.SUCCESS("Seed complete."))
