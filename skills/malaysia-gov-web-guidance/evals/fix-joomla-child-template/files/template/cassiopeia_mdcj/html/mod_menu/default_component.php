<?php
// Override of mod_menu/tmpl/default_component.php (Joomla 5)
defined('_JEXEC') or die;
use Joomla\CMS\HTML\HTMLHelper;

$attributes = [];
if ($item->anchor_title) { $attributes['title'] = $item->anchor_title; }
if ($item->anchor_css)   { $attributes['class'] = $item->anchor_css; }
$linktype = $item->title;

// SPLaSK tags by menu title
$icon = '';
if ($item->title === 'Tentang Kami') {
    $attributes['splwpk-about-us'] = 'splwpk-about-us';
    $attributes['timestamp'] = '2026-11-03 09:00:00';
}
if ($item->title === 'Hubungi Kami') {
    // tag goes on the icon so it shows next to the text
    $icon = '<i class="icon-phone" splwpk-contact-details="splwpk-contact-details" timestamp="12/11/2026"></i> ';
}
echo HTMLHelper::_('link', $item->flink, $icon . $linktype, $attributes);
