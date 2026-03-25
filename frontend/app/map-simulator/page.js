"use client";

import { useMemo, useState } from "react";
import { useRouter } from "next/navigation";
import { FaArrowLeft } from "react-icons/fa";

export default function MapSimulatorPage() {
  const router = useRouter();

  const images = useMemo(
    () => [
      "/images/apartment1.jpg",
      "/images/apartment2.jpg",
      "/images/apartment3.jpg",
      "/images/apartment4.jpg",
      "/images/apartment5.jpg",
      "/images/apartment6.jpg",
      "/images/apartment7.jpg",
      "/images/apartment8.jpg",
      "/images/apartment9.jpg",
      "/images/apartment10.jpg",
      "/images/apartment11.jpg",
      "/images/apartment12.jpg",
      "/images/apartment13.jpg",
    ],
    []
  );

  const [query, setQuery] = useState("");
  const [selectedImg, setSelectedImg] = useState(images[0] || "");
  const [loading, setLoading] = useState(false);

  // ✅ Use existing ENV
  const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL;

  async function viewStreetView() {
    console.log("Map search triggered for:", query);

    setLoading(true);
    setSelectedImg("");

    try {
      // ✅ Call backend endpoint (you can create this later)
      if (API_BASE) {
        const res = await fetch(`${API_BASE}/map-simulator?q=${query}`);

        if (res.ok) {
          const data = await res.json();

          if (data?.image) {
            setSelectedImg(data.image);
          } else {
            const index = query.length % images.length;
            setSelectedImg(images[index]);
          }
        } else {
          throw new Error("API failed");
        }
      } else {
        throw new Error("No API base");
      }
    } catch (error) {
      console.warn("Using fallback image:", error.message);

      // ✅ deterministic fallback (NO RANDOM)
      const index = query.length % images.length;

      setTimeout(() => {
        setSelectedImg(images[index]);
      }, 500);
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="min-h-screen">
      <div className="mx-auto max-w-4xl px-4 py-8">

        {/* 🔥 BACK BUTTON */}
        <div className="mb-4">
          <button
            onClick={() => router.push("/")}
            className="flex items-center gap-2 px-4 py-2 rounded-xl bg-white/5 border border-white/10 text-slate-200 hover:bg-white/10 transition"
          >
            <FaArrowLeft />
            Back
          </button>
        </div>

        <div className="glass rounded-2xl border border-white/10 p-5">
          <div className="text-2xl font-extrabold tracking-tight text-slate-50">
            Map Simulator
          </div>

          <div className="mt-1 text-sm text-slate-300">
            Used by the AI agent via Selenium/Playwright.
          </div>

          {/* 🔥 IMPORTANT: Agent selectors */}
          <div className="mt-6 flex gap-3 flex-col sm:flex-row">
            <input
              id="search-box"
              name="search-box"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Search address or neighborhood..."
              className="w-full rounded-2xl bg-white/5 border border-white/10 px-4 py-3 text-slate-100 placeholder:text-slate-400 outline-none focus-visible:ring-2 focus-visible:ring-sky-400"
            />

            <button
              id="search-btn"
              name="search-btn"
              type="button"
              onClick={viewStreetView}
              className="rounded-2xl bg-sky-500/15 border border-sky-400/20 px-5 py-3 font-semibold text-sky-50 hover:bg-sky-500/25 transition focus-visible:ring-2 focus-visible:ring-sky-400"
            >
              View Street View
            </button>
          </div>

          <div className="mt-6">
            {/* ✅ IMPORTANT: Selenium container */}
            <div
              id="street-view"
              data-testid="street-view"
              className="relative aspect-[16/9] rounded-2xl overflow-hidden border border-white/10 bg-white/5"
            >
              {loading && (
                <div className="absolute inset-0 flex items-center justify-center bg-black/30">
                  <p className="animate-pulse text-sm text-white">
                    Loading...
                  </p>
                </div>
              )}

              <img
                id="street-view-image"
                data-loaded={selectedImg ? "true" : "false"}
                src={selectedImg}
                alt="Simulated street view"
                className="h-full w-full object-cover"
                onError={(e) => {
                  e.currentTarget.src = "/images/apartment1.jpg";
                }}
              />
            </div>

            <div className="mt-3 text-xs text-slate-400">
              Query:{" "}
              <span className="text-slate-200">
                {query ? query : "—"}
              </span>
            </div>
          </div>
        </div>
      </div>
    </main>
  );
}