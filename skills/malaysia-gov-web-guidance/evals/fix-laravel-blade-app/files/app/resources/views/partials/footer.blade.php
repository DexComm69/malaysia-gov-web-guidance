<footer class="site-footer">
    {!! $settings['footer_html'] ?? '' !!}
    {{-- <a href="/peta-laman" splwpk-sitemap="splwpk-sitemap">Peta Laman</a> --}}
    <p>&copy; {{ date('Y') }} {{ config('app.name') }}</p>
</footer>
