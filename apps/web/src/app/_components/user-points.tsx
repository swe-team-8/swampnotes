"use client";

import { Coins } from "lucide-react";
import { usePoints } from "./points-provider";

export function UserPoints() {
  const { points, loading } = usePoints();

  if (loading) {
    return null;
  }

  return (
    <div className="flex items-center gap-2 px-3 py-1.5 bg-gradient-to-r from-amber-50 to-yellow-50 border border-amber-200 rounded-lg">
      <Coins className="w-4 h-4 text-amber-600" />
      <span className="text-sm font-semibold text-amber-900">
        {points?.toLocaleString() ?? 0}
      </span>
    </div>
  );
}