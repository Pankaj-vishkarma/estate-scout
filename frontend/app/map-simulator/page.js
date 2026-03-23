"use client";

import { useMemo, useState } from "react";

export default function MapSimulatorPage() {
  const images = useMemo(
    () => [
      "/images/street-1.svg",
      "/images/street-2.svg",
      "/images/street-3.svg",
      "/images/street-4.svg",
      "/images/street-5.svg",
      "/images/street-6.svg",
    ],
    []
  );

  const [query, setQuery] = useState("");
  const [selectedImg, setSelectedImg] = useState(images[0]);

  function viewStreetView() {
    // 🔥 Ensure new image always loads
    let next = selectedImg;

    while (next === selectedImg && images.length > 1) {
      next = images[Math.floor(Math.random() * images.length)];
    }

    console.log("Map search triggered for:", query);

    setSelectedImg(next);
  }

  return (
    <main className="min-h-screen">
      <div className="mx-auto max-w-4xl px-4 py-8">
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
            <div className="aspect-[16/9] rounded-2xl overflow-hidden border border-white/10 bg-white/5">
              {/* eslint-disable-next-line @next/next/no-img-element */}
              <img
                id="street-view-image" // 🔥 agent screenshot target
                src={selectedImg}
                alt="Simulated street view"
                className="h-full w-full object-cover"
                onError={(e) => {
                  e.currentTarget.src = "/images/street-1.svg";
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