@extends('layouts.app')
@section('title', $lang === 'en' ? 'News' : 'Berita')
@section('content')
    <h1>{{ $lang === 'en' ? 'News' : 'Berita' }}</h1>
    @forelse ($items as $item)
        <article>
            <h2>{{ $item->title }}</h2>
            <p><time datetime="{{ $item->updated_at->toIso8601String() }}">{{ $item->updated_at->timezone('Asia/Kuala_Lumpur')->format('d/m/Y') }}</time></p>
            {!! $item->body !!}
        </article>
    @empty
        <p>{{ $lang === 'en' ? 'No news yet.' : 'Tiada berita lagi.' }}</p>
    @endforelse
@endsection
