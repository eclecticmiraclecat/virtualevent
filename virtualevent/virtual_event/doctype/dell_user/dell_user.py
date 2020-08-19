# -*- coding: utf-8 -*-
# Copyright (c) 2020, ERP-X and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe.utils import random_string, nowdate, now_datetime

class DellUser(Document):

    def validate(self):
        if frappe.db.exists('User', self.email) is None and self.sign_up_type == 'Pre-Registered':
            user = frappe.get_doc({
                "doctype": "User",
                "email": self.email,
                "enabled": 1,
                "username": self.email,
                "first_name": self.first_name,
                "user_type": "System User",
            })
            user.new_password = self.badge_id
            user.flags.no_welcome_mail = True
            user.flags.ignore_permissions = True
            user.insert(ignore_permissions=True)
            user.add_roles("Dell User")
            


