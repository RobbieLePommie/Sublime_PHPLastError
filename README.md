Sublime_PHPLastError
====================

This is a Sublime Text Plugin that allows you to jump directly to the file and line of the last reported PHP error ocurred

Settings
--------

The only settings is to add the location of the PHP Error Log. You can usually find this in php.ini. If not in php.ini, errors will go to your webserver log (e.g. apache log)


Shortcut Keys
-------------

The shortcut key ctrl+atl+d is set.


How It Works
------------

It reads the error log and traces back for the last line with the format

[Date Time] Error in FileName on line XX

and will open FileName on line XX

Notes
-----

You can hook this up to your code through error_log() function, for example database errors can add the correct information to the error log, and you can use this script to jump directly to the error line.