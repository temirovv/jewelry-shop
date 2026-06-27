import apiClient from "./client";
import type { DeliveryRegion, DeliveryZone } from "../../types";

export async function getRegions(): Promise<DeliveryRegion[]> {
  const response = await apiClient.get("/delivery/regions/");
  const data = response.data;
  return Array.isArray(data) ? data : data.results || [];
}

export async function getZones(regionId?: number): Promise<DeliveryZone[]> {
  const url = regionId ? `/delivery/zones/?region=${regionId}` : "/delivery/zones/";
  const response = await apiClient.get(url);
  const data = response.data;
  return Array.isArray(data) ? data : data.results || [];
}

export function calculateZoneFee(zone: DeliveryZone, orderTotal: number): number {
  if (zone.free_threshold > 0 && orderTotal >= zone.free_threshold) {
    return 0;
  }
  return Number(zone.fee);
}
