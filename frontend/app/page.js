"use client";

import Link from "next/link";
import { useChat } from "../hooks/useChat";
import ChatWindow from "../components/chat/ChatWindow";
import PropertyGrid from "../components/property/PropertyGrid";
import Button from "../components/ui/Button";

export default function HomePage() {
  const { messages, isLoading, error, clearError, sendUserMessage } = useChat();

  return (
    <main className="min-h-screen">
      <div className="relative">
        <div className="absolute inset-0 pointer-events-none bg-hero-gradient" />
        <div className="relative mx-auto max-w-7xl px-4 py-6">
          <header className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 mb-5">
            <div>
              <div className="text-2xl sm:text-3xl font-extrabold tracking-tight text-slate-50">
                Estate Scout
              </div>
              <div className="text-sm text-slate-300 mt-1">
                AI Property Agent dashboard: chat + listings.
              </div>
            </div>
            <div className="flex gap-2">
              <Link href="/map-simulator">
                <Button variant="ghost" size="md">
                  Map Simulator
                </Button>
              </Link>
            </div>
          </header>

          <div className="grid grid-cols-1 lg:grid-cols-12 gap-4">
            <section className="lg:col-span-5 xl:col-span-5">
              <ChatWindow
                messages={messages}
                isLoading={isLoading}
                error={error}
                onSend={sendUserMessage}
                onClearError={clearError}
              />
            </section>

            <section className="lg:col-span-7 xl:col-span-7">
              <PropertyGrid key={messages.length} />
            </section>
          </div>

          <footer className="mt-6 text-center text-xs text-slate-400">
            Estate Scout UI demo. Connect your backend at `http://localhost:8000`.
          </footer>
        </div>
      </div>
    </main>
  );
}

