import { Link } from "react-router";
import { Trash2, Plus, Minus, ShoppingBag, ArrowLeft, ArrowRight } from "lucide-react";
import { useMemo } from "react";
import { useCart } from "../context/CartContext";
import { getUi, getBootstrap, formatMoney, formatCartItemsLine } from "../lib/bootstrap";

export function Cart() {
  const { items, removeFromCart, updateQuantity, getTotalPrice } = useCart();
  const ui = useMemo(() => getUi(), []);
  const lang = useMemo(() => getBootstrap().languageCode, []);

  if (items.length === 0) {
    return (
      <div
        className="min-h-screen bg-[#F7F3EE] flex flex-col items-center justify-center px-6 text-center"
        style={{ fontFamily: "'DM Sans', sans-serif" }}
      >
        <ShoppingBag className="w-16 h-16 text-[#D5C9BC] mb-8" />
        <p className="text-[#A99A8C] text-xs tracking-widest uppercase mb-4" style={{ fontSize: "0.65rem" }}>
          {ui.cartEmptyLabel || "Пусто"}
        </p>
        <h1
          className="text-[#1C1714] mb-6"
          style={{
            fontFamily: "'Cormorant Garamond', serif",
            fontSize: "clamp(1.8rem, 3vw, 2.5rem)",
            fontWeight: 300,
          }}
        >
          {ui.cartEmptyTitle || "Корзина пуста"}
        </h1>
        <p className="text-[#6B5E54] text-sm mb-10" style={{ lineHeight: 1.8 }}>
          {ui.cartEmptyBody || ""}
        </p>
        <Link
          to="/catalog"
          className="inline-flex items-center gap-3 bg-[#1C1714] text-white px-8 py-4 hover:bg-[#B85538] transition-colors text-xs tracking-widest uppercase"
          style={{ letterSpacing: "0.15em", fontSize: "0.7rem" }}
        >
          {ui.toCatalog || "В каталог"} <ArrowRight className="w-4 h-4" />
        </Link>
      </div>
    );
  }

  return (
    <div
      className="min-h-screen bg-[#F7F3EE]"
      style={{ fontFamily: "'DM Sans', sans-serif" }}
    >
      {/* Header */}
      <div className="bg-[#1C1714] pt-28 pb-12 px-6 lg:px-12">
        <div className="max-w-7xl mx-auto">
          <p className="text-[#D4895A] text-xs tracking-widest uppercase mb-4" style={{ fontSize: "0.65rem" }}>
            {ui.cartYourChoice || "Ваш выбор"}
          </p>
          <h1
            className="text-white"
            style={{
              fontFamily: "'Cormorant Garamond', serif",
              fontSize: "clamp(2rem, 4vw, 3.5rem)",
              fontWeight: 300,
            }}
          >
            {ui.cartTitle || "Корзина"}
          </h1>
        </div>
      </div>

      {/* Content */}
      <div className="max-w-7xl mx-auto px-6 lg:px-12 py-12">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-10">
          {/* Items */}
          <div className="lg:col-span-2 space-y-4">
            <Link
              to="/catalog"
              className="inline-flex items-center gap-2 text-[#6B5E54] hover:text-[#B85538] transition-colors text-xs tracking-wider mb-4"
              style={{ fontSize: "0.7rem", letterSpacing: "0.1em" }}
            >
              <ArrowLeft className="w-3 h-3" /> {(ui.continueShopping || "Продолжить покупки").toUpperCase()}
            </Link>

            {items.map((item) => (
              <div
                key={item.cartLineId ?? item.id}
                className="bg-white border border-[#E8DED4] flex gap-4 md:gap-6 p-4 md:p-6 group"
              >
                {/* Image */}
                <Link to={`/product/${item.id}`} className="flex-shrink-0">
                  <div className="w-20 h-20 md:w-28 md:h-28 overflow-hidden bg-[#EDE5DA]">
                    <img
                      src={item.image}
                      alt={item.name}
                      className="w-full h-full object-cover hover:scale-105 transition-transform duration-500"
                    />
                  </div>
                </Link>

                {/* Info */}
                <div className="flex-1 min-w-0">
                  <p className="text-[#A99A8C] text-xs tracking-widest uppercase mb-1" style={{ fontSize: "0.6rem" }}>
                    {item.category}
                  </p>
                  <Link to={`/product/${item.id}`}>
                    <p
                      className="text-[#1C1714] hover:text-[#B85538] transition-colors mb-2"
                      style={{ fontSize: "0.9rem", lineHeight: 1.4 }}
                    >
                      {item.name}
                    </p>
                  </Link>
                  <p className="text-[#B85538]" style={{ fontSize: "0.85rem" }}>
                    {formatMoney(item.price, lang)} / {ui.perUnit || "шт."}
                  </p>
                </div>

                {/* Quantity + Total + Delete */}
                <div className="flex flex-col items-end justify-between gap-3">
                  <button
                    onClick={() => void removeFromCart(item.id)}
                    className="text-[#D5C9BC] hover:text-[#B85538] transition-colors p-1"
                  >
                    <Trash2 className="w-4 h-4" />
                  </button>

                  <div className="flex items-center border border-[#E0D5C8]">
                    <button
                      onClick={() => void updateQuantity(item.id, item.quantity - 1)}
                      className="w-8 h-8 flex items-center justify-center text-[#6B5E54] hover:bg-[#EDE5DA] transition-colors"
                    >
                      <Minus className="w-3 h-3" />
                    </button>
                    <span
                      className="w-10 text-center text-[#1C1714]"
                      style={{ fontSize: "0.85rem" }}
                    >
                      {item.quantity}
                    </span>
                    <button
                      onClick={() => void updateQuantity(item.id, item.quantity + 1)}
                      className="w-8 h-8 flex items-center justify-center text-[#6B5E54] hover:bg-[#EDE5DA] transition-colors"
                    >
                      <Plus className="w-3 h-3" />
                    </button>
                  </div>

                  <p className="text-[#1C1714]" style={{ fontSize: "0.9rem" }}>
                    {formatMoney(item.price * item.quantity, lang)}
                  </p>
                </div>
              </div>
            ))}
          </div>

          {/* Summary */}
          <div className="lg:col-span-1">
            <div className="bg-[#1C1714] p-8 sticky top-28">
              <p
                className="text-white mb-8"
                style={{ fontFamily: "'Cormorant Garamond', serif", fontSize: "1.5rem", fontWeight: 300 }}
              >
                {ui.totalLabel || "Итого"}
              </p>

              <div className="space-y-4 mb-8">
                <div className="flex justify-between text-[#A99A8C] text-sm">
                  <span>{formatCartItemsLine(items.reduce((s, i) => s + i.quantity, 0), lang)}</span>
                  <span>{formatMoney(getTotalPrice(), lang)}</span>
                </div>
                <div className="flex justify-between text-[#A99A8C] text-sm">
                  <span>{ui.deliveryLabel || "Доставка"}</span>
                  <span className="text-[#D4895A]">{ui.deliveryAtCheckout || "При оформлении"}</span>
                </div>
              </div>

              <div className="border-t border-[#2E2520] pt-6 mb-8">
                <div className="flex justify-between items-baseline">
                  <span className="text-[#A99A8C] text-xs tracking-widest uppercase" style={{ fontSize: "0.65rem" }}>
                    {ui.toPayLabel || "К оплате"}
                  </span>
                  <span
                    className="text-white"
                    style={{ fontFamily: "'Cormorant Garamond', serif", fontSize: "1.6rem", fontWeight: 300 }}
                  >
                    {formatMoney(getTotalPrice(), lang)}
                  </span>
                </div>
              </div>

              <Link
                to="/checkout"
                className="w-full block text-center bg-[#B85538] text-white py-4 hover:bg-[#9E4630] transition-colors text-xs tracking-widest uppercase mb-4"
                style={{ letterSpacing: "0.15em", fontSize: "0.7rem" }}
              >
                {ui.checkoutButton || "Оформить заказ"}
              </Link>

              <p className="text-[#6B5E54] text-center text-xs" style={{ lineHeight: 1.6, fontSize: "0.7rem" }}>
                {ui.cartTrustFootnote || ""}
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
