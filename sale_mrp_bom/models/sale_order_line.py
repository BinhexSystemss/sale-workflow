# Copyright 2020 Akretion Renato Lima <renato.lima@akretion.com.br>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    bom_id = fields.Many2one(
        comodel_name="mrp.bom",
        string="BoM",
        domain="[('product_tmpl_id.product_variant_ids', '=', product_id),"
        "'|', ('product_id', '=', product_id), "
        "('product_id', '=', False)]",
    )

    can_set_bom_id = fields.Boolean(store=True, compute="_compute_can_set_bom_id")

    @api.constrains("bom_id", "product_id")
    def _check_match_product_variant_ids(self):
        for line in self:
            if line.bom_id:
                bom_product_tmpl = line.bom_id.product_tmpl_id
                bom_product = bom_product_tmpl.product_variant_ids
            else:
                bom_product_tmpl, bom_product = None, None
            line_product = line.product_id
            if not bom_product or line_product == bom_product:
                continue
            raise ValidationError(
                _(
                    "Please select BoM that has matched product with the line `{}`"
                ).format(line_product.name)
            )

    @api.depends("product_id.route_ids", "is_mto")
    def _compute_can_set_bom_id(self):
        manufacture_route = self.env.ref(
            "mrp.route_warehouse0_manufacture", raise_if_not_found=False
        )
        for line in self:
            can_set_bom_id = False
            if line.product_id and manufacture_route:
                can_set_bom_id = (
                    manufacture_route in line.product_id.route_ids and line.is_mto
                )
            line.can_set_bom_id = can_set_bom_id
