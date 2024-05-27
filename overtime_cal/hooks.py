from . import __version__ as app_version

app_name = "overtime_cal"
app_title = "Overtime Cal"
app_publisher = "Abhishek Chougule"
app_description = "Overtime Calculation"
app_email = "chouguleabhis@gmail.com"
app_license = "Copyright @2023 - Abhishek Chougule chouguleabhis@gmail.com"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/overtime_cal/css/overtime_cal.css"
# app_include_js = "/assets/overtime_cal/js/overtime_cal.js"

# include js, css files in header of web template
# web_include_css = "/assets/overtime_cal/css/overtime_cal.css"
# web_include_js = "/assets/overtime_cal/js/overtime_cal.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "overtime_cal/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
#	"methods": "overtime_cal.utils.jinja_methods",
#	"filters": "overtime_cal.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "overtime_cal.install.before_install"
# after_install = "overtime_cal.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "overtime_cal.uninstall.before_uninstall"
# after_uninstall = "overtime_cal.uninstall.after_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "overtime_cal.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
#	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
#	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
#	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
#	"*": {
#		"on_update": "method",
#		"on_cancel": "method",
#		"on_trash": "method"
#	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
#	"all": [
#		"overtime_cal.tasks.all"
#	],
#	"daily": [
#		"overtime_cal.tasks.daily"
#	],
#	"hourly": [
#		"overtime_cal.tasks.hourly"
#	],
#	"weekly": [
#		"overtime_cal.tasks.weekly"
#	],
#	"monthly": [
#		"overtime_cal.tasks.monthly"
#	],
# }

# Testing
# -------

# before_tests = "overtime_cal.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
#	"frappe.desk.doctype.event.event.get_events": "overtime_cal.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
#	"Task": "overtime_cal.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]


# User Data Protection
# --------------------

# Copyright (c) 2023, Frappe Technologies Pvt. Ltd. and contributors
# Copyright (c) 2023, by Abhishek Chougule developer.mrabhi@gmail.com
# For license information, please see license.txt

# user_data_fields = [
#	{
#		"doctype": "{doctype_1}",
#		"filter_by": "{filter_by}",
#		"redact_fields": ["{field_1}", "{field_2}"],
#		"partial": 1,
#	},
#	{
#		"doctype": "{doctype_2}",
#		"filter_by": "{filter_by}",
#		"partial": 1,
#	},
#	{
#		"doctype": "{doctype_3}",
#		"strict": False,
#	},
#	{
#		"doctype": "{doctype_4}"
#	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
#	"overtime_cal.auth.validate"
# ]
