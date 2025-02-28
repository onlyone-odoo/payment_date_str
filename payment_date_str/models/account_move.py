from odoo import api, fields, models


class AccountMove(models.Model):
    _inherit = "account.move"

    payment_date_str = fields.Char(
        string="Fechas de Pago",
        compute="_compute_payment_date_str",
        store=True,
        help="Fechas de los pagos asociados a esta factura, separadas por coma.",
    )

    @api.depends(
        "line_ids.matched_debit_ids.debit_move_id.date",
        "line_ids.matched_credit_ids.credit_move_id.date",
    )
    def _compute_payment_date_str(self):
        for move in self:
            payments = (
                move.line_ids.matched_debit_ids.debit_move_id
                | move.line_ids.matched_credit_ids.credit_move_id
            )
            payments = payments.filtered(lambda p: p.state == "posted")

            if payments:
                payment_dates = sorted(payments.mapped("date"))
                move.payment_date_str = ", ".join(
                    date.strftime("%Y-%m-%d") for date in payment_dates
                )
            else:
                if move.move_type == "out_invoice":
                    move.payment_date_str = "Sin pago cobrado"
                elif move.move_type == "in_invoice":
                    move.payment_date_str = "Sin pago realizado"
                else:
                    move.payment_date_str = False
