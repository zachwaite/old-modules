# © 2018 Waite Perspectives, LLC - Zach Waite
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import tempfile

from odoo import models, fields, api
from odoo.tools.convert import convert_xml_import
from odoo.service.db import dump_db

class Utility(models.AbstractModel):
    _name = 'base.utility'
    _description = 'Generic utilities'

    @api.model
    def load_xml(self, xml):
        #https://www.odoo.com/forum/help-1/question/can-t-write-file-on-linux-server-88221
        CR = self.env.cr
        MODULE = "__rpc_import__"
        tmp = tempfile.NamedTemporaryFile(prefix='odoo_', delete=False)
        with open(tmp.name, 'w') as f:
            f.write(xml)
        success = convert_xml_import(CR, MODULE, tmp.name)
        return success

    @api.model
    def dump_tmp(self):
        """Dump to a temp file and return it's location to the caller. Later,
        copy the dump via scp, then clean_tmp.
        """
        t = tempfile.NamedTemporaryFile(suffix='.zip', prefix='odoo_', delete=False)
        dump_db(self.env.cr.dbname, t)
        return t.name

