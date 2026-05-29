/** Общий тип товара (витрина + корзина). */
export interface Product {
  id: number;
  slug?: string;
  name: string;
  price: number;
  image: string;
  description: string;
  category: string;
  material?: string;
  dimensions?: string;
  inStock?: boolean;
  isNew?: boolean;
  isBestseller?: boolean;
  rating?: number;
  reviewsCount?: number;
}

export type CartLineItem = Product & {
  quantity: number;
  cartLineId?: number;
  /** цвет строки корзины (если API отдал) */
  color?: string;
};
