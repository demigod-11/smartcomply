from loguru import logger

from apps.alerts.usecases.evaluate_transaction import evaluate_transaction


def run(transaction_id: str) -> None:
    logger.info("evaluating_transaction transaction_id={}", transaction_id)
    alerts = evaluate_transaction(transaction_id)
    logger.info(
        "evaluation_complete transaction_id={} alerts_created={}",
        transaction_id,
        len(alerts),
    )
