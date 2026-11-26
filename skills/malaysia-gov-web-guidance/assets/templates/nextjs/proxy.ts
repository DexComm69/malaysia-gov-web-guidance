// Locale routing for the starter layout:
// - bare paths go to the BM version (/ -> /ms, /berita -> /ms/berita): BM is the default on gov sites;
// - /en/... is only served when English content really exists (LANGUAGES in lib/splask.ts);
// - passes the path without the locale to the layout in an `x-pathname` header, so the language switch
//   can link to the same page in the other language.
// Next.js 16+: this file is proxy.ts with `export function proxy`. On Next.js 15 or older, name it
// middleware.ts and rename the function to `middleware`.
import { NextResponse, type NextRequest } from 'next/server';
import { LANGUAGES } from '@/lib/splask';

export function proxy(req: NextRequest) {
  const { pathname } = req.nextUrl;
  const m = pathname.match(/^\/(ms|en)(?=\/|$)/);
  if (!m || !(LANGUAGES as string[]).includes(m[1])) {
    const url = req.nextUrl.clone();
    url.pathname = '/ms' + (m ? pathname.slice(3) : pathname === '/' ? '' : pathname);
    return NextResponse.redirect(url);
  }
  const headers = new Headers(req.headers);
  headers.set('x-pathname', pathname);
  return NextResponse.next({ request: { headers } });
}

export const config = {
  // everything except Next.js internals, API routes and files with an extension (images, the MYDS flag, ...)
  matcher: ['/((?!_next|api|.*\\..*).*)'],
};
