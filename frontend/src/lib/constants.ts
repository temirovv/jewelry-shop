// Yetkazish narxi konstantalari
export const DELIVERY_FEE = 30000;
export const FREE_DELIVERY_THRESHOLD = 500000;

export function calculateDeliveryFee(total: number): number {
  return total >= FREE_DELIVERY_THRESHOLD ? 0 : DELIVERY_FEE;
}
