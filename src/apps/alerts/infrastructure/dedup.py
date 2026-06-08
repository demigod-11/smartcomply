from django.core.cache import cache

FREQ_DEDUP_PREFIX = "tm:dedup:freq:"
FREQ_DEDUP_TTL = 86400


def should_create_frequency_alert(account_id: str) -> bool:
    key = f"{FREQ_DEDUP_PREFIX}{account_id}"
    return cache.add(key, "1", FREQ_DEDUP_TTL)
