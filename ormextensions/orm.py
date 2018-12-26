# © 2018 Waite Perspectives, LLC - Zach Waite
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import operator
from odoo import models, api

def ensure_data(method):
    def wrapper(self, *args, **kwargs):
        if not self._data:
            self._load()
        return method(self, *args, **kwargs)
    return wrapper


class SplitRecordset():
    """Collection object to define ordered groups of recordsets.
    """
    def __init__(self, recordset, keys):
        """
        Store the definition of the split recordset, but don't build the
        _data contents until the 'apply' or 'iter' call in lazy fashion.

        Args:
            recordset (recordset): Any Odoo recordset instance
            keys (list): A list of field names of the provided recordset


        """
        self._recordset = recordset
        self._keys = keys
        self._data = [] # will hold ((keys), [ids]) pairs

    def _ensure_compatible(self, key, value):
        """Handle edge cases for relational fields
        """
        typ = self._recordset._fields[key].type
        if typ not in ('many2one', 'one2many', 'many2many'):
            return value
        elif typ == 'many2one' and not value:
            return (False, '')
        elif typ in ('one2many', 'many2many'):
            return tuple(value)

    def _browse(self, ids):
        """Browse a list of ids using the environment provided by the initial
        recordset
        """
        return self._recordset.browse(ids)

    def _read_raw(self):
        raw_read = self._recordset.read(self._keys)
        raw_data = []
        for d in raw_read:
            key_tup = tuple(self._ensure_compatible(k, d[k]) for k in self._keys)
            raw_data.append((key_tup, d['id']))
        return raw_data

    def _compute_keys(self, raw_data):
        keys = list({tup[0] for tup in raw_data})
        rng = list(range(len(self._keys)))
        keys.sort(key=operator.itemgetter(*rng))
        return keys

    def _load(self):
        raw_data = self._read_raw()
        keys = self._compute_keys(raw_data)
        for key in keys:
            self._data.append((key, [t[1] for t in raw_data if t[0] == key]))

    @ensure_data
    def __iter__(self):
        return iter(self._data)

    @ensure_data
    def keys(self):
        """Return the list of keys only
        """
        return [t[0] for t in self._data]

    @ensure_data
    def ids(self):
        """Return the lists of ids only
        """
        return [t[1] for t in self._data]

    @ensure_data
    def values(self):
        """Return the list of recordsets only, converted from ids during this call
        """
        return [self._browse(t[1]) for t in self._data]

    @ensure_data
    def items(self):
        """Return a list of tups from self._data, as a list.

        This implementation uses comprehension to return a copy.
        """
        return [(t[0], self._browse(t[1])) for t in self._data]

    # no need to ensure data, since calling self.values()
    # Note: Implementing a `combine()` method should not be done without
    # standardizing the output of apply() or implementing an extensible dispatch
    # strategy.
    def apply(self, expr):
        """Map expr across the groups. If expr is callable, it will be called on
        each group of the SplitRecordset. If the expr is a string, it will be
        curried and called as the arg of mapped in the enclosed rs.
        """
        if type(expr) == str:
            return [(t[0], t[1].mapped(expr)) for t in self.items()]
        else:
            return [(t[0], expr(t[1])) for t in self.items()]

    def mapped(self, *args, **kwargs):
        raise AttributeError('SplitRecordset object has no "mapped()" method. Perhaps you meant "apply()"')


class OrmExtensions():
    """Mixin class to add fluent access to SplitRecordset class

    Example:
        >>> from odoo import models, fields, api, _
        >>> import fluent_odoo as fluent
        >>> class Partner(models.Model, fluent.OrmExtensions)
        ....    _inherit = 'res.partner'
        ....
        ....    @api.multi
        ....    def split_by_company(self):
        ....        return self.split(['company_id'])
        ....

    """

    @api.multi
    def split(self, keys):
        """Instantiate and return a SplitRecordset object

        Example:
            >>> partners = self.env['res.partner'].search([])
            >>> partners_by_company = partners.split(['company_id'])
        """
        return SplitRecordset(self, keys)


