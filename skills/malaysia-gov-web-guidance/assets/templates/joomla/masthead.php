<?php
defined('_JEXEC') or die;
/** Official MYDS masthead (wording from the MYDS locale files; see guide masthead-html). */
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
][str_starts_with(\Joomla\CMS\Factory::getApplication()->getLanguage()->getTag(), 'en') ? 'en' : 'ms'];
?>
<details id="masthead" class="masthead bg-bg-washed print:hidden" data-nosnippet>
  <summary class="mx-auto flex max-w-screen-xl items-center gap-2 px-4.5 py-2 md:px-6 text-body-sm text-txt-black-700">
    <img src="/assets/img/malaysia-flag.svg" width="32" height="16" alt="" aria-hidden="true">
    <span><?= htmlspecialchars($m['title'], ENT_QUOTES, 'UTF-8') ?></span>
    <span class="text-txt-primary"><?= htmlspecialchars($m['how'], ENT_QUOTES, 'UTF-8') ?></span>
  </summary>
  <div class="mx-auto grid max-w-screen-xl gap-4.5 px-4.5 pb-6 pt-3 md:px-6 sm:grid-cols-2">
    <div>
      <p class="text-body-sm font-medium text-txt-black-900"><?= htmlspecialchars($m['off_h'], ENT_QUOTES, 'UTF-8') ?></p>
      <p class="text-body-sm text-txt-black-700"><?= htmlspecialchars($m['off_b'], ENT_QUOTES, 'UTF-8') ?></p>
    </div>
    <div>
      <p class="text-body-sm font-medium text-txt-black-900"><?= htmlspecialchars($m['sec_h'], ENT_QUOTES, 'UTF-8') ?></p>
      <p class="text-body-sm text-txt-black-700"><?= htmlspecialchars($m['sec_b'], ENT_QUOTES, 'UTF-8') ?></p>
    </div>
  </div>
</details>
