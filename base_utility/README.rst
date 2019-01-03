======================
Odoo Utilities
======================

load_xml()
---------------

This module creates a utility model ``base.utility`` and exposes a
classmethod ``load_xml()`` using the ``@api.model`` decorator. It
simply transmits the xml string, writes to a tempfile  and calls the Odoo
native xml import function ``convert_xml_import``.

.. code-block:: python

  >>> odoo = odoorpc.ODOO(...)
  >>> odoo.login(...)
  >>> utils = odoo.env['base.utility']
  >>> with open('demo_data.xml', 'r') as f:
  ....    xmlstring = f.read()
  >>> utils.load_xml(xmlstring)

dump_tmp()
-----------

The module also exposes a method ``dump_tmp()`` on the ``base.utility`` model.
The method takes a backup of the database and dumps it to a tempfile, returning
the name of the tempfile. This can be used over RPC to e.g. take a backup for
staging.
