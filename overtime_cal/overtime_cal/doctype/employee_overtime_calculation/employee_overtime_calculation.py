# Copyright (c) 2024, Abhishek Chougule and contributors
# For license information, please see license.txt

import csv
from datetime import datetime, timedelta
from datetime import datetime, time
import frappe
from frappe.model.document import Document

class EmployeeOvertimeCalculation(Document):
      
	@frappe.whitelist()
	def getemplist(self):
		self.allow_import=1
		doc = frappe.db.get_list("Employee", fields=["name","employee_name","isotallow"])
		for d in doc:
			if d.isotallow==1:
				self.append("employee_list",
				{
					"empid": d.name,
					"empname": d.employee_name,
				},)

	@frappe.whitelist()
	def selectall(self):
		children = self.get('employee_list')
		if not children:
			return
		all_selected = all([child.empcheckbox for child in children])  
		value = 0 if all_selected else 1 
		for child in children:
			child.empcheckbox = value

	
	@frappe.whitelist()
	def get_ot(self):
		self.get_overtime_details()
		self.get_employee_sum()

	@frappe.whitelist()
	def get_overtime_details(self):
		if self.from_date and self.to_date:
			current_date = datetime.strptime(self.from_date, "%Y-%m-%d")
			end_date = datetime.strptime(self.to_date, "%Y-%m-%d")
			end_day = current_date.replace(hour=23, minute=59, second=59)
			otamount = 0
			while current_date <= end_date:
				empshift=shift_data=""
				end_day = current_date.replace(hour=23, minute=59, second=59)
				for i in self.get("employee_list",{"empcheckbox":1}):
					empshift= frappe.get_value("Shift Assignment",{'employee':i.empid,"docstatus":1,'start_date':["<=", current_date] , 'end_date': [">=", current_date]},"shift_type")
					shiftin=shiftout=shift_data=""
					if empshift:
						empshift = empshift
						# shiftin,shiftout,shift_data= frappe.get_value("Shift Type",{"name":empshift},["start_time","end_time","custom_shift_type"])		
					else:
					# pass          ,'start_date':["=", current_date] , 'end_date': [">=", current_date]
						empshift = frappe.get_value("Employee",{"name":i.empid},"default_shift")
					# frappe.throw(str(empshift))
					shiftin,shiftout,shift_data= frappe.get_value("Shift Type",{"name":empshift},["start_time","end_time","custom_shift_type"])
						
					dayrate = frappe.get_value("Salary Structure Assignment", {"employee": i.empid }, "base")
					out_duty = frappe.get_value("On Duty Pass",{'employee_id': i.empid, 'date': current_date},"total_t")
					sal_advance = frappe.get_value("Employee Advance", {'employee': i.empid, 'posting_date': current_date}, "advance_amount")
					shift_details = frappe.get_doc("Shift Type", empshift)

					breaktime = shift_details.custom_total_break_time
					lbreak = shift_details.custom_lunch_break
					tbreak = shift_details.custom_tea_break

					if breaktime is not None:
						breaktime = int(breaktime) 
						lbreak = int(lbreak)
						tbreak = int(tbreak)
					
					breakmin = timedelta(minutes=breaktime)
					lbreak = timedelta(minutes=lbreak)
					tbreak = timedelta(minutes=tbreak)



					if shift_data == "Second":
						temp_date = current_date + timedelta(days=1)
						ottime = 0
						check_in_time = None
						check_out_time = None

						checkin_li = frappe.get_all("Employee Checkin", 
													{"employee": i.empid, 
													"time": ["between", [current_date, current_date]], 
													"log_type": "IN"}, 
													["time", "log_type", "employee"], 
													order_by="time ASC", 
													limit=1)
						if checkin_li:
							for checkin in checkin_li:
								check_in_time = checkin["time"]
								ci = check_in_time.strftime('%H:%M:%S') # Exit loop after getting the first check-in time
								break  
						else:
							ci = 0
							
						# frappe.throw(str(end_day))
						# ci = check_in_time.strftime('%H:%M:%S') if check_in_time else '00:00:00'

						outcount = frappe.db.count("Employee Checkin",{"employee": i.empid, 
														"time": ["between", [current_date, end_day]], 
														"log_type": "OUT"})
						# frappe.msgprint(str(outcount))
						if outcount == 2:
							check_out = frappe.get_all("Employee Checkin", 
														{"employee": i.empid, 
														"time": ["between", [current_date, end_day]], 
														"log_type": "OUT"}, 
														["time", "log_type", "employee"], 
														order_by="time DESC", 
														limit=1)
							# frappe.msgprint("hi im if")
							if check_out:
								for checkout in check_out:
									check_out_time = checkout["time"]
									# frappe.throw(str(check_out_time))
									co = check_out_time.strftime('%H:%M:%S') if check_out_time else '00:00:00'
									if check_in_time and check_out_time and check_out_time >= check_in_time and check_in_time != '00:00:00':
										co = check_out_time.strftime('%H:%M:%S')
										check_out_time = checkout["time"]
										break
									else:
										co = 0  

						# elif outcount == 1:



						else:
							check_out_li = frappe.get_all("Employee Checkin", 
															{"employee": i.empid, 
															"time": ["between", [current_date, current_date]], 
															"log_type": "OUT"}, 
															["time", "log_type", "employee"], 
															order_by="time DESC", 
															limit=1)
							# frappe.msgprint("hi im else")
							if check_out_li:
								for checkout in check_out_li:
									check_out_time = checkout["time"]
									# frappe.throw(str(check_out_time))
									co = check_out_time.strftime('%H:%M:%S') if check_out_time else '00:00:00'
									if check_in_time and check_out_time and check_out_time >= check_in_time and check_in_time != '00:00:00':
										co = check_out_time.strftime('%H:%M:%S')
										check_out_time = checkout["time"]
										break 
									else:
										co  = 0
										break 
							else:
								check_out_lis = frappe.get_all("Employee Checkin", 
																{"employee": i.empid, 
																"time": ["between", [temp_date, temp_date]], 
																"log_type": "OUT"}, 
																["time", "log_type", "employee"], 
																order_by="time ASC", 
																limit=1)

								if check_out_lis :
									for checkout in check_out_lis:
										check_out_time = checkout["time"]
										if check_in_time and check_out_time and check_out_time >= check_in_time and check_in_time != '00:00:00':
											co = check_out_time.strftime('%H:%M:%S')
											check_out_time = checkout["time"]
											break  
										else:
											co  = 0
											break 
								else:
									# frappe.msgprint("hii no checkout")
									co = 0

						check_in_out = [ci, co]
						
						# Night shift hours
						night_shift_start = datetime.strptime("00:00:00", "%H:%M:%S")
						night_shift_end = datetime.strptime("23:59:59", "%H:%M:%S")

						# Calculate hours worked on the first day
						if check_in_time and check_out_time:
							if check_in_time.time() < night_shift_start.time():
								hours_worked_first_day = (night_shift_end - night_shift_start).seconds / 3600
							else:
								hours_worked_first_day = (night_shift_end - check_in_time).seconds / 3600

							# Calculate hours worked on the second day
							if check_out_time and check_out_time.time() >= night_shift_start.time():
								hours_worked_second_day = (check_out_time - night_shift_start).seconds / 3600
							else:
								hours_worked_second_day = 0
							
						if ci and co : # Total working hours
							total_working_hours = hours_worked_first_day + hours_worked_second_day

						# Extracting hours, minutes, and seconds from the total_working_hours
							hours = int(total_working_hours)
							minutes = int((total_working_hours * 60) % 60)
							seconds = int((total_working_hours * 3600) % 60)

						# 
						# Format the hours, minutes, and seconds into a string
							total_working_hours_formatted = "{:02d}:{:02d}:{:02d}".format(hours % 24, minutes, seconds)
							hours, minutes, seconds = map(int, total_working_hours_formatted.split(':'))
							total_working_hours_timedelta = timedelta(hours=hours, minutes=minutes, seconds=seconds)
						
						
						if out_duty is not None:
							out_duty = float(out_duty)
							
							
						else:
							out_duty = 0
						
						outd = timedelta(hours=out_duty)
						eight_hours = timedelta(hours=8)
						#with breaktime minus
						# total_hr = (check_out_time - check_in_time) - breakmin - outd
						# without break time minus
						if check_out_time and check_in_time:
							total_hr = total_working_hours_timedelta - outd
						else:
							total_hr = 0

						if total_hr:
							overtime_timedelta = total_hr - eight_hours
							totalpresent = round(total_hr.total_seconds() / 3600, 2)
							ottime = round(overtime_timedelta.total_seconds() / 3600, 2)
							otamount = ottime * (dayrate * (1.5 / 8)) if ottime > 0.5 else 0

						
						norhr_amount = 0
						if total_hr and check_in_time and check_out_time:
							if timedelta(hours=8) <= total_hr <= timedelta(hours=8, minutes=30):
								norhr_amount = 8 * (dayrate / 8)
							else:
								norhr_amount = dayrate if ottime > 0.50 else totalpresent * (dayrate / 8)

						self.append("eodetails", {
							"otdate": current_date.date(),
							"otid": i.empid,
							"otname": i.empname,
							"shift": empshift if empshift else None,
							"checkin": ci,
							"checkout":co,
							"normal_hr": 8,
							"out_duty": outd if out_duty else 0,
							"break_time": 0,
							"present_hrs":total_working_hours_formatted if ci  and co else 0,
							"total_hr": total_hr if ci and co else 0,
							"nrate": (dayrate / 8) if dayrate else 0,
							"norhr_amount": norhr_amount,
							"ot_hrs": ottime if ottime > 0.50 else 0,
							"ot_rate": dayrate * (1.5 / 8),
							"otamount": otamount,
							"salary_advance": sal_advance if sal_advance else 0,
							"net_payble":(norhr_amount + otamount) - (sal_advance or 0),
							})
					

					elif(shift_data=="Third"):
						temp_date = current_date + timedelta(days=1)
						check_in_time = None
						check_out_time = None
						ci = 0
						co = 0
						ottime = 0

						check_in_out_list = frappe.get_all("Employee Checkin", 
												{"employee": i.empid, 
												"time": ["between", [current_date, current_date ]],}, 
												["time", "log_type", "employee"], 
												order_by="time ASC", 
												)
						if check_in_out_list:
							flag1 = False
							for j in check_in_out_list:
								if j.log_type == "OUT":
									flag1 = True
								if flag1 and j.log_type =="IN":
									check_in_time = j["time"]
									# frappe.throw(str(check_in_time))
									ci = check_in_time.strftime('%H:%M:%S') if check_in_time else 0

							check_in_out_list2 = frappe.get_all("Employee Checkin", 
												{"employee": i.empid, 
												"time": ["between", [temp_date, temp_date]], 
												}, 
												["time", "log_type", "employee"], 
												order_by="time ASC", 
												)
								
								# frappe.throw(str(check_in_out_list2))
							if check_in_out_list2:
								flag2 = True
								flag3 = True
								for k in check_in_out_list2: 
									if ci == 0:
										if k.log_type == "IN" and flag2:
											flag2 = False
											check_in_time = k["time"]
											# frappe.throw(str(check_in_time))
											ci = check_in_time.strftime('%H:%M:%S') if check_in_time else 0					
									if k.log_type == "OUT" and flag3:
										check_out_time = k["time"]
										co = check_out_time.strftime('%H:%M:%S') if check_out_time else 0	

							# frappe.throw(str(checkin)+"===="+str(checkout))
						night_shift_start = datetime.strptime("00:00:00", "%H:%M:%S")
						night_shift_end = datetime.strptime("23:59:59", "%H:%M:%S")

						# Calculate hours worked on the first day
						if check_in_time and check_out_time:
							
							if check_in_time.time() < night_shift_start.time():
								hours_worked_first_day = (night_shift_end - night_shift_start).seconds / 3600
							else:
								hours_worked_first_day = (night_shift_end - check_in_time).seconds / 3600

							# Calculate hours worked on the second day
							if check_out_time and check_out_time.time() >= night_shift_start.time():
								hours_worked_second_day = (check_out_time - night_shift_start).seconds / 3600
							else:
								hours_worked_second_day = 0
							
						if ci and co : 
							# frappe.throw(str(hours_worked_first_day)+"======="+str(hours_worked_second_day))# Total working hours
							total_working_hours = hours_worked_first_day + hours_worked_second_day
							# frappe.throw(str(total_working_hours))
						# Extracting hours, minutes, and seconds from the total_working_hours
							hours = int(total_working_hours)
							minutes = int((total_working_hours * 60) % 60)
							seconds = int((total_working_hours * 3600) % 60)

						# 
						# Format the hours, minutes, and seconds into a string
							total_working_hours_formatted = "{:02d}:{:02d}:{:02d}".format(hours % 24, minutes, seconds)
							hours, minutes, seconds = map(int, total_working_hours_formatted.split(':'))
							total_working_hours_timedelta = timedelta(hours=hours, minutes=minutes, seconds=seconds)
						
							# frappe.msgprint(str(total_working_hours_formatted))
						if out_duty is not None:
							out_duty = float(out_duty)
							
							
						else:
							out_duty = 0
						
						outd = timedelta(hours=out_duty)
						eight_hours = timedelta(hours=8)
						# #with breaktime minus
						# # total_hr = (check_out_time - check_in_time) - breakmin - outd
						# # without break time minus
						if check_out_time and check_in_time:
							total_hr = total_working_hours_timedelta - outd
						else:
							total_hr = 0
						# frappe.throw(total_hr)
						if total_hr:
							overtime_timedelta = total_hr - eight_hours
							totalpresent = round(total_hr.total_seconds() / 3600, 2)
							ottime = round(overtime_timedelta.total_seconds() / 3600, 2)
							otamount = ottime * (dayrate * (1.5 / 8)) if ottime > 0.5 else 0

						
						norhr_amount = 0
						if total_hr and check_in_time and check_out_time:
							if timedelta(hours=8) <= total_hr <= timedelta(hours=8, minutes=30):
								norhr_amount = 8 * (dayrate / 8)
							else:
								norhr_amount = dayrate if ottime > 0.50 else totalpresent * (dayrate / 8)

						# frappe.throw(str(total_working_hours_formatted)+"=======&"+str(total_hr))
						self.append("eodetails", {
							"otdate": current_date.date(),
							"otid": i.empid,
							"otname": i.empname,
							"shift": empshift if empshift else None,
							"checkout":co if co  else 0,
							"checkin": ci if ci else 0,	
							"normal_hr": 8,
							"out_duty": outd if out_duty else 0,
							"break_time": 0,
							"present_hrs":total_working_hours_formatted if ci  and co else 0,
							"total_hr": total_hr if ci and co else 0,
							"nrate": (dayrate / 8) if dayrate else 0,
							"norhr_amount": norhr_amount,
							"ot_hrs":ottime if ottime > 0.50 else 0,
							"ot_rate": dayrate * (1.5 / 8),
							"otamount": otamount,
							"salary_advance": sal_advance if sal_advance else 0,
							"net_payble":(norhr_amount + otamount) - (sal_advance or 0),
							})
						

	  
					else:
						# Below code for First Shift Which is Working general shift (9 to 5.45)
						start = datetime(current_date.year, current_date.month, current_date.day, 0, 0, 1)
						
						emp_check_in_out = frappe.db.sql("""
									SELECT 
										COALESCE(ci.employee, co.employee) AS employee,
										COALESCE(ci.employee_name, co.employee_name) AS employee_name,
										COALESCE(ci.Indate, co.out_date) AS date,
										ci.Intime AS check_in_time,
										ci.shift,
										co.out_time AS check_out_time
									FROM
										(SELECT 
											employee,
											employee_name,
											shift,
											CASE WHEN log_type = 'IN' THEN DATE(time) ELSE 0 END AS Indate, 
											MIN(CASE WHEN log_type = 'IN' THEN TIME(time) ELSE 0 END) AS Intime
										FROM 
											`tabEmployee Checkin` 
										WHERE 
											log_type = 'IN' AND 
											employee = %s AND 
											DATE(time) = %s
										GROUP BY 
											DATE(time), employee, employee_name) AS ci
									LEFT JOIN
										(SELECT 
											employee,
											employee_name,
											CASE WHEN log_type = 'OUT' THEN DATE(time) ELSE 0 END AS out_date, 
											MAX(CASE WHEN log_type = 'OUT' THEN TIME(time) ELSE 0 END) AS out_time
										FROM 
											`tabEmployee Checkin` 
										WHERE 
											log_type = 'OUT' AND 
											employee = %s AND 
											DATE(time) = %s
										GROUP BY 
											DATE(time), employee, employee_name) AS co
									ON ci.employee = co.employee AND ci.Indate = co.out_date
								""", (i.empid, start.strftime("%Y-%m-%d"), i.empid, start.strftime("%Y-%m-%d")),as_dict=True)
						
						# frappe.throw(str(emp_check_in_out))
						if emp_check_in_out:
							for i in emp_check_in_out:
								
								check_out_time = datetime.strptime(str(i.check_out_time) if i.check_out_time else '00:00:00', '%H:%M:%S.%f' if '.' in str(i.check_out_time) else '%H:%M:%S')
								check_in_time = datetime.strptime(str(i.check_in_time) if i.check_in_time else '00:00:00', '%H:%M:%S.%f' if '.' in str(i.check_in_time) else '%H:%M:%S')
								ci = check_in_time.strftime('%H:%M:%S') if check_in_time else 0
								co = check_out_time.strftime('%H:%M:%S') if check_out_time else 0

								if i.shift is None:
									dshift = frappe.get_value("Employee", {"name": i.employee}, "default_shift")
									if dshift is None:
										frappe.throw("Please Assign Shift For Selected Employee")
									else:
										shift = dshift
								else:
									shift = i.shift

								shift_details = frappe.get_doc("Shift Type", shift)

								breaktime = shift_details.custom_total_break_time
								lbreak = shift_details.custom_lunch_break
								tbreak = shift_details.custom_tea_break

								if breaktime is not None:
									breaktime = int(breaktime) 
									lbreak = int(lbreak)
									tbreak = int(tbreak)
								else:
									dshift_details = frappe.get_doc("Shift Type", dshift)
									dbreaktime = dshift_details.custom_total_break_time
									dlbreak = dshift_details.custom_lunch_break
									dtbreak = dshift_details.custom_tea_break
									breaktime = int(dbreaktime) if dbreaktime is not None else 0
									lbreak = int(dlbreak) if dlbreak is not None else 0
									tbreak = int(dtbreak) if dtbreak is not None else 0

								breakmin = timedelta(minutes=breaktime)
								lbreak = timedelta(minutes=lbreak)
								tbreak = timedelta(minutes=tbreak)

								# frappe.throw(str(tbreak))
								time_difference = check_out_time - check_in_time
								
								# frappe.throw(str(time_difference))
								if time_difference < timedelta(0):
									present_hrs = 0
								else:
									present_hrs = time_difference
			
								eight_hours = timedelta(hours=8)
								

								sal_advance = frappe.get_value("Employee Advance", {'employee': i.employee, 'posting_date': i.date}, "advance_amount")
								out_duty = frappe.get_value("On Duty Pass",{'employee_id': i.employee, 'date': i.date},"total_t")
								
								if out_duty is not None:
									out_duty = float(out_duty)
									
									
								else:
									out_duty = 0
								
								outd = timedelta(hours=out_duty)
								
								
								if check_out_time.time() <= datetime.strptime('12:00:00', '%H:%M:%S').time():
									total_hr = (check_out_time - check_in_time) - outd
									breakmin = 0 
								elif check_in_time.time() >= datetime.strptime('13:00:00', '%H:%M:%S').time() and check_out_time.time()  <= datetime.strptime('15:30:00', '%H:%M:%S').time():
									total_hr = (check_out_time - check_in_time) - outd
									breakmin = 0
								elif check_out_time.time()  <= datetime.strptime('15:30:00', '%H:%M:%S').time():
									total_hr = (check_out_time - check_in_time) - lbreak - outd
									breakmin = lbreak
								elif check_out_time.time() <= datetime.strptime('13:00:00', '%H:%M:%S').time():
									total_hr = (check_out_time - check_in_time) - lbreak - outd
									breakmin = lbreak
								elif check_in_time.time() >= datetime.strptime('13:00:00', '%H:%M:%S').time():
									total_hr = (check_out_time - check_in_time) - outd - tbreak 
									breakmin = tbreak
								else:
									total_hr = (check_out_time - check_in_time) - breakmin - outd
									breakmin = breakmin


								overtime_timedelta = total_hr - eight_hours
								totalpresent = round(total_hr.total_seconds() / 3600, 2)
								ottime = round(overtime_timedelta.total_seconds() / 3600, 2)
								otamount = ottime * (dayrate * (1.5 / 8)) if ottime > 0.5 else 0

								norhr_amount = 0
								if total_hr and i.check_in_time and i.check_out_time:
									if timedelta(hours=8) <= total_hr <= timedelta(hours=8, minutes=30):
										norhr_amount = 8 * (dayrate / 8)
									else:
										norhr_amount = dayrate if ottime > 0.50 else totalpresent * (dayrate / 8)
								# frappe.throw(str(check_in_time))
								self.append("eodetails", {
									"otdate": i.date,
									"otid": i.employee,
									"otname": i.employee_name,
									"shift": i.shift if i.shift else dshift,
									# "checkin": i.check_in_time if i.check_in_time else 0,
									# "checkout": i.check_out_time if i.check_out_time else 0,
									"checkin": ci,
									"checkout":co,
									"normal_hr": 8,
									"out_duty": out_duty if out_duty else 0,
									"break_time": breakmin if breakmin else 0,
									"present_hrs": present_hrs,
									"total_hr": total_hr if total_hr and i.check_in_time and i.check_out_time else 0,
									"nrate": (dayrate / 8),
									"norhr_amount": norhr_amount,
									"ot_hrs": ottime if ottime > 0.50 else None,
									"ot_rate": dayrate * (1.5 / 8),
									"otamount": otamount,
									"salary_advance": sal_advance or 0,
									"net_payble": (norhr_amount + otamount) - (sal_advance or 0),
								})

				current_date += timedelta(days=1)



	@frappe.whitelist()
	def get_employee_sum(self):
		employee_id_dict = {}

		for i in self.get('eodetails'):
			if i.otid not in employee_id_dict:
				employee_id_dict[i.otid] = {
					"totid": i.otid,
					"totname": i.otname,
					"ot_hrs": i.ot_hrs or 0,  # Replace None with 0
					"ot_rate": i.ot_rate,
					"otamount": i.otamount,
					"normal_rate": i.nrate,
					"normal_hrs": i.normal_hr,
					"normal_hrs_amount": i.norhr_amount,
					"salary_advance": i.salary_advance or 0,
					"net_payble": i.net_payble,
				}
			else:
				# Handle None values by replacing with 0 before addition
				employee_id_dict[i.otid]['ot_hrs'] += i.ot_hrs or 0
				employee_id_dict[i.otid]['salary_advance'] += i.salary_advance or 0
				employee_id_dict[i.otid]['net_payble'] += i.net_payble
				employee_id_dict[i.otid]['otamount'] += i.otamount

		for data in employee_id_dict:
			self.append('emptotal', {
				"totid": employee_id_dict[data]['totid'],
				"totname": employee_id_dict[data]['totname'],
				"ot_hrs": employee_id_dict[data]['ot_hrs'],
				"ot_rate": employee_id_dict[data]['ot_rate'],
				"otamount": employee_id_dict[data]['otamount'],
				"normal_hrs": employee_id_dict[data]['normal_hrs'],
				"normal_hrs_amount": employee_id_dict[data]['normal_hrs_amount'],
				"salary_advance": employee_id_dict[data]['salary_advance'],
				"net_payble": employee_id_dict[data]['net_payble'],
			})

	@frappe.whitelist()
	def download_file(self):
		# frappe.throw("hiii")
		data = frappe.get_all('Employee Overtime Details', 	
									filters={'parent': self.name}, 
									fields=["otdate", "otid","otname","shift","checkin","checkout","normal_hr","nrate","norhr_amount","ot_hrs","otamount","salary_advance","net_payble"])

		file_path = frappe.get_site_path('public', 'files', 'output.csv')
		with open(file_path, 'w', newline='') as csvfile:
			fieldnames = ["otdate", "otid","otname","shift","checkin","checkout","normal_hr","nrate","norhr_amount","ot_hrs","otamount","salary_advance","net_payble"]  # Replace with your actual field names
			writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
			writer.writeheader()
			for row in data:
				writer.writerow(row)
		return file_path	
	

	@frappe.whitelist()
	def download(self):
		# frappe.throw("hiii")
		data = frappe.get_all('Employee Total Overtime', 	
									filters={'parent': self.name}, 
									fields=["totid", "totname","ot_hrs","ot_rate","otamount","normal_hrs","normal_rate","normal_hrs_amount","salary_advance","net_payble"])

		file_path = frappe.get_site_path('public', 'files', 'output.csv')
		with open(file_path, 'w', newline='') as csvfile:
			fieldnames = ["totid", "totname","ot_hrs","ot_rate","otamount","normal_hrs","normal_rate","normal_hrs_amount","salary_advance","net_payble"]  # Replace with your actual field names
			writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
			writer.writeheader()
			for row in data:
				writer.writerow(row)
		return file_path