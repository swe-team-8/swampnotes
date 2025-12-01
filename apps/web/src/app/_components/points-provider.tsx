"use client";

import { createContext, useContext, useState, useEffect, useCallback } from "react";
import { useAuth } from "@clerk/nextjs";

interface PointsContextType {
  points: number | null;
  loading: boolean;
  refreshPoints: () => Promise<void>;
}

const PointsContext = createContext<PointsContextType | undefined>(undefined);

export function PointsProvider({ children }: { children: React.ReactNode }) {
  const { getToken, isSignedIn } = useAuth();
  const [points, setPoints] = useState<number | null>(null);
  const [loading, setLoading] = useState(true);

  const refreshPoints = useCallback(async () => {
    if (!isSignedIn) {
      setPoints(null);
      setLoading(false);
      return;
    }

    try {
      const token = await getToken({ template: "fastapi" });
      if (!token) {
        setPoints(0);
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
        setPoints(0);
      }
    } catch (error) {
      console.error('Failed to fetch user points:', error);
      setPoints(0);
    } finally {
      setLoading(false);
    }
  }, [isSignedIn, getToken]);

  useEffect(() => {
    refreshPoints();
  }, [refreshPoints]);

  return (
    <PointsContext.Provider value={{ points, loading, refreshPoints }}>
      {children}
    </PointsContext.Provider>
  );
}

export function usePoints() {
  const context = useContext(PointsContext);
  if (context === undefined) {
    throw new Error('usePoints must be used within a PointsProvider');
  }
  return context;
}