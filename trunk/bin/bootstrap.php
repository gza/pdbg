<?php
define('APP_PATH', dirname(dirname(__FILE__)));
define('LIB_PATH', APP_PATH . DIRECTORY_SEPARATOR . 'library');
define('GLADE_PATH', APP_PATH . DIRECTORY_SEPARATOR . 'glade');

set_include_path(implode(PATH_SEPARATOR, array(
    get_include_path(),
    LIB_PATH,
)));
