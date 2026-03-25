const DEFAULT_API_BASE_URL = "http://localhost:8000";

function getApiBaseUrl() {
  return process.env.NEXT_PUBLIC_API_BASE_URL || DEFAULT_API_BASE_URL;
}

// ✅ SAFE LOCALSTORAGE (SSR SAFE)
function getAuthHeaders() {
  if (typeof window === "undefined") {
    return { "Content-Type": "application/json" };
  }

  const token = localStorage.getItem("token");

  return {
    "Content-Type": "application/json",
    ...(token && { Authorization: `Bearer ${token}` }),
  };
}

// ✅ FETCH WITH TIMEOUT
async function fetchWithTimeout(url, options = {}, timeout = 10000) {
  const controller = new AbortController();
  const id = setTimeout(() => controller.abort(), timeout);

  try {
    const res = await fetch(url, {
      ...options,
      signal: controller.signal,
    });
    return res;
  } finally {
    clearTimeout(id);
  }
}

// ✅ SAFE JSON PARSER
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

    // 🔥 IMPORTANT: long timeout for AI
    const res = await fetchWithTimeout(
      `${baseUrl}/chat`,
      {
        method: "POST",
        headers: getAuthHeaders(),
        body: JSON.stringify({ message }),
        cache: "no-store",
      },
      60000 // ✅ 60 seconds
    );

    if (!res.ok) {
      const payload = await readJsonSafe(res);
      return {
        reply: payload?.detail || "Server error. Please try again.",
        properties: [],
      };
    }

    const payload = await res.json();

    return {
      reply: payload?.reply || "No response",
      properties: Array.isArray(payload?.properties)
        ? payload.properties
        : [],
    };

  } catch (error) {
    console.error("Chat Timeout/Error:", error);

    return {
      reply: "AI is taking longer than expected. Please wait or try again.",
      properties: [],
    };
  }
}

// 🔥 PROPERTY API
export async function getProperties() {
  try {
    const baseUrl = getApiBaseUrl();

    const res = await fetchWithTimeout(`${baseUrl}/properties`, {
      method: "GET",
      headers: getAuthHeaders(),
      cache: "no-store",
    });

    if (!res.ok) return [];

    const payload = await res.json();

    return Array.isArray(payload)
      ? payload
      : Array.isArray(payload?.properties)
        ? payload.properties
        : [];
  } catch {
    return [];
  }
}

// 🔥 HISTORY API
export async function getHistory() {
  try {
    const baseUrl = getApiBaseUrl();

    const res = await fetchWithTimeout(`${baseUrl}/history`, {
      method: "GET",
      headers: getAuthHeaders(),
      cache: "no-store",
    });

    if (!res.ok) return { messages: [], properties: [] };

    const payload = await res.json();

    return {
      messages: Array.isArray(payload?.messages) ? payload.messages : [],
      properties: Array.isArray(payload?.properties) ? payload.properties : [],
    };
  } catch {
    return { messages: [], properties: [] };
  }
}

// 🔐 LOGIN API
export async function loginUser(data) {
  try {
    const baseUrl = getApiBaseUrl();

    const res = await fetchWithTimeout(`${baseUrl}/auth/login`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    });

    const payload = await readJsonSafe(res);

    return payload;
  } catch {
    return null;
  }
}

// 🔐 REGISTER API
export async function registerUser(data) {
  try {
    const baseUrl = getApiBaseUrl(); // ✅ FIXED

    const res = await fetchWithTimeout(`${baseUrl}/auth/register`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    });

    const payload = await readJsonSafe(res);

    return payload;
  } catch {
    return null;
  }
}

// 🔐 LOGOUT
export function logoutUser() {
  if (typeof window !== "undefined") {
    localStorage.removeItem("token");
    localStorage.removeItem("user");
  }
}