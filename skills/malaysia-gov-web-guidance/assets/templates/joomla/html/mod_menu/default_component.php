<?php
/**
 * Override of mod_menu/tmpl/default_component.php: adds the SPLaSK tag (and real timestamp) from the Link Class.
 * Copy the same two lines into default_url.php for external menu items.
 */
defined('_JEXEC') or die;

use Joomla\CMS\HTML\HTMLHelper;

require_once JPATH_THEMES . '/' . $app->getTemplate() . '/helper/splask.php';

$attributes = [];
if ($item->anchor_title) { $attributes['title'] = $item->anchor_title; }
if ($item->anchor_css)   { $attributes['class'] = $item->anchor_css; }
if ($item->anchor_rel)   { $attributes['rel'] = $item->anchor_rel; }
if ($item->id == $active_id) { $attributes['aria-current'] = 'page'; }
$attributes += SplaskHelper::attributes($item);   // tag on the <a>, never on an icon

echo HTMLHelper::_('link', $item->flink, htmlspecialchars($item->title, ENT_QUOTES, 'UTF-8'), $attributes);
