# Copyright (c) 2024, Abhishek Chougule and contributors
# For license information, please see license.txt

from datetime import datetime, timedelta
import frappe
from frappe.utils import time_diff_in_hours
from frappe.model.document import Document

class OnDutyPass(Document):
	
	@frappe.whitelist()
	def calculate_total_time(self):
		if self.pass_type == "Out Pass" and self.out_time and self.in_time:
			# frappe.throw(str(self.out_time))
			outdiff = time_diff_in_hours(self.in_time, self.out_time)
			# frappe.throw(str(outdiff))
			self.total_t = outdiff
			self.save()
		# elif self.pass_type == "Early Going" and self.out_time and self.in_time:
		# 	diffearly = time_diff_in_hours(self.out_time, self.in_time)
		# 	self.total_t =  diffearly
		# 	self.save()
			