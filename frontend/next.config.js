/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,

  // 🔥 FIX: allow external images
  images: {
    domains: ["source.unsplash.com"],
  },
};

export default nextConfig;