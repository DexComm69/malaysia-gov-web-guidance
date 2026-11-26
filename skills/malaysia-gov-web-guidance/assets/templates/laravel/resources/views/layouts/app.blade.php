<!DOCTYPE html>
<html lang="{{ app()->getLocale() === 'en' ? 'en' : 'ms' }}">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    {{-- Keep the home page title under 70 characters and the description 1-159. --}}
    <title>@hasSection('title')@yield('title') | @endif{{ config('app.name') }}</title>
    <meta name="description" content="@yield('description', 'TODO one-sentence summary of the site')">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@govtechmy/myds-style@1.0.0/dist/index.css">
    <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Poppins:wght@500;600&family=Inter:wght@400;500;600&display=swap">
    {{-- The app's own assets, only once built (npm run build) or served (npm run dev): without this check a
         fresh install answers every page with ViteManifestNotFoundException (HTTP 500). --}}
    @if (file_exists(public_path('build/manifest.json')) || file_exists(public_path('hot')))
        @vite(['resources/css/app.css', 'resources/js/app.js'])
    @endif
</head>
<body class="font-body">
    <a class="skip-link" href="#kandungan">{{ app()->getLocale() === 'en' ? 'Skip to main content' : 'Langkau ke kandungan utama' }}</a>
    @include('partials.masthead')
    @include('partials.header')
    {{-- One <h1> per page: the page's own heading, in @section('content'). --}}
    <main id="kandungan">@yield('content')</main>
    @include('partials.footer')
</body>
</html>
