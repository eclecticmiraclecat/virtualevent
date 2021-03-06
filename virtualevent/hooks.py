# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from . import __version__ as app_version

app_name = "virtualevent"
app_title = "VirtualEvent"
app_publisher = "ERP-X"
app_description = "VirtualEvent Portal"
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "dev.erpx@gmail.com"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/virtualevent/css/virtualevent.css"
# app_include_js = "/assets/virtualevent/js/virtualevent.js"

# include js, css files in header of web template
# web_include_css = "/assets/virtualevent/css/virtualevent.css"
# web_include_js = "/assets/virtualevent/js/virtualevent.js"

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

# Website user home page (by function)
# get_website_user_home_page = "virtualevent.utils.get_home_page"

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "virtualevent.install.before_install"
# after_install = "virtualevent.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "virtualevent.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }


# login

on_session_creation = [
        "virtualevent.api.setup_log",
]

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
#	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"virtualevent.tasks.all"
# 	],
# 	"daily": [
# 		"virtualevent.tasks.daily"
# 	],
# 	"hourly": [
# 		"virtualevent.tasks.hourly"
# 	],
# 	"weekly": [
# 		"virtualevent.tasks.weekly"
# 	]
# 	"monthly": [
# 		"virtualevent.tasks.monthly"
# 	]
# }

# Testing
# -------

# before_tests = "virtualevent.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "virtualevent.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "virtualevent.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

