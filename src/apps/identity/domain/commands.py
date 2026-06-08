from dataclasses import dataclass


@dataclass(frozen=True)
class CreateApiClientCommand:
    name: str
    scopes: list[str]


@dataclass(frozen=True)
class UpdateApiClientCommand:
    client_id: str
    is_active: bool | None = None
    scopes: list[str] | None = None
