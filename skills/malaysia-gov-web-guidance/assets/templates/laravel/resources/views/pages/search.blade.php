{{-- Search results. The search box with splwpk-search-function is in partials.header (every page). --}}
@extends('layouts.app')
@section('title', $lang === 'en' ? 'Search' : 'Carian')
@section('content')
    <h1>{{ $lang === 'en' ? 'Search' : 'Carian' }}</h1>
    @if ($q === '')
        <p>{{ $lang === 'en' ? 'Enter a word in the search box above.' : 'Masukkan perkataan dalam kotak carian di atas.' }}</p>
    @else
        <p>{{ $lang === 'en' ? 'Results for' : 'Hasil carian untuk' }} "{{ $q }}":</p>
        @forelse ($results as $r)
            <p><a href="{{ $r['url'] }}">{{ $r['title'] }}</a></p>
        @empty
            <p>{{ $lang === 'en' ? 'Nothing found.' : 'Tiada hasil dijumpai.' }}</p>
        @endforelse
    @endif
    <p><a href="/carian-terperinci">{{ $lang === 'en' ? 'Advanced search' : 'Carian terperinci' }}</a></p>
@endsection
