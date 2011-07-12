Paster
======
*A generic pastebin posting tool*

Supported Paste services:

 - **Dpaste** (http://dpaste.com/)
   A django base simple and popular pastebin

 - **Pastebin** (http://pastebin.com/)
   The very famous pastebin. Complete version 3 api supported

Add support for more services easily

Usage
-----

Do `pstr -h`, `pstr paste -h`, `pstr list -h` for help

Examples
--------

Paste some content
> pstr paste "some content"

Paste to the service pastebin
> pstr paste -s pastebin "some content"

Paste file contents (deprecated after piping support)
> pstr paste -f path/to/file/filename.extension

Paste git diff (deprecated after piping support)
> pstr paste -c "git diff"

Paste through the familiar piping
> git diff | pstr paste

List available syntax/languages/formats
> pstr list syntax

List available pastebin services
> pstr list services

For the lazy
------------

  - Alias `pstr paste` to something like `p` and do `echo foo | p`
  - Use a config file to store settings
