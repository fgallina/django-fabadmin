========
Fabadmin
========

Fabadmin provides fabric administration from the Django admin
interface.

Installation
============

Edit your Django project settings and put fabadmin in your
INSTALLED_APPS. Then set the FABADMIN_FABFILE setting to the full path
of your fabfile like so::

    FABADMIN_FABFILE = "/full/path/to/fabfile.py"

Requirements
============

* ansi2html
