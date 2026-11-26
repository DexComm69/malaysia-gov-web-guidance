<?php
defined('_JEXEC') or die;
use Joomla\CMS\Factory;
$app = Factory::getApplication();
$wa  = $this->getWebAssetManager();
$sitename = htmlspecialchars($app->get('sitename'), ENT_QUOTES, 'UTF-8');
// SPLaSK: vendor said the news date must always be fresh
$now = Factory::getDate('now', $app->get('offset'))->format('Y-m-d H:i:s');
?>
<!DOCTYPE html>
<html lang="<?php echo $this->language; ?>" dir="<?php echo $this->direction; ?>">
<head>
  <jdoc:include type="metas" />
  <jdoc:include type="styles" />
  <jdoc:include type="scripts" />
</head>
<body class="site">
  <header class="header">
    <jdoc:include type="modules" name="topbar" style="none" />
    <h1 class="brand"><?php echo $sitename; ?></h1>
    <jdoc:include type="modules" name="search" style="none" />
    <jdoc:include type="modules" name="menu" style="none" />
    <div class="ticker"><a href="index.php?option=com_content&view=category&id=8" splwpk-news="splwpk-news" timestamp="<?php echo $now; ?>">Berita Terkini</a></div>
  </header>
  <jdoc:include type="modules" name="banner" style="none" />
  <main><jdoc:include type="message" /><jdoc:include type="component" /></main>
  <aside><jdoc:include type="modules" name="sidebar-right" style="card" /></aside>
  <footer class="footer">
    <a href="dasar-privasi" splwpk-privacy-policy="splwpk-privacy-policy">Dasar Privasi</a> |
    <!-- <a href="peta-laman" splwpk-sitemap="splwpk-sitemap">Peta Laman</a> | -->
    <a href="arkib" splwpk-electronic-archieve="splwpk-electronic-archieve">Arkib</a> |
    <a href="http://www.malaysia.gov.my">MyGov</a>
    <jdoc:include type="modules" name="footer" style="none" />
  </footer>
</body>
</html>
