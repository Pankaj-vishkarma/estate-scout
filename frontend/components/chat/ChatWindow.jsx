"use client";

import { useEffect, useMemo, useRef, useState } from "react";
import { AnimatePresence, motion } from "framer-motion";
import ChatInput from "./ChatInput";
import MessageBubble from "./MessageBubble";
import Button from "../ui/Button";

export default function ChatWindow({
  messages = [],
  isLoading = false,
  error = null,
  onSend,
  onClearError,
}) {
  const endRef = useRef(null);

  // 🔥 FIX: Prevent hydration mismatch (render after mount)
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
  }, []);

  // ✅ Smooth auto scroll (safe)
  useEffect(() => {
    if (!mounted) return;

    const el = endRef.current;
    if (!el) return;

    const timer = setTimeout(() => {
      el.scrollIntoView({ behavior: "smooth", block: "end" });
    }, 100);

    return () => clearTimeout(timer);
  }, [messages, isLoading, mounted]);

  const tips = useMemo(
    () => [
      "Find properties in a price range",
      "What neighborhoods are best for families?",
      "Compare listings and shortlist options",
    ],
    []
  );

  // 🔥 FIX: Avoid SSR hydration mismatch
  if (!mounted) {
    return (
      <div className="glass rounded-2xl border border-white/10 overflow-hidden h-[560px]" />
    );
  }

  return (
    <div className="glass rounded-2xl border border-white/10 overflow-hidden">
      <div className="flex items-start justify-between gap-4 p-5 border-b border-white/10">
        <div>
          <div className="text-lg font-bold tracking-tight text-slate-50">
            Estate Scout Chat
          </div>
          <div className="text-xs text-slate-300 mt-1">
            Ask the AI about properties, pricing, or locations.
          </div>
        </div>
        <div className="hidden sm:flex">
          <div className="rounded-full bg-white/5 border border-white/10 px-3 py-1 text-xs text-slate-200">
            Premium Agent UX
          </div>
        </div>
      </div>

      <div className="flex flex-col h-[560px]">
        <div className="flex-1 overflow-auto p-4 space-y-3">
          {/* ✅ Empty State */}
          {messages.length === 0 && !isLoading && (
            <div className="pt-6 text-center">
              <div className="text-sm font-semibold text-slate-200">
                Welcome! What are you looking for?
              </div>
              <div className="mt-3 space-y-2">
                {tips.map((t) => (
                  <div
                    key={t}
                    className="mx-auto w-fit rounded-full bg-white/5 border border-white/10 px-4 py-2 text-xs text-slate-200"
                  >
                    {t}
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* ✅ Messages (safe render) */}
          <AnimatePresence initial={false}>
            {messages.map((m, index) => {
              if (!m || typeof m.content !== "string") return null;

              return (
                <motion.div key={m.id || index} layout>
                  <MessageBubble role={m.role} content={m.content} />
                </motion.div>
              );
            })}
          </AnimatePresence>

          {/* ✅ Loading */}
          {isLoading && (
            <motion.div
              className="w-full flex justify-start"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
            >
              <div className="max-w-[92%] rounded-2xl px-4 py-3 glass border border-white/10">
                <div className="mb-1 text-xs font-semibold text-slate-300">
                  Estate Scout
                </div>
                <div className="h-5 w-32 rounded-lg bg-white/5 animate-pulse" />
              </div>
            </motion.div>
          )}

          {/* ✅ Error */}
          {error && (
            <div className="mt-4 rounded-2xl border border-red-400/20 bg-red-500/10 p-4">
              <div className="text-sm font-semibold text-red-100">Error</div>
              <div className="mt-1 text-sm text-red-100/90">{error}</div>
              <div className="mt-3 flex items-center gap-2">
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={onClearError}
                  aria-label="Dismiss error"
                >
                  Dismiss
                </Button>
              </div>
            </div>
          )}

          <div ref={endRef} />
        </div>

        {/* ✅ Input */}
        <div className="p-4 border-t border-white/10">
          <ChatInput
            onSend={(text) => {
              if (!text || typeof onSend !== "function") return;
              onSend(text);
            }}
            isLoading={isLoading}
          />
        </div>
      </div>
    </div>
  );
}