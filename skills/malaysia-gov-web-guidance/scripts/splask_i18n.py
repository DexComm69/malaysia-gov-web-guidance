"""Bahasa Melayu output for `scan --lang ms`.

Findings are produced in English and translated here at report time, so the checks stay in one place.
Criterion names follow the skill's splask-criteria-checklist BM section. A message with no matching
pattern is shown in English, so nothing is lost; add a pattern here when that happens.
"""
import re

CRITERIA = {
    'Search Function': 'Fungsi Carian',
    'Advanced Search Option': 'Carian Terperinci',
    'W3C Disability Accessibility': 'Kemudahan W3C (OKU)',
    'Multi-Language for Content': 'Kandungan Pelbagai Bahasa',
    'Sitemap': 'Peta Laman',
    'Mobile Apps': 'Aplikasi Mudah Alih',
    'Presence of Datasets': 'Set Data Terbuka',
    'Publication': 'Penerbitan',
    'Updated Content: Broadcast': 'Kandungan Dikemas Kini: Hebahan',
    'Updated Content: About Us': 'Kandungan Dikemas Kini: Tentang Kami',
    'Updated Content: News': 'Kandungan Dikemas Kini: Berita',
    'Updated Content: Government Policies': 'Kandungan Dikemas Kini: Dasar Kerajaan',
    'Updated Content: FAQ': 'Kandungan Dikemas Kini: Soalan Lazim',
    'Updated Content: Client Charter': 'Kandungan Dikemas Kini: Piagam Pelanggan',
    'Updated Content: Contact Details': 'Kandungan Dikemas Kini: Hubungi Kami',
    'Number of Online Services': 'Perkhidmatan Dalam Talian',
    'Electronic Archive': 'Arkib Elektronik',
    'Publicising Agency CIO/CDO': 'Maklumat CIO/CDO Agensi',
    'Freedom of Information': 'Kebebasan Maklumat',
    'Online Procurement Announcement': 'Hebahan Perolehan Dalam Talian',
    'Online E-Participation': 'E-Penyertaan Dalam Talian',
    'Privacy Policy': 'Dasar Privasi',
    'Feedback Form': 'Borang Maklum Balas',
    'Link to MyGov Portal': 'Pautan ke Portal MyGov',
    'Device Responsiveness': 'Responsif Peranti',
    'HTTPS Availability': 'HTTPS',
    'Loading Time': 'Masa Muat',
    'Active Link': 'Pautan Aktif',
    'Downtime': 'Downtime',
    'Find Website Using Search Tool': 'Carian Google (10 teratas)',
    'SEO': 'SEO',
    'Tag spelling': 'Ejaan tag',
    'Commented-out tags': 'Tag dalam komen',
    'Rendering': 'Paparan pelayan',
    'Language': 'Bahasa halaman',
    'Page choice': 'Pilihan halaman',
    'Page fetch': 'Muat halaman',
    'MYDS masthead (not SPLaSK)': 'Masthead MYDS (bukan SPLaSK)',
    'MYDS: masthead': 'MYDS: masthead',
    'MYDS: fonts': 'MYDS: fon',
    'MYDS: colour mode': 'MYDS: mod warna',
    'Accessibility: form labels': 'Kebolehcapaian: label borang',
    'Accessibility: names': 'Kebolehcapaian: nama pautan/butang',
    'Accessibility: headings': 'Kebolehcapaian: tajuk',
    'Accessibility: duplicate ids': 'Kebolehcapaian: id berganda',
    'Accessibility: skip link': 'Kebolehcapaian: pautan langkau',
}

