<footer class="site-footer">
    <nav aria-label="{{ $lang === 'en' ? 'Footer' : 'Pautan kaki' }}">
        @foreach ($splaskFooter as $link)
            <a href="{{ $link['url'] }}" @if ($link['tag']) {{ $link['tag'] }}="{{ $link['tag'] }}" @endif>{{ $link[$lang] }}</a>
        @endforeach
        <a href="{{ config('splask.mygov') }}">MyGov</a>
    </nav>
    <p>&copy; {{ date('Y') }} {{ config('app.name') }}. {{ $lang === 'en' ? 'All Rights Reserved' : 'Hak Cipta Terpelihara' }}.</p>
</footer>
<script>
document.querySelectorAll('[splwpk-w3c] [data-size]').forEach(function (b) {
    b.addEventListener('click', function () {
        var s = parseInt(b.dataset.size, 10);
        document.documentElement.style.fontSize = s === 0 ? '' : (100 + s * 12.5) + '%';
    });
});
</script>
