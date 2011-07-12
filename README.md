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

    usage: pstr [-h] [-v] {list,paste} ...

    A generic pastebin tools

    optional arguments:
      -h, --help     show this help message and exit
      -v, --version  show program's version number and exit

    subcommands:
      available subcommands

      {list,paste}   additional help
        paste        paste a snippet
        list         list various available properties

###Subcommands
**paste**

    usage: pstr paste [-h] [-x syntax] [-t title] [-n name/email] [-s service]
                      [-e extra] [-d] [-p] [-c] [-f] [-k api_key] [--verbose]
                      content

    positional arguments:
      content               content of the paste

    optional arguments:
      -h, --help            show this help message and exit
      -x syntax, --syntax syntax
                            syntax of the paste
      -t title, --title title
                            title of paste
      -n name/email , --poster name/email
                            name or email of poster
      -s service , --service service
                            specify the pastebin service to be used
      -e extra , --extra extra
                            specify some extra arguements (urlencoded)
      -d, --hold            delay the deletion of post
      -p, --private         keep the paste private
      -c, --command         post output of command supplied as content
      -f, --file            post output of file supplied as content
      -k api_key, --api-key api_key
                            for pastebin: api_dev_key
      --verbose

**list**

    usage: pstr list [-h] [-v service] type

    positional arguments:
      type                  the property to be listed
      currently available:

        - syntax: list of syntax/languages/formats available
        - services: list of services available
        - configs: the existing configuration settings

    optional arguments:
      -h, --help            show this help message and exit
      -s service , --service service
                            specify the pastebin service to be used

Config
------
Files:
> `~/.pastercfg` or `/etc/paster.cfg`

The default configuration and available settings:

    [user]
    name =
    email =

    [preferences]
    syntax =
    extra =
    title =
    service = dpaste
    hold = false
    command = false
    file = false
    private = false

    [pastebin]
    api_dev_key =
    api_paste_expire_date =
    api_user_name =
    api_user_password =

Examples
--------

Paste some content
> pstr paste "some content"

Paste to pastebin
> pstr paste -v pastebin "some content"

Paste file contents
> pstr paste -f path/to/file/filename.extension

Paste git diff
> pstr paste -c "git diff"

Paste through the familiar piping
> git diff | pstr paste

List available syntax/languages/formats
> pstr list syntax

List available pastebin services
> pstr list services


For the lazy
------------

  - Alias `pstr paste` to something small
  - Use a config file to store settings
