"use client";
import { useAuth } from "@clerk/nextjs";
import { useEffect, useState } from "react";

export default function WhoAmI() {
  const { isSignedIn, getToken } = useAuth();
  const [me, setMe] = useState<any>(null);

  useEffect(() => {
    (async () => {
      const token = isSignedIn ? await getToken({ template: "fastapi" }) : null;
      const res = await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL}/auth/me`, {
        headers: token ? { Authorization: `Bearer ${token}` } : {},
        cache: "no-store",
      });
      setMe(await res.json());
    })();
  }, [isSignedIn, getToken]);

  return <pre className="p-3 bg-gray-100 rounded">{JSON.stringify(me, null, 2)}</pre>;
}
