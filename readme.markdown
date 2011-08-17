Transmission File Completion Notifier
=====================================

A script which monitors the Transmission Bittorrent client for files that have
finished downloading. Sends a growl notification when a file is finished

file_completion.py
------------------

A script written in Python3. It watches the currently downloading torrent's
files for the transition to 100% completion.

Notes
-----

The server's address is currently hardwired. This script uses growlnotify
instead of the python growl bindings. The script may be backgrounded by the
caller, it does not fork itself.

License
-------

This code is available for use and modification, but please do attribute the
author. Patches and suggestions are welcome.
