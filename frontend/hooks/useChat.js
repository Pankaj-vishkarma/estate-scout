"use client";

import { useCallback, useEffect, useMemo, useState } from "react";
import { sendMessage } from "../lib/api";

function safeId() {
  if (typeof crypto !== "undefined" && crypto.randomUUID) {
    return crypto.randomUUID();
  }
  return `${Date.now()}-${Math.random().toString(16).slice(2)}`;
}

const STORAGE_KEY = "estate_scout_chat_messages_v1";

export function useChat() {
  const [messages, setMessages] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  // ✅ FIX: Load messages ONLY on client (no SSR mismatch)
  useEffect(() => {
    try {
      const raw = window.localStorage.getItem(STORAGE_KEY);

      if (!raw) {
        setMessages([
          {
            id: safeId(),
            role: "assistant",
            content: "Hi! Tell me what kind of property you're looking for 🏠",
            createdAt: Date.now(),
          },
        ]);
        return;
      }

      const parsed = JSON.parse(raw);

      if (!Array.isArray(parsed)) {
        setMessages([]);
        return;
      }

      const validMessages = parsed
        .filter(
          (m) =>
            m &&
            typeof m.content === "string" &&
            (m.role === "user" || m.role === "assistant")
        )
        .slice(-50);

      setMessages(validMessages);
    } catch {
      setMessages([]);
    }
  }, []);

  // ✅ Persist chat in localStorage
  useEffect(() => {
    if (!messages.length) return;

    try {
      window.localStorage.setItem(STORAGE_KEY, JSON.stringify(messages));
    } catch {
      // ignore storage errors
    }
  }, [messages]);

  const api = useMemo(
    () => ({
      async sendUserMessage(text) {
        const trimmed = String(text || "").trim();
        if (!trimmed) return;

        setError(null);

        const userMsg = {
          id: safeId(),
          role: "user",
          content: trimmed,
          createdAt: Date.now(),
        };

        setMessages((prev) => [...prev, userMsg]);
        setIsLoading(true);

        try {
          // 🔥 FIX: sendMessage returns STRING (reply)
          const reply = await sendMessage(trimmed);

          console.log("🔥 Reply from backend:", reply);

          const assistantMsg = {
            id: safeId(),
            role: "assistant",
            content: typeof reply === "string" ? reply : "No response from server",
            createdAt: Date.now(),
          };

          setMessages((prev) => [...prev, assistantMsg]);
        } catch (e) {
          console.error("Chat Hook Error:", e);
          setError("Server not responding. Please try again.");
        } finally {
          setIsLoading(false);
        }
      },
    }),
    []
  );

  const clearError = useCallback(() => setError(null), []);

  return {
    messages,
    isLoading,
    error,
    clearError,
    sendUserMessage: api.sendUserMessage,
  };
}