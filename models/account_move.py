from odoo import api, fields, models


class AccountMove(models.Model):
    _inherit = "account.move"

    payment_date_str = fields.Char(
        string="Fechas de Pago",
        compute="_compute_payment_date_str",
        store=True,
        help="Fechas de los pagos asociados a esta factura, separadas por coma.",
    )

    @api.depends("payment_ids", "payment_ids.date", "move_type")
    def _compute_payment_date_str(self):
        for move in self:
            payments = move.payment_ids.filtered(lambda p: p.state == "posted")
            if payments:
                payment_dates = sorted(payments.mapped("date"))
                move.payment_date_str = ", ".join(
                    date.strftime("%Y-%m-%d") for date in payment_dates
                )
            else:
                move.payment_date_str = False
            # Opcional: ajustar el nombre del campo según el tipo
            if move.move_type == "out_invoice":
                move.payment_date_str = move.payment_date_str or "Sin pagos recibidos"
            elif move.move_type == "in_invoice":
                move.payment_date_str = move.payment_date_str or "Sin pagos realizados"
