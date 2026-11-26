<!DOCTYPE html>
<html lang="{{ str_replace('_', '-', app()->getLocale()) }}">
<head>
    <meta charset="utf-8">
    <title>@yield('title') | {{ config('app.name') }} - Portal Rasmi Pihak Berkuasa Tempatan</title>
    <meta name="description" content="@yield('description')">
    @vite(['resources/css/app.css', 'resources/js/app.js'])
</head>
<body>
    @include('partials.header')
    <main>@yield('content')</main>
    @include('partials.footer')
</body>
</html>
