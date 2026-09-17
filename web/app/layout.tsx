import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Análise Apostas 365",
  description: "Análises estatísticas de partidas de futebol.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="pt-BR">
      <body>{children}</body>
    </html>
  );
}
