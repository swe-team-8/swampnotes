"use client";

import "./globals.css";
import { ClerkProvider } from "@clerk/nextjs";
import { Inter } from "next/font/google";
import Header from "./_components/header";
import { PointsProvider } from "./_components/points-provider";

const inter = Inter({ subsets: ["latin"] });

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <ClerkProvider>
      <html lang="en">
        <body className={inter.className}>
          <PointsProvider>
            <Header />
            {children}
          </PointsProvider>
        </body>
      </html>
    </ClerkProvider>
  );
}
