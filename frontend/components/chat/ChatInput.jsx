"use client";

import { useMemo, useState } from "react";
import Button from "../ui/Button";

export default function ChatInput({ onSend, isLoading = false }) {
  const [value, setValue] = useState("");

  const canSend = useMemo(() => {
    return (
      !isLoading &&
      typeof onSend === "function" &&
      String(value || "").trim().length > 0
    );
  }, [isLoading, value, onSend]);

  function submit() {
    if (!canSend) return;

    const trimmed = String(value || "").trim();
    if (!trimmed) return;

    try {
      onSend(trimmed);
      setValue("");
    } catch (err) {
      console.error("Send message error:", err);
    }
  }

  return (
    <div className="glass rounded-2xl border border-white/10 p-3">
      <div className="flex items-end gap-2">
        <div className="flex-1">
          <label className="sr-only" htmlFor="chat-input">
            Message
          </label>

          <textarea
            id="chat-input"
            value={value}
            onChange={(e) => setValue(e.target.value)}
            placeholder="Ask about a neighborhood, price range, or a property..."
            className="w-full resize-none bg-transparent text-sm leading-relaxed placeholder:text-slate-400 text-slate-100 outline-none"
            rows={1}
            disabled={isLoading}
            onKeyDown={(e) => {
              if (e.key === "Enter" && !e.shiftKey) {
                e.preventDefault();
                submit();
              }
            }}
          />
        </div>

        <Button
          type="button"
          variant="primary"
          size="md"
          onClick={submit}
          disabled={!canSend}
          aria-disabled={!canSend}
          className="min-w-[120px]"
        >
          {isLoading ? "Thinking..." : "Send"}
        </Button>
      </div>
    </div>
  );
}