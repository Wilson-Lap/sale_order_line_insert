from odoo import models, _
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    _inherit = 'sale.order.line'

    def button_insert_after(self):
        self.ensure_one()
        if not self.order_id:
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': _("No sale order already created"),
                    'type': 'warning',
                    'sticky': True,
                    'next': {'type': 'ir.actions.act_window_close'},
                },
            }

        return {
            'name': _('Insert Line'),
            'type': 'ir.actions.act_window',
            'res_model': 'sale.order.line.insert.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'active_id': self.id,
                'default_insert_type': 'product',
            },
        }
