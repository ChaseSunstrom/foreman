import { Inter, Fraunces, JetBrains_Mono } from "next/font/google";

const inter = Inter({ subsets: ["latin"] });
const display = Fraunces({ subsets: ["latin"] });

export default function Layout({ children }) {
  return <body className={`${inter.className} ${display.variable} font-sans`}>{children}</body>;
}
