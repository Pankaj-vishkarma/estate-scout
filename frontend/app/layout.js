import "./globals.css";

export const metadata = {
  title: "Estate Scout",
  description: "AI Property Agent dashboard",
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>
        <div className="min-h-screen">{children}</div>
      </body>
    </html>
  );
}