LABELS = {
    'title': 'Semakan awal SPLaSK 2.0',
    'final': 'URL akhir {url}; tidak rasmi, penilaian SPLaSK ialah rujukan muktamad',
    'pages': 'Halaman diimbas',
    'fix': 'pembetulan',
    'due_head': 'Tarikh luput kesegaran (setiap item gagal pada tarikh ini melainkan kandungannya benar-benar dikemas kini):',
    'due_row': '  {crit:38} kemas kini terakhir {last}   luput {due}   {left}',
    'overdue': 'TELAH LUPUT', 'today': 'luput hari ini', 'in_days': 'dalam {n} hari',
    'crit_head': 'Daftarkan halaman ini sebagai Criteria URL dalam profil laman SPLaSK:',
    'totals': '{FAIL} GAGAL, {WARN} AMARAN, {PASS} LULUS, {INFO} MAKLUMAN',
    'md_title': 'Semakan awal SPLaSK 2.0',
    'md_totals': '**{FAIL} gagal** · {WARN} amaran · {PASS} lulus · {INFO} makluman',
    'md_pages': 'Halaman', 'md_cols': '| | Kriteria | Halaman | Dapatan | Cadangan pembetulan |',
    'md_due': '### Tarikh luput kesegaran', 'md_due_cols': '| Item | Kemas kini terakhir | Luput | |',
    'md_crit': '### Criteria URL untuk didaftarkan dalam profil laman SPLaSK', 'md_crit_cols': '| Tag | Halaman |',
    'md_pass': '{n} semakan lulus', 'md_foot': '_Semakan awal tidak rasmi; penilaian SPLaSK ialah rujukan muktamad._',
    'md_days': '{n} hari', 'md_overdue': '❌ telah luput', 'md_today': '⚠️ hari ini',
}
LEVEL = {'FAIL': 'GAGAL', 'WARN': 'AMARAN', 'PASS': 'LULUS', 'INFO': 'INFO'}

