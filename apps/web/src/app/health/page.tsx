"use client";
import { useAuth } from "@clerk/nextjs";
import { useEffect, useState } from "react";

export default function health() {
  const [me, setMe] = useState<any>(null);
  useEffect(() => {
    (async () => {
      const res = await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL}/health`, {});
      setMe(await res.json());
    })();
  }, []);

  return <pre className="p-3 bg-gray-100 rounded">{JSON.stringify(me, null, 2)}</pre>;
}
