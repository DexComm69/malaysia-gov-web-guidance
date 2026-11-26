<?php
/**
 * Override of mod_languages/tmpl/default.php: tags the language switcher for SPLaSK.
 * Joomla's multilingual setup gives real BM and EN content, which is what the criterion needs.
 * With only one published language the switcher (and its tag) is not printed.
 */
defined('_JEXEC') or die;

if (count($list) < 2) { return; }
?>
<div class="mod-languages lang-switch" splwpk-multilang="splwpk-multilang">
  <?php foreach ($list as $language): ?>
    <a href="<?php echo htmlspecialchars($language->link, ENT_QUOTES, 'UTF-8'); ?>"
       lang="<?php echo htmlspecialchars($language->lang_code, ENT_QUOTES, 'UTF-8'); ?>"
       hreflang="<?php echo htmlspecialchars($language->lang_code, ENT_QUOTES, 'UTF-8'); ?>"
       <?php echo $language->active ? 'aria-current="true"' : ''; ?>><?php echo htmlspecialchars(strtoupper($language->sef === 'ms' ? 'BM' : $language->sef), ENT_QUOTES, 'UTF-8'); ?></a>
  <?php endforeach; ?>
</div>
