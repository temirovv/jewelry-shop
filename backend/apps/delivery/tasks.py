import logging

from celery import shared_task

logger = logging.getLogger(__name__)

# BTS status → Order status mapping
BTS_STATUS_MAP = {
    "created": "processing",
    "accepted": "processing",
    "in_transit": "shipped",
    "on_delivery": "shipped",
    "delivered": "delivered",
    "returned": "cancelled",
    "cancelled": "cancelled",
}


@shared_task
def send_order_to_bts(order_id: int):
    """Buyurtmani BTS ga yuborish (async)."""
    from apps.orders.models import Order
    from .services import create_bts_shipment

    try:
        order = Order.objects.select_related(
            "user", "delivery_region", "delivery_city"
        ).get(id=order_id)
    except Order.DoesNotExist:
        logger.error(f"Order #{order_id} not found for BTS shipment")
        return

    if order.bts_shipment_id:
        logger.info(f"Order #{order_id} already has BTS shipment, skipping")
        return

    if not order.delivery_region or not order.delivery_city:
        logger.info(f"Order #{order_id} has no BTS delivery info, skipping")
        return

    try:
        result = create_bts_shipment(order)
        order.bts_shipment_id = result["shipment_id"]
        order.bts_tracking_code = result["tracking_code"]
        order.bts_status = "created"
        order.save(update_fields=["bts_shipment_id", "bts_tracking_code", "bts_status"])
        logger.info(f"Order #{order_id} sent to BTS: tracking={result['tracking_code']}")
    except Exception as e:
        logger.error(f"Failed to send order #{order_id} to BTS: {e}")


@shared_task
def sync_bts_tracking():
    """Sync BTS tracking statuses for active orders (Celery cron every 2 hours)."""
    from apps.orders.models import Order
    from apps.orders.utils import send_status_notification
    from .services import get_bts_tracking

    active_statuses = ["confirmed", "processing", "shipped"]
    orders = Order.objects.filter(
        status__in=active_statuses,
        bts_shipment_id__isnull=False,
    ).exclude(bts_shipment_id="")

    updated = 0
    for order in orders:
        try:
            tracking_data = get_bts_tracking(order.bts_shipment_id)
            bts_status = (
                tracking_data.get("status", "")
                .lower()
                .replace(" ", "_")
            )

            new_order_status = BTS_STATUS_MAP.get(bts_status)
            if not new_order_status or new_order_status == order.status:
                # Update bts_status field even if order status unchanged
                if bts_status and bts_status != order.bts_status:
                    order.bts_status = bts_status
                    order.save(update_fields=["bts_status"])
                continue

            old_status = order.status
            order.status = new_order_status
            order.bts_status = bts_status
            order.save(update_fields=["status", "bts_status"])

            try:
                send_status_notification(order, new_order_status)
            except Exception as e:
                logger.error(f"Failed to send notification for order #{order.id}: {e}")

            updated += 1
            logger.info(
                f"Order #{order.id} status updated: {old_status} -> {new_order_status} (BTS: {bts_status})"
            )
        except Exception as e:
            logger.warning(f"Failed to sync tracking for order #{order.id}: {e}")

    logger.info(f"BTS tracking sync complete: {updated}/{orders.count()} orders updated")
    return updated
