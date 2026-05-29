import { Link } from "react-router";
import { ArrowRight } from "lucide-react";
import { useMemo } from "react";
import { getAbout, getAboutStats, getFeatures, getStore, getUi } from "../lib/bootstrap";

const WORKSHOP_FALLBACK =
  "https://images.unsplash.com/photo-1763824371988-8c8eb3d13eff?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&q=80&w=1080";
const HANDS_FALLBACK =
  "https://images.unsplash.com/photo-1772487488987-425a4a0c1499?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&q=80&w=1080";

const FALLBACK_STEPS_UI_KEYS = [
  { num: "01", titleKey: "fallbackStep01Title" as const, textKey: "fallbackStep01Text" as const },
  { num: "02", titleKey: "fallbackStep02Title" as const, textKey: "fallbackStep02Text" as const },
  { num: "03", titleKey: "fallbackStep03Title" as const, textKey: "fallbackStep03Text" as const },
];

export function About() {
  const store = useMemo(() => getStore(), []);
  const about = useMemo(() => getAbout(), []);
  const stats = useMemo(() => getAboutStats(), []);
  const features = useMemo(() => getFeatures(), []);
  const ui = useMemo(() => getUi(), []);

  const heroImg = (about?.imageUrl || "").trim() || WORKSHOP_FALLBACK;
  const heroTitle =
    (about?.title || "").trim() ||
    (ui.aboutHeroTitleFallback || "").trim() ||
    `О ${store.name}`;
  const introTitle =
    (about?.mission || "").trim() || (about?.title || "").trim() || ui.aboutFallbackIntro || "О нас";
  const introP1 = (about?.description || "").trim();
  const introP2 = (about?.vision || "").trim();
  const handsImg = HANDS_FALLBACK;
  const statHighlight = stats[0];

  const valueBlocks = useMemo(() => {
    if (about?.values?.length) {
      return about.values.map((v) => ({
        title: v,
        description: "",
      }));
    }
    if (features.length > 0) {
      return features.slice(0, 4).map((f) => ({
        title: f.title,
        description: f.description || "",
      }));
    }
    return [
      { title: ui.fallbackValueCraftTitle || "", description: ui.fallbackValueCraftText || "" },
      { title: ui.fallbackValueUniqueTitle || "", description: ui.fallbackValueUniqueText || "" },
      { title: ui.fallbackValueEcoTitle || "", description: ui.fallbackValueEcoText || "" },
      { title: ui.fallbackValueHonestyTitle || "", description: ui.fallbackValueHonestyText || "" },
    ];
  }, [about, features, ui]);

  const steps = useMemo(() => {
    if (features.length > 0) {
      return features.map((f, i) => ({
        num: String(i + 1).padStart(2, "0"),
        title: f.title,
        text: f.description,
      }));
    }
    return FALLBACK_STEPS_UI_KEYS.map((s) => ({
      num: s.num,
      title: ui[s.titleKey] || "",
      text: ui[s.textKey] || "",
    }));
  }, [features, ui]);

  return (
    <div className="bg-[#F7F3EE]" style={{ fontFamily: "'DM Sans', sans-serif" }}>
      <div className="relative overflow-hidden min-h-[70vh] flex items-end">
        <img src={heroImg} alt={heroTitle} className="absolute inset-0 w-full h-full object-cover" />
        <div className="absolute inset-0 bg-gradient-to-t from-[#1C1714] via-[#1C1714]/40 to-transparent" />
        <div className="relative z-10 max-w-7xl mx-auto px-6 lg:px-12 pb-20 pt-36 w-full">
          <p className="text-[#D4895A] text-xs tracking-widest uppercase mb-5" style={{ fontSize: "0.65rem" }}>
            {ui.aboutPageEyebrow || "О нас"}
          </p>
          <h1
            className="text-white max-w-3xl whitespace-pre-line"
            style={{
              fontFamily: "'Cormorant Garamond', serif",
              fontSize: "clamp(2.5rem, 5vw, 5rem)",
              fontWeight: 300,
              lineHeight: 1.05,
            }}
          >
            {heroTitle}
          </h1>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-6 lg:px-12 py-20">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-16 items-center">
          <div>
            <p className="text-[#B85538] text-xs tracking-widest uppercase mb-5" style={{ fontSize: "0.65rem" }}>
              {ui.ourStoryEyebrow || "Наша история"}
            </p>
            <h2
              className="text-[#1C1714] mb-6 whitespace-pre-line"
              style={{
                fontFamily: "'Cormorant Garamond', serif",
                fontSize: "clamp(1.8rem, 3vw, 2.8rem)",
                fontWeight: 300,
                lineHeight: 1.2,
              }}
            >
              {introTitle}
            </h2>
            {introP1 ? (
              <p className="text-[#6B5E54] mb-6 whitespace-pre-line" style={{ lineHeight: 1.9, fontSize: "0.9rem" }}>
                {introP1}
              </p>
            ) : null}
            {introP2 ? (
              <p className="text-[#6B5E54] whitespace-pre-line" style={{ lineHeight: 1.9, fontSize: "0.9rem" }}>
                {introP2}
              </p>
            ) : null}
          </div>
          <div className="relative">
            <img src={handsImg} alt="" className="w-full object-cover" style={{ aspectRatio: "4/3" }} />
            {statHighlight ? (
              <div
                className="absolute -bottom-6 -left-6 bg-[#B85538] text-white p-8 hidden md:block"
                style={{ width: "180px" }}
              >
                <p
                  style={{ fontFamily: "'Cormorant Garamond', serif", fontSize: "2.5rem", fontWeight: 300, lineHeight: 1 }}
                >
                  {statHighlight.value}
                </p>
                <p className="text-white/70 text-xs mt-1" style={{ fontSize: "0.65rem", letterSpacing: "0.1em" }}>
                  {statHighlight.label}
                </p>
              </div>
            ) : null}
          </div>
        </div>
      </div>

      <div className="bg-[#1C1714] py-20 px-6 lg:px-12">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-16">
            <p className="text-[#D4895A] text-xs tracking-widest uppercase mb-4" style={{ fontSize: "0.65rem" }}>
              {ui.whatDefinesUsEyebrow || "Что нас определяет"}
            </p>
            <h2
              className="text-white"
              style={{
                fontFamily: "'Cormorant Garamond', serif",
                fontSize: "clamp(1.8rem, 3vw, 2.8rem)",
                fontWeight: 300,
              }}
            >
              {ui.ourValuesHeading || "Наши ценности"}
            </h2>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
            {valueBlocks.map((val) => (
              <div key={val.title} className="border-t border-[#2E2520] pt-8">
                <p
                  className="text-white mb-3"
                  style={{ fontFamily: "'Cormorant Garamond', serif", fontSize: "1.2rem", fontWeight: 400 }}
                >
                  {val.title}
                </p>
                {val.description ? (
                  <p className="text-[#A99A8C] text-sm" style={{ lineHeight: 1.8, fontSize: "0.85rem" }}>
                    {val.description}
                  </p>
                ) : null}
              </div>
            ))}
          </div>
        </div>
      </div>

      <div className="py-20 px-6 lg:px-12">
        <div className="max-w-7xl mx-auto">
          <div className="mb-14">
            <p className="text-[#B85538] text-xs tracking-widest uppercase mb-4" style={{ fontSize: "0.65rem" }}>
              {ui.fromIdeaToHomeEyebrow || "От замысла до вашего дома"}
            </p>
            <h2
              className="text-[#1C1714]"
              style={{
                fontFamily: "'Cormorant Garamond', serif",
                fontSize: "clamp(1.8rem, 3vw, 2.8rem)",
                fontWeight: 300,
              }}
            >
              {ui.howMadeHeading || "Как создаётся изделие"}
            </h2>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {steps.map((step) => (
              <div key={step.num} className="flex gap-6">
                <p
                  className="text-[#E0D5C8] flex-shrink-0"
                  style={{ fontFamily: "'Cormorant Garamond', serif", fontSize: "2.5rem", fontWeight: 300, lineHeight: 1 }}
                >
                  {step.num}
                </p>
                <div className="border-t border-[#E0D5C8] pt-4 flex-1">
                  <p
                    className="text-[#1C1714] mb-3"
                    style={{ fontFamily: "'Cormorant Garamond', serif", fontSize: "1.15rem", fontWeight: 400 }}
                  >
                    {step.title}
                  </p>
                  <p className="text-[#6B5E54] text-sm" style={{ lineHeight: 1.8 }}>
                    {step.text}
                  </p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      <div className="bg-[#EDE5DA] py-20 px-6 lg:px-12 text-center">
        <div className="max-w-xl mx-auto">
          <h2
            className="text-[#1C1714] mb-6"
            style={{
              fontFamily: "'Cormorant Garamond', serif",
              fontSize: "clamp(1.8rem, 3vw, 2.5rem)",
              fontWeight: 300,
            }}
          >
            {ui.readyToChooseHeading || "Готовы выбрать своё изделие?"}
          </h2>
          <p className="text-[#6B5E54] text-sm mb-10" style={{ lineHeight: 1.8 }}>
            {ui.readyToChooseBody || ""}
          </p>
          <Link
            to="/catalog"
            className="inline-flex items-center gap-3 bg-[#1C1714] text-white px-10 py-4 hover:bg-[#B85538] transition-colors text-xs tracking-widest uppercase"
            style={{ letterSpacing: "0.15em", fontSize: "0.7rem" }}
          >
            {ui.viewCatalog || "Смотреть каталог"} <ArrowRight className="w-4 h-4" />
          </Link>
        </div>
      </div>
    </div>
  );
}
