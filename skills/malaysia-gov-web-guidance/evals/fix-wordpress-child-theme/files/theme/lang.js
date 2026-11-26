document.addEventListener('DOMContentLoaded', function () {
  var d = document.createElement('div');
  d.setAttribute('splwpk-multilang', 'splwpk-multilang');
  d.innerHTML = '<a href="?lang=ms">BM</a> | <a href="?lang=en">EN</a>';
  document.querySelector('.site-header').appendChild(d);
});
