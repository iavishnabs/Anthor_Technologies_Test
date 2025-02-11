# Copyright (c) 2025, avishna and contributors
# For license information, please see license.txt

import frappe

def execute(filters=None):
    columns = [
        {
            "fieldname": "item_code",
            "label": "Item",
            "fieldtype": "Data",
            "width": 200
        },
        {
            "fieldname": "quantity",
            "label": "Quantity",
            "fieldtype": "Float",
            "width": 100
        },
        {
            "fieldname": "sales_value",
            "label": "Total Sale",
            "fieldtype": "Currency",
            "width": 150
        },
        {
            "fieldname": "time_zone",
            "label": "Time Zone",
            "fieldtype": "Data",
            "width": 400
        }
    ]

    # fetching sales invoice items from sales invoices and group by time zone (fetch from custom field custom_time_zone in sales invoice)
    
    data = frappe.db.sql("""
        SELECT  
            sii.item_code,
            SUM(sii.qty) AS quantity,
            SUM(sii.amount) AS sales_value,
            si.custom_time_zone AS time_zone
        FROM 
            `tabSales Invoice` AS si
        JOIN 
            `tabSales Invoice Item` AS sii ON si.name = sii.parent
        INNER JOIN 
            `tabCustomer` AS c ON si.customer = c.name
        WHERE 
            si.docstatus = 1
        GROUP BY 
            si.custom_time_zone, sii.item_code
    """, as_dict=True)
    
    return columns, data
