{{-- Tags are plain attributes in the server HTML: no Alpine x-bind or Vue binding for splwpk-*. --}}
<header class="site-header">
    <a class="site-name" href="/">{{ config('app.name') }}</a>

    <form action="/carian" method="get" role="search" splwpk-search-function="splwpk-search-function">
        <label for="carian">{{ $lang === 'en' ? 'Search' : 'Carian' }}</label>
        <input id="carian" name="q" type="search" value="{{ request('q') }}">
        <button type="submit">{{ $lang === 'en' ? 'Search' : 'Cari' }}</button>
    </form>
    {{-- The advanced-search page's <form> carries splwpk-advanced-search-function; register that page as a Criteria URL. --}}
    <a href="/carian-terperinci">{{ $lang === 'en' ? 'Advanced search' : 'Carian terperinci' }}</a>

    <div role="group" aria-label="{{ $lang === 'en' ? 'Text size' : 'Saiz tulisan' }}" splwpk-w3c="splwpk-w3c">
        <button type="button" data-fs="0.875" aria-label="{{ $lang === 'en' ? 'Smaller text' : 'Kecilkan tulisan' }}" aria-pressed="false">A-</button><button type="button" data-fs="1" aria-label="{{ $lang === 'en' ? 'Normal text size' : 'Saiz tulisan biasa' }}" aria-pressed="true">A</button><button type="button" data-fs="1.25" aria-label="{{ $lang === 'en' ? 'Larger text' : 'Besarkan tulisan' }}" aria-pressed="false">A+</button>
    </div>

    @if (count($splaskLanguages) > 1)
        <div class="lang-switch" splwpk-multilang="splwpk-multilang">
            @foreach ($splaskLanguages as $code)
                <a href="{{ request()->fullUrlWithQuery(['lang' => $code]) }}" lang="{{ $code }}" hreflang="{{ $code }}" @if ($code === $lang) aria-current="true" @endif>{{ $code === 'ms' ? 'BM' : 'EN' }}</a>
            @endforeach
        </div>
    @endif

    <nav aria-label="{{ $lang === 'en' ? 'Main menu' : 'Menu utama' }}">
        @foreach ($splaskMenu as $link)
            <a href="{{ $link['url'] }}" {{ $link['tag'] }}="{{ $link['tag'] }}" @if ($link['timestamp']) timestamp="{{ $link['timestamp'] }}" @endif>{{ $link[$lang] }}</a>
        @endforeach
    </nav>
</header>
