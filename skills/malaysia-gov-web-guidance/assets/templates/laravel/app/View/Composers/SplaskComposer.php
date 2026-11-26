<?php

namespace App\View\Composers;

use App\Models\News;
use App\Models\Page;
use Illuminate\View\View;

/**
 * Gives the header and footer partials their SPLaSK links on EVERY page, with timestamps from the
 * records' real updated_at (never now()). Register it in a service provider's boot():
 *   View::composer(['partials.header', 'partials.footer'], \App\View\Composers\SplaskComposer::class);
 * Adjust the model names and columns to the app.
 */
class SplaskComposer
{
    public function compose(View $view): void
    {
        $menu = [];
        foreach (config('splask.menu') as $link) {
            [$kind, $slug] = $link['source'];
            $updated = match ($kind) {
                'page' => Page::where('slug', $slug)->value('updated_at'),
                'news' => News::max('updated_at'),
                default => null,
            };
            $link['timestamp'] = $updated ? \Illuminate\Support\Carbon::parse($updated)->timezone('Asia/Kuala_Lumpur')->format('Y-m-d H:i:s') : null;
            $menu[] = $link;
        }
        $view->with([
            'splaskMenu' => $menu,
            'splaskFooter' => array_filter(config('splask.footer'), fn ($l) => $l['url'] !== null),
            'splaskLanguages' => config('splask.languages'),
            'lang' => app()->getLocale() === 'en' ? 'en' : 'ms',
        ]);
    }
}
