# Copyright (c) 2023, Abhishek Chougule and contributors
# For license information, please see license.txt
import requests
import zk
from datetime import datetime, timedelta
import re
import frappe
from frappe.model.document import Document

class BiometricSyncSetting(Document):
	def get_attendance_data(self,start_date,end_date,machine_ip,common_key):
		zk_instance = zk.base.ZK(machine_ip, port=4370, timeout=60, password=common_key)
		# try:
		# conn = zk_instance.connect()
		frappe.throw("HI")
	# 		if conn:
	# 			attendance_data = conn.get_attendance()
	# 			conn.disable_device()
	# 			# Get attendance data
	# 			pattern = r"<Attendance>: (\d+) : (\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) \((\d+), (\d+)\)"
	# 			attendance_records=[]
	# 			for record in attendance_data:
	# 				record_date = record.timestamp.date()
	# 				if(record_date.strftime('%Y-%m-%d')>=start_date and record_date.strftime('%Y-%m-%d')<=end_date):
	# 					attendance_string=record
	# 					match = re.match(pattern,str(attendance_string))
	# 					if match:
	# 						user_id = int(match.group(1))
	# 						timestamp = match.group(2)
	# 						in_value = int(match.group(3))
	# 						out_value = int(match.group(4))
	# 						if(user_id==1021 or user_id==1019):
	# 							attendance_records.append({"id":user_id,"timestamp":timestamp,"in_value":in_value,"out_value":out_value})
	# 			conn.enable_device()
	# 			return attendance_records
	# 	except Exception as e:
	# 		print(e)
	# 	finally:
	# 		if conn:
	# 			conn.disconnect()


	# def send_to_erpnext(self,erpnext_api_url,erpnext_api_key,attendance_data):
	# 	headers = {
	# 		'Authorization': erpnext_api_key,
	# 		'Content-Type': 'application/json',
	# 	}
	# 	for data in attendance_data:
	# 		print(data)
		
	# 	punch_type=""
	# 	for data in attendance_data:
	# 		if(int(data["out_value"])>0):
	# 			punch_type="OUT"
	# 		else:
	# 			punch_type="IN"
				
	# 		print(data["id"],punch_type)
	# 		payload = {}
	# 		url = f"{erpnext_api_url}/api/method/hrms.hr.doctype.employee_checkin.employee_checkin.add_log_based_on_employee_field?employee_field_value={str(data['id'])}&timestamp={data['timestamp']}&log_type={str(punch_type)}"
	# 		response = requests.request("POST", url, headers=headers, data=payload)
	# 		if response.status_code == 200:
	# 			print(f'Data synced for {data["id"]} successfully.')
	# 		else:
	# 			print(f'Error syncing data for{data["id"]}:{response.text}')


	@frappe.whitelist()
	def sync_data(self):
		# machine_ip='192.168.1.180'
		# start_date ='2023-11-21'
		# end_date ='2023-11-21'
		# common_key = '41410'

		# erpnext_api_url="https://demomilkunion.erpdata.in"
		# erpnext_api_key='token 933d5b377069335:e9615d8ae83d625'

		machine_ip=self.machine_ip_address
		start_date =self.from_date
		end_date =self.to_date
		common_key = self.machine_common_key

		erpnext_api_url=self.erpnext_api_url

		erpnext_api_key=f'token {self.api_key}:{self.api_secret_key}'


		# attendance_data=self.get_attendance_data(start_date,end_date,machine_ip,common_key)
		# self.send_to_erpnext(erpnext_api_url,erpnext_api_key,attendance_data)








# record_date = record.timestamp.date()
# if(record_date.strftime('%Y-%m-%d')>=start_date and record_date.strftime('%Y-%m-%d')<=end_date and record.uid==1019):
#     print(record_date.strftime('%Y-%m-%d'),record.uid)