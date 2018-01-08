# -*- coding: utf-8 -*-
# Copyright 2018 Humanytek - Manuel Marquez <manuel@humanytek.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from openerp import api, fields, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    invoices_paid = fields.Boolean(
        'Invoices Paid', compute='_compute_invoices_paid')

    @api.depends('state', 'invoice_ids')
    def _compute_invoices_paid(self):

        for record in self:

            if record.invoice_ids:

                record.invoices_paid = True

                for inv in record.invoice_ids:

                    if inv.state != 'paid':
                        record.invoices_paid = False

    def _search_invoices_paid(self, operator, value):

        sales_ids_invoices_paid = list()

        for record in self.search([('state', 'in', ['sale', 'done'])]):

            if record.invoices_paid:

                sales_ids_invoices_paid.append(record.id)

        return ([('id', 'in', sales_ids_invoices_paid)])
