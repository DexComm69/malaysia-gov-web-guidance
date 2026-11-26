// Server component: the tags are in the first HTML response, which is what the SPLaSK crawler reads.
import { LANGUAGES, MENU, formatSplask, type Lang } from '@/lib/splask';
import { TextSize } from './TextSize';

export async function SiteHeader({ lang, path }: { lang: Lang; path: string }) {
  const menu = await Promise.all(
    MENU.filter((l) => l.url).map(async (l) => ({ ...l, ts: formatSplask((await l.updatedAt?.()) ?? null) })),
  );
  const en = lang === 'en';
  return (
    <header className="site-header">
      <a className="site-name" href={`/${lang}`}>{en ? 'TODO Agency Name' : 'TODO Nama Agensi'}</a>

      <form action={`/${lang}/carian`} method="get" role="search" splwpk-search-function="splwpk-search-function">
        <label htmlFor="carian">{en ? 'Search' : 'Carian'}</label>
        <input id="carian" name="q" type="search" />
        <button type="submit">{en ? 'Search' : 'Cari'}</button>
      </form>

      <TextSize label={en ? 'Text size' : 'Saiz tulisan'} />

      {LANGUAGES.length > 1 && (
        <nav aria-label={en ? 'Language' : 'Bahasa'} splwpk-multilang="splwpk-multilang">
          {LANGUAGES.map((code) => (
            <a key={code} href={`/${code}${path}`} lang={code} hrefLang={code} aria-current={code === lang ? 'true' : undefined}>
              {code === 'ms' ? 'BM' : 'EN'}
            </a>
          ))}
        </nav>
      )}

      <nav aria-label={en ? 'Main menu' : 'Menu utama'}>
        {menu.map((l) => {
          const tag = l.tag ? { [l.tag]: l.tag } : {};
          return (
            <a key={l.url} href={`/${lang}${l.url}`} {...tag} timestamp={l.ts}>
              {en ? l.en : l.ms}
            </a>
          );
        })}
      </nav>
    </header>
  );
}