# (English regex, Malay template) - groups are reused by name or position
MESSAGES = [
    (r'no `(?P<t>[^`]+)` in the home page HTML', 'tiada `{t}` dalam HTML halaman utama'),
    (r'`(?P<t>[^`]+)` found \((?P<n>\d+)x\)(?P<rest>.*)', '`{t}` dijumpai ({n}x){rest}'),
    (r'; newest timestamp (?P<d>\S+), (?P<a>\d+) days old \(limit (?P<l>\d+)\)', '; timestamp terkini {d}, {a} hari ({l} hari dibenarkan)'),
    (r'; newest timestamp (?P<d>\S+) \(no freshness limit\)', '; timestamp terkini {d} (tiada had kesegaran)'),
    (r'`(?P<t>[^`]+)` is on an <i> element \((?P<n>\d+)x\)', '`{t}` diletakkan pada elemen <i> ({n}x)'),
    (r'`(?P<t>[^`]+)` must be on a real <form>', '`{t}` mesti diletakkan pada <form> sebenar'),
    (r'`(?P<t>[^`]+)` is on a <(?P<w>\w+)> around \(or inside\) the form, not on the <form> itself; the manual puts it on the <form>',
     '`{t}` diletakkan pada <{w}> di sekeliling borang, bukan pada <form> itu sendiri; manual meletakkannya pada <form>'),
    (r'`(?P<t>[^`]+)` has no timestamp \((?P<n>\d+) element\(s\)\)', '`{t}` tiada timestamp ({n} elemen)'),
    (r'(?P<n>\d+) of (?P<m>\d+) `(?P<t>[^`]+)` elements lack a timestamp \(the dated ones are used\)', '{n} daripada {m} elemen `{t}` tiada timestamp (yang bertarikh digunakan)'),
    (r'timestamp not in YYYY-MM-DD HH:MM:SS: "(?P<v>[^"]*)"', 'timestamp bukan dalam format YYYY-MM-DD HH:MM:SS: "{v}"'),
    (r'newest timestamp (?P<d>\S+) is (?P<a>\d+) days old \(limit (?P<l>\d+)\)', 'timestamp terkini {d} sudah {a} hari (had {l} hari)'),
    (r'timestamp (?P<d>\S+) is in the future', 'timestamp {d} ialah tarikh akan datang'),
    (r'`(?P<t>[^`]+)` timestamp is the scan date/time \((?P<d>[^)]+)\): check it is the real date the content changed, not the time the page was generated',
     'timestamp `{t}` sama dengan masa imbasan ({d}): pastikan ia tarikh sebenar kandungan diubah, bukan masa halaman dijana'),
    (r'`(?P<t>[^`]+)` value should repeat the name \(found "(?P<v>[^"]*)"\)', 'nilai `{t}` mesti sama dengan namanya (dijumpai "{v}")'),
    (r'`(?P<t>[^`]+)` needs a link with href', '`{t}` memerlukan pautan dengan href'),
    (r'`(?P<k>[^`]+)` is not an official tag; did you mean `(?P<c>[^`]+)`\?', '`{k}` bukan tag rasmi; mungkin maksud anda `{c}`?'),
    (r'`(?P<k>[^`]+)` is not an official tag', '`{k}` bukan tag rasmi'),
    (r'`(?P<k>[^`]+)` is not in the official manual \(harmless, scores nothing\)', '`{k}` tiada dalam manual rasmi (tidak memudaratkan, tiada markah)'),
    (r'no `(?P<t>[^`]+)`, but `(?P<p>[^`]+)` is present \(the manual accepts either\)', 'tiada `{t}`, tetapi `{p}` ada (manual menerima salah satu)'),
    (r'`(?P<t>[^`]+)` is not on the home page but is on "(?P<p>[^"]+)" \((?P<u>[^)]+)\)', '`{t}` tiada di halaman utama tetapi ada di "{p}" ({u})'),
    (r'goes stale on (?P<d>\S+) \((?P<n>\d+) days\): last updated (?P<l>\S+), limit (?P<m>\d+) days', 'luput pada {d} (dalam {n} hari): kemas kini terakhir {l}, had {m} hari'),
    (r'tags that exist only inside HTML comments <!-- --> \(switched off\): (?P<t>.+)', 'tag yang hanya wujud dalam komen HTML <!-- --> (tidak aktif): {t}'),
    (r'tags bound by JavaScript \(Alpine\.js / Vue `x-bind:` or `:` attributes\), so the crawler never sees them: (?P<t>.+)',
     'tag diikat oleh JavaScript (atribut `x-bind:` atau `:` Alpine.js / Vue), jadi crawler tidak melihatnya: {t}'),
    (r'tags that appear only inside <script> \(added by JavaScript, may be invisible to the crawler\): (?P<t>.+)',
     'tag yang hanya ada dalam <script> (ditambah oleh JavaScript, mungkin tidak dilihat crawler): {t}'),
    (r'privacy page heading is not tagged', 'tajuk halaman privasi tidak ditag'),
    (r'privacy page has no H1-H6 heading containing "privasi"/"privacy"', 'halaman privasi tiada tajuk H1-H6 yang mengandungi "privasi"/"privacy"'),
    (r'dedicated privacy page has a tagged heading with the keyword', 'halaman privasi khas mempunyai tajuk bertag dengan kata kunci'),
    (r'`splwpk-privacy-policy` must be on the link \(<a href>\) to the privacy page, on every page',
     '`splwpk-privacy-policy` mesti pada pautan (<a href>) ke halaman privasi, di setiap halaman'),
    (r'<title> is (?P<n>\d+) characters \(must be under 70\): "(?P<t>.*)"', '<title> {n} aksara (mesti kurang daripada 70): "{t}"'),
    (r'meta description is (?P<n>\d+) characters \(must be 1-159\)', 'meta description {n} aksara (mesti 1-159)'),
    (r'(?P<n>\d+) <h1> on the page \(must be exactly 1\)', '{n} <h1> pada halaman (mesti tepat 1)'),
    (r'(?P<n>\d+) <img> without alt(?P<rest>.*)', '{n} <img> tanpa alt{rest}'),
    (r'no deprecated HTML tags', 'tiada tag HTML lapuk'),
    (r'deprecated tags: (?P<t>.+)', 'tag lapuk: {t}'),
    (r'viewport meta present', 'meta viewport ada'),
    (r'missing viewport meta', 'meta viewport tiada'),
    (r'link to https://www\.malaysia\.gov\.my found', 'pautan ke https://www.malaysia.gov.my dijumpai'),
    (r'no link to https://www\.malaysia\.gov\.my', 'tiada pautan ke https://www.malaysia.gov.my'),
    (r'MyGov link is not exactly https://www\.malaysia\.gov\.my: (?P<u>.+)', 'pautan MyGov bukan tepat https://www.malaysia.gov.my: {u}'),
    (r'final URL (?P<u>\S+)', 'URL akhir {u}'),
    (r'(?P<n>\d+) redirect\(s\) \(max 5\)', '{n} redirect (maksimum 5)'),
    (r'HTML fetched in (?P<s>[\d.]+)s from here \(SPLaSK measures its own; limit 5s\)', 'HTML dimuat dalam {s}s dari sini (SPLaSK mengukur sendiri; had 5s)'),
    (r'checked by SPLaSK via Google/SerpAPI \(needs the SerpAPI token in the SPLaSK profile\)', 'disemak oleh SPLaSK melalui Google/SerpAPI (perlu token SerpAPI dalam profil SPLaSK)'),
    (r'checked by the SPLaSK crawler over time; not testable from one page load', 'disemak oleh crawler SPLaSK dari masa ke masa; tidak boleh diuji daripada satu muat halaman'),
    (r'links not checked; add --check-links to test every link on the scanned pages', 'pautan tidak disemak; tambah --check-links untuk menguji setiap pautan'),
    (r'broken link (?P<u>\S+) \((?P<w>[^)]+)\)(?:, link text "(?P<x>[^"]*)")?', 'pautan rosak {u} ({w})'),
    (r'could not check (?P<u>\S+) \((?P<w>[^)]+)\); try again later', 'tidak dapat menyemak {u} ({w}); cuba lagi kemudian'),
    (r'(?P<n>\d+) unique link\(s\) tried \((?P<s>[^)]+)\): (?P<b>\d+) broken, (?P<c>\d+) could not be checked(?P<rest>.*)',
     '{n} pautan unik dicuba: {b} rosak, {c} tidak dapat disemak'),
    (r'link text "(?P<x>[^"]*)" matches the (?P<w>dataset title|app name) on (?P<h>\S+)', 'teks pautan "{x}" sepadan dengan nama di {h}'),
    (r'link text "(?P<x>[^"]*)" does not match the (?P<w>dataset title|app name): (?P<t>.+)', 'teks pautan "{x}" tidak sepadan dengan nama rasmi: {t}'),
    (r'(?P<u>\S+) does not exist \((?P<w>[^)]+)\)', '{u} tidak wujud'),
    (r'(?P<u>\S+) is not a dataset page; the open-data tag needs a link to a specific dataset', '{u} bukan halaman set data; tag open-data memerlukan pautan ke set data tertentu'),
    (r'could not open (?P<u>\S+) to compare the (?P<w>[^;]+); try again later', 'tidak dapat membuka {u} untuk dibandingkan; cuba lagi kemudian'),
    (r'link text must equal the dataset title on data\.gov\.my; add --check-links to compare it', 'teks pautan mesti sama dengan tajuk set data di data.gov.my; tambah --check-links untuk membandingkan'),
    (r'open-data tag must link to a dataset on data\.gov\.my \(link text = dataset title\)', 'tag open-data mesti memaut ke set data di data.gov.my (teks pautan = tajuk set data)'),
    (r'mobile-apps tag must be on a link to the app page on gamma\.malaysia\.gov\.my', 'tag mobile-apps mesti pada pautan ke halaman aplikasi di gamma.malaysia.gov.my'),
    (r'<html lang="(?P<l>[^"]*)">', '<html lang="{l}">'),
    (r'<html> has no lang attribute', '<html> tiada atribut lang'),
    (r'official masthead wording found in the server HTML', 'teks masthead rasmi dijumpai dalam HTML pelayan'),
    (r'masthead wording exists only inside a <script> \(built by JavaScript\)', 'teks masthead hanya wujud dalam <script> (dibina oleh JavaScript)'),
    (r'no official masthead wording.*', 'tiada teks masthead rasmi ("Portal Rasmi Kerajaan Malaysia")'),
    (r'no official masthead \(.*', 'tiada masthead rasmi ("Portal Rasmi Kerajaan Malaysia") dalam HTML pelayan'),
    (r'the masthead comes after the page heading.*', 'masthead terletak selepas tajuk halaman; MYDS meletakkannya di bahagian paling atas'),
    (r'masthead found, but without its .* toggle', 'masthead dijumpai, tetapi tiada butang "Kenal pasti begini"'),
    (r'official masthead wording and toggle, above the page heading', 'teks masthead rasmi dan butangnya, di atas tajuk halaman'),
    (r'Poppins and Inter \(or the MYDS stylesheet\) are loaded', 'Poppins dan Inter (atau stylesheet MYDS) dimuatkan'),
    (r'loads (?P<f>.+) instead of Poppins \(headings\) and Inter \(body\)', 'memuatkan {f}, bukan Poppins (tajuk) dan Inter (teks)'),
    (r'Poppins/Inter not seen in the server HTML.*', 'Poppins/Inter tidak dilihat dalam HTML pelayan; mungkin dimuatkan oleh stylesheet luaran'),
    (r'<html> starts in dark mode', '<html> bermula dalam mod gelap'),
    (r'light mode by default', 'mod cerah secara lalai'),
    (r'(?P<n>\d+) form field\(s\) without a label \(first: (?P<f>[^)]+)\)', '{n} medan borang tanpa label (pertama: {f})'),
    (r'every form field has a label', 'setiap medan borang mempunyai label'),
    (r'(?P<n>\d+) link\(s\)/button\(s\) with no text a screen reader can read.*', '{n} pautan/butang tanpa teks yang boleh dibaca oleh pembaca skrin'),
    (r'heading level jumps from h(?P<a>\d) to h(?P<b>\d)', 'aras tajuk melompat dari h{a} ke h{b}'),
    (r'duplicate id\(s\): (?P<i>.+)', 'id berganda: {i}'),
    (r'skip link at the start of the page', 'pautan langkau di awal halaman'),
    (r'no "skip to main content" link at the start of the page', 'tiada pautan "Langkau ke kandungan utama" di awal halaman'),
    (r'very little server HTML.*', 'HTML pelayan sangat sedikit: jika laman dipaparkan oleh JavaScript, crawler mungkin tidak melihat kandungan atau tag'),
    (r'only (?P<n>\d+) official tag\(s\) here: this may be a splash/landing page.*?; try scanning (?P<u>\S+)', 'hanya {n} tag rasmi di sini: ini mungkin halaman pembuka; cuba imbas {u}'),
    (r'page "(?P<p>[^"]+)" was not found on the home page.*', 'halaman "{p}" tidak dijumpai di halaman utama (jalankan --list-pages untuk melihat pilihan)'),
    (r'could not open (?P<u>\S+): (?P<e>\w+)', 'tidak dapat membuka {u}: {e}'),
    (r'tags that exist only after JavaScript runs \(the crawler never sees them\): (?P<t>.+)', 'tag yang hanya wujud selepas JavaScript dijalankan (crawler tidak melihatnya): {t}'),
    (r'the rendered page adds no tags that the server HTML lacks', 'halaman yang dipaparkan tidak menambah tag yang tiada dalam HTML pelayan'),
    (r'--render skipped: (?P<e>.+)', '--render dilangkau: {e}'),
]

