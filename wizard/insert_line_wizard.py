from odoo import api, fields, models


class InsertLineWizard(models.TransientModel):
    _name = 'sale.order.line.insert.wizard'
    _description = 'Insert Line Wizard'

    insert_type = fields.Selection([
        ('note', 'Note'),
        ('section', 'Section'),
        ('product', 'Product')
    ], string='Type', required=True)

    product_id = fields.Many2one(
        'product.product',
        string='Product',
        domain=[('sale_ok', '=', True)],
    )
    name = fields.Text(
        string='Name',
        help="Content of the note or section"
    )

    @api.onchange('insert_type')
    def _onchange_insert_type(self):
        if self.insert_type == 'product':
            self.name = False
        if self.insert_type != 'product':
            self.product_id = False

    def action_validate(self):
        self.ensure_one()
        active_id = self.env.context.get('active_id')
        if not active_id:
            return

        sale_line = self.env['sale.order.line'].browse(active_id)
        current_sequence = sale_line.sequence

        # Update following sequences
        following_lines = self.env['sale.order.line'].search([
            ('order_id', '=', sale_line.order_id.id),
            ('sequence', '>', current_sequence),
        ], order='sequence DESC')

        for line in following_lines:
            line.sequence = line.sequence + 1

        # Prepare values for new line
        vals = {
            'order_id': sale_line.order_id.id,
            'sequence': current_sequence + 1,
        }

        if self.insert_type == 'note':
            vals.update({
                'display_type': 'line_note',
                'name': self.name or 'New Note',
                'product_id': False,
            })
        elif self.insert_type == 'section':
            vals.update({
                'display_type': 'line_section',
                'name': self.name or 'New Section',
                'product_id': False,
            })
        elif self.insert_type == 'product' and self.product_id:
            vals.update({
                'product_id': self.product_id.id,
                'product_uom_qty': 1.0,
                'product_uom': self.product_id.uom_id.id,
            })

        # Create the new line
        self.env['sale.order.line'].create(vals)

        return {'type': 'ir.actions.act_window_close'}
