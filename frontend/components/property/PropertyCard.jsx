"use client";

import { motion } from "framer-motion";

const BASE_URL =
  process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:8000";

function resolveImage(img) {
  if (!img || typeof img !== "string") return null;

  // 🔥 FIX: local frontend images
  if (img.startsWith("/images")) {
    return img; // ✅ frontend serve karega
  }

  // 🔥 backend files (screenshots)
  if (img.startsWith("/data")) {
    return `${BASE_URL}${img}`;
  }

  return img;
}

function getPropTitle(p) {
  return p?.title || p?.name || p?.listingTitle || "Untitled Listing";
}

function formatPrice(price) {
  if (price === null || price === undefined || price === "") return "—";

  const cleaned = String(price).replace(/[^\d.]/g, "");
  const n = Number(cleaned);

  if (Number.isFinite(n)) {
    return n.toLocaleString("en-IN", {
      style: "currency",
      currency: "INR",
      maximumFractionDigits: 0,
    });
  }

  return String(price);
}

function getPropAddress(p) {
  return p?.address || p?.location || p?.streetAddress || "Address unavailable";
}

export default function PropertyCard({ property }) {
  if (!property || typeof property !== "object") return null;

  const title = getPropTitle(property);
  const price = formatPrice(property?.price);
  const address = getPropAddress(property);

  // 🔥 IMAGE RESOLVE
  const primaryImage = resolveImage(property?.image); // local image
  const streetImage = resolveImage(property?.street_view); // screenshot

  // 🔥 FINAL STRICT PRIORITY FIX
  let finalImage = "/images/street-1.svg";

  if (primaryImage && primaryImage.includes("/images")) {
    finalImage = primaryImage; // ✅ ALWAYS local image first
  } else if (streetImage) {
    finalImage = streetImage; // fallback
  }

  return (
    <motion.div
      whileHover={{ scale: 1.02 }}
      className="rounded-2xl overflow-hidden glass border border-white/10"
    >
      <div className="relative">
        <div className="aspect-[16/10] bg-white/5">
          {/* eslint-disable-next-line @next/next/no-img-element */}
          <img
            src={finalImage}
            alt={title}
            className="h-full w-full object-cover"
            loading="lazy"
            onError={(e) => {
              e.currentTarget.src = "/images/street-1.svg";
            }}
          />
        </div>

        <div className="absolute left-3 top-3">
          <div className="rounded-full bg-black/30 border border-white/10 px-3 py-1 text-[11px] text-slate-100 font-semibold">
            Featured
          </div>
        </div>
      </div>

      <div className="p-4">
        <div className="text-sm font-bold tracking-tight text-slate-50">
          {title}
        </div>

        <div className="mt-2 text-sky-200 font-semibold text-sm">
          {price}
        </div>

        <div className="mt-1 text-xs text-slate-300">{address}</div>
      </div>
    </motion.div>
  );
}