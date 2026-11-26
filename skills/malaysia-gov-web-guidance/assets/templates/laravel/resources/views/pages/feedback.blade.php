{{-- Feedback form (SPLaSK Responsiveness): splwpk-feedback-form is on the <form> itself; register this page as the
     Criteria URL. Laravel validation, @csrf, Post/Redirect/Get, a focused error summary and a reference number
     (guide: service-form-pattern). The POST route is in routes/splask.php. --}}
@extends('layouts.app')
@section('title', $lang === 'en' ? 'Feedback' : 'Maklum Balas')
@section('description', 'Hantar maklum balas, cadangan atau aduan.')
@section('content')
    <h1>{{ $lang === 'en' ? 'Feedback' : 'Maklum Balas' }}</h1>

    @if (session('feedback_ref'))
        <div role="status">
            <p>{{ $lang === 'en' ? 'Thank you. Your feedback has been received.' : 'Terima kasih. Maklum balas anda telah diterima.' }}</p>
            <p>{{ $lang === 'en' ? 'Reference number' : 'Nombor rujukan' }}: <strong>{{ session('feedback_ref') }}</strong></p>
        </div>
    @else
        @if ($errors->any())
            <div class="error-summary" role="alert" tabindex="-1" id="ringkasan-ralat">
                <h2>{{ $lang === 'en' ? 'Please correct the following' : 'Sila betulkan perkara berikut' }}</h2>
                <ul>
                    @foreach ($errors->getMessages() as $field => $messages)
                        <li><a href="#{{ $field }}">{{ $messages[0] }}</a></li>
                    @endforeach
                </ul>
            </div>
            <script>document.getElementById('ringkasan-ralat').focus();</script>
        @endif

        <form action="/maklum-balas" method="post" novalidate splwpk-feedback-form="splwpk-feedback-form">
            @csrf
            @foreach (['nama' => ['Nama', 'Name', 'name'], 'emel' => ['E-mel', 'Email', 'email']] as $f => [$ms, $en, $ac])
                <label for="{{ $f }}">{{ $lang === 'en' ? $en : $ms }}</label>
                <input id="{{ $f }}" name="{{ $f }}" @if ($f === 'emel') type="email" @endif autocomplete="{{ $ac }}" value="{{ old($f) }}"
                       @error($f) aria-invalid="true" aria-describedby="{{ $f }}-ralat" @enderror>
                @error($f)<p class="field-error" id="{{ $f }}-ralat">{{ $message }}</p>@enderror
            @endforeach

            <label for="mesej">{{ $lang === 'en' ? 'Your feedback' : 'Maklum balas anda' }}</label>
            <textarea id="mesej" name="mesej" rows="6" @error('mesej') aria-invalid="true" aria-describedby="mesej-ralat" @enderror>{{ old('mesej') }}</textarea>
            @error('mesej')<p class="field-error" id="mesej-ralat">{{ $message }}</p>@enderror

            <p>{{ $lang === 'en' ? 'We use your details only to reply to this feedback.' : 'Maklumat anda hanya digunakan untuk membalas maklum balas ini.' }}
               <a href="/dasar-privasi">{{ $lang === 'en' ? 'Privacy Policy' : 'Dasar Privasi' }}</a></p>

            <button type="submit">{{ $lang === 'en' ? 'Submit' : 'Hantar' }}</button>
        </form>
    @endif
@endsection
