# Copyright (c) 2025, avishna and contributors
# For license information, please see license.txt

import frappe
from frappe.utils import cint

def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
    return columns, data

def get_columns():
    columns = [
        {"label": "Item Name", "fieldname": "item_name", "fieldtype": "Data", "width": 200},
        {"label": "Item Group", "fieldname": "item_group", "fieldtype": "Data", "width": 150},
        {"label": "UOM", "fieldname": "uom", "fieldtype": "Data", "width": 80},
        {"label": "Total Sale", "fieldname": "total_qty", "fieldtype": "Data", "width": 80},
        {"label": "Total Amount", "fieldname": "total_amount", "fieldtype": "Data", "width": 80},
        {"label": "Posting Date", "fieldname": "posting_date", "fieldtype": "Date", "width": 120}
    ]
    
    # Add hourly columns dynamically
    for hour in range(24):
        hour_label = f"{hour:02d}:00 - {hour+1:02d}:00"
        columns.append({
            "label": hour_label,
            "fieldname": f"hour_{hour}",
            "fieldtype": "Data",
            "width": 120
        })
    
    return columns

def get_data(filters):
    conditions = ""
    
    # Apply item name filter
    if filters.get("item_name"):
        conditions += f" AND sii.item_name = '{filters['item_name']}'"
    # Apply date range filter
    if filters.get("from_date") and filters.get("to_date"):
        conditions += f" AND si.posting_date BETWEEN '{filters['from_date']}' AND '{filters['to_date']}'"
    
    # Apply company filter
    if filters.get("company"):
        conditions += f" AND si.company = '{filters['company']}'"
    
    # Apply POS profile filter
    if filters.get("pos_profile"):
        conditions += f" AND si.pos_profile = '{filters['pos_profile']}'"
    
    # Apply cost center filter
    if filters.get("cost_center"):
        conditions += f" AND sii.cost_center = '{filters['cost_center']}'"
    
    query = f"""
        SELECT sii.item_name, sii.item_group, sii.uom, si.posting_date, 
               HOUR(si.posting_time) as hour, SUM(sii.qty) as qty, SUM(sii.amount) as amount
        FROM `tabSales Invoice Item` sii
        JOIN `tabSales Invoice` si ON sii.parent = si.name
        WHERE si.docstatus = 1 {conditions}
        GROUP BY sii.item_name, sii.item_group, sii.uom, si.posting_date, HOUR(si.posting_time)
        ORDER BY si.posting_date, sii.item_name, hour
    """
    
    sales_data = frappe.db.sql(query, as_dict=True)
    
    report_data = {}
    for row in sales_data:
        key = (row.item_name, row.item_group, row.uom, row.posting_date)
        
        if key not in report_data:
            report_data[key] = {
                "item_name": row.item_name,
                "item_group": row.item_group,
                "uom": row.uom,
                "posting_date": row.posting_date,
                "total_qty": 0,
                "total_amount": 0.0,
            }
            for i in range(24):
                report_data[key][f"hour_{i}"] = "0 / 0.00"
        
        report_data[key][f"hour_{row.hour}"] = f"{row.qty} / {row.amount:.2f}"
        report_data[key]["total_qty"] += row.qty
        report_data[key]["total_amount"] += row.amount
    
    return list(report_data.values())
