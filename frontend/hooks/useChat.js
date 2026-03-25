"use client";

import { useCallback, useMemo, useRef, useState } from "react";
import { sendMessage, getHistory } from "../lib/api";

function safeId() {
  if (typeof crypto !== "undefined" && crypto.randomUUID) {
    return crypto.randomUUID();
  }
  return `${Date.now()}-${Math.random().toString(16).slice(2)}`;
}

export function useChat() {
  const [messages, setMessages] = useState([]);
  const [properties, setProperties] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  const isRequesting = useRef(false); // ✅ prevent duplicate calls

  const api = useMemo(
    () => ({
      async sendUserMessage(text) {
        const trimmed = String(text || "").trim();
        if (!trimmed || isRequesting.current) return;

        isRequesting.current = true;
        setError(null);

        const userMsg = {
          id: safeId(),
          role: "user",
          content: trimmed,
          createdAt: Date.now(),
        };

        setIsLoading(true);

        try {
          const res = await sendMessage(trimmed);

          const reply =
            typeof res === "string"
              ? res
              : res?.reply || "No response from server";

          const assistantMsg = {
            id: safeId(),
            role: "assistant",
            content: reply,
            createdAt: Date.now(),
          };

          // ✅ SINGLE STATE UPDATE (performance)
          setMessages((prev) => [...prev, userMsg, assistantMsg]);

          // ✅ safe property update
          setProperties(
            Array.isArray(res?.properties) ? res.properties : []
          );
        } catch (e) {
          console.error("Chat Hook Error:", e);
          setError("Server not responding. Please try again.");

          // ✅ still push user message (UX safe)
          setMessages((prev) => [...prev, userMsg]);
        } finally {
          setIsLoading(false);
          isRequesting.current = false;
        }
      },
    }),
    []
  );

  const clearError = useCallback(() => setError(null), []);

  // 🔥 HISTORY
  const loadHistory = useCallback(async () => {
    try {
      setIsLoading(true);

      const data = await getHistory();

      // ✅ safe guards
      setMessages(
        Array.isArray(data?.messages) ? data.messages : []
      );

      setProperties(
        Array.isArray(data?.properties) ? data.properties : []
      );
    } catch (err) {
      console.error("History Load Error:", err);
    } finally {
      setIsLoading(false);
    }
  }, []);

  // 🔥 NEW SEARCH
  const newSearch = useCallback(() => {
    setMessages([
      {
        id: safeId(),
        role: "assistant",
        content: "Hi! Tell me what kind of property you're looking for 🏠",
        createdAt: Date.now(),
      },
    ]);

    setProperties([]);
    setError(null);
  }, []);

  return {
    messages,
    properties,
    isLoading,
    error,
    clearError,
    sendUserMessage: api.sendUserMessage,
    loadHistory,
    newSearch,
  };
}