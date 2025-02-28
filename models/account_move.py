from odoo import api, fields, models


class AccountMove(models.Model):
    _inherit = "account.move"

    payment_date_str = fields.Char(
        string="Payment Dates",
        compute="_compute_payment_date_str",
        store=True,
        help="Payment dates of associated payments, separated by comma.",
    )

    @api.depends("payment_ids", "payment_ids.payment_date", "move_type")
    def _compute_payment_date_str(self):
        for move in self:
            payments = move.payment_ids.filtered(lambda p: p.state == "posted")
            if payments:
                payment_dates = sorted(payments.mapped("payment_date"))
                move.payment_date_str = ", ".join(payment_dates)
            else:
                if move.move_type == "out_invoice":
                    move.payment_date_str = "No payment collected"
                elif move.move_type == "in_invoice":
                    move.payment_date_str = "No payment made"
                else:
                    move.payment_date_str = False
