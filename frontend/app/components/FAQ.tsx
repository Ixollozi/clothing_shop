import { useMemo, useState } from "react";
import { Plus, Minus } from "lucide-react";
import { Link } from "react-router";
import { getFaqs, getContact, getFaqStaticGroups, getUi } from "../lib/bootstrap";

interface FAQItemProps {
  question: string;
  answer: string;
  isOpen: boolean;
  onToggle: () => void;
  index: number;
}

function FAQItem({ question, answer, isOpen, onToggle, index }: FAQItemProps) {
  return (
    <div className="border-b border-[#E0D5C8]">
      <button
        onClick={onToggle}
        className="w-full py-6 flex items-start justify-between gap-8 text-left group"
      >
        <div className="flex items-start gap-6">
          <span
            className="text-[#D5C9BC] flex-shrink-0 pt-0.5"
            style={{ fontFamily: "'Cormorant Garamond', serif", fontSize: "0.9rem" }}
          >
            {String(index + 1).padStart(2, "0")}
          </span>
          <span
            className={`transition-colors duration-200 ${isOpen ? "text-[#B85538]" : "text-[#1C1714] group-hover:text-[#B85538]"}`}
            style={{ fontSize: "0.95rem", lineHeight: 1.5 }}
          >
            {question}
          </span>
        </div>
        <div className="flex-shrink-0 mt-1">
          {isOpen ? (
            <Minus className="w-4 h-4 text-[#B85538]" />
          ) : (
            <Plus className="w-4 h-4 text-[#A99A8C]" />
          )}
        </div>
      </button>
      {isOpen && (
        <div className="pl-12 pb-6">
          <p className="text-[#6B5E54] text-sm" style={{ lineHeight: 1.9 }}>
            {answer}
          </p>
        </div>
      )}
    </div>
  );
}

export function FAQ() {
  const [openItem, setOpenItem] = useState<string | null>(null);
  const contact = useMemo(() => getContact(), []);
  const ui = useMemo(() => getUi(), []);
  const faqGroups = useMemo(() => {
    const db = getFaqs();
    if (db.length > 0) return [{ category: ui.faqDbCategory || "Частые вопросы", items: db }];
    return getFaqStaticGroups();
  }, [ui.faqDbCategory]);

  const toggle = (key: string) => {
    setOpenItem(openItem === key ? null : key);
  };

  return (
    <div className="bg-[#F7F3EE] min-h-screen" style={{ fontFamily: "'DM Sans', sans-serif" }}>
      {/* Header */}
      <div className="bg-[#1C1714] pt-32 pb-16 px-6 lg:px-12">
        <div className="max-w-7xl mx-auto">
          <p className="text-[#D4895A] text-xs tracking-widest uppercase mb-4" style={{ fontSize: "0.65rem" }}>
            {ui.faqHelpEyebrow || "Помощь"}
          </p>
          <h1
            className="text-white max-w-xl"
            style={{
              fontFamily: "'Cormorant Garamond', serif",
              fontSize: "clamp(2.5rem, 5vw, 4.5rem)",
              fontWeight: 300,
              lineHeight: 1.05,
            }}
          >
            {ui.faqTitleLine1 || "Часто задаваемые"}
            <br />
            <em>{ui.faqTitleEmphasis || "вопросы"}</em>
          </h1>
        </div>
      </div>

      {/* FAQ Content */}
      <div className="max-w-4xl mx-auto px-6 lg:px-12 py-16">
        {faqGroups.map((group) => (
          <div key={group.category} className="mb-16">
            <p
              className="text-[#B85538] text-xs tracking-widest uppercase mb-8"
              style={{ fontSize: "0.65rem" }}
            >
              {group.category}
            </p>
            <div>
              {group.items.map((faq, idx) => {
                const key = `${group.category}-${idx}`;
                return (
                  <FAQItem
                    key={key}
                    question={faq.question}
                    answer={faq.answer}
                    isOpen={openItem === key}
                    onToggle={() => toggle(key)}
                    index={idx}
                  />
                );
              })}
            </div>
          </div>
        ))}

        {/* Contact Block */}
        <div className="bg-[#1C1714] p-10 md:p-14 mt-8">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-10 items-center">
            <div>
              <p className="text-[#D4895A] text-xs tracking-widest uppercase mb-4" style={{ fontSize: "0.65rem" }}>
                {ui.faqStillQuestions || "Остались вопросы?"}
              </p>
              <h2
                className="text-white mb-4"
                style={{
                  fontFamily: "'Cormorant Garamond', serif",
                  fontSize: "clamp(1.5rem, 2.5vw, 2rem)",
                  fontWeight: 300,
                }}
              >
                {ui.faqAlwaysHere || "Мы всегда на связи"}
              </h2>
              <p className="text-[#A99A8C] text-sm" style={{ lineHeight: 1.8 }}>
                {ui.faqContactBlurb || ""}
              </p>
            </div>
            <div className="space-y-5">
              {contact?.email ? (
                <div>
                  <p className="text-[#6B5E54] text-xs tracking-widest uppercase mb-1" style={{ fontSize: "0.6rem" }}>
                    {ui.labelEmail || "Email"}
                  </p>
                  <a
                    href={`mailto:${contact.email}`}
                    className="text-white hover:text-[#D4895A] transition-colors text-sm"
                  >
                    {contact.email}
                  </a>
                </div>
              ) : null}
              {contact?.phone ? (
                <div>
                  <p className="text-[#6B5E54] text-xs tracking-widest uppercase mb-1" style={{ fontSize: "0.6rem" }}>
                    {ui.labelPhone || "Телефон"}
                  </p>
                  <a href={`tel:${contact.phone.replace(/\s/g, "")}`} className="text-white hover:text-[#D4895A] transition-colors text-sm">
                    {contact.phone}
                  </a>
                </div>
              ) : null}
              {contact?.weekdays || contact?.weekend ? (
                <div>
                  <p className="text-[#6B5E54] text-xs tracking-widest uppercase mb-1" style={{ fontSize: "0.6rem" }}>
                    {ui.labelWorkingHours || "Режим работы"}
                  </p>
                  <p className="text-white text-sm whitespace-pre-line">
                    {[contact.weekdays, contact.weekend].filter(Boolean).join("\n")}
                  </p>
                </div>
              ) : null}
              <Link
                to="/catalog"
                className="inline-flex items-center gap-2 text-[#D4895A] text-xs tracking-widest uppercase border-b border-[#D4895A] pb-1 hover:text-white hover:border-white transition-colors mt-2"
                style={{ fontSize: "0.65rem" }}
              >
                {ui.faqViewCatalog || "Смотреть каталог →"}
              </Link>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
