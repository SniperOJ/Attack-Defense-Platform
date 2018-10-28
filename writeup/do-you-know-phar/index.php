<?php
$phar = new Phar('c.phar', 0, 'c.phar');
$phar->buildFromDirectory('./c');
$phar->setStub($phar->createDefaultStub('e.php', ' => .php'));
$phar->compressFiles(Phar::GZ);
?>
