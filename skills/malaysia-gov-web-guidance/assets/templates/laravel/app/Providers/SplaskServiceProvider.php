<?php

namespace App\Providers;

use App\View\Composers\SplaskComposer;
use Illuminate\Support\Facades\View;
use Illuminate\Support\ServiceProvider;

/**
 * Register in bootstrap/providers.php (Laravel 11+):  App\Providers\SplaskServiceProvider::class,
 */
class SplaskServiceProvider extends ServiceProvider
{
    public function boot(): void
    {
        // SPLaSK links (with real timestamps) for the header and footer on every page.
        View::composer(['partials.header', 'partials.footer'], SplaskComposer::class);
        // $lang ('ms' or 'en') for every view, read when the view renders (after any locale middleware).
        View::composer('*', fn ($view) => $view->with('lang', app()->getLocale() === 'en' ? 'en' : 'ms'));
    }
}
