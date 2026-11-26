@extends('layouts.app')
@section('title', 'Maklum Balas')
@section('description', 'Hantar maklum balas kepada Majlis Daerah Contoh Jaya.')
@section('content')
    <h1>Maklum Balas</h1>
    <form action="/maklum-balas" method="post">
        @csrf
        <label for="mesej">Mesej</label>
        <textarea id="mesej" name="mesej"></textarea>
        <button type="submit"><i class="icon-send" splwpk-feedback-form="splwpk-feedback-form"></i> Hantar</button>
    </form>
@endsection
