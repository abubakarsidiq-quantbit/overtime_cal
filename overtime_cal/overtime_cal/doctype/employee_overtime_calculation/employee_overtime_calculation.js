// Copyright (c) 2024, Abhishek Chougule and contributors
// For license information, please see license.txt

frappe.ui.form.on('Employee Overtime Calculation', {
	// refresh: function(frm) {

	// }
});


frappe.ui.form.on('Employee Overtime Calculation', {
	onload: function(frm) {
		frm.call({
			method:'getemplist',
			doc: frm.doc,
		});
	}
  });


  frappe.ui.form.on('Employee Overtime Calculation', {
	select_all: function(frm) {
		frm.call({
			method:'selectall',
			doc:frm.doc
		})
	}
});

frappe.ui.form.on('Employee Overtime Calculation', {
	overtimebtn: function(frm) {
		frm.clear_table("eodetails");
		frm.refresh_field('eodetails');
		frm.clear_table("emptotal");
		frm.refresh_field('emptotal');
		frm.call({
			method:'get_ot',
			doc:frm.doc
		})
	}
});

frappe.ui.form.on('Employee Overtime Calculation', {
    download_file: function(frm) {
        // Check if the form is saved
        if (!frm.doc.__islocal) {
            frappe.call({
                method: 'download_file',
                doc: frm.doc,
                callback: function(r) {
                    if (r.message) {
                        var file_path = "https://training-ntfoods.erpdata.in/files/output.csv";
                        window.open(file_path);
                    }
                }
            });
        } else {
            frappe.msgprint(__("Please save the form before downloading."));
        }
    }
});



frappe.ui.form.on('Employee Overtime Calculation', {
    download: function(frm) {
        // Check if the form is saved
        if (!frm.doc.__islocal) {
            frappe.call({
                method: 'download',
                doc: frm.doc,
                callback: function(r) {
                    if (r.message) {
                        var file_path = "https://training-ntfoods.erpdata.in/files/output.csv";
                        window.open(file_path);
                    }
                }
            });
        } else {
            frappe.msgprint(__("Please save the form before downloading."));
        }
    }
});
// frappe.ui.form.on('Employee Overtime Calculation', {
// 	overtimebtn: function(frm) {
// 		frm.clear_table("emptotal");
// 		frm.refresh_field('emptotal');
// 		frm.call({
// 			method:'get_employee_sum',
// 			doc:frm.doc
// 		})
// 	}
// });