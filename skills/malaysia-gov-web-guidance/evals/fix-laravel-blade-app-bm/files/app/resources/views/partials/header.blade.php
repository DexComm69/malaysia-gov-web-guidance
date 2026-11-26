<header class="site-header">
    <x-banner />
    <h1 class="brand">{{ config('app.name') }}</h1>
    <x-search-box />
    <div x-data="{ langs: ['ms', 'en'] }" x-bind:splwpk-multilang="'splwpk-multilang'">
        <a href="?lang=ms">BM</a> | <a href="?lang=en">EN</a>
    </div>
    <nav>
        <a href="/tentang-kami" splwpk-about-us="splwpk-about-us" timestamp="{{ now() }}">Tentang Kami</a>
        <a href="/soalan-lazim">Soalan Lazim</a>
        <a href="/hubungi-kami" splwpk-contact-details="splwpk-contact-details">Hubungi Kami</a>
        <a href="/maklum-balas">Maklum Balas</a>
    </nav>
    @isset($latestNews)
        <a href="/berita" splwpk-news="splwpk-news" timestamp="{{ $latestNews->published_at->format('d/m/Y') }}">Berita Terkini</a>
    @endisset
</header>
