"use client";

import Link from "next/link";
import { useEffect, useState, useRef } from "react";

import { useChat } from "../hooks/useChat";
import { useAuth } from "../hooks/useAuth";
import AuthModal from "../components/auth/AuthModal";

import ChatWindow from "../components/chat/ChatWindow";
import PropertyGrid from "../components/property/PropertyGrid";
import Button from "../components/ui/Button";

import { FaUserCircle, FaSignOutAlt } from "react-icons/fa";

export default function HomePage() {
  const {
    messages,
    properties,
    isLoading,
    error,
    clearError,
    sendUserMessage,
    loadHistory,
    newSearch,
  } = useChat();

  const { user, logout } = useAuth();

  const [showModal, setShowModal] = useState(false);
  const [isProfileOpen, setIsProfileOpen] = useState(false);

  const dropdownRef = useRef(null);
  const hasCheckedAuth = useRef(false); // ✅ prevent flicker

  // ✅ SAFE AUTH CHECK (NO SSR CRASH)
  useEffect(() => {
    if (typeof window === "undefined") return;

    const token = localStorage.getItem("token");

    if (!token) {
      setShowModal(true);
    }

    hasCheckedAuth.current = true;
  }, []);

  // ✅ CLOSE DROPDOWN OUTSIDE CLICK
  useEffect(() => {
    const handleClickOutside = (event) => {
      if (
        dropdownRef.current &&
        !dropdownRef.current.contains(event.target)
      ) {
        setIsProfileOpen(false);
      }
    };

    document.addEventListener("mousedown", handleClickOutside);
    return () =>
      document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  const handleNewSearch = () => {
    newSearch();
  };

  const handleLoadHistory = () => {
    loadHistory();
  };

  const handleLogout = () => {
    logout();
    window.location.reload();
  };

  return (
    <main className="min-h-screen">
      <div className="relative">

        {/* 🔥 BLUR WHEN NOT LOGGED IN */}
        <div className={showModal ? "blur-sm" : ""}>
          <div className="absolute inset-0 pointer-events-none bg-hero-gradient" />

          <div className="relative mx-auto max-w-7xl px-4 py-6">

            {/* 🔥 HEADER */}
            <header className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 mb-5">

              {/* LEFT */}
              <div>
                <div className="text-2xl sm:text-3xl font-extrabold tracking-tight text-slate-50">
                  Estate Scout
                </div>
                <div className="text-sm text-slate-300 mt-1">
                  AI Property Agent dashboard: chat + listings.
                </div>
              </div>

              {/* RIGHT */}
              <div className="flex items-center gap-3 flex-wrap">

                {/* MAP */}
                <Link href="/map-simulator">
                  <Button variant="ghost" size="md">
                    Map Simulator
                  </Button>
                </Link>

                {/* PROFILE */}
                {user && (
                  <div className="relative" ref={dropdownRef}>
                    <Button
                      variant="ghost"
                      size="md"
                      onClick={() => setIsProfileOpen((prev) => !prev)}
                      className="flex items-center gap-2"
                    >
                      <FaUserCircle className="text-blue-400" />
                      {user?.name || "User"}
                    </Button>

                    {isProfileOpen && (
                      <div className="absolute right-0 mt-2 w-40 bg-slate-900 border border-white/10 rounded-lg shadow-lg overflow-hidden z-50">
                        <button
                          onClick={handleLogout}
                          className="w-full flex items-center gap-2 px-4 py-2 text-sm text-white hover:bg-red-500/20 transition"
                        >
                          <FaSignOutAlt />
                          Logout
                        </button>
                      </div>
                    )}
                  </div>
                )}
              </div>
            </header>

            {/* MAIN GRID */}
            <div className="grid grid-cols-1 lg:grid-cols-12 gap-4">
              <section className="lg:col-span-5 xl:col-span-5">
                <ChatWindow
                  messages={messages}
                  isLoading={isLoading}
                  error={error}
                  onSend={sendUserMessage}
                  onClearError={clearError}
                  onNewSearch={handleNewSearch}
                  onLoadHistory={handleLoadHistory}
                />
              </section>

              <section className="lg:col-span-7 xl:col-span-7">
                <PropertyGrid properties={properties} />
              </section>
            </div>

            <footer className="mt-6 text-center text-xs text-slate-400">
              Estate Scout UI demo.
            </footer>
          </div>
        </div>

        {/* 🔥 AUTH MODAL */}
        {hasCheckedAuth.current && <AuthModal isOpen={showModal} />}

      </div>
    </main>
  );
}