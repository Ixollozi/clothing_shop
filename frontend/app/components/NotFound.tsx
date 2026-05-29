import { Link } from "react-router";
import { ArrowLeft } from "lucide-react";
import { useMemo } from "react";
import { getUi } from "../lib/bootstrap";

export function NotFound() {
  const ui = useMemo(() => getUi(), []);
  return (
    <div
      className="min-h-screen bg-[#F7F3EE] flex items-center justify-center px-6"
      style={{ fontFamily: "'DM Sans', sans-serif" }}
    >
      <div className="text-center">
        <p
          className="text-[#E0D5C8] mb-4"
          style={{
            fontFamily: "'Cormorant Garamond', serif",
            fontSize: "clamp(6rem, 15vw, 12rem)",
            fontWeight: 300,
            lineHeight: 1,
          }}
        >
          404
        </p>
        <p className="text-[#B85538] text-xs tracking-widest uppercase mb-4" style={{ fontSize: "0.65rem" }}>
          {ui.notFoundEyebrow || "Страница не найдена"}
        </p>
        <h1
          className="text-[#1C1714] mb-6"
          style={{
            fontFamily: "'Cormorant Garamond', serif",
            fontSize: "clamp(1.5rem, 3vw, 2.5rem)",
            fontWeight: 300,
          }}
        >
          {ui.notFoundTitle || "Такой страницы не существует"}
        </h1>
        <p className="text-[#6B5E54] text-sm mb-10" style={{ lineHeight: 1.8 }}>
          {ui.notFoundBody || ""}
        </p>
        <div className="flex flex-col sm:flex-row gap-4 justify-center">
          <Link
            to="/"
            className="inline-flex items-center justify-center gap-3 bg-[#1C1714] text-white px-8 py-4 hover:bg-[#B85538] transition-colors text-xs tracking-widest uppercase"
            style={{ letterSpacing: "0.15em", fontSize: "0.7rem" }}
          >
            <ArrowLeft className="w-4 h-4" /> {ui.toHome || "На главную"}
          </Link>
          <Link
            to="/catalog"
            className="inline-flex items-center justify-center gap-3 border border-[#1C1714] text-[#1C1714] px-8 py-4 hover:bg-[#1C1714] hover:text-white transition-colors text-xs tracking-widest uppercase"
            style={{ letterSpacing: "0.15em", fontSize: "0.7rem" }}
          >
            {ui.toCatalog || "В каталог"}
          </Link>
        </div>
      </div>
    </div>
  );
}
