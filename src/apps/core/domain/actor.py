from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class Actor:
    id: UUID
    name: str
    scopes: frozenset[str]
    type: str = "api_client"

    def has_scope(self, scope: str) -> bool:
        return scope in self.scopes
