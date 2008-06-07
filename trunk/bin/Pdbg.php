<?php

define('APP_PATH', dirname(dirname(__FILE__)));
define('LIB_PATH', APP_PATH . DIRECTORY_SEPARATOR . 'library');
define('GLADE_PATH', APP_PATH . DIRECTORY_SEPARATOR . 'glade');

set_include_path(get_include_path() . PATH_SEPARATOR . LIB_PATH);

require_once 'Pdbg/Application.php';

$app = new Pdbg_Application();
$app->run();
