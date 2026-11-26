<?php
// Override of mod_finder/tmpl/default.php (Joomla 5), simplified
defined('_JEXEC') or die;
use Joomla\CMS\Router\Route;
?>
<div class="mod-finder" splwpk-search-function="splwpk-search-function">
  <form action="<?php echo Route::_($route); ?>" method="get" role="search">
    <label for="mod-finder-searchword" class="visually-hidden">Carian</label>
    <input type="text" name="q" id="mod-finder-searchword" value="">
    <button type="submit">Cari</button>
  </form>
</div>
