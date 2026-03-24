const DEFAULT_API_BASE_URL = "http://localhost:8000";

function getApiBaseUrl() {
  return process.env.NEXT_PUBLIC_API_BASE_URL || DEFAULT_API_BASE_URL;
}

// 🔐 NEW: Auth Headers
function getAuthHeaders() {
  const token = localStorage.getItem("token");

  return {
    "Content-Type": "application/json",
    ...(token && { Authorization: `Bearer ${token}` }),
  };
}

// Safe JSON reader
async function readJsonSafe(res) {
  const contentType = res.headers.get("content-type") || "";

  if (contentType.includes("application/json")) {
    return res.json();
  }

  const text = await res.text();
  try {
    return JSON.parse(text);
  } catch {
    return { raw: text };
  }
}

// 🔥 CHAT API
export async function sendMessage(message) {
  try {
    const baseUrl = getApiBaseUrl();

    const res = await fetch(`${baseUrl}/chat`, {
      method: "POST",
      headers: getAuthHeaders(), // ✅ UPDATED
      body: JSON.stringify({ message }),
      cache: "no-store",
    });

    if (!res.ok) {
      const payload = await readJsonSafe(res);
      console.error("Chat API Error:", payload);
      return "Server error. Please try again.";
    }

    const payload = await res.json();

    return payload || "No response from server";
  } catch (error) {
    console.error("Chat Fetch Error:", error);
    return "Unable to connect to server.";
  }
}

// 🔥 PROPERTY API
export async function getProperties() {
  try {
    const baseUrl = getApiBaseUrl();

    const res = await fetch(`${baseUrl}/properties`, {
      method: "GET",
      cache: "no-store",
    });

    if (!res.ok) {
      const payload = await readJsonSafe(res);
      console.error("Property API Error:", payload);
      return [];
    }

    const payload = await res.json();

    if (Array.isArray(payload)) return payload;
    if (Array.isArray(payload?.properties)) return payload.properties;

    return [];
  } catch (error) {
    console.error("Property Fetch Error:", error);
    return [];
  }
}

// 🔥 HISTORY API (UPDATED WITH AUTH)
export async function getHistory() {
  try {
    const baseUrl = getApiBaseUrl();

    const res = await fetch(`${baseUrl}/history`, {
      method: "GET",
      headers: getAuthHeaders(), // ✅ UPDATED
      cache: "no-store",
    });

    if (!res.ok) {
      const payload = await readJsonSafe(res);
      console.error("History API Error:", payload);
      return { messages: [], properties: [] };
    }

    const payload = await res.json();

    return {
      messages: Array.isArray(payload?.messages) ? payload.messages : [],
      properties: Array.isArray(payload?.properties) ? payload.properties : [],
    };
  } catch (error) {
    console.error("History Fetch Error:", error);
    return { messages: [], properties: [] };
  }
}

// 🔐 LOGIN API (FIXED)
export async function loginUser(data) {
  try {
    console.log("API CALL START");

    const baseUrl = getApiBaseUrl();

    const res = await fetch(`${baseUrl}/auth/login`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    });

    console.log("API STATUS:", res.status);

    const payload = await res.json();

    console.log("API RESPONSE:", payload);

    return payload;
  } catch (error) {
    console.error("Login Error:", error);
    return null;
  }
}

// 🔐 REGISTER API
export async function registerUser(data) {
  try {
    console.log("🚀 REGISTER API START");

    const baseUrl = "http://localhost:8000";

    const res = await fetch(`${baseUrl}/auth/register`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    });

    console.log("✅ RESPONSE STATUS:", res.status);

    const payload = await res.json();

    console.log("📦 RESPONSE DATA:", payload);

    return payload;
  } catch (error) {
    console.error("❌ REGISTER ERROR:", error);
    return null;
  }
}

// 🔐 LOGOUT (BONUS - SAFE)
export function logoutUser() {
  localStorage.removeItem("token");
  localStorage.removeItem("user");
}