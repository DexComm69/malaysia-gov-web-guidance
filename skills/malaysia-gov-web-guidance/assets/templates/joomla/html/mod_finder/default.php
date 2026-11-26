<?php
/** Override of mod_finder/tmpl/default.php (Smart Search): the search tag is on the <form> itself. */
defined('_JEXEC') or die;

use Joomla\CMS\Language\Text;
use Joomla\CMS\Router\Route;

$label = Text::_('MOD_FINDER_SEARCH_VALUE');
?>
<form action="<?php echo Route::_($route); ?>" method="get" role="search" class="mod-finder js-finder-searchform" splwpk-search-function="splwpk-search-function">
  <label for="mod-finder-searchword<?php echo $module->id; ?>"><?php echo $label; ?></label>
  <input type="text" name="q" id="mod-finder-searchword<?php echo $module->id; ?>" value="<?php echo htmlspecialchars($app->getInput()->getString('q', ''), ENT_QUOTES, 'UTF-8'); ?>">
  <button type="submit"><?php echo Text::_('JSEARCH_FILTER_SUBMIT'); ?></button>
</form>
<?php /* Advanced search: switch on Smart Search > Options > Show Advanced Search, override com_finder's
   search form the same way with splwpk-advanced-search-function on its <form>, and register that page as a Criteria URL. */ ?>
