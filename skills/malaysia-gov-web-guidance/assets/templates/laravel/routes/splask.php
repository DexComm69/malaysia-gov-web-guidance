<?php
/*
 | Routes for the starter pages. Load this file at the END of routes/web.php (its last route is a catch-all):
 |     require __DIR__ . '/splask.php';
 | Models: App\Models\Page (slug, title, body) and App\Models\News; adjust to the app's own.
 */

use App\Models\News;
use App\Models\Page;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Route;

Route::view('/', 'pages.home');

Route::get('/berita', fn () => view('pages.news', ['items' => News::orderByDesc('updated_at')->get()]));

Route::get('/carian', function (Request $request) {
    $q = trim((string) $request->query('q', ''));
    $results = [];
    if ($q !== '') {
        $like = '%' . addcslashes($q, '%_\\') . '%';   // bound parameter: never put $q into SQL directly
        foreach (Page::where('title', 'like', $like)->orWhere('body', 'like', $like)->limit(20)->get() as $p) {
            $results[] = ['url' => '/' . $p->slug, 'title' => $p->title];
        }
        foreach (News::where('title', 'like', $like)->orWhere('body', 'like', $like)->limit(20)->get() as $n) {
            $results[] = ['url' => '/berita#' . $n->slug, 'title' => $n->title];
        }
    }
    return view('pages.search', ['q' => $q, 'results' => $results]);
});
Route::view('/carian-terperinci', 'pages.advanced-search');

Route::view('/maklum-balas', 'pages.feedback');
Route::post('/maklum-balas', function (Request $request) {
    $en = app()->getLocale() === 'en';
    $request->validate([
        'nama' => 'required|string|max:100',
        'emel' => 'required|email',
        'mesej' => 'required|string|min:10|max:2000',
    ], [
        'nama.*' => $en ? 'Enter your name.' : 'Masukkan nama anda.',
        'emel.*' => $en ? 'Enter a valid email address, e.g. nama@contoh.com.' : 'Masukkan alamat e-mel yang sah, contohnya nama@contoh.com.',
        'mesej.*' => $en ? 'Write your feedback (10 to 2000 characters).' : 'Tulis maklum balas anda (10 hingga 2000 aksara).',
    ]);
    $ref = 'MB-' . now('Asia/Kuala_Lumpur')->format('Ymd') . '-' . strtoupper(bin2hex(random_bytes(3)));
    // TODO: save the feedback with $ref (a Feedback model) and send the acknowledgement e-mail.
    return redirect('/maklum-balas')->with('feedback_ref', $ref);   // Post/Redirect/Get
});

// Content pages (tentang-kami, soalan-lazim, hubungi-kami, dasar-privasi, peta-laman, ...): keep this last.
Route::get('/{slug}', fn (string $slug) => view('pages.page', ['page' => Page::where('slug', $slug)->firstOrFail()]))
    ->where('slug', '[a-z0-9-]+');
