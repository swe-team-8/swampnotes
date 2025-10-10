import { clerkMiddleware } from '@clerk/nextjs/server';

// We want to use this to protect routes with auth
export default clerkMiddleware({
  authorizedParties: ["http://localhost:3000","http://127.0.0.1:3000"], // can add preview/prod domains later (just dev domain for now)
});

// The below example would set /notes to require auth (turned off for development)
export const config = {
  // Protect these paths (add more as needed)
  //matcher: ["/notes/:path*"],
  matcher: ["/((?!_next/static|_next/image|favicon.ico).*)"]
};