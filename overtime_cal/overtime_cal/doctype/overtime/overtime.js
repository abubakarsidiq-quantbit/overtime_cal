// Copyright (c) 2023, Abhishek Chougule and contributors
// Copyright (c) 2023, Frappe Technologies Pvt. Ltd. and contributors
//Copyright (c) 2023, by Abhishek Chougule developer.mrabhi@gmail.com
// For license information, please see license.txt

frappe.ui.form.on('Overtime', {

	getemplist: function(frm) {
				frm.clear_table("emp")
				frm.refresh_field('emp')
				 }
});
frappe.ui.form.on('Overtime', {

	getempot: function(frm) {
				frm.clear_table("ot")
				frm.refresh_field('ot')
				 }
});
frappe.ui.form.on('Overtime', {

	getempot: function(frm) {
				frm.clear_table("tot")
				frm.refresh_field('tot')
				 }
});

frappe.ui.form.on('Overtime', {
	onload: function(frm) {
		frm.call({
			method:'getemplist',
			doc: frm.doc,
		});
	}
  });

frappe.ui.form.on('Overtime', {
	getempot: function (frm) {
		frm.call({
			method:'getempot',
			doc: frm.doc,
		});
	}
});

frappe.ui.form.on('Overtime', {
	selectall: function (frm) {
		frm.call({
			method:'selectall',
			doc: frm.doc, 
		});
	}
});
