import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Análise Apostas 365",
  description:
    "Análise estatística de partidas de futebol.",
  keywords: [
    "futebol",
    "estatísticas",
    "análise esportiva",
    "apostas",
    "jogos",
  ],
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
