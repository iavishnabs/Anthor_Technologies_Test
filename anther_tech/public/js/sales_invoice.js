// here fetching the time zone from country doctype via billing address of customer
// (must create a billing address to the customer when sales invoice create against that customer)

frappe.ui.form.on('Sales Invoice', {
    validate: function(frm) {
        if (frm.doc.customer_address) {
            frappe.db.get_doc('Address', frm.doc.customer_address)
                .then(address => {
                    if (address.country) {
                        frappe.db.get_doc('Country', address.country)
                            .then(country => {
                                if (country.time_zones) {
                                    frm.set_value('custom_time_zone', country.time_zones);
                                }
                            });
                    }
                });
        }
    }
});
