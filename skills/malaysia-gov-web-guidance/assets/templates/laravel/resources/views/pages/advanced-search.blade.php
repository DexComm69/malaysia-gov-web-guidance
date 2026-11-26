{{-- Advanced search: the splwpk-advanced-search-function tag is on the <form>. Register this page as its Criteria URL. --}}
@extends('layouts.app')
@section('title', $lang === 'en' ? 'Advanced search' : 'Carian terperinci')
@section('content')
    <h1>{{ $lang === 'en' ? 'Advanced search' : 'Carian terperinci' }}</h1>
    <form action="/carian" method="get" splwpk-advanced-search-function="splwpk-advanced-search-function">
        <label for="as-q">{{ $lang === 'en' ? 'Words' : 'Perkataan' }}</label>
        <input id="as-q" name="q" type="search">
        <label for="as-jenis">{{ $lang === 'en' ? 'Type' : 'Jenis' }}</label>
        <select id="as-jenis" name="jenis">
            <option value="">{{ $lang === 'en' ? 'All' : 'Semua' }}</option>
            <option value="halaman">{{ $lang === 'en' ? 'Pages' : 'Halaman' }}</option>
            <option value="berita">{{ $lang === 'en' ? 'News' : 'Berita' }}</option>
        </select>
        <label for="as-dari">{{ $lang === 'en' ? 'From date' : 'Dari tarikh' }}</label>
        <input id="as-dari" name="dari" type="date">
        <label for="as-hingga">{{ $lang === 'en' ? 'To date' : 'Hingga tarikh' }}</label>
        <input id="as-hingga" name="hingga" type="date">
        <button type="submit">{{ $lang === 'en' ? 'Search' : 'Cari' }}</button>
    </form>
@endsection
