const DEFAULT_API_BASE_URL = "http://localhost:8000";

function getApiBaseUrl() {
  return process.env.NEXT_PUBLIC_API_BASE_URL || DEFAULT_API_BASE_URL;
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
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message }),
      cache: "no-store",
    });

    if (!res.ok) {
      const payload = await readJsonSafe(res);
      console.error("Chat API Error:", payload);
      return "Server error. Please try again.";
    }

    const payload = await res.json();

    // 🔥 RETURN STRING ONLY
    return payload?.reply || "No response from server";
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