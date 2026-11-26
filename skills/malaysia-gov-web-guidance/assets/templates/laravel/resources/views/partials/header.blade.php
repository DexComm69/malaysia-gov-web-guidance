{{-- Tags are plain attributes in the server HTML: no Alpine x-bind or Vue binding for splwpk-*. --}}
<header class="site-header">
    <a class="site-name" href="/">{{ config('app.name') }}</a>

    <form action="/carian" method="get" role="search" splwpk-search-function="splwpk-search-function">
        <label for="carian">{{ $lang === 'en' ? 'Search' : 'Carian' }}</label>
        <input id="carian" name="q" type="search" value="{{ request('q') }}">
        <button type="submit">{{ $lang === 'en' ? 'Search' : 'Cari' }}</button>
    </form>

    <div role="group" aria-label="{{ $lang === 'en' ? 'Text size' : 'Saiz tulisan' }}" splwpk-w3c="splwpk-w3c">
        <button type="button" data-size="-1">A-</button><button type="button" data-size="0">A</button><button type="button" data-size="1">A+</button>
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
