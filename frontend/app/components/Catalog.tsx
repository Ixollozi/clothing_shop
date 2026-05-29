import { useMemo, useState } from "react";
import { Link } from "react-router";
import { ArrowUpRight, SlidersHorizontal } from "lucide-react";
import { getProducts, getCategoryFilterNames, getUi, getBootstrap, formatHandmadePiecesLine, formatMoney } from "../lib/bootstrap";

export function Catalog() {
  const categories = useMemo(() => getCategoryFilterNames(), []);
  const products = useMemo(() => getProducts(), []);
  const ui = useMemo(() => getUi(), []);
  const lang = useMemo(() => getBootstrap().languageCode, []);
  const allLabel = categories[0] || "Все";
  const [selectedCategory, setSelectedCategory] = useState<string>(allLabel);
  const [sortBy, setSortBy] = useState<string>("default");

  const filtered =
    selectedCategory === allLabel
      ? products
      : products.filter((p) => p.category === selectedCategory);

  const sorted = [...filtered].sort((a, b) => {
    if (sortBy === "price-asc") return a.price - b.price;
    if (sortBy === "price-desc") return b.price - a.price;
    return 0;
  });

  return (
    <div className="bg-[#F7F3EE] min-h-screen" style={{ fontFamily: "'DM Sans', sans-serif" }}>
      {/* Header */}
      <div className="bg-[#1C1714] pt-32 pb-16 px-6 lg:px-12">
        <div className="max-w-7xl mx-auto">
          <p className="text-[#D4895A] text-xs tracking-widest uppercase mb-4" style={{ fontSize: "0.65rem" }}>
            {ui.catalogCollectionEyebrow || "Наша коллекция"}
          </p>
          <h1
            className="text-white"
            style={{
              fontFamily: "'Cormorant Garamond', serif",
              fontSize: "clamp(2.5rem, 5vw, 4.5rem)",
              fontWeight: 300,
              lineHeight: 1.05,
            }}
          >
            {ui.catalogTitle || "Каталог"}
          </h1>
          <p className="text-[#A99A8C] mt-4 text-sm" style={{ maxWidth: "400px", lineHeight: 1.7 }}>
            {formatHandmadePiecesLine(sorted.length, lang)}
          </p>
        </div>
      </div>

      {/* Filters */}
      <div className="sticky top-16 md:top-20 z-30 bg-[#F7F3EE] border-b border-[#E0D5C8] px-6 lg:px-12 py-4">
        <div className="max-w-7xl mx-auto flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
          {/* Category pills */}
          <div className="flex flex-wrap gap-2">
            {categories.map((cat) => (
              <button
                key={cat}
                onClick={() => setSelectedCategory(cat)}
                className={`px-5 py-2 text-xs tracking-widest uppercase transition-all duration-200 ${
                  selectedCategory === cat
                    ? "bg-[#1C1714] text-white"
                    : "bg-transparent text-[#6B5E54] border border-[#D5C9BC] hover:border-[#1C1714] hover:text-[#1C1714]"
                }`}
                style={{ fontSize: "0.65rem", letterSpacing: "0.12em" }}
              >
                {cat}
              </button>
            ))}
          </div>

          {/* Sort */}
          <div className="flex items-center gap-2 text-[#6B5E54]">
            <SlidersHorizontal className="w-4 h-4" />
            <select
              value={sortBy}
              onChange={(e) => setSortBy(e.target.value)}
              className="bg-transparent text-xs outline-none cursor-pointer"
              style={{ fontSize: "0.75rem" }}
            >
              <option value="default">{ui.sortDefault || "По умолчанию"}</option>
              <option value="price-asc">{ui.sortPriceAsc || "Цена: дешевле"}</option>
              <option value="price-desc">{ui.sortPriceDesc || "Цена: дороже"}</option>
            </select>
          </div>
        </div>
      </div>

      {/* Grid */}
      <div className="max-w-7xl mx-auto px-6 lg:px-12 py-12">
        {sorted.length === 0 ? (
          <div className="text-center py-24">
            <p
              className="text-[#1C1714]"
              style={{ fontFamily: "'Cormorant Garamond', serif", fontSize: "1.5rem", fontWeight: 300 }}
            >
              {ui.catalogNoProducts || "Товары не найдены"}
            </p>
          </div>
        ) : (
          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4 md:gap-6">
            {sorted.map((product) => (
              <Link key={product.id} to={`/product/${product.id}`} className="group block">
                <div
                  className="relative overflow-hidden bg-[#EDE5DA] mb-4"
                  style={{ aspectRatio: "3/4" }}
                >
                  <img
                    src={product.image}
                    alt={product.name}
                    className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-700"
                  />
                  {/* Overlay */}
                  <div className="absolute inset-0 bg-[#1C1714]/0 group-hover:bg-[#1C1714]/15 transition-colors duration-500" />

                  {/* Badges */}
                  <div className="absolute top-3 left-3 flex flex-col gap-1">
                    {product.isNew && (
                      <span className="bg-[#B85538] text-white px-2 py-1 text-[10px] tracking-widest uppercase">
                        {ui.badgeNew || "Новинка"}
                      </span>
                    )}
                    {product.isBestseller && (
                      <span className="bg-[#1C1714] text-white px-2 py-1 text-[10px] tracking-widest uppercase">
                        {ui.badgeHit || "Хит"}
                      </span>
                    )}
                  </div>

                  {/* Quick view btn */}
                  <div className="absolute bottom-3 right-3 opacity-0 group-hover:opacity-100 transition-all duration-300 translate-y-2 group-hover:translate-y-0">
                    <div className="bg-white w-9 h-9 flex items-center justify-center shadow-md">
                      <ArrowUpRight className="w-4 h-4 text-[#1C1714]" />
                    </div>
                  </div>
                </div>

                <p className="text-[#6B5E54] text-xs tracking-widest uppercase mb-1" style={{ fontSize: "0.6rem" }}>
                  {product.category}
                </p>
                <p className="text-[#1C1714] mb-2 leading-snug" style={{ fontSize: "0.875rem" }}>
                  {product.name}
                </p>
                <p className="text-[#B85538]" style={{ fontSize: "0.875rem" }}>
                  {formatMoney(product.price, lang)}
                </p>
              </Link>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
