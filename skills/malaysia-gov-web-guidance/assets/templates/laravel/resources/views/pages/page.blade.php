{{-- A content page from the pages table. The privacy page's heading carries splwpk-privacy-policy
     (SPLaSK Privacy Policy, part 2; part 1 is the tagged footer link on every page). --}}
@extends('layouts.app')
@section('title', $page->title)
@section('content')
    <h1 @if ($page->slug === 'dasar-privasi') splwpk-privacy-policy="splwpk-privacy-policy" @endif>{{ $page->title }}</h1>
    {!! $page->body !!}{{-- body is trusted admin HTML; sanitise it on save (e.g. HTML Purifier) --}}
@endsection
