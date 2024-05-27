// Copyright (c) 2023, Abhishek Chougule and contributors
// For license information, please see license.txt

frappe.ui.form.on('Biometric Sync Setting', {
	// refresh: function(frm) {

	// }
});
frappe.ui.form.on('Biometric Sync Setting', {
	sync_data:function(frm)
	{
		    frm.call({
		     	method:'sync_data',
		 		doc: frm.doc
		     });
	},
});