import { Link } from "react-router";
import { ArrowRight, ArrowUpRight } from "lucide-react";
import { useMemo } from "react";
import {
  getProducts,
  getStore,
  getHero,
  getAbout,
  getAboutStats,
  getFeatures,
  getUi,
  getBootstrap,
  formatMoney,
} from "../lib/bootstrap";

const HERO_IMG_FALLBACK =
  "https://images.unsplash.com/photo-1763824371988-8c8eb3d13eff?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&q=80&w=1080";
const ABOUT_IMG_FALLBACK =
  "https://images.unsplash.com/photo-1772487488987-425a4a0c1499?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&q=80&w=1080";

function defaultValueCards(ui: Record<string, string>) {
  return [
    {
      icon: "◌",
      title: ui.defaultValHandmadeTitle || "Ручная работа",
      text: ui.defaultValHandmadeText || "",
    },
    {
      icon: "◎",
      title: ui.defaultValMaterialsTitle || "Живые материалы",
      text: ui.defaultValMaterialsText || "",
    },
    {
      icon: "◈",
      title: ui.defaultValShippingTitle || "Доставка без потерь",
      text: ui.defaultValShippingText || "",
    },
  ];
}

export function Home() {
  const store = useMemo(() => getStore(), []);
  const hero = useMemo(() => getHero(), []);
  const about = useMemo(() => getAbout(), []);
  const products = useMemo(() => getProducts(), []);
  const stats = useMemo(() => getAboutStats(), []);
  const features = useMemo(() => getFeatures(), []);
  const ui = useMemo(() => getUi(), []);
  const lang = useMemo(() => getBootstrap().languageCode, []);

  const heroTitle = (hero?.title || "").trim() || store.title || store.name;
  const heroSubtitle = (hero?.subtitle || "").trim() || (store.description || "").trim();
  const heroImg = (hero?.backgroundImageUrl || "").trim() || HERO_IMG_FALLBACK;
  const heroBtn = (hero?.buttonText || "").trim() || ui.heroBrowseCatalogFallback || "Смотреть каталог";

  const aboutSplitImg = (about?.imageUrl || "").trim() || ABOUT_IMG_FALLBACK;
  const aboutSplitTitle = (about?.title || "").trim() || ui.aboutSplitFallbackTitle || "О мастерской";
  const aboutSplitLead =
    (about?.mission || "").trim() || (about?.description || "").trim() || store.description;
  const valueCards = useMemo(() => {
    if (features.length > 0) {
      return features.slice(0, 3).map((f) => ({
        icon: f.icon?.startsWith("fa") ? "" : "◌",
        faIcon: f.icon?.startsWith("fa") ? f.icon : "",
        title: f.title,
        text: f.description,
      }));
    }
    return defaultValueCards(ui).map((v) => ({ ...v, faIcon: "" as string }));
  }, [features, ui]);

  const featured = useMemo(
    () => products.filter((p) => p.isBestseller).slice(0, 4),
    [products]
  );
  const newArrivals = useMemo(() => products.filter((p) => p.isNew).slice(0, 3), [products]);

  return (
    <div style={{ fontFamily: "'DM Sans', sans-serif" }}>
      {/* ── HERO ── */}
      <section className="relative h-screen min-h-[600px] overflow-hidden">
        <img
          src={heroImg}
          alt={store.name}
          className="absolute inset-0 w-full h-full object-cover"
        />
        <div className="absolute inset-0 bg-gradient-to-r from-[#1C1714]/80 via-[#1C1714]/50 to-transparent" />

        <div className="relative z-10 h-full flex flex-col justify-end pb-20 px-6 lg:px-16 max-w-7xl mx-auto">
          <div className="max-w-2xl">
            <h1
              className="text-white mb-6 whitespace-pre-line"
              style={{
                fontFamily: "'Cormorant Garamond', serif",
                fontSize: "clamp(3rem, 7vw, 6rem)",
                fontWeight: 300,
                lineHeight: 1.05,
                letterSpacing: "-0.01em",
              }}
            >
              {heroTitle}
            </h1>
            {heroSubtitle ? (
              <p className="text-white/70 mb-10 max-w-md whitespace-pre-line" style={{ lineHeight: 1.8, fontSize: "0.95rem" }}>
                {heroSubtitle}
              </p>
            ) : null}
            <div className="flex flex-col sm:flex-row gap-4">
              <Link
                to="/catalog"
                className="inline-flex items-center gap-3 bg-[#B85538] text-white px-8 py-4 hover:bg-[#9E4630] transition-colors duration-300 text-sm tracking-wider"
                style={{ letterSpacing: "0.1em" }}
              >
                {heroBtn.toUpperCase()}
                <ArrowRight className="w-4 h-4" />
              </Link>
              <Link
                to="/about"
                className="inline-flex items-center gap-3 border border-white/50 text-white px-8 py-4 hover:bg-white/10 transition-colors duration-300 text-sm tracking-wider"
                style={{ letterSpacing: "0.1em" }}
              >
                {(ui.aboutWorkshopLink || "О мастерской").toUpperCase()}
              </Link>
            </div>
          </div>
        </div>

        {/* Scroll indicator */}
        <div className="absolute bottom-8 right-12 hidden md:flex flex-col items-center gap-2 text-white/50">
          <div className="w-px h-12 bg-white/30 animate-pulse" />
          <span style={{ fontSize: "0.6rem", letterSpacing: "0.2em", writingMode: "vertical-rl" }}>
            {ui.scrollLabel || "SCROLL"}
          </span>
        </div>
      </section>

      {/* ── STATS BAND ── */}
      {stats.length > 0 ? (
        <section className="bg-[#1C1714] py-8">
          <div className="max-w-7xl mx-auto px-6 lg:px-12">
            <div
              className={`grid gap-8 text-center ${
                stats.length >= 4 ? "grid-cols-2 md:grid-cols-4" : "grid-cols-2 md:grid-cols-3"
              }`}
            >
              {stats.map((stat) => (
                <div key={stat.label}>
                  <p
                    className="text-[#D4895A] mb-1"
                    style={{ fontFamily: "'Cormorant Garamond', serif", fontSize: "1.75rem", fontWeight: 300 }}
                  >
                    {stat.value}
                  </p>
                  <p className="text-[#A99A8C] text-xs tracking-widest uppercase" style={{ fontSize: "0.65rem" }}>
                    {stat.label}
                  </p>
                </div>
              ))}
            </div>
          </div>
        </section>
      ) : null}

      {/* ── BESTSELLERS ── */}
      <section className="py-24 px-6 lg:px-12">
        <div className="max-w-7xl mx-auto">
          <div className="flex items-end justify-between mb-14">
            <div>
              <p className="text-[#B85538] text-xs tracking-widest uppercase mb-3" style={{ fontSize: "0.65rem" }}>
                {ui.sectionPopularLabel || "Популярное"}
              </p>
              <h2
                style={{
                  fontFamily: "'Cormorant Garamond', serif",
                  fontSize: "clamp(2rem, 4vw, 3rem)",
                  fontWeight: 300,
                  color: "#1C1714",
                  lineHeight: 1.1,
                }}
              >
                {ui.hitsCollectionHeading || "Хиты коллекции"}
              </h2>
            </div>
            <Link
              to="/catalog"
              className="hidden md:inline-flex items-center gap-2 text-[#B85538] hover:gap-4 transition-all duration-300 text-sm"
              style={{ letterSpacing: "0.08em" }}
            >
              {ui.viewFullCatalog || "Весь каталог"} <ArrowRight className="w-4 h-4" />
            </Link>
          </div>

          <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 md:gap-6">
            {featured.map((product, i) => (
              <Link
                key={product.id}
                to={`/product/${product.id}`}
                className="group block"
              >
                <div className="relative overflow-hidden bg-[#EDE5DA] mb-4" style={{ aspectRatio: i === 0 ? "3/4" : "1/1" }}>
                  <img
                    src={product.image}
                    alt={product.name}
                    className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-700"
                  />
                  <div className="absolute inset-0 bg-[#1C1714]/0 group-hover:bg-[#1C1714]/20 transition-colors duration-500" />
                  <div className="absolute top-3 left-3">
                    {product.isNew && (
                      <span className="bg-[#B85538] text-white px-2 py-1 text-[10px] tracking-widest uppercase">
                        {ui.badgeNew || "Новинка"}
                      </span>
                    )}
                    {product.isBestseller && !product.isNew && (
                      <span className="bg-[#1C1714] text-white px-2 py-1 text-[10px] tracking-widest uppercase">
                        {ui.badgeHit || "Хит"}
                      </span>
                    )}
                  </div>
                  <div className="absolute bottom-3 right-3 opacity-0 group-hover:opacity-100 transition-opacity duration-300">
                    <div className="bg-white w-9 h-9 flex items-center justify-center">
                      <ArrowUpRight className="w-4 h-4 text-[#1C1714]" />
                    </div>
                  </div>
                </div>
                <p className="text-[#6B5E54] text-xs tracking-widest uppercase mb-1" style={{ fontSize: "0.6rem" }}>
                  {product.category}
                </p>
                <p className="text-[#1C1714] mb-2" style={{ fontSize: "0.9rem", lineHeight: 1.4 }}>
                  {product.name}
                </p>
                <p className="text-[#B85538]" style={{ fontSize: "0.9rem" }}>
                  {formatMoney(product.price, lang)}
                </p>
              </Link>
            ))}
          </div>

          <div className="mt-10 md:hidden text-center">
            <Link
              to="/catalog"
              className="inline-flex items-center gap-2 text-[#B85538] text-sm border-b border-[#B85538] pb-1"
            >
              {ui.watchAll || "Смотреть всё"} <ArrowRight className="w-4 h-4" />
            </Link>
          </div>
        </div>
      </section>

      {/* ── ABOUT SPLIT ── */}
      <section className="grid grid-cols-1 md:grid-cols-2 min-h-[500px]">
        <div className="relative overflow-hidden min-h-[400px]">
          <img
            src={aboutSplitImg}
            alt={aboutSplitTitle}
            className="absolute inset-0 w-full h-full object-cover"
          />
        </div>
        <div className="bg-[#1C1714] flex items-center px-10 lg:px-16 py-20">
          <div>
            <p className="text-[#D4895A] text-xs tracking-widest uppercase mb-6" style={{ fontSize: "0.65rem" }}>
              {ui.sectionAboutLabel || "О нас"}
            </p>
            <h2
              className="text-white mb-6 whitespace-pre-line"
              style={{
                fontFamily: "'Cormorant Garamond', serif",
                fontSize: "clamp(1.8rem, 3vw, 2.8rem)",
                fontWeight: 300,
                lineHeight: 1.2,
              }}
            >
              {aboutSplitTitle}
            </h2>
            <p className="text-[#A99A8C] mb-8 whitespace-pre-line" style={{ lineHeight: 1.9, fontSize: "0.9rem" }}>
              {aboutSplitLead}
            </p>
            <Link
              to="/about"
              className="inline-flex items-center gap-3 text-white border-b border-[#D4895A] pb-1 text-sm hover:text-[#D4895A] transition-colors"
              style={{ letterSpacing: "0.08em" }}
            >
              {ui.ourStoryLink || "Наша история"} <ArrowRight className="w-4 h-4" />
            </Link>
          </div>
        </div>
      </section>

      {/* ── NEW ARRIVALS ── */}
      <section className="py-24 px-6 lg:px-12 bg-[#EDE5DA]">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-14">
            <p className="text-[#B85538] text-xs tracking-widest uppercase mb-3" style={{ fontSize: "0.65rem" }}>
              {ui.sectionNewLabel || "Только появились"}
            </p>
            <h2
              style={{
                fontFamily: "'Cormorant Garamond', serif",
                fontSize: "clamp(2rem, 4vw, 3rem)",
                fontWeight: 300,
                color: "#1C1714",
                lineHeight: 1.1,
              }}
            >
              {ui.newArrivalsHeading || "Новинки"}
            </h2>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {newArrivals.map((product) => (
              <Link
                key={product.id}
                to={`/product/${product.id}`}
                className="group block bg-[#F7F3EE]"
              >
                <div className="relative overflow-hidden" style={{ aspectRatio: "4/5" }}>
                  <img
                    src={product.image}
                    alt={product.name}
                    className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-700"
                  />
                  <div className="absolute top-3 left-3">
                    <span className="bg-[#B85538] text-white px-2 py-1 text-[10px] tracking-widest uppercase">
                      {ui.badgeNew || "Новинка"}
                    </span>
                  </div>
                </div>
                <div className="p-5">
                  <p className="text-[#6B5E54] text-xs tracking-widest uppercase mb-2" style={{ fontSize: "0.6rem" }}>
                    {product.category}
                  </p>
                  <p className="text-[#1C1714] mb-2" style={{ fontSize: "0.95rem" }}>
                    {product.name}
                  </p>
                  <p className="text-[#B85538]" style={{ fontSize: "0.9rem" }}>
                    {formatMoney(product.price, lang)}
                  </p>
                </div>
              </Link>
            ))}
          </div>
        </div>
      </section>

      {/* ── VALUES ── */}
      <section className="py-24 px-6 lg:px-12">
        <div className="max-w-7xl mx-auto">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-12">
            {valueCards.map((val) => (
              <div key={val.title} className="flex flex-col">
                <p
                  className="text-[#B85538] mb-6 flex items-center justify-center md:justify-start min-h-[2rem]"
                  style={{ fontFamily: "'Cormorant Garamond', serif", fontSize: "2rem" }}
                >
                  {val.faIcon ? <i className={val.faIcon} aria-hidden /> : val.icon}
                </p>
                <p
                  className="text-[#1C1714] mb-3"
                  style={{ fontFamily: "'Cormorant Garamond', serif", fontSize: "1.3rem", fontWeight: 400 }}
                >
                  {val.title}
                </p>
                <p className="text-[#6B5E54] text-sm" style={{ lineHeight: 1.8 }}>
                  {val.text}
                </p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ── CTA BANNER ── */}
      <section className="relative overflow-hidden bg-[#B85538] py-20 px-6 lg:px-12 text-center">
        <div
          className="absolute inset-0 opacity-10"
          style={{
            backgroundImage: "radial-gradient(circle at 30% 50%, #fff 0%, transparent 50%), radial-gradient(circle at 70% 50%, #fff 0%, transparent 50%)",
          }}
        />
        <div className="relative z-10 max-w-2xl mx-auto">
          <p className="text-white/70 text-xs tracking-widest uppercase mb-4" style={{ fontSize: "0.65rem" }}>
            {ui.individualOrderCta || "Индивидуальный заказ"}
          </p>
          <h2
            className="text-white mb-6"
            style={{
              fontFamily: "'Cormorant Garamond', serif",
              fontSize: "clamp(1.8rem, 4vw, 3rem)",
              fontWeight: 300,
              lineHeight: 1.2,
            }}
          >
            {ui.ctaUniqueLine1 || "Хотите что-то"}
            <br />
            <em>{ui.ctaUniqueEmphasis || "по-настоящему уникальное?"}</em>
          </h2>
          <p className="text-white/80 mb-10 text-sm" style={{ lineHeight: 1.8 }}>
            {ui.ctaUniqueBody || ""}
          </p>
          <Link
            to="/faq"
            className="inline-flex items-center gap-3 bg-white text-[#B85538] px-8 py-4 hover:bg-[#F7F3EE] transition-colors text-sm tracking-wider"
            style={{ letterSpacing: "0.1em" }}
          >
            {(ui.learnMoreCta || "Узнать больше").toUpperCase()} <ArrowRight className="w-4 h-4" />
          </Link>
        </div>
      </section>
    </div>
  );
}
