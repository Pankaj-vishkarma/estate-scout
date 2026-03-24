"use client";

import { useCallback, useMemo, useState } from "react";
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
          const res = await sendMessage(trimmed);

          // 🔥 handle reply properly
          const reply =
            typeof res === "string" ? res : res?.reply || "No response from server";

          const assistantMsg = {
            id: safeId(),
            role: "assistant",
            content: reply,
            createdAt: Date.now(),
          };

          setMessages((prev) => [...prev, assistantMsg]);

          // 🔥 SET ONLY CURRENT SEARCH PROPERTIES
          if (res?.properties) {
            setProperties(res.properties);
          } else {
            setProperties([]);
          }

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

  // 🔥 HISTORY FROM BACKEND
  const loadHistory = useCallback(async () => {
    try {
      setIsLoading(true);

      const data = await getHistory();

      if (data?.messages) {
        setMessages(data.messages);
      }

      if (data?.properties) {
        setProperties(data.properties);
      }
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