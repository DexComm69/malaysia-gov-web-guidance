// Root layout under app/[lang]/: <html lang> per locale; middleware redirects bare paths to /ms (BM default).
// One <h1> per page: each page renders its own heading; the site name in SiteHeader is a link.
import type { Metadata } from 'next';
import { headers } from 'next/headers';
import '@govtechmy/myds-style/full.css';   // the package only exports full.css, color.css, light.css, dark.css
import { Masthead } from '@/components/Masthead';
import { SiteFooter } from '@/components/SiteFooter';
import { SiteHeader } from '@/components/SiteHeader';
import type { Lang } from '@/lib/splask';

export const metadata: Metadata = {
  title: 'TODO Nama Agensi',                                      // home title under 70 characters
  description: 'TODO one-sentence summary of the site (1-159 characters)',
};

export default async function RootLayout({ children, params }: { children: React.ReactNode; params: Promise<{ lang: string }> }) {
  const { lang: raw } = await params;
  const lang: Lang = raw === 'en' ? 'en' : 'ms';
  const path = ((await headers()).get('x-pathname') ?? `/${lang}`).replace(/^\/(ms|en)/, '') || '';
  return (
    <html lang={lang}>
      <head>
        <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Poppins:wght@500;600&family=Inter:wght@400;500;600&display=swap" />
      </head>
      <body className="font-body">
        <a className="skip-link" href="#kandungan">{lang === 'en' ? 'Skip to main content' : 'Langkau ke kandungan utama'}</a>
        <Masthead lang={lang} />
        <SiteHeader lang={lang} path={path} />
        <main id="kandungan">{children}</main>
        <SiteFooter lang={lang} />
      </body>
    </html>
  );
}
