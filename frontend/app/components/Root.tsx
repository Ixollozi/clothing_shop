import { Outlet, Link, useLocation } from "react-router";
import { CartProvider, useCart } from "../context/CartContext";
import { ShoppingBag, Menu, X, Languages, ChevronDown } from "lucide-react";
import { useState, useEffect, useMemo, useRef } from "react";
import {
  getStore,
  getContact,
  getLanguages,
  getBootstrap,
  submitDjangoLanguage,
  getUi,
} from "../lib/bootstrap";
import { cn } from "./ui/utils";

/**
 * Кастомный список языков без Radix Select: у Radix на контенте стоит RemoveScroll,
 * из‑за чего при открытом списке блокируется скролл страницы.
 */
function LanguageSwitcher({ isOnHero }: { isOnHero: boolean }) {
  const location = useLocation();
  const languages = useMemo(() => getLanguages(), []);
  const raw = useMemo(() => getBootstrap().languageCode || "ru", []);
  const current = useMemo(() => {
    const codes = new Set(languages.map((l) => l.code));
    return codes.has(raw) ? raw : languages[0]?.code ?? "ru";
  }, [languages, raw]);

  const [open, setOpen] = useState(false);
  const wrapRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    setOpen(false);
  }, [location.pathname]);

  useEffect(() => {
    if (!open) return;
    const onPointerDown = (e: PointerEvent) => {
      if (wrapRef.current && !wrapRef.current.contains(e.target as Node)) {
        setOpen(false);
      }
    };
    const onKey = (e: KeyboardEvent) => {
      if (e.key === "Escape") setOpen(false);
    };
    document.addEventListener("pointerdown", onPointerDown, true);
    document.addEventListener("keydown", onKey);
    return () => {
      document.removeEventListener("pointerdown", onPointerDown, true);
      document.removeEventListener("keydown", onKey);
    };
  }, [open]);

  if (languages.length <= 1) return null;

  const currentLabel = languages.find((l) => l.code === current)?.label ?? current.toUpperCase();

  const btnClass = isOnHero
    ? "border-white/40 bg-white/12 text-white hover:bg-white/20 focus-visible:ring-2 focus-visible:ring-white/30"
    : "border-[#E8DED4] bg-[#FDFAF7] text-[#1C1714] hover:bg-[#F3EBE3] focus-visible:ring-2 focus-visible:ring-[#B85538]/25";

  const panelClass = isOnHero
    ? "border border-white/15 bg-[#1C1714] text-[#F7F3EE] shadow-2xl"
    : "border border-[#E8DED4] bg-[#FDFAF7] text-[#1C1714] shadow-xl";

  return (
    <div className="relative shrink-0" ref={wrapRef}>
      <button
        type="button"
        aria-haspopup="listbox"
        aria-expanded={open}
        aria-label={getUi().ariaSiteLanguage || "Язык сайта"}
        onClick={() => setOpen((v) => !v)}
        className={cn(
          "flex h-9 min-w-[9.25rem] items-center gap-2 rounded-lg border px-2.5 text-left text-sm font-medium transition-colors outline-none",
          btnClass,
        )}
      >
        <Languages className="size-3.5 shrink-0 opacity-90" aria-hidden />
        <span className="min-w-0 flex-1 truncate">{currentLabel}</span>
        <ChevronDown
          className={cn("size-4 shrink-0 opacity-70 transition-transform duration-200", open && "rotate-180")}
          aria-hidden
        />
      </button>
      {open ? (
        <ul
          className={cn("absolute right-0 z-[200] mt-1.5 min-w-full overflow-hidden rounded-lg py-1", panelClass)}
          role="listbox"
          aria-label={getUi().ariaLanguagePicker || "Выбор языка"}
        >
          {languages.map((l) => (
            <li key={l.code} role="none">
              <button
                type="button"
                role="option"
                aria-selected={l.code === current}
                className={cn(
                  "flex w-full items-baseline justify-between gap-3 px-3 py-2.5 text-left text-[0.8125rem] transition-colors",
                  l.code === current
                    ? isOnHero
                      ? "bg-white/15"
                      : "bg-[#E4D9CF]"
                    : isOnHero
                      ? "hover:bg-white/10"
                      : "hover:bg-[#ECE4DC]",
                )}
                onClick={() => {
                  setOpen(false);
                  if (l.code !== current) submitDjangoLanguage(l.code);
                }}
              >
                <span className="font-medium leading-snug">{l.label}</span>
                <span
                  className={cn(
                    "shrink-0 text-[0.65rem] font-semibold uppercase tracking-[0.12em]",
                    isOnHero ? "text-[#A99A8C]" : "text-[#8A7B70]",
                  )}
                >
                  {l.code}
                </span>
              </button>
            </li>
          ))}
        </ul>
      ) : null}
    </div>
  );
}

