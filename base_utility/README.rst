======================
Import Odoo XML Files
======================

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
