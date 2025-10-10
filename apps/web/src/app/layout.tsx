import "./globals.css";
import { ClerkProvider } from "@clerk/nextjs";
import Header from "./_components/header";


// Clerk auth
export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <ClerkProvider>
      <html lang="en">
        <body>
          <Header />
          {children}
        </body>
      </html>
    </ClerkProvider>
  );
}