function Navigation() {
  const location = useLocation();
  const { getTotalItems } = useCart();
  const totalItems = getTotalItems();
  const [scrolled, setScrolled] = useState(false);
  const [menuOpen, setMenuOpen] = useState(false);
  const ui = useMemo(() => getUi(), []);
  const storeName = useMemo(() => getStore().name || ui.storeDefaultName || "Магазин", [ui.storeDefaultName]);

  const isHome = location.pathname === "/";

  useEffect(() => {
    const handleScroll = () => setScrolled(window.scrollY > 60);
    window.addEventListener("scroll", handleScroll);
    return () => window.removeEventListener("scroll", handleScroll);
  }, []);

  useEffect(() => {
    setMenuOpen(false);
  }, [location.pathname]);

  const links = [
    { path: "/catalog", label: ui.navCatalog || "Каталог" },
    { path: "/about", label: ui.navAbout || "О нас" },
    { path: "/faq", label: ui.navFaq || "FAQ" },
  ];

  const navBg = isHome && !scrolled ? "bg-transparent" : "bg-[#FDFAF7]";
  const navBorder = scrolled || !isHome ? "border-b border-[#E8DED4]" : "";
  const textColor = isHome && !scrolled ? "text-white" : "text-[#1C1714]";
  const logoColor = isHome && !scrolled ? "text-white" : "text-[#1C1714]";

  return (
    <>
      <nav
        className={`fixed top-0 left-0 right-0 z-50 transition-all duration-500 ${navBg} ${navBorder}`}
        style={{ fontFamily: "'DM Sans', sans-serif" }}
      >
        <div className="max-w-7xl mx-auto px-6 lg:px-12">
          <div className="flex justify-between items-center h-16 md:h-20">
            {/* Logo */}
            <Link
              to="/"
              className={`tracking-[0.25em] uppercase text-sm ${logoColor} transition-colors duration-300`}
              style={{ fontFamily: "'Cormorant Garamond', serif", fontSize: "1.1rem", fontWeight: 600, letterSpacing: "0.3em" }}
            >
              {storeName}
            </Link>

            {/* Desktop Nav */}
            <div className="hidden md:flex items-center space-x-10">
              {links.map((link) => (
                <Link
                  key={link.path}
                  to={link.path}
                  className={`text-xs tracking-widest uppercase transition-all duration-300 relative group ${textColor}`}
                  style={{ letterSpacing: "0.15em", fontSize: "0.7rem" }}
                >
                  {link.label}
                  <span
                    className={`absolute -bottom-1 left-0 h-px transition-all duration-300 ${
                      location.pathname.startsWith(link.path)
                        ? "w-full bg-[#B85538]"
                        : "w-0 group-hover:w-full bg-[#B85538]"
                    }`}
                  />
                </Link>
              ))}
            </div>

            {/* Cart, language, mobile menu */}
            <div className="flex items-center gap-4 md:gap-5">
              <Link
                to="/cart"
                className={`relative transition-colors duration-300 flex items-center gap-2 ${textColor}`}
              >
                <ShoppingBag className="w-5 h-5" />
                {totalItems > 0 && (
                  <span className="absolute -top-2 -right-2 bg-[#B85538] text-white text-[10px] rounded-full w-4 h-4 flex items-center justify-center">
                    {totalItems}
                  </span>
                )}
              </Link>
              <LanguageSwitcher isOnHero={isHome && !scrolled} />
              <button
                className={`md:hidden transition-colors duration-300 ${textColor}`}
                onClick={() => setMenuOpen(!menuOpen)}
              >
                {menuOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
              </button>
            </div>
          </div>
        </div>
      </nav>

      {/* Mobile Menu */}
      {menuOpen && (
        <div
          className="fixed inset-0 z-40 bg-[#1C1714] flex flex-col items-center justify-center space-y-10"
          style={{ fontFamily: "'Cormorant Garamond', serif" }}
        >
          {[{ path: "/", label: ui.navHome || "Главная" }, ...links].map((link) => (
            <Link
              key={link.path}
              to={link.path}
              className="text-white text-4xl tracking-widest hover:text-[#D4895A] transition-colors"
              style={{ fontStyle: "italic" }}
            >
              {link.label}
            </Link>
          ))}
          {getLanguages().length > 1 && (
            <div className="mt-6 flex flex-col items-center gap-3">
              <p className="text-[#A99A8C] text-xs tracking-widest uppercase">{ui.mobileLanguage || "Язык"}</p>
              <div className="flex flex-wrap justify-center gap-2">
                {getLanguages().map((l) => (
                  <button
                    key={l.code}
                    type="button"
                    className="px-4 py-2 border border-white/30 rounded text-white text-sm tracking-widest uppercase hover:bg-white/10"
                    onClick={() => submitDjangoLanguage(l.code)}
                  >
                    {l.label}
                  </button>
                ))}
              </div>
            </div>
          )}
        </div>
      )}
    </>
  );
}

function Footer() {
  const store = useMemo(() => getStore(), []);
  const contact = useMemo(() => getContact(), []);
  const ui = useMemo(() => getUi(), []);
  const year = new Date().getFullYear();

  return (
    <footer
      className="bg-[#1C1714] text-[#A99A8C]"
      style={{ fontFamily: "'DM Sans', sans-serif" }}
    >
      <div className="max-w-7xl mx-auto px-6 lg:px-12 py-16">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-12 mb-16">
          <div className="md:col-span-2">
            <p
              className="text-white tracking-[0.3em] uppercase mb-6 text-lg"
              style={{ fontFamily: "'Cormorant Garamond', serif", fontWeight: 600 }}
            >
              {store.name}
            </p>
            <p className="text-sm leading-relaxed max-w-xs" style={{ lineHeight: 1.8 }}>
              {store.description || ""}
            </p>
          </div>
          <div>
            <p className="text-white text-xs tracking-widest uppercase mb-6" style={{ fontSize: "0.65rem" }}>
              {ui.footerNavigation || "Навигация"}
            </p>
            <div className="space-y-3">
              {[
                { to: "/catalog", label: ui.navCatalog || "Каталог" },
                { to: "/about", label: ui.navAbout || "О нас" },
                { to: "/faq", label: ui.navFaq || "FAQ" },
                { to: "/cart", label: ui.navCart || "Корзина" },
              ].map((link) => (
                <Link
                  key={link.to}
                  to={link.to}
                  className="block text-sm hover:text-white transition-colors"
                >
                  {link.label}
                </Link>
              ))}
            </div>
          </div>
          <div>
            <p className="text-white text-xs tracking-widest uppercase mb-6" style={{ fontSize: "0.65rem" }}>
              {ui.footerContacts || "Контакты"}
            </p>
            <div className="space-y-3 text-sm">
              {contact?.email ? (
                <p>
                  <a href={`mailto:${contact.email}`} className="hover:text-white transition-colors">
                    {contact.email}
                  </a>
                </p>
              ) : null}
              {contact?.phone ? <p>{contact.phone}</p> : null}
              {contact?.addressFull ? (
                <p className="leading-relaxed whitespace-pre-line">{contact.addressFull}</p>
              ) : null}
            </div>
          </div>
        </div>
        <div className="border-t border-[#2E2520] pt-8 flex flex-col md:flex-row justify-between items-center gap-4">
          <p className="text-xs" style={{ fontSize: "0.65rem", letterSpacing: "0.1em" }}>
            © {year} {store.name}. {ui.footerCopyright || "Все права защищены."}
          </p>
          <p className="text-xs" style={{ fontSize: "0.65rem", letterSpacing: "0.1em" }}>
            {(ui.footerTagline || "Сделано с любовью к ремеслу").toUpperCase()}
          </p>
        </div>
      </div>
    </footer>
  );
}

export function Root() {
  return (
    <CartProvider>
      <div className="min-h-screen flex flex-col bg-[#F7F3EE]">
        <Navigation />
        <main className="flex-1">
          <Outlet />
        </main>
        <Footer />
      </div>
    </CartProvider>
  );
}
