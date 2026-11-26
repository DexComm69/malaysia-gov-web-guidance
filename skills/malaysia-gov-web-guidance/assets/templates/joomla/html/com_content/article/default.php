<?php
/**
 * Override of com_content article/default.php: renders Joomla's own article layout unchanged (included,
 * not copied) and, on the privacy page, adds splwpk-privacy-policy to the title heading
 * (SPLaSK Privacy Policy, part 2; part 1 is the tagged footer link on every page).
 * The privacy page is the article opened from a menu item whose Link Class contains "splask-privacy",
 * or an article whose alias contains "privasi"/"privacy".
 */
defined('_JEXEC') or die;

use Joomla\CMS\Factory;

ob_start();
include JPATH_ROOT . '/components/com_content/tmpl/article/default.php';
$html = ob_get_clean();

$active = Factory::getApplication()->getMenu()->getActive();
$linkClass = $active ? ' ' . (string) $active->getParams()->get('menu-anchor_css', '') . ' ' : '';
$isPrivacy = str_contains($linkClass, ' splask-privacy ') || preg_match('/privasi|privacy/i', (string) $this->item->alias);

if ($isPrivacy) {
    $title = preg_quote($this->escape($this->item->title), '/');
    // the first <h1>/<h2> whose text is the article title (h1, or h2 under a menu page heading)
    $html = preg_replace('/<(h[12])>(\s*' . $title . '\s*)<\/\1>/u', '<$1 splwpk-privacy-policy="splwpk-privacy-policy">$2</$1>', $html, 1);
}
echo $html;
