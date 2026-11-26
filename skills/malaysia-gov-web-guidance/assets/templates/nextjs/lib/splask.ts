// SPLaSK links and helpers for the starter layout (Next.js App Router, server components).
// Tagged links live in code, not in CMS-editable HTML. A null url is not rendered (no placeholder links).

export type Lang = 'ms' | 'en';

// Languages that REALLY have content. Add 'en' only when the English pages exist.
export const LANGUAGES: Lang[] = ['ms'];

export const MYGOV = 'https://www.malaysia.gov.my';

export type SplaskLink = { tag: string | null; url: string | null; ms: string; en: string; updatedAt?: () => Promise<Date | null> };

// updatedAt must read the real last-changed date from the CMS/database (e.g. prisma.page.findUnique(...).updatedAt).
export const MENU: SplaskLink[] = [
  { tag: 'splwpk-about-us', url: '/tentang-kami', ms: 'Tentang Kami', en: 'About Us', updatedAt: async () => null /* TODO */ },
  { tag: 'splwpk-news', url: '/berita', ms: 'Berita', en: 'News', updatedAt: async () => null /* TODO newest news item */ },
  { tag: 'splwpk-faq', url: '/soalan-lazim', ms: 'Soalan Lazim', en: 'FAQ', updatedAt: async () => null /* TODO */ },
  { tag: 'splwpk-contact-details', url: '/hubungi-kami', ms: 'Hubungi Kami', en: 'Contact Us', updatedAt: async () => null /* TODO */ },
];

export const FOOTER: SplaskLink[] = [
  { tag: 'splwpk-privacy-policy', url: '/dasar-privasi', ms: 'Dasar Privasi', en: 'Privacy Policy' },
  { tag: 'splwpk-sitemap', url: '/peta-laman', ms: 'Peta Laman', en: 'Sitemap' },
  { tag: null, url: '/maklum-balas', ms: 'Maklum Balas', en: 'Feedback' }, // the tag goes on the feedback page's <form>
  { tag: 'splwpk-publication', url: null, ms: 'Penerbitan', en: 'Publications' }, // TODO real url
  { tag: 'splwpk-electronic-archive', url: null, ms: 'Arkib', en: 'Archive' }, // TODO real url
];

/** SPLaSK timestamp: YYYY-MM-DD HH:MM:SS in Malaysia time, from a real update. Never new Date(). */
export function formatSplask(d: Date | null): string | undefined {
  if (!d) return undefined;
  const p = new Intl.DateTimeFormat('en-GB', {
    timeZone: 'Asia/Kuala_Lumpur', year: 'numeric', month: '2-digit', day: '2-digit',
    hour: '2-digit', minute: '2-digit', second: '2-digit', hour12: false,
  }).formatToParts(d);
  const v = (t: string) => p.find((x) => x.type === t)?.value ?? '00';
  return `${v('year')}-${v('month')}-${v('day')} ${v('hour')}:${v('minute')}:${v('second')}`;
}
