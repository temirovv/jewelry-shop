import logging

from django.conf import settings

from .bts_client import get_bts_client
from .models import BTSRegion, BTSCity

logger = logging.getLogger(__name__)


def sync_regions_and_cities():
    """Sync BTS regions and cities to local database."""
    client = get_bts_client()

    regions = client.get_regions()
    synced_regions = 0
    synced_cities = 0

    for region_data in regions:
        region_id = region_data.get("id") or region_data.get("region_id")
        region_name = region_data.get("name") or region_data.get("region_name", "")
        if not region_id:
            continue

        region, _ = BTSRegion.objects.update_or_create(
            bts_id=region_id,
            defaults={"name": region_name},
        )
        synced_regions += 1

        try:
            cities = client.get_cities(region_id)
            for city_data in cities:
                city_id = city_data.get("id") or city_data.get("city_id")
                city_name = city_data.get("name") or city_data.get("city_name", "")
                if not city_id:
                    continue

                BTSCity.objects.update_or_create(
                    bts_id=city_id,
                    defaults={"region": region, "name": city_name},
                )
                synced_cities += 1
        except Exception as e:
            logger.warning(f"Failed to sync cities for region {region_name}: {e}")

    logger.info(f"BTS sync complete: {synced_regions} regions, {synced_cities} cities")
    return synced_regions, synced_cities


def calculate_delivery_cost(region_id: int, city_id: int, weight: float = 0.5) -> dict:
    """Calculate delivery cost via BTS API."""
    client = get_bts_client()
    sender_region = int(getattr(settings, "BTS_SENDER_REGION_ID", 0))

    result = client.calculate_delivery(
        sender_region=sender_region,
        receiver_region=region_id,
        receiver_city=city_id,
        weight=weight,
    )

    delivery_fee = result.get("price") or result.get("cost") or result.get("total", 0)
    estimated_days = result.get("delivery_days") or result.get("estimated_days") or result.get("days")

    return {
        "delivery_fee": delivery_fee,
        "estimated_days": estimated_days,
    }


def create_bts_shipment(order) -> dict:
    """Create a BTS shipment for an order."""
    client = get_bts_client()
    sender_region = int(getattr(settings, "BTS_SENDER_REGION_ID", 0))
    sender_city = int(getattr(settings, "BTS_SENDER_CITY_ID", 0))

    items_description = ", ".join(
        f"{item.product.name} x{item.quantity}" for item in order.items.all()
    )

    order_data = {
        "sender_region_id": sender_region,
        "sender_city_id": sender_city,
        "receiver_region_id": order.delivery_region.bts_id if order.delivery_region else 0,
        "receiver_city_id": order.delivery_city.bts_id if order.delivery_city else 0,
        "receiver_name": order.user.full_name or order.user.first_name,
        "receiver_phone": order.phone,
        "receiver_address": order.delivery_address or "",
        "weight": 0.5,
        "description": items_description[:200],
        "cod_amount": float(order.total) if order.payment_method == "cash" else 0,
    }

    result = client.create_order(order_data)

    shipment_id = str(result.get("shipment_id") or result.get("id", ""))
    tracking_code = str(result.get("tracking_code") or result.get("barcode") or shipment_id)

    return {
        "shipment_id": shipment_id,
        "tracking_code": tracking_code,
    }


def get_bts_tracking(shipment_id: str) -> dict:
    """Get tracking status from BTS."""
    client = get_bts_client()
    return client.get_tracking(shipment_id)
