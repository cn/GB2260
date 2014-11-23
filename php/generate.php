<?php
/**
 * Generate data file for PHP.
 */

$lines = file('../GB2260.txt', FILE_IGNORE_NEW_LINES | FILE_SKIP_EMPTY_LINES);

$rv = array();

foreach($lines as $line) {
  list($code, $value) = explode("\t", $line);
  $rv[$code] = $value;
}

echo "<?php \nreturn ";
var_export($rv);
echo ";\n";
