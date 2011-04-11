Paster
======
*A generic pastebin pasting tool*

Supported Paste services:
 
 - **Dpaste** (http://dpaste.com/)  
   A django base simple and popular pastebin
   
 - **Pastebin** (http://pastebin.com/)  
   The very famous pastebin. Complete version 3 api supported
   
And many more will be added soon

Usage
-----

    paster.py [-h] [-s syntax] [-t title] [-n name/email] [-v service]
              [-e extra] [-d] [-p] [-c] [-f]
              content

Help
----

    positional arguments:
      content               the content

    optional arguments:
      -h, --help            show this help message and exit
      -s syntax, --syntax syntax
                            syntax of the paste
      -t title, --title title
                            title of paste
      -n name/email , --poster name/email 
                            name or email of poster
      -v service , --service service 
                            specify the pastebin service to be used
      -e extra , --extra extra 
                            specify some extra arguements (urlencoded)
      -d, --hold            delay the deletion of post
      -p, --private         hold the paste (delay in deletion)
      -c, --command         post output of command supplied as content
      -f, --file            post output of file supplied as content

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
