"use client";

import { useState } from "react";
import { useAuth } from "../../hooks/useAuth";
import { loginUser } from "../../lib/api"; // ✅ NEW
import { FaEnvelope, FaLock } from "react-icons/fa";

export default function LoginForm({ switchToRegister }) {
    const { login } = useAuth();

    const [form, setForm] = useState({
        email: "",
        password: "",
    });

    const [error, setError] = useState("");
    const [loading, setLoading] = useState(false);

    // 🔐 VALIDATION
    const validateForm = () => {
        if (!form.email || !form.password) {
            return "All fields are required";
        }

        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(form.email)) {
            return "Invalid email format";
        }

        if (form.password.length < 6) {
            return "Password must be at least 6 characters";
        }

        return null;
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError("");

        const validationError = validateForm();
        if (validationError) {
            setError(validationError);
            return;
        }

        try {
            setLoading(true);

            const data = await loginUser(form); // ✅ UPDATED

            if (data?.access_token) {
                login(data);
                window.location.reload();
            } else {
                setError(data?.detail || "Login failed");
            }
        } catch (err) {
            console.error("Login Error:", err);
            setError("Something went wrong. Please try again.");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div>
            <h3 className="text-white text-2xl font-semibold mb-4">
                Welcome Back 👋
            </h3>

            <form onSubmit={handleSubmit} className="space-y-4">

                {/* EMAIL */}
                <div className="relative">
                    <FaEnvelope className="absolute left-3 top-3 text-gray-400" />
                    <input
                        type="email"
                        placeholder="Email"
                        value={form.email}
                        className="w-full pl-10 p-2 bg-slate-800 border border-slate-700 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
                        onChange={(e) => setForm({ ...form, email: e.target.value })}
                    />
                </div>

                {/* PASSWORD */}
                <div className="relative">
                    <FaLock className="absolute left-3 top-3 text-gray-400" />
                    <input
                        type="password"
                        placeholder="Password"
                        value={form.password}
                        className="w-full pl-10 p-2 bg-slate-800 border border-slate-700 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
                        onChange={(e) => setForm({ ...form, password: e.target.value })}
                    />
                </div>

                {/* ERROR MESSAGE */}
                {error && (
                    <div className="text-red-400 text-sm">
                        {error}
                    </div>
                )}

                <button
                    disabled={loading}
                    className="w-full bg-gradient-to-r from-blue-500 to-purple-500 text-white p-2 rounded-lg hover:opacity-90 transition disabled:opacity-60"
                >
                    {loading ? "Logging in..." : "Login"}
                </button>
            </form>

            <p className="mt-4 text-sm text-gray-400">
                New user?{" "}
                <span
                    className="text-blue-400 cursor-pointer hover:underline"
                    onClick={switchToRegister}
                >
                    Create account
                </span>
            </p>
        </div>
    );
}