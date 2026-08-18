import type { Metadata } from "next";
import { headers } from "next/headers";
import "./globals.css";

export async function generateMetadata(): Promise<Metadata> {
  const requestHeaders = await headers();
  const host = (requestHeaders.get("x-forwarded-host") ?? requestHeaders.get("host") ?? "localhost:3000")
    .split(",")[0]
    .trim();
  const protocol = (requestHeaders.get("x-forwarded-proto") ?? (host.startsWith("localhost") ? "http" : "https"))
    .split(",")[0]
    .trim();
  const metadataBase = new URL(`${protocol}://${host}`);
  const socialImage = new URL("/og.png", metadataBase).toString();

  return {
    metadataBase,
    title: "Metabo-Diet | CFDE training module",
    description:
      "A hands-on course in harmonizing dietary and exercise phenotypes with public metabolomics data.",
    openGraph: {
      title: "Metabo-Diet",
      description: "Harmonize phenotype metadata with public metabolomics data.",
      type: "website",
      images: [{ url: socialImage, width: 1536, height: 1024, alt: "Metabo-Diet course card linking a dietary plate through a metabolite crosswalk to an exercise response waveform." }],
    },
    twitter: {
      card: "summary_large_image",
      title: "Metabo-Diet",
      description: "Harmonize phenotype metadata with public metabolomics data.",
      images: [socialImage],
    },
    icons: {
      icon: "/favicon.svg",
      shortcut: "/favicon.svg",
    },
  };
}

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
