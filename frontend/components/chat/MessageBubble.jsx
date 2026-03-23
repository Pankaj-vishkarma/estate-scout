"use client";

import { motion } from "framer-motion";

function formatRole(role) {
  if (role === "user") return "You";
  return "Estate Scout";
}

export default function MessageBubble({ role, content }) {
  // 🔥 FIX: Safety checks (avoid hydration + runtime crash)
  const safeRole = role === "user" ? "user" : "assistant";
  const isUser = safeRole === "user";

  const safeContent =
    typeof content === "string" && content.trim().length > 0
      ? content
      : "—";

  return (
    <motion.div
      className={`w-full flex ${isUser ? "justify-end" : "justify-start"}`}
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.18 }}
    >
      <div
        className={`max-w-[92%] rounded-2xl px-4 py-3 glass border ${isUser
            ? "bg-sky-500/15 border-sky-400/25"
            : "bg-white/5 border-white/10"
          }`}
      >
        <div className="mb-1 text-xs font-semibold text-slate-300">
          {formatRole(safeRole)}
        </div>

        <div className="whitespace-pre-wrap text-sm leading-relaxed text-slate-100">
          {safeContent}
        </div>
      </div>
    </motion.div>
  );
}