FIXES = [
    (r'register (?P<u>\S+) as a Criteria URL for this tag in the SPLaSK site profile, or also tag it on the home page',
     'daftarkan {u} sebagai Criteria URL bagi tag ini dalam profil laman SPLaSK, atau tag juga di halaman utama'),
    (r'move (?P<t>\S+?)="(?P=t)" from the <i> icon to its <a> link(?P<o> or <form>)?', 'pindahkan {t}="{t}" daripada ikon <i> ke pautan <a>{o_ms}'),
    (r'move (?P<t>\S+?)="(?P=t)" onto the <form> element.*', 'pindahkan {t}="{t}" ke elemen <form> (dalam CMS, dalam override templat modul borang)'),
    (r'rename to (?P<c>\S+?)="(?P=c)"', 'tukar nama kepada {c}="{c}"'),
    (r'update the content itself, then set timestamp to that real date.*', 'kemas kini kandungan itu sendiri, kemudian tetapkan timestamp kepada tarikh sebenar itu (tarikh palsu tetap gagal SPLaSK)'),
    (r'update the content itself before that date.*', 'kemas kini kandungan itu sendiri sebelum tarikh tersebut (timestamp akan mengikut perubahan sebenar)'),
    (r'add timestamp="YYYY-MM-DD HH:MM:SS" from the content.s real last-updated date', 'tambah timestamp="YYYY-MM-DD HH:MM:SS" berdasarkan tarikh sebenar kandungan dikemas kini'),
    (r"take it from the CMS's modified date.*", 'ambil daripada tarikh kemas kini dalam CMS atau pangkalan data; jangan sekali-kali masa semasa'),
    (r'use the real last-updated date', 'gunakan tarikh kemas kini sebenar'),
    (r'fix the link or remove it; if the page moved, redirect the old URL to the new one', 'betulkan atau buang pautan itu; jika halaman dipindahkan, buat redirect dari URL lama ke URL baharu'),
    (r'use the exact (?P<w>dataset title|app name) as the link text: (?P<t>.+)', 'gunakan nama rasmi sebagai teks pautan: {t}'),
    (r'remove the <!-- --> around that markup, or add the tag to the live element', 'buang <!-- --> di sekeliling markup itu, atau letakkan tag pada elemen yang aktif'),
    (r'write the plain attribute in the server HTML.*', 'tulis atribut biasa dalam HTML pelayan, contohnya splwpk-multilang="splwpk-multilang" (bukan x-bind:splwpk-multilang)'),
    (r'output these attributes in the server HTML instead of adding them with JavaScript', 'cetak atribut ini dalam HTML pelayan, bukan menambahnya dengan JavaScript'),
    (r'remove it, or use a tag from the official list \(splask-tagging\)', 'buang, atau gunakan tag daripada senarai rasmi (splask-tagging)'),
    (r'add the masthead above the site header \(guide: masthead-html\)', 'tambah masthead di atas pengepala laman (panduan: masthead-html)'),
    (r'move the masthead markup to the start of <body>', 'pindahkan markup masthead ke awal <body>'),
    (r'add the toggle that explains \.gov\.my and HTTPS.*', 'tambah butang "Kenal pasti begini" yang menerangkan .gov.my dan HTTPS (panduan: masthead-html)'),
    (r'MYDS uses Poppins and Inter;.*', 'MYDS menggunakan Poppins dan Inter; jika agensi ada fon jenama sendiri, ini konflik untuk dibincangkan, bukan diputuskan sendiri'),
    (r'start in light mode; offer dark mode as a user choice', 'mulakan dalam mod cerah; tawarkan mod gelap sebagai pilihan pengguna'),
    (r'<label for="id">…</label> for each field.*', '<label for="id">…</label> bagi setiap medan (placeholder bukan label)'),
    (r'add visible text, or aria-label="…" on icon-only links and buttons', 'tambah teks yang kelihatan, atau aria-label="…" pada pautan dan butang ikon sahaja'),
    (r'use h(?P<n>\d) \(style it with CSS if it should look smaller\)', 'gunakan h{n} (gayakan dengan CSS jika perlu kelihatan lebih kecil)'),
    (r'make each id unique.*', 'pastikan setiap id unik (label dan rujukan aria bergantung padanya)'),
    (r'<a class="skip-link" href="#kandungan">Langkau ke kandungan utama</a>.*', '<a class="skip-link" href="#kandungan">Langkau ke kandungan utama</a> sebagai pautan pertama, dengan <main id="kandungan">'),
    (r'serve the site over HTTPS.*', 'sediakan laman melalui HTTPS dan redirect http:// ke https://'),
    (r'link straight to the final URL; remove redirect chains', 'pautkan terus ke URL akhir; buang rantaian redirect'),
    (r'reduce page weight, enable caching and compression', 'kurangkan saiz halaman, aktifkan cache dan mampatan'),
    (r'add alt="what the image shows".*', 'tambah alt="apa yang ditunjukkan imej" (atau alt="" untuk imej hiasan semata-mata)'),
    (r'replace with modern HTML \+ CSS.*', 'ganti dengan HTML + CSS moden (contoh <center> -> style="text-align:center")'),
    (r'keep one <h1> \(the agency name or the page title, not both\).*', 'kekalkan satu <h1> (nama agensi atau tajuk halaman, bukan kedua-duanya); nama laman dalam pengepala jadikan <p> atau <a>'),
    (r'add one <h1> with the agency name or page subject', 'tambah satu <h1> dengan nama agensi atau subjek halaman'),
    (r'render the page \(or at least its tags\) on the server', 'paparkan halaman (sekurang-kurangnya tagnya) dari pelayan'),
    (r'link to https://data\.gov\.my/data-catalogue/<dataset-id>.*', 'pautkan ke https://data.gov.my/data-catalogue/<id-set-data>, dengan tajuk set data sebagai teks pautan'),
    (r'link to a real (?P<w>.+)', 'pautkan ke set data atau aplikasi yang sebenar'),
    (r'print these attributes in the server HTML \(template code\), not with JavaScript', 'cetak atribut ini dalam HTML pelayan (kod templat), bukan dengan JavaScript'),
]


