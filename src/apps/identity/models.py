import hashlib
import secrets
import uuid

from django.db import models


class ApiClient(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, unique=True)
    key_hash = models.CharField(max_length=64, unique=True)
    scopes = models.JSONField(default=list)
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="created_clients",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "api_clients"
        indexes = [
            models.Index(fields=["is_active"]),
            models.Index(fields=["created_by", "-created_at"]),
        ]

    @staticmethod
    def hash_key(raw_key: str) -> str:
        return hashlib.sha256(raw_key.encode()).hexdigest()

    @classmethod
    def generate_key(cls) -> str:
        return f"sc_{secrets.token_urlsafe(32)}"

    @classmethod
    def create_client(
        cls,
        name: str,
        scopes: list[str],
        *,
        created_by_id: uuid.UUID | None = None,
    ) -> tuple["ApiClient", str]:
        raw_key = cls.generate_key()
        client = cls.objects.create(
            name=name,
            key_hash=cls.hash_key(raw_key),
            scopes=scopes,
            created_by_id=created_by_id,
        )
        return client, raw_key

    def __str__(self):
        return self.name
