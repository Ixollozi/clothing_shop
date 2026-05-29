import { Link, useNavigate } from "react-router";
import { useEffect, useMemo, useState, type FormEvent } from "react";
import { ArrowLeft } from "lucide-react";
import { useCart } from "../context/CartContext";
import { getUi, getBootstrap, formatMoney } from "../lib/bootstrap";
import { postCreateOrder } from "../lib/api";

export function Checkout() {
  const navigate = useNavigate();
  const { items, getTotalPrice, refreshCart } = useCart();
  const ui = useMemo(() => getUi(), []);
  const lang = useMemo(() => getBootstrap().languageCode, []);

  const [firstName, setFirstName] = useState("");
  const [phone, setPhone] = useState("");
  const [address, setAddress] = useState("");
  const [city, setCity] = useState("");
  const [notes, setNotes] = useState("");
  const [paymentMethod, setPaymentMethod] = useState("cash");
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [done, setDone] = useState(false);

  useEffect(() => {
    if (items.length === 0 && !done) {
      navigate("/cart", { replace: true });
    }
  }, [items.length, navigate, done]);

  async function onSubmit(e: FormEvent) {
    e.preventDefault();
    setError(null);
    if (!firstName.trim() || !phone.trim() || !address.trim()) {
      setError(ui.checkoutErrorGeneric || "Заполните обязательные поля");
      return;
    }
    setSubmitting(true);
    try {
      await postCreateOrder({
        first_name: firstName.trim(),
        phone: phone.trim(),
        address: address.trim(),
        city: city.trim() || "Ташкент",
        notes: notes.trim(),
        payment_method: paymentMethod,
        items: items.map((i) => ({
          product_id: i.id,
          quantity: i.quantity,
          color: i.color || "",
        })),
      });
      try {
        await refreshCart();
      } catch {
        /* корзина на сервере уже очищена — обновление не критично */
      }
      setDone(true);
    } catch (err) {
      setError(err instanceof Error ? err.message : ui.checkoutErrorGeneric || "Ошибка");
    } finally {
      setSubmitting(false);
    }
  }

  if (done) {
    return (
      <div
        className="min-h-screen bg-[#F7F3EE] flex flex-col items-center justify-center px-6 text-center py-24"
        style={{ fontFamily: "'DM Sans', sans-serif" }}
      >
        <p className="text-[#D4895A] text-xs tracking-widest uppercase mb-4" style={{ fontSize: "0.65rem" }}>
          {ui.checkoutEyebrow || "Доставка"}
        </p>
        <h1
          className="text-[#1C1714] mb-4"
          style={{
            fontFamily: "'Cormorant Garamond', serif",
            fontSize: "clamp(1.8rem, 3vw, 2.5rem)",
            fontWeight: 300,
          }}
        >
          {ui.checkoutSuccessTitle || "Спасибо!"}
        </h1>
        <p className="text-[#6B5E54] text-sm mb-10 max-w-md" style={{ lineHeight: 1.8 }}>
          {ui.checkoutSuccessBody || ""}
        </p>
        <Link
          to="/catalog"
          className="inline-flex items-center gap-3 bg-[#1C1714] text-white px-8 py-4 hover:bg-[#B85538] transition-colors text-xs tracking-widest uppercase"
          style={{ letterSpacing: "0.15em", fontSize: "0.7rem" }}
        >
          {ui.toCatalog || "В каталог"}
        </Link>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-[#F7F3EE]" style={{ fontFamily: "'DM Sans', sans-serif" }}>
      <div className="bg-[#1C1714] pt-28 pb-12 px-6 lg:px-12">
        <div className="max-w-7xl mx-auto">
          <p className="text-[#D4895A] text-xs tracking-widest uppercase mb-4" style={{ fontSize: "0.65rem" }}>
            {ui.checkoutEyebrow || "Доставка"}
          </p>
          <h1
            className="text-white"
            style={{
              fontFamily: "'Cormorant Garamond', serif",
              fontSize: "clamp(2rem, 4vw, 3rem)",
              fontWeight: 300,
            }}
          >
            {ui.checkoutPageTitle || "Оформление заказа"}
          </h1>
        </div>
      </div>

      <div className="max-w-3xl mx-auto px-6 lg:px-12 py-12">
        <Link
          to="/cart"
          className="inline-flex items-center gap-2 text-[#6B5E54] hover:text-[#B85538] transition-colors text-xs tracking-wider mb-8"
          style={{ fontSize: "0.7rem", letterSpacing: "0.1em" }}
        >
          <ArrowLeft className="w-3 h-3" /> {(ui.checkoutBackToCart || "В корзину").toUpperCase()}
        </Link>

        <div className="bg-white border border-[#E8DED4] p-6 md:p-10 mb-8">
          <p className="text-[#A99A8C] text-xs tracking-widest uppercase mb-4" style={{ fontSize: "0.65rem" }}>
            {ui.toPayLabel || "К оплате"}
          </p>
          <p className="text-[#1C1714]" style={{ fontFamily: "'Cormorant Garamond', serif", fontSize: "1.75rem" }}>
            {formatMoney(getTotalPrice(), lang)}
          </p>
        </div>

        <form onSubmit={(e) => void onSubmit(e)} className="space-y-6 bg-white border border-[#E8DED4] p-6 md:p-10">
          {error ? (
            <p className="text-sm text-red-700 bg-red-50 border border-red-200 px-4 py-3" role="alert">
              {error}
            </p>
          ) : null}

          <div>
            <label className="block text-[#6B5E54] text-xs tracking-widest uppercase mb-2" style={{ fontSize: "0.65rem" }}>
              {ui.labelYourName || "Имя"} *
            </label>
            <input
              required
              value={firstName}
              onChange={(e) => setFirstName(e.target.value)}
              className="w-full border border-[#E0D5C8] px-4 py-3 text-[#1C1714] focus:outline-none focus:border-[#B85538]"
            />
          </div>

          <div>
            <label className="block text-[#6B5E54] text-xs tracking-widest uppercase mb-2" style={{ fontSize: "0.65rem" }}>
              {ui.labelPhoneRequired || "Телефон"} *
            </label>
            <input
              required
              type="tel"
              value={phone}
              onChange={(e) => setPhone(e.target.value)}
              className="w-full border border-[#E0D5C8] px-4 py-3 text-[#1C1714] focus:outline-none focus:border-[#B85538]"
            />
          </div>

          <div>
            <label className="block text-[#6B5E54] text-xs tracking-widest uppercase mb-2" style={{ fontSize: "0.65rem" }}>
              {ui.labelCityOptional || "Город"}
            </label>
            <input
              value={city}
              onChange={(e) => setCity(e.target.value)}
              placeholder="Ташкент"
              className="w-full border border-[#E0D5C8] px-4 py-3 text-[#1C1714] focus:outline-none focus:border-[#B85538]"
            />
          </div>

          <div>
            <label className="block text-[#6B5E54] text-xs tracking-widest uppercase mb-2" style={{ fontSize: "0.65rem" }}>
              {ui.labelAddressRequired || "Адрес"} *
            </label>
            <textarea
              required
              rows={3}
              value={address}
              onChange={(e) => setAddress(e.target.value)}
              className="w-full border border-[#E0D5C8] px-4 py-3 text-[#1C1714] focus:outline-none focus:border-[#B85538] resize-y min-h-[5rem]"
            />
          </div>

          <div>
            <label className="block text-[#6B5E54] text-xs tracking-widest uppercase mb-2" style={{ fontSize: "0.65rem" }}>
              {ui.labelPaymentMethod || "Оплата"}
            </label>
            <select
              value={paymentMethod}
              onChange={(e) => setPaymentMethod(e.target.value)}
              className="w-full border border-[#E0D5C8] px-4 py-3 text-[#1C1714] bg-white focus:outline-none focus:border-[#B85538]"
            >
              <option value="cash">{ui.payCash || "Наличные"}</option>
              <option value="card">{ui.payCard || "Карта"}</option>
              <option value="wallet">{ui.payWallet || "Кошелёк"}</option>
              <option value="bank">{ui.payBank || "Перевод"}</option>
            </select>
          </div>

          <div>
            <label className="block text-[#6B5E54] text-xs tracking-widest uppercase mb-2" style={{ fontSize: "0.65rem" }}>
              {ui.labelNotesOptional || "Комментарий"}
            </label>
            <textarea
              rows={2}
              value={notes}
              onChange={(e) => setNotes(e.target.value)}
              className="w-full border border-[#E0D5C8] px-4 py-3 text-[#1C1714] focus:outline-none focus:border-[#B85538] resize-y"
            />
          </div>

          <button
            type="submit"
            disabled={submitting || items.length === 0}
            className="w-full bg-[#B85538] text-white py-4 hover:bg-[#9E4630] transition-colors text-xs tracking-widest uppercase disabled:opacity-50 disabled:pointer-events-none"
            style={{ letterSpacing: "0.15em", fontSize: "0.7rem" }}
          >
            {submitting ? ui.checkoutSubmitting || "…" : ui.checkoutSubmit || "Подтвердить заказ"}
          </button>
        </form>
      </div>
    </div>
  );
}
