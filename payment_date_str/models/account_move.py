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
        "line_ids.matched_debit_ids.debit_move_id",
        "line_ids.matched_credit_ids.credit_move_id",
    )
    def _compute_payment_date_str(self):
        for move in self:
            payment_moves = (
                move.line_ids.matched_debit_ids.debit_move_id
                | move.line_ids.matched_credit_ids.credit_move_id
            )
            payments = payment_moves.filtered(
                lambda m: m.payment_id and m.payment_id.state == "posted"
            )

            if payments:
                payment_dates = sorted(payments.mapped("date"))
                move.payment_date_str = ", ".join(
                    date.strftime("%Y-%m-%d") for date in payment_dates
                )
            else:
                move.payment_date_str = (
                    "Sin pago cobrado"
                    if move.move_type == "out_invoice"
                    else "Sin pago realizado"
                    if move.move_type == "in_invoice"
                    else False
                )
