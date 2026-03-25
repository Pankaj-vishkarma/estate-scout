"use client";

import { motion } from "framer-motion";
import { memo, useMemo } from "react";

function formatRole(role) {
  return role === "user" ? "You" : "Estate Scout";
}

function MessageBubble({ role, content }) {
  // ✅ safe role
  const safeRole = role === "user" ? "user" : "assistant";
  const isUser = safeRole === "user";

  // ✅ memoized values (performance)
  const { label, safeContent } = useMemo(() => {
    const label = formatRole(safeRole);

    const safeContent =
      typeof content === "string" && content.trim().length > 0
        ? content
        : "—";

    return { label, safeContent };
  }, [safeRole, content]);

  return (
    <motion.div
      className={`w-full flex ${isUser ? "justify-end" : "justify-start"}`}
      initial={{ opacity: 0, y: 8 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.15 }}
    >
      <div
        className={`max-w-[92%] rounded-2xl px-4 py-3 glass border ${isUser
            ? "bg-sky-500/15 border-sky-400/25"
            : "bg-white/5 border-white/10"
          }`}
      >
        <div className="mb-1 text-xs font-semibold text-slate-300">
          {label}
        </div>

        <div className="whitespace-pre-wrap break-words text-sm leading-relaxed text-slate-100">
          {safeContent}
        </div>
      </div>
    </motion.div>
  );
}

export default memo(MessageBubble); // ✅ prevent unnecessary re-renders