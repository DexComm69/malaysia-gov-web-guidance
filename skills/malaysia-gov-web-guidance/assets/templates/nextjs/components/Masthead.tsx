// Official MYDS masthead in plain JSX (wording from the MYDS locale files; see guide masthead-html).
// MYDS also ships a React component (@govtechmy/myds-react/masthead): retrieve develop-masthead for its
// exact parts and props before switching to it.
import type { Lang } from '@/lib/splask';

const TEXT = {
  ms: {
    title: 'Portal Rasmi Kerajaan Malaysia', how: 'Kenal pasti begini',
    offH: 'Pautan portal rasmi berakhir dengan .gov.my',
    offB: 'Sekiranya anda melihat pautan selain .gov.my, segera tutupkan halaman itu walaupun ia menyerupai portal rasmi!',
    secH: 'Portal yang selamat menggunakan HTTPS',
    secB: 'Periksa ikon kunci mangga (🔒) atau https:// di depan pautan. Sekiranya tiada, tinggalkan laman sesawang serta merta.',
  },
  en: {
    title: 'Official Malaysia Government Website', how: "Here's how you know",
    offH: 'Official government websites end with .gov.my',
    offB: 'If the link does not end with .gov.my, exit the website immediately even if it looks similar.',
    secH: 'Secure websites use HTTPS',
    secB: 'Look for the lock icon (🔒) or https:// as an added precaution. If not present, leave the site immediately.',
  },
} as const;

export function Masthead({ lang }: { lang: Lang }) {
  const m = TEXT[lang];
  return (
    <details id="masthead" className="masthead bg-bg-washed print:hidden" data-nosnippet>
      <summary className="mx-auto flex max-w-screen-xl items-center gap-2 px-4.5 py-2 md:px-6 text-body-sm text-txt-black-700">
        <img src="/assets/img/malaysia-flag.svg" width={32} height={16} alt="" aria-hidden="true" />
        <span>{m.title}</span>
        <span className="text-txt-primary">{m.how}</span>
      </summary>
      <div className="mx-auto grid max-w-screen-xl gap-4.5 px-4.5 pb-6 pt-3 md:px-6 sm:grid-cols-2">
        <div>
          <p className="text-body-sm font-medium text-txt-black-900">{m.offH}</p>
          <p className="text-body-sm text-txt-black-700">{m.offB}</p>
        </div>
        <div>
          <p className="text-body-sm font-medium text-txt-black-900">{m.secH}</p>
          <p className="text-body-sm text-txt-black-700">{m.secB}</p>
        </div>
      </div>
    </details>
  );
}
