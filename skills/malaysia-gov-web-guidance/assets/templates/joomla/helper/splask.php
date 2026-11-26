<?php
/**
 * SPLaSK helper for the child template (Joomla 4/5). Loaded by the overrides in html/.
 * Menu items get their tag from the Link Class field (Menu item > Link Type > Link Class):
 *   splask-about, splask-news, splask-faq, splask-contact, splask-sitemap, splask-privacy, splask-charter, splask-cio
 */
defined('_JEXEC') or die;

use Joomla\CMS\Factory;
use Joomla\CMS\HTML\HTMLHelper;

final class SplaskHelper
{
    private const MAP = [
        'splask-about'   => ['splwpk-about-us', true],
        'splask-news'    => ['splwpk-news', true],
        'splask-faq'     => ['splwpk-faq', true],
        'splask-contact' => ['splwpk-contact-details', true],
        'splask-charter' => ['splwpk-client-charter', true],
        'splask-cio'     => ['splwpk-publicising', true],
        'splask-sitemap' => ['splwpk-sitemap', false],
        'splask-privacy' => ['splwpk-privacy-policy', false],
    ];

    /** Attributes to add to a menu link: the tag, and a real timestamp when the item links to an article or category. */
    public static function attributes(object $item): array
    {
        $classes = ' ' . (string) $item->getParams()->get('menu-anchor_css', '') . ' ';
        foreach (self::MAP as $class => [$tag, $needsTs]) {
            if (strpos($classes, ' ' . $class . ' ') === false) continue;
            $attrs = [$tag => $tag];
            if ($needsTs && ($ts = self::timestampFor($item)) !== '') $attrs['timestamp'] = $ts;
            return $attrs;
        }
        return [];
    }

    /** Real modified date of the linked article, or of the newest article in a linked category: never the current time. */
    public static function timestampFor(object $item): string
    {
        $q = $item->query ?? [];
        $db = Factory::getContainer()->get('DatabaseDriver');
        $query = $db->getQuery(true)->select('MAX(' . $db->quoteName('modified') . ')')->from($db->quoteName('#__content'))
            ->where($db->quoteName('state') . ' = 1');
        if (($q['view'] ?? '') === 'article' && !empty($q['id'])) {
            $query->where($db->quoteName('id') . ' = ' . (int) $q['id']);
        } elseif (in_array($q['view'] ?? '', ['category', 'featured'], true) && !empty($q['id'])) {
            $query->where($db->quoteName('catid') . ' = ' . (int) $q['id']);
        } else {
            return '';
        }
        $modified = $db->setQuery($query)->loadResult();
        return $modified ? HTMLHelper::_('date', $modified, 'Y-m-d H:i:s') : '';   // site time zone
    }

    public static function attrString(array $attrs): string
    {
        $out = '';
        foreach ($attrs as $k => $v) $out .= ' ' . $k . '="' . htmlspecialchars((string) $v, ENT_QUOTES, 'UTF-8') . '"';
        return $out;
    }
}
