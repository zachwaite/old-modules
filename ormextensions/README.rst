Model.split() and the SplitRecordset
=====================================

The ``.split()`` method instantiates a SplitRecordset object, keyed on the
list of fieldnames passed to ``split()``. SplitRecordset implements the
iterator protocol for working with the split groups as well as an ``apply()``
method to operate on the groups. There is currently no ``combine()``
implementation since the output of ``apply()`` is not standardized, but outputs
can easily be combined with python comprehensions, itertools.chain() and/or
Odoo recordset operators, depending on the output type.

Some examples:

.. code-block:: python

    >>> from odoo import models, fields, api, _
    >>> from odoo.addons.ormextensions import OrmExtensions

    >>> class Partner(models.Model, OrmExtensions)
    ....    _inherit = 'res.partner'
    ....
    ....    @api.multi
    ....    def split_by_company(self):
    ....        return self.split(['company_id'])
    ....

    >>> partners = self.env['res.partner'].search([])
    >>> partners_by_type = partners.split_by_company()
    >>> partners_by_type.keys()
    # [('company',), ('person',)]

    >>> partners_by_type.items()
    # [(('company',), res.partner(14, 10, 11, 15, 12)), (('person',), res.partner(26, 33, 27, 35, 18, 19, 20, 21))]

    >>> for rs in partners_by_type.values():
    ....    print(rs)
    ....
    # res.partner(14, 10, 11, 15, 12)
    # res.partner(26, 33, 27, 35, 18, 19, 20, 21)

    >>> partners_by_type.apply('id')
    # [(('company',), [14, 10, 11, 15, 12]), (('person',), [26, 33, 27, 35, 18, 19, 20, 21])]

    >>> partners_by_type.apply(len)
    # [(('company',), 5), (('person',), 8)]

    >>> partners_by_type.apply(lambda rs: max(rs.mapped('id')))
    # [(('company',), 15), (('person',), 33)]

    # Count individual partners, grouped by company, in one query
    >>> self.env['res.partner'].search([('is_company', '=', False)]).split(['parent_id']).apply(len) 
    #[(((False, ''),), 3), (((1, 'YourCompany'),), 2), (((9, 'Wood Corner'),), 3),
    # (((10, 'Deco Addict'),), 3), (((11, 'Gemini Furniture'),), 4), (((12, 'Ready Mat'),), 7),
    # (((13, 'The Jackson Group'),), 2), (((14, 'Azure Interior'),), 3), (((15, 'Lumber Inc'),), 1)]

