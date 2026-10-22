import { Inter } from "next/font/google"; // expect

const inter = Inter({ subsets: ["latin"] });

export default function Layout({ children }) {
  return <body className={`${inter.className} font-sans`}>{children}</body>;
}
