from odoo import http
from odoo.http import request
import json
from datetime import datetime, timedelta



class SaleOrder(http.Controller):
    ############################################################################### SEARCH ###################################3
    @http.route("/get_order", type='json', auth='user')
    def get_order(self):
        print('yes enterd')
        sales = request.env['sale.order'].search([])
        data = []
        for rec in sales:
            vals = {
                'id': rec.id,
                'name': rec.name,
                'partner_id': rec.partner_id

            }
            data.append(vals)
        datas = {"status": 200, "response": sales, "message": "success"}

        return datas

    ###################################################################v  CREATE ##########################################################

    @http.route('/create_order', type="json", auth='user')
    def create_order(self, orders):
        order_ids = []
        for rec in orders:
            if rec['partner_id']:
                order_lines = []
                for line in rec['order_line']:
                    order_line = (0, 0, {
                        "product_id": line["product_id"],
                        "product_uom_qty": line["product_uom_qty"],
                        "price_unit": line["price_unit"]
                    })
                    order_lines.append(order_line)
                vals = {
                    "partner_id": rec['partner_id'],
                    "sale_description": rec['sale_description'],
                    "validity_date": rec['validity_date'],
                    "order_line": order_lines
                }

                order = request.env['sale.order'].sudo().create(vals)
                order_ids.append(order.id)

        args = {"status": 200, "message": "success", 'IDs': order_ids}
        return args

    ######################################################################### UPDATE RECORD ############################################

    @http.route('/update_order', type="json", auth='user', methods=["PUT"])
    def update_order(self, **rec):
        if rec["id"]:
            order = request.env['sale.order'].sudo().search([('id', '=', rec['id'])])
            if order:
                order_lines = []
                for line in rec['order_line']:
                    order_line = (0, 0,
                                  {
                                      "product_id": line["product_id"],
                                      "product_uom_qty": line["product_uom_qty"],
                                      "price_unit": line["price_unit"]
                                  },
                                  )
                    order_lines.append(order_line)
                vals = {
                    "id": rec['id'],
                    "sale_description": rec['sale_description'],
                    "validity_date": rec['validity_date'],
                    "order_line": order_lines
                }
                order.write(vals)
                args = {"status": 200, "message": "success", 'ID': order.id}
            else:
                args = {"status": 404, "message": "order not found"}
        else:
            args = {"status": 400, "message": "order_id parameter is missing"}
        return args

    ##################################################################################### DELETE RECORD ###############################################

    """Sale order"""

    @http.route('/delete_order', type="json", auth='user', methods=["DELETE"])
    def delete_order(self, **rec):
        if rec.get("id"):
            order = request.env['sale.order'].sudo().search([('id', '=', rec['id'])])
            if order:
                order.unlink()
                args = {"status": 200, "message": "success"}
            else:
                args = {"status": 404, "message": "order not found"}
        else:
            args = {"status": 400, "message": "order_id parameter is missing"}
        return args

    """Sale order line"""


    @http.route('/delete_order_line', type="json", auth='user', methods=["DELETE"])
    def delete_order_line(self, **rec):
        if rec.get("order_id"):
            order = request.env['sale.order'].sudo().search([('id', '=', rec['order_id'])])
            print("order is",order)
            if order:
                order_line=request.env['sale.order.line'].sudo().search([('order_id', '=', rec['order_id'])])
                print("order_line is",order_line)
                if order_line:
                    order_line.unlink()
                    args = {"status": 200, "message": "success"}

                else:
                    args = {"status": 400, "message": "order_id missing"}
            else:
                args = {"status": 400, "message": "order missing"}
            return args

    ########################################################################################## Changes in las 24 Hrs ######################################


    @http.route('/get_sale_order_changes', type='json', auth='user')
    def get_sale_order_changes(self):
            last_24_hours = datetime.now() - timedelta(hours=24)
            sale_orders = request.env['sale.order'].sudo().search([('write_date', '>=', last_24_hours)])
            changes = []
            for order in sale_orders:
                changes.append({
                    'id': order.id,
                    'write_date': order.write_date,
                    'sale_description': order.sale_description,
                    'validity_date': order.validity_date,
                    'order_lines': [(line.product_id.name, line.product_uom_qty, line.price_unit) for line in
                                    order.order_line]
                })
            return {'status': 200, 'changes': changes}






