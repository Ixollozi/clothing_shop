import {
  createContext,
  useContext,
  useState,
  ReactNode,
  useCallback,
  useMemo,
} from "react";
import type { Product, CartLineItem } from "../types/product";
import { getBootstrap } from "../lib/bootstrap";
import { mapCartToItems } from "../lib/cartMap";
import {
  fetchCartCurrent,
  postCartAddItem,
  putCartUpdateItem,
  deleteCartRemoveItem,
} from "../lib/api";

export type { Product, CartLineItem } from "../types/product";

interface CartContextType {
  items: CartLineItem[];
  addToCart: (product: Product) => Promise<void>;
  removeFromCart: (productId: number) => Promise<void>;
  updateQuantity: (productId: number, quantity: number) => Promise<void>;
  getTotalPrice: () => number;
  getTotalItems: () => number;
  refreshCart: () => Promise<void>;
}

const CartContext = createContext<CartContextType | undefined>(undefined);

export function CartProvider({ children }: { children: ReactNode }) {
  const initialItems = useMemo(() => {
    const boot = getBootstrap();
    if (boot.initialCart) {
      return mapCartToItems(boot.initialCart as Record<string, unknown>);
    }
    return [];
  }, []);

  const [items, setItems] = useState<CartLineItem[]>(initialItems);

  const refreshCart = useCallback(async () => {
    try {
      const data = await fetchCartCurrent();
      setItems(mapCartToItems(data));
    } catch {
      /* сеть / гость без сессии — оставляем текущее состояние */
    }
  }, []);

  const addToCart = useCallback(
    async (product: Product) => {
      try {
        await postCartAddItem(product.id, 1, "");
        await refreshCart();
      } catch (e) {
        console.error("[cart] addToCart", e);
      }
    },
    [refreshCart]
  );

  const removeFromCart = useCallback(
    async (productId: number) => {
      const line = items.find((i) => i.id === productId);
      try {
        if (line?.cartLineId) {
          await deleteCartRemoveItem(line.cartLineId);
          await refreshCart();
        } else {
          setItems((prev) => prev.filter((i) => i.id !== productId));
        }
      } catch (e) {
        console.error("[cart] removeFromCart", e);
      }
    },
    [items, refreshCart]
  );

  const updateQuantity = useCallback(
    async (productId: number, quantity: number) => {
      const line = items.find((i) => i.id === productId);
      try {
        if (line?.cartLineId) {
          if (quantity <= 0) {
            await deleteCartRemoveItem(line.cartLineId);
          } else {
            await putCartUpdateItem(line.cartLineId, quantity);
          }
          await refreshCart();
        } else {
          setItems((prev) => {
            if (quantity <= 0) return prev.filter((i) => i.id !== productId);
            return prev.map((i) => (i.id === productId ? { ...i, quantity } : i));
          });
        }
      } catch (e) {
        console.error("[cart] updateQuantity", e);
      }
    },
    [items, refreshCart]
  );

  const getTotalPrice = () =>
    items.reduce((sum, item) => sum + item.price * item.quantity, 0);

  const getTotalItems = () => items.reduce((sum, item) => sum + item.quantity, 0);

  return (
    <CartContext.Provider
      value={{
        items,
        addToCart,
        removeFromCart,
        updateQuantity,
        getTotalPrice,
        getTotalItems,
        refreshCart,
      }}
    >
      {children}
    </CartContext.Provider>
  );
}

export function useCart() {
  const context = useContext(CartContext);
  if (!context) {
    throw new Error("useCart must be used within a CartProvider");
  }
  return context;
}
