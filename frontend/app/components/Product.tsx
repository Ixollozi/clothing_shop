import { useParams, Link } from "react-router";
import { ArrowLeft, ShoppingBag, Check, Truck, Shield, RotateCcw } from "lucide-react";
import { useCart } from "../context/CartContext";
import { getProducts, getProductFeatures, getUi, getBootstrap, formatMoney } from "../lib/bootstrap";
import { useMemo, useState } from "react";

export function Product() {
  const { id } = useParams();
  const products = useMemo(() => getProducts(), []);
  const productFeatures = useMemo(() => getProductFeatures().slice(0, 3), []);
  const ui = useMemo(() => getUi(), []);
  const lang = useMemo(() => getBootstrap().languageCode, []);
  const { addToCart, items } = useCart();
  const [added, setAdded] = useState(false);

  const product = products.find((p) => p.id === Number(id));
  const related = products.filter((p) => p.category === product?.category && p.id !== product?.id).slice(0, 4);

  const inCart = items.some((item) => item.id === Number(id));

  const handleAdd = async () => {
    if (!product) return;
    await addToCart({
      id: product.id,
      slug: product.slug,
      name: product.name,
      price: product.price,
      image: product.image,
      description: product.description,
      category: product.category,
      material: product.material ?? "",
      dimensions: product.dimensions ?? "",
      inStock: product.inStock,
      isNew: product.isNew,
      isBestseller: product.isBestseller,
    });
    setAdded(true);
    setTimeout(() => setAdded(false), 2000);
  };

  if (!product) {
    return (
      <div className="min-h-screen bg-[#F7F3EE] flex items-center justify-center" style={{ fontFamily: "'DM Sans', sans-serif" }}>
        <div className="text-center">
          <p
            className="text-[#1C1714] mb-6"
            style={{ fontFamily: "'Cormorant Garamond', serif", fontSize: "2rem", fontWeight: 300 }}
          >
            {ui.productNotFound || "Товар не найден"}
          </p>
          <Link
            to="/catalog"
            className="inline-flex items-center gap-2 text-[#B85538] text-sm border-b border-[#B85538] pb-1"
          >
            <ArrowLeft className="w-4 h-4" /> {ui.backToCatalog || "Вернуться в каталог"}
          </Link>
        </div>
      </div>
    );
  }

  return (
    <div className="bg-[#F7F3EE] min-h-screen" style={{ fontFamily: "'DM Sans', sans-serif" }}>
      {/* Breadcrumb */}
      <div className="pt-24 md:pt-28 px-6 lg:px-12 pb-6 max-w-7xl mx-auto">
        <Link
          to="/catalog"
          className="inline-flex items-center gap-2 text-[#6B5E54] hover:text-[#B85538] transition-colors text-xs tracking-wider"
          style={{ letterSpacing: "0.1em", fontSize: "0.7rem" }}
        >
          <ArrowLeft className="w-3 h-3" /> {(ui.breadcrumbCatalog || "Каталог").toUpperCase()}
        </Link>
        <span className="text-[#D5C9BC] mx-3" style={{ fontSize: "0.7rem" }}>·</span>
        <span className="text-[#6B5E54]" style={{ fontSize: "0.7rem", letterSpacing: "0.1em" }}>{product.category.toUpperCase()}</span>
      </div>

      {/* Main Content */}
      <div className="max-w-7xl mx-auto px-6 lg:px-12 pb-20">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-10 lg:gap-20">
          {/* Image */}
          <div className="relative">
            <div className="bg-[#EDE5DA] overflow-hidden" style={{ aspectRatio: "4/5" }}>
              <img
                src={product.image}
                alt={product.name}
                className="w-full h-full object-cover"
              />
            </div>
            {/* Floating badge */}
            {product.isNew && (
              <div
                className="absolute top-5 left-5 bg-[#B85538] text-white px-3 py-1 text-[10px] tracking-widest uppercase"
              >
                {ui.badgeNew || "Новинка"}
              </div>
            )}
          </div>

          {/* Info */}
          <div className="flex flex-col justify-center">
            <p className="text-[#6B5E54] text-xs tracking-widest uppercase mb-4" style={{ fontSize: "0.65rem" }}>
              {product.category} · {product.material}
            </p>

            <h1
              className="text-[#1C1714] mb-4"
              style={{
                fontFamily: "'Cormorant Garamond', serif",
                fontSize: "clamp(2rem, 3.5vw, 3rem)",
                fontWeight: 300,
                lineHeight: 1.1,
              }}
            >
              {product.name}
            </h1>

            <p
              className="text-[#B85538] mb-8"
              style={{
                fontFamily: "'Cormorant Garamond', serif",
                fontSize: "1.75rem",
                fontWeight: 300,
              }}
            >
              {formatMoney(product.price, lang)}
            </p>

            <p className="text-[#6B5E54] mb-10 leading-relaxed text-sm" style={{ lineHeight: 1.85 }}>
              {product.description}
            </p>

            {/* Specs */}
            <div className="border-t border-b border-[#E0D5C8] py-6 mb-8 space-y-3">
              {[
                { label: ui.labelMaterial || "Материал", value: product.material },
                { label: ui.labelDimensions || "Размеры", value: product.dimensions },
                { label: ui.labelCategory || "Категория", value: product.category },
                {
                  label: ui.labelAvailability || "Наличие",
                  value: product.inStock ? ui.inStock || "В наличии" : ui.madeToOrder || "Под заказ",
                  accent: product.inStock,
                },
              ].map((spec) => (
                <div key={spec.label} className="flex justify-between items-center">
                  <span className="text-[#A99A8C] text-xs tracking-wider uppercase" style={{ fontSize: "0.65rem" }}>
                    {spec.label}
                  </span>
                  <span
                    className={`text-sm ${spec.accent ? "text-[#5A8C5A]" : "text-[#1C1714]"}`}
                    style={{ fontSize: "0.85rem" }}
                  >
                    {spec.value}
                  </span>
                </div>
              ))}
            </div>

            {/* Add to Cart */}
            <button
              onClick={handleAdd}
              className={`w-full py-4 flex items-center justify-center gap-3 transition-all duration-300 text-sm tracking-widest uppercase mb-4 ${
                added || inCart
                  ? "bg-[#5A8C5A] text-white"
                  : "bg-[#1C1714] text-white hover:bg-[#B85538]"
              }`}
              style={{ letterSpacing: "0.15em", fontSize: "0.7rem" }}
            >
              {added ? (
                <>
                  <Check className="w-4 h-4" /> {ui.addedToCart || "Добавлено"}
                </>
              ) : inCart ? (
                <>
                  <Check className="w-4 h-4" /> {ui.inCartLabel || "В корзине"}
                </>
              ) : (
                <>
                  <ShoppingBag className="w-4 h-4" /> {ui.addToCart || "Добавить в корзину"}
                </>
              )}
            </button>

            <Link
              to="/cart"
              className="w-full py-4 border border-[#1C1714] text-[#1C1714] text-center hover:bg-[#1C1714] hover:text-white transition-all duration-300 text-sm tracking-widest uppercase"
              style={{ letterSpacing: "0.15em", fontSize: "0.7rem", display: "block" }}
            >
              {ui.goToCart || "Перейти в корзину"}
            </Link>

            {/* Trust Signals */}
            <div className="grid grid-cols-3 gap-4 mt-10">
              {productFeatures.length > 0
                ? productFeatures.map((f) => (
                    <div key={f.title} className="text-center">
                      <i className={`${f.icon} text-[#B85538] text-lg mb-2`} aria-hidden />
                      <p className="text-[#6B5E54]" style={{ fontSize: "0.65rem", lineHeight: 1.4 }}>
                        {f.text}
                      </p>
                    </div>
                  ))
                : [
                    { icon: Truck, label: ui.trustShipping || "Доставка 3–7 дней" },
                    { icon: Shield, label: ui.trustQuality || "Гарантия качества" },
                    { icon: RotateCcw, label: ui.trustReturns || "Возврат 14 дней" },
                  ].map(({ icon: Icon, label }) => (
                    <div key={label} className="text-center">
                      <Icon className="w-5 h-5 text-[#B85538] mx-auto mb-2" />
                      <p className="text-[#6B5E54]" style={{ fontSize: "0.65rem", lineHeight: 1.4 }}>
                        {label}
                      </p>
                    </div>
                  ))}
            </div>
          </div>
        </div>

        {/* Related Products */}
        {related.length > 0 && (
          <div className="mt-24">
            <div className="border-t border-[#E0D5C8] pt-16 mb-12">
              <p className="text-[#B85538] text-xs tracking-widest uppercase mb-3" style={{ fontSize: "0.65rem" }}>
                {ui.sameCollection || "Из той же коллекции"}
              </p>
              <h2
                style={{
                  fontFamily: "'Cormorant Garamond', serif",
                  fontSize: "clamp(1.5rem, 3vw, 2.2rem)",
                  fontWeight: 300,
                  color: "#1C1714",
                }}
              >
                {ui.similarPieces || "Похожие изделия"}
              </h2>
            </div>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4 md:gap-6">
              {related.map((rel) => (
                <Link key={rel.id} to={`/product/${rel.id}`} className="group block">
                  <div className="overflow-hidden bg-[#EDE5DA] mb-3" style={{ aspectRatio: "1/1" }}>
                    <img
                      src={rel.image}
                      alt={rel.name}
                      className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-700"
                    />
                  </div>
                  <p className="text-[#1C1714] mb-1" style={{ fontSize: "0.85rem" }}>
                    {rel.name}
                  </p>
                  <p className="text-[#B85538]" style={{ fontSize: "0.85rem" }}>
                    {formatMoney(rel.price, lang)}
                  </p>
                </Link>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}