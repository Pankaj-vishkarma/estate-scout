"use client";

import { useState } from "react";
import { registerUser } from "../../lib/api"; // ✅ NEW
import { FaUser, FaEnvelope, FaLock } from "react-icons/fa";

export default function RegisterForm({ switchToLogin }) {
    const [form, setForm] = useState({
        name: "",
        email: "",
        password: "",
    });

    const [error, setError] = useState("");
    const [loading, setLoading] = useState(false);
    const [success, setSuccess] = useState("");

    // 🔐 VALIDATION
    const validateForm = () => {
        if (!form.name || !form.email || !form.password) {
            return "All fields are required";
        }

        if (form.name.length < 2) {
            return "Name must be at least 2 characters";
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

        console.log("🔥 REGISTER CLICKED"); // ADD THIS

        setError("");
        setSuccess("");

        const validationError = validateForm();
        if (validationError) {
            setError(validationError);
            return;
        }

        try {
            setLoading(true);

            console.log("🚀 CALLING REGISTER API"); // ADD THIS

            const data = await registerUser(form);

            console.log("📦 RESPONSE:", data); // ADD THIS

            if (data && !data?.detail) {
                setSuccess("Registered successfully 🎉");

                setTimeout(() => {
                    switchToLogin();
                }, 1000);
            } else {
                setError(data?.detail || "Registration failed");
            }
        } catch (err) {
            console.error("❌ ERROR:", err);
            setError("Something went wrong. Please try again.");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div>
            <h3 className="text-white text-2xl font-semibold mb-4">
                Create Account 🚀
            </h3>

            <form onSubmit={handleSubmit} className="space-y-4">

                {/* NAME */}
                <div className="relative">
                    <FaUser className="absolute left-3 top-3 text-gray-400" />
                    <input
                        type="text"
                        placeholder="Name"
                        value={form.name}
                        className="w-full pl-10 p-2 bg-slate-800 border border-slate-700 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-purple-500"
                        onChange={(e) => setForm({ ...form, name: e.target.value })}
                    />
                </div>

                {/* EMAIL */}
                <div className="relative">
                    <FaEnvelope className="absolute left-3 top-3 text-gray-400" />
                    <input
                        type="email"
                        placeholder="Email"
                        value={form.email}
                        className="w-full pl-10 p-2 bg-slate-800 border border-slate-700 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-purple-500"
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
                        className="w-full pl-10 p-2 bg-slate-800 border border-slate-700 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-purple-500"
                        onChange={(e) => setForm({ ...form, password: e.target.value })}
                    />
                </div>

                {/* ERROR */}
                {error && (
                    <div className="text-red-400 text-sm">
                        {error}
                    </div>
                )}

                {/* SUCCESS */}
                {success && (
                    <div className="text-green-400 text-sm">
                        {success}
                    </div>
                )}

                <button
                    disabled={loading}
                    className="w-full bg-gradient-to-r from-purple-500 to-blue-500 text-white p-2 rounded-lg hover:opacity-90 transition disabled:opacity-60"
                >
                    {loading ? "Creating account..." : "Register"}
                </button>
            </form>

            <p className="mt-4 text-sm text-gray-400">
                Already have an account?{" "}
                <span
                    className="text-blue-400 cursor-pointer hover:underline"
                    onClick={switchToLogin}
                >
                    Login
                </span>
            </p>
        </div>
    );
}