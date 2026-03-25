"use client";

import { useEffect, useState } from "react";

export const useAuth = () => {
    const [user, setUser] = useState(null);

    useEffect(() => {
        try {
            if (typeof window === "undefined") return;

            const storedUser = localStorage.getItem("user");
            const token = localStorage.getItem("token");

            if (!storedUser || !token) return;

            const parsedUser = JSON.parse(storedUser);

            if (parsedUser && parsedUser.id) {
                setUser(parsedUser);
            } else {
                // cleanup invalid data
                localStorage.removeItem("user");
                localStorage.removeItem("token");
            }
        } catch (e) {
            console.error("Auth Load Error:", e);

            // cleanup corrupted data
            localStorage.removeItem("user");
            localStorage.removeItem("token");
        }
    }, []);

    const login = (data) => {
        try {
            if (!data?.access_token || !data?.user) return;

            localStorage.setItem("token", data.access_token);
            localStorage.setItem("user", JSON.stringify(data.user));

            setUser(data.user);
        } catch (e) {
            console.error("Login Error:", e);
        }
    };

    const logout = () => {
        try {
            localStorage.removeItem("token");
            localStorage.removeItem("user");
            setUser(null);
        } catch (e) {
            console.error("Logout Error:", e);
        }
    };

    return { user, login, logout };
};