def _apply(pairs, text):
    if not text: return text
    for pat, tpl in pairs:
        m = re.fullmatch(pat, text) or re.match(pat, text)
        if m:
            g = {k: (v or '') for k, v in m.groupdict().items()}
            g['o_ms'] = ' atau <form>' if g.get('o') else ''
            rest = g.get('rest', '')
            if rest:
                g['rest'] = translate_message(rest) if rest.startswith('; newest') else rest
            try:
                out = tpl.format(**g)
            except (KeyError, IndexError):
                return text
            tail = text[m.end():]
            return out + tail
    return text


def translate_message(msg):
    return _apply(MESSAGES, msg)


FRAGMENTS = [
    ('(the tag goes on the <form> itself)', '(tag diletakkan pada <form> itu sendiri)'),
    ('(timestamp = the real date the content last changed)', '(timestamp = tarikh sebenar kandungan terakhir diubah)'),
    ('App name as listed in GAMMA', 'Nama aplikasi seperti dalam GAMMA'),
    ('Exact dataset title on data.gov.my', 'Tajuk set data yang tepat di data.gov.my'),
    ('(usually in the footer)', '(biasanya di footer)'),
    ('Agency name, short (under 70 characters)', 'Nama agensi, ringkas (kurang 70 aksara)'),
    ('One-sentence summary of the site (under 160 characters)', 'Ringkasan laman dalam satu ayat (kurang 160 aksara)'),
    ('(24-hour)', '(format 24 jam)'),
]


def translate_fix(fix):
    out = _apply(FIXES, fix)
    for en, ms in FRAGMENTS:
        if out and en in out: out = out.replace(en, ms)
    return out


def translate_result(x):
    y = dict(x)
    y['criterion'] = CRITERIA.get(x['criterion'], x['criterion'])
    y['message'] = translate_message(x['message'])
    y['fix'] = translate_fix(x.get('fix'))
    return y
