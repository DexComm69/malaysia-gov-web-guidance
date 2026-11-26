<?php
/**
 * Feedback form (SPLaSK Responsiveness): the splwpk-feedback-form tag is on the <form> itself.
 * Register this page as the Criteria URL for the tag. Server-side validation, CSRF token,
 * Post/Redirect/Get, an error summary that receives focus, and a reference number (guide: service-form-pattern).
 */
require_once __DIR__ . '/config.php';
session_start();
$en = lang() === 'en';
$_SESSION['csrf'] ??= bin2hex(random_bytes(32));
$errors = []; $old = ['nama' => '', 'emel' => '', 'mesej' => ''];

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $old = ['nama' => trim((string) ($_POST['nama'] ?? '')), 'emel' => trim((string) ($_POST['emel'] ?? '')), 'mesej' => trim((string) ($_POST['mesej'] ?? ''))];
    if (!hash_equals($_SESSION['csrf'], (string) ($_POST['csrf'] ?? ''))) $errors['form'] = $en ? 'Your session expired. Please submit again.' : 'Sesi anda telah tamat. Sila hantar semula.';
    if ($old['nama'] === '' || mb_strlen($old['nama']) > 100) $errors['nama'] = $en ? 'Enter your name.' : 'Masukkan nama anda.';
    if (!filter_var($old['emel'], FILTER_VALIDATE_EMAIL)) $errors['emel'] = $en ? 'Enter a valid email address, e.g. nama@contoh.com.' : 'Masukkan alamat e-mel yang sah, contohnya nama@contoh.com.';
    if (mb_strlen($old['mesej']) < 10 || mb_strlen($old['mesej']) > 2000) $errors['mesej'] = $en ? 'Write your feedback (10 to 2000 characters).' : 'Tulis maklum balas anda (10 hingga 2000 aksara).';
    if (!$errors) {
        $ref = 'MB-' . date('Ymd') . '-' . strtoupper(bin2hex(random_bytes(3)));
        // TODO: save $old + $ref to the database (prepared statement) and send the acknowledgement e-mail.
        $_SESSION['feedback_ref'] = $ref;
        header('Location: ' . url('/maklum-balas') . '?terima=1', true, 303);
        exit;
    }
    http_response_code(422);
}
$PAGE = ['title' => 'Maklum Balas', 'description' => 'Hantar maklum balas, cadangan atau aduan.'];
require __DIR__ . '/header.php';
$field = function (string $name) use ($errors): string {
    return isset($errors[$name]) ? ' aria-invalid="true" aria-describedby="' . $name . '-ralat"' : '';
};
?>
<h1><?= $en ? 'Feedback' : 'Maklum Balas' ?></h1>

<?php if (isset($_GET['terima']) && !empty($_SESSION['feedback_ref'])): ?>
  <div role="status">
    <p><?= $en ? 'Thank you. Your feedback has been received.' : 'Terima kasih. Maklum balas anda telah diterima.' ?></p>
    <p><?= $en ? 'Reference number' : 'Nombor rujukan' ?>: <strong><?= e($_SESSION['feedback_ref']) ?></strong></p>
  </div>
  <?php unset($_SESSION['feedback_ref']); ?>
<?php else: ?>
  <?php if ($errors): ?>
    <div class="error-summary" role="alert" tabindex="-1" id="ringkasan-ralat">
      <h2><?= $en ? 'Please correct the following' : 'Sila betulkan perkara berikut' ?></h2>
      <ul>
        <?php foreach ($errors as $k => $msg): ?>
          <li><?= $k === 'form' ? e($msg) : '<a href="#' . e($k) . '">' . e($msg) . '</a>' ?></li>
        <?php endforeach; ?>
      </ul>
    </div>
    <script>document.getElementById('ringkasan-ralat').focus();</script>
  <?php endif; ?>

  <form action="<?= e(url('/maklum-balas')) ?>" method="post" novalidate splwpk-feedback-form="splwpk-feedback-form">
    <input type="hidden" name="csrf" value="<?= e($_SESSION['csrf']) ?>">

    <label for="nama"><?= $en ? 'Name' : 'Nama' ?></label>
    <input id="nama" name="nama" autocomplete="name" value="<?= e($old['nama']) ?>"<?= $field('nama') ?>>
    <?php if (isset($errors['nama'])): ?><p class="field-error" id="nama-ralat"><?= e($errors['nama']) ?></p><?php endif; ?>

    <label for="emel"><?= $en ? 'Email' : 'E-mel' ?></label>
    <input id="emel" name="emel" type="email" autocomplete="email" value="<?= e($old['emel']) ?>"<?= $field('emel') ?>>
    <?php if (isset($errors['emel'])): ?><p class="field-error" id="emel-ralat"><?= e($errors['emel']) ?></p><?php endif; ?>

    <label for="mesej"><?= $en ? 'Your feedback' : 'Maklum balas anda' ?></label>
    <textarea id="mesej" name="mesej" rows="6"<?= $field('mesej') ?>><?= e($old['mesej']) ?></textarea>
    <?php if (isset($errors['mesej'])): ?><p class="field-error" id="mesej-ralat"><?= e($errors['mesej']) ?></p><?php endif; ?>

    <p><?= $en ? 'We use your details only to reply to this feedback.' : 'Maklumat anda hanya digunakan untuk membalas maklum balas ini.' ?>
       <a href="<?= e(url('/dasar-privasi')) ?>"><?= $en ? 'Privacy Policy' : 'Dasar Privasi' ?></a></p>

    <button type="submit"><?= $en ? 'Submit' : 'Hantar' ?></button>
  </form>
<?php endif; ?>
<?php require __DIR__ . '/footer.php'; ?>
