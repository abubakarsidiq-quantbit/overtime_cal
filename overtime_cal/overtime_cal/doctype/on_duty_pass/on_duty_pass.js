// Copyright (c) 2024, Abhishek Chougule and contributors
// For license information, please see license.txt

frappe.ui.form.on('On Duty Pass', {
	// refresh: function(frm) {

	// }
});


frappe.ui.form.on('On Duty Pass', {
	after_save: function(frm) {
		frm.call({
			method:'calculate_total_time',
			doc:frm.doc
		})
	}
});