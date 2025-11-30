"use client";
import { useEffect, useState } from "react";

type HealthResponse = Record<string, unknown>;

export default function Health() {
  const [data, setData] = useState<HealthResponse | null>(null);
  useEffect(() => {
    (async () => {
      try {
        const res = await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL}/health`);
        setData(await res.json());
      } catch {
        // swallow network error for health page
      }
    })();
  }, []);
  return <pre className="p-3 bg-gray-100 rounded">{JSON.stringify(data, null, 2)}</pre>;
}
