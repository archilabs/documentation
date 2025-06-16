from odoo import models, api

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    def write(self, vals):
        res = super().write(vals)
        self._generate_exclusion_rules()
        return res

    def _generate_exclusion_rules(self):
        for template in self:
            # Recupera le linee degli attributi
            bl_line = template.attribute_line_ids.filtered(lambda l: l.attribute_id.name == 'Caisson Blanc')
            cl_line = template.attribute_line_ids.filtered(lambda l: l.attribute_id.name == 'CAISSON COULEUR')
            if not bl_line or not cl_line:
                continue

            # Genera le regole di esclusione
            for bl_value in bl_line.value_ids:
                for cl_value in cl_line.value_ids:
                    existing = self.env['product.variant.exclusion'].search([
                        ('product_tmpl_id', '=', template.id),
                        ('value_ids', 'in', [bl_value.id, cl_value.id])
                    ])
                    if not existing:
                        self.env['product.variant.exclusion'].create({
                            'product_tmpl_id': template.id,
                            'value_ids': [(6, 0, [bl_value.id, cl_value.id])]
                        })
