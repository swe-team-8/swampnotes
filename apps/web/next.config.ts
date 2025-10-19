import type { NextConfig } from "next";
const isCI = process.env.CI === "true";

const nextConfig: NextConfig = {
  /* config options here */

  // Don't fail the build in CI on lint or TS issues (while we're just testing things)
  eslint: { ignoreDuringBuilds: isCI },
  typescript: { ignoreBuildErrors: isCI },

  // Tell Turbopack THIS folder is the root to silence the lockfile warning
  turbopack: { root: __dirname },
};

export default nextConfig;
