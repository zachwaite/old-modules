# © 2018 Waite Perspectives, LLC - Zach Waite
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, fields, api
from odoo.tools.convert import convert_xml_import

class Utility(models.AbstractModel):
    _name = 'base.utility'

    @api.model
    def load_xml(self, xml):
        CR = self.env.cr
        MODULE = "__rpc_import__"
        #https://www.odoo.com/forum/help-1/question/can-t-write-file-on-linux-server-88221
        with open('/tmp/data', 'w') as f:
            f.write(xml)

        success = convert_xml_import(CR, MODULE, f.name)
        return success

