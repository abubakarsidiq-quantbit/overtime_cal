# Copyright (c) 2023, Frappe Technologies Pvt. Ltd. and contributors
# Copyright (c) 2023, by Abhishek Chougule developer.mrabhi@gmail.com
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from datetime import datetime as dt,timedelta


class Overtime(Document):
    
    @frappe.whitelist()
    def getemplist(self):
        self.allow_import=1
        doc = frappe.db.get_list("Employee", fields=["name","employee_name","isotallow"])
        for d in doc:
            if d.isotallow==1:
                self.append("emp",
                {
                    "empid": d.name,
                    "empname": d.employee_name,
                },
                            )
                  
    @frappe.whitelist()
    def getempot(self): 
        doc = frappe.db.get_list("Employee Checkin", fields=["time","employee","employee_name","overtime"])
        sal = frappe.db.get_list("Salary Structure Assignment", fields=["employee","base"])
        company=frappe.db.get_list("Overtime Settings", fields=["minreqot","workinghours","overtimerate"])
        overtimerate=""
        overtimesal=""
        workinghours=""
        if str(self.fromdate)!='None':
            for d in doc:
                for row in self.get("emp"):
                        if row.empcheckbox and row.empid==d.employee and (dt.strptime(str(self.fromdate), "%Y-%m-%d") <= dt.strptime(str(d.time)[:10], "%Y-%m-%d")) and (dt.strptime(str(self.todate), "%Y-%m-%d") >= dt.strptime(str(d.time)[:10], "%Y-%m-%d")):
                            count=0
                            if str(d.overtime)!='None' and str(d.overtime)[0]!='-' and str(d.overtime)!='0':
                                for s in company:
                                    self.minreqot=str(s.minreqot)
                                    overtimerate=str(s.overtimerate)
                                    workinghours=str(s.workinghours)
                                    
                                if (dt.strptime(d.overtime, "%H:%M:%S") >= dt.strptime(str(self.minreqot), "%H:%M:%S")):
                                                                                                
                                        for m in self.get('ot'):
                                            temp2=str(m.otdate)[:10]
                                            temp3=str(d.time)[:10]
                                            if dt.strptime(str(temp2), "%Y-%m-%d") == dt.strptime(str(temp3), "%Y-%m-%d")  and m.otid==d.employee:
                                                m.otovertime='0:00:00'        
                                               
                                        self.append("ot",{"otdate":d.time,"otid": d.employee,"otname": d.employee_name,"otovertime":d.overtime},)
                
                                
        else:
            frappe.msgprint('Please Select From Date to proceed !')
        
        time_by_name = {}
       
        for row in self.ot:
            
            if row.otid in time_by_name:
                total_time=dt.strptime(time_by_name[row.otid], '%H:%M:%S')+timedelta(hours=dt.strptime(row.otovertime, '%H:%M:%S').hour,minutes=dt.strptime(row.otovertime, '%H:%M:%S').minute,seconds=dt.strptime(row.otovertime, '%H:%M:%S').second)
                time_by_name[row.otid] = total_time.strftime('%H:%M:%S')
              
                
            else:
                time_by_name[row.otid] = dt.strptime(row.otovertime, '%H:%M:%S').strftime('%H:%M:%S')
               

        self.tot = []

        for otid, otovertime in time_by_name.items():
            for nm in self.get('ot'):
                if otid==nm.otid:
                    otname=nm.otname
            for salary in sal:     
                    if otid==salary.employee:
                        h, m, s = workinghours.split(':')
                        whours=(int(h) * 3600 + int(m) * 60 + int(s))/3600
                        h, m, s = otovertime.split(':')
                        othours=(int(h) * 3600 + int(m) * 60 + int(s))/3600
                        
                    
                        #number of days in month
                        for row in self.ot:
                            today = row.otdate
                            
                            month = today.month
                            year = today.year
                            workingdays=30
                            
                            if(month == 1 or month == 3 or month == 5 or month == 7 or month == 8 or month == 10 or month == 12):
                                workingdays=31
                            elif((month == 2) and ((year%400==0) or (year%4==0 and year%100!=0))):	
                                workingdays=29
                            elif(month == 2):
                                workingdays=28
                            else:
                                workingdays=30
                            
                            #working days set to 1 for daily salary structure remove below line if want for monthly
                            workingdays=1
                            
                            overtimesal=(((salary.base/workingdays)/float(str(whours)))*float(str(overtimerate)))*float(str(othours))
                            if row.otid==otid:
                                row = self.append('tot', {})
                                row.totid = otid
                                row.totname=otname
                                row.tottot = otovertime
                                row.totsalary=overtimesal
                                break
                        break
                        
                    else:
                        overtimesal=0
                    
            
            
    @frappe.whitelist()
    def selectall(self):
        children = self.get("emp")
        if not children:
            return
        for child in children:
            all_selected = all([child.empcheckbox for child in children])
            if not all_selected:
                value = 1   
            else:
                value = 0
            for child in children:
                child.empcheckbox = value
            
                  	