"use client";

import { useState } from "react";
import LoginForm from "./LoginForm";
import RegisterForm from "./RegisterForm";
import { FaHome } from "react-icons/fa";

export default function AuthModal({ isOpen }) {
    const [mode, setMode] = useState("login");

    if (!isOpen) return null;

    return (
        <div className="fixed inset-0 z-50 flex items-center justify-center">

            {/* 🔥 BACKDROP (VISIBLE BG + BLUR) */}
            <div className="absolute inset-0 bg-gradient-to-br from-black/40 via-black/20 to-black/40 backdrop-blur-[2px] transition-all duration-300"></div>

            {/* 🔥 MODAL WRAPPER */}
            <div className="relative w-full max-w-md px-4">

                {/* 🔥 MODAL BOX */}
                <div className="bg-slate-900 rounded-2xl p-6 shadow-2xl border border-white/10 animate-scaleIn max-h-[85vh] overflow-y-auto">

                    {/* HEADER */}
                    <div className="flex items-center gap-2 mb-4">
                        <FaHome className="text-blue-400 text-xl" />
                        <h2 className="text-white font-bold text-lg">
                            Estate Scout AI
                        </h2>
                    </div>

                    {mode === "login" ? (
                        <LoginForm switchToRegister={() => setMode("register")} />
                    ) : (
                        <RegisterForm switchToLogin={() => setMode("login")} />
                    )}

                </div>
            </div>
        </div>
    );
}