"use client";

import { useAuth } from "@clerk/nextjs";
import { useEffect, useState } from "react";
import { Coins } from "lucide-react";

export function UserPoints() {
  const { getToken, isSignedIn } = useAuth();
  const [points, setPoints] = useState<number | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchPoints() {
      if (!isSignedIn) {
        setLoading(false);
        return;
      }

      try {
        // Need to include the "aud" claim in the token
        const token = await getToken({ template: "fastapi" });
        
        if (!token) {
          console.error('No token available');
          setPoints(0);
          setLoading(false);
          return;
        }

        const response = await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL}/users/me`, {
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json',
          },
        });

        if (response.ok) {
          const data = await response.json();
          setPoints(data.user?.points ?? 0);
        } else {
          const errorText = await response.text();
          console.error('Failed to fetch points, status:', response.status, 'Error:', errorText);
          setPoints(0);
        }
      } catch (error) {
        console.error('Failed to fetch user points:', error);
        setPoints(0);
      } finally {
        setLoading(false);
      }
    }

    fetchPoints();
  }, [isSignedIn, getToken]);

  if (!isSignedIn || loading) {
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