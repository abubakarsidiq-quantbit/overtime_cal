// Copyright (c) 2023, Abhishek Chougule and contributors
// For license information, please see license.txt

frappe.ui.form.on('Employee Checkinout', {
	before_save: function(frm) {
		frm.call({
			method:'calot',
			doc: frm.doc, 
		});
	}
});


