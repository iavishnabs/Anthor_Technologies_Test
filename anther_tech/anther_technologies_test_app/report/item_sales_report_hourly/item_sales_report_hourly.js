// Copyright (c) 2025, avishna and contributors
// For license information, please see license.txt

frappe.query_reports["Item Sales Report-Hourly"] = {
    "filters": [
		{
            "fieldname": "item_name",
            "label":"Item",
            "fieldtype": "Link",
            "options": "Item",
			"default": "",
        },
        {
            "fieldname": "from_date",
            "label":"From Date",
            "fieldtype": "Date",
            "default": frappe.datetime.month_start(),
        },
        {
            "fieldname": "to_date",
            "label": "To Date",
            "fieldtype": "Date",
            "default": frappe.datetime.month_end(),
        },
        {
            "fieldname": "company",
            "label": "Company",
            "fieldtype": "Link",
            "options": "Company",
            "default": frappe.defaults.get_default("company"),
        },
        {
            "fieldname": "pos_profile",
            "label": "POS Profile",
            "fieldtype": "Link",
            "options": "POS Profile",
            "default": "",
        },
        {
            "fieldname": "cost_center",
            "label": "Cost Center",
            "fieldtype": "Link",
            "options": "Cost Center",
            "default": "",
        }
    ]
};
