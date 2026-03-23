import apiClient from "./client";

export interface BTSRegion {
  id: number;
  bts_id: number;
  name: string;
}

export interface BTSCity {
  id: number;
  bts_id: number;
  name: string;
}

export interface DeliveryCalculation {
  delivery_fee: number;
  estimated_days: number | null;
}

export async function getRegions(): Promise<BTSRegion[]> {
  const response = await apiClient.get<BTSRegion[]>("/delivery/regions/");
  return response.data;
}

export async function getCities(regionBtsId: number): Promise<BTSCity[]> {
  const response = await apiClient.get<BTSCity[]>(
    `/delivery/cities/?region=${regionBtsId}`
  );
  return response.data;
}

export async function calculateDelivery(
  regionId: number,
  cityId: number
): Promise<DeliveryCalculation> {
  const response = await apiClient.post<DeliveryCalculation>(
    "/delivery/calculate/",
    { region_id: regionId, city_id: cityId }
  );
  return response.data;
}
