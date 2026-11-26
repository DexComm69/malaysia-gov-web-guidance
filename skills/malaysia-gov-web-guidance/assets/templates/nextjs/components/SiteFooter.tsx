import { FOOTER, MYGOV, type Lang } from '@/lib/splask';

export function SiteFooter({ lang }: { lang: Lang }) {
  const en = lang === 'en';
  return (
    <footer className="site-footer">
      <nav aria-label={en ? 'Footer' : 'Pautan kaki'}>
        {FOOTER.filter((l) => l.url).map((l) => (
          <a key={l.url} href={`/${lang}${l.url}`} {...(l.tag ? { [l.tag]: l.tag } : {})}>
            {en ? l.en : l.ms}
          </a>
        ))}
        <a href={MYGOV}>MyGov</a>
      </nav>
      <p>
        &copy; {new Date().getFullYear()} {en ? 'TODO Agency Name. All Rights Reserved.' : 'TODO Nama Agensi. Hak Cipta Terpelihara.'}
      </p>
    </footer>
  );
}
