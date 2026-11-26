{{-- Official MYDS masthead (wording from the MYDS locale files; see guide masthead-html). --}}
@php
$m = [
  'ms' => ['title' => 'Portal Rasmi Kerajaan Malaysia', 'how' => 'Kenal pasti begini',
           'off_h' => 'Pautan portal rasmi berakhir dengan .gov.my',
           'off_b' => 'Sekiranya anda melihat pautan selain .gov.my, segera tutupkan halaman itu walaupun ia menyerupai portal rasmi!',
           'sec_h' => 'Portal yang selamat menggunakan HTTPS',
           'sec_b' => 'Periksa ikon kunci mangga (🔒) atau https:// di depan pautan. Sekiranya tiada, tinggalkan laman sesawang serta merta.'],
  'en' => ['title' => 'Official Malaysia Government Website', 'how' => "Here's how you know",
           'off_h' => 'Official government websites end with .gov.my',
           'off_b' => 'If the link does not end with .gov.my, exit the website immediately even if it looks similar.',
           'sec_h' => 'Secure websites use HTTPS',
           'sec_b' => 'Look for the lock icon (🔒) or https:// as an added precaution. If not present, leave the site immediately.'],
][app()->getLocale() === 'en' ? 'en' : 'ms'];
@endphp
<details id="masthead" class="masthead bg-bg-washed print:hidden" data-nosnippet>
  <summary class="mx-auto flex max-w-screen-xl items-center gap-2 px-4.5 py-2 md:px-6 text-body-sm text-txt-black-700">
    <img src="/assets/img/malaysia-flag.svg" width="32" height="16" alt="" aria-hidden="true">
    <span>{{ $m['title'] }}</span>
    <span class="text-txt-primary">{{ $m['how'] }}</span>
  </summary>
  <div class="mx-auto grid max-w-screen-xl gap-4.5 px-4.5 pb-6 pt-3 md:px-6 sm:grid-cols-2">
    <div>
      <p class="text-body-sm font-medium text-txt-black-900">{{ $m['off_h'] }}</p>
      <p class="text-body-sm text-txt-black-700">{{ $m['off_b'] }}</p>
    </div>
    <div>
      <p class="text-body-sm font-medium text-txt-black-900">{{ $m['sec_h'] }}</p>
      <p class="text-body-sm text-txt-black-700">{{ $m['sec_b'] }}</p>
    </div>
  </div>
</details>
