# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Payment Day String",
    "summary": """
        Adds a sting to account.move tree view to show the dates of any payments asociated with invoices""",
    "author": "Be OnlyOne",
    "maintainers": ["onlyone-odoo"],
    "website": "https://onlyone.odoo.com/",
    "license": "AGPL-3",
    "category": "Technical Settings",
    "version": "17.0.2.0.0",
    "development_status": "Production/Stable",
    "application": False,
    "installable": True,
    "depends": ["base", "account"],
    "data": [
        "views/account_move_tree.xml",
    ],
}
