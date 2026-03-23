"use client";

import { useEffect, useMemo, useState } from "react";
import { AnimatePresence, motion } from "framer-motion";
import { getProperties } from "../../lib/api";
import Loader from "../ui/Loader";
import PropertyCard from "./PropertyCard";

function normalizeProperties(data) {
  if (!Array.isArray(data)) return [];

  return data
    .map((p, idx) => ({
      id: p?.id ?? p?._id ?? `${idx}`,
      title: p?.title || "Untitled Property",
      price: p?.price || "N/A",
      address: p?.address || "Unknown location",
      image: p?.image || "/images/street-1.svg",
    }))
    .slice(0, 60);
}

export default function PropertyGrid() {
  const [properties, setProperties] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  async function loadProperties() {
    setIsLoading(true);
    setError(null);

    try {
      const data = await getProperties();
      console.log("Fetched properties:", data);

      const normalized = normalizeProperties(data);
      setProperties(normalized);
    } catch (e) {
      console.error("PropertyGrid Error:", e);
      setError("Failed to load properties. Check backend connection.");
      setProperties([]);
    } finally {
      setIsLoading(false);
    }
  }

  // 🔥 INITIAL LOAD
  useEffect(() => {
    loadProperties();
  }, []);


  const skeletons = useMemo(() => Array.from({ length: 6 }, (_, i) => i), []);

  return (
    <div className="glass rounded-2xl border border-white/10 overflow-hidden">
      <div className="p-5 border-b border-white/10">
        <div className="flex items-start justify-between gap-4">
          <div>
            <div className="text-lg font-bold tracking-tight text-slate-50">
              Property Grid
            </div>
            <div className="text-xs text-slate-300 mt-1">
              AI curated listings from your backend.
            </div>
          </div>

          <div className="hidden sm:flex items-center gap-2">
            <div className="rounded-full bg-white/5 border border-white/10 px-3 py-1 text-xs text-slate-200">
              {isLoading ? "Loading..." : `${properties.length} results`}
            </div>

            {/* Manual Refresh */}
            <button
              onClick={loadProperties}
              className="text-xs text-slate-300 hover:text-white"
            >
              Refresh
            </button>
          </div>
        </div>
      </div>

      <div className="p-4">
        <AnimatePresence mode="popLayout">
          {isLoading ? (
            <motion.div
              key="skeleton"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              className="grid grid-cols-1 sm:grid-cols-2 gap-4"
            >
              {skeletons.map((i) => (
                <div
                  key={i}
                  className="rounded-2xl border border-white/10 bg-white/5 overflow-hidden"
                >
                  <div className="aspect-[16/10] bg-white/10 animate-pulse" />
                  <div className="p-4 space-y-3">
                    <div className="h-4 bg-white/10 rounded animate-pulse" />
                    <div className="h-4 bg-sky-400/20 rounded animate-pulse" />
                    <div className="h-3 bg-white/10 rounded animate-pulse w-4/5" />
                  </div>
                </div>
              ))}
            </motion.div>
          ) : error ? (
            <motion.div
              key="error"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              className="rounded-2xl border border-red-400/20 bg-red-500/10 p-4"
            >
              <div className="text-sm font-semibold text-red-100">Error</div>
              <div className="mt-1 text-sm text-red-100/90">{error}</div>

              <button
                onClick={loadProperties}
                className="mt-3 text-xs text-red-200 underline"
              >
                Retry
              </button>
            </motion.div>
          ) : properties.length === 0 ? (
            <motion.div
              key="empty"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              className="rounded-2xl border border-white/10 bg-white/5 p-6 text-center"
            >
              <div className="text-sm font-semibold text-slate-200">
                No properties found
              </div>
              <div className="mt-2 text-sm text-slate-300">
                Try again later or check the backend `/properties` endpoint.
              </div>
            </motion.div>
          ) : (
            <motion.div
              key="grid"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              className="grid grid-cols-1 sm:grid-cols-2 gap-4"
            >
              {properties.map((p) => (
                <PropertyCard key={p.id} property={p} />
              ))}
            </motion.div>
          )}
        </AnimatePresence>

        <div className="mt-4 flex sm:hidden items-center justify-center">
          {isLoading ? <Loader label="Loading listings..." /> : null}
        </div>
      </div>
    </div>
  );
}