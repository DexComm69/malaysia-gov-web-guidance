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
(function () {
  /* Text-size control for splwpk-w3c: the tag is in the server HTML; this adds the behaviour and remembers the choice. */
  var buttons = document.querySelectorAll('[splwpk-w3c] [data-fs]');
  function set(v) {
    document.documentElement.style.fontSize = (16 * parseFloat(v)) + 'px';
    buttons.forEach(function (b) { b.setAttribute('aria-pressed', String(b.dataset.fs === String(v))); });
  }
  buttons.forEach(function (b) {
    b.addEventListener('click', function () { set(b.dataset.fs); try { localStorage.setItem('fs', b.dataset.fs); } catch (e) {} });
  });
  try { var saved = localStorage.getItem('fs'); if (saved) set(saved); } catch (e) {}
})();
</script>
