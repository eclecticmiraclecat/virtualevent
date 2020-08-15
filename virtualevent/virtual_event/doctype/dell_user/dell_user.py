# -*- coding: utf-8 -*-
# Copyright (c) 2020, ERP-X and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe.utils import random_string

class DellUser(Document):
	pass


import json
import random

@frappe.whitelist(allow_guest=True)
def member_registration():
    data = json.loads(frappe.request.data)

    print('data'*10, data)

    dell_user = frappe.get_doc({
        'doctype': 'Dell User',
        'email': data['email'],
        'first_name': data['first_name'],
        'last_name': data['last_name'],
        'user_type': data['user_type']
    })
    dell_user.insert(ignore_permissions=True)

    user = frappe.get_doc({
        "doctype": "User",
        "email": data['email'],
        "enabled": 1,
        "username": data['first_name'],
        "first_name": data['first_name'],
        "user_type": "System User",
    })
    user.new_password = hi = random_string(10)
    print('passwd'*10, user.new_password)
    print('passwd'*10, hi)
    user.flags.no_welcome_mail = True
    user.flags.ignore_permissions = True
    user.insert(ignore_permissions=True)
    user.add_roles("Dell User")

    frappe.sendmail(
        recipients=data['email'],
        subject='Your NAMLIFA account is approved',
        template='welcome',
        args={
            'msg': 'Your NAMLIFA application has been approved. Thank you for your support.',
            'full_name': data['first_name'],
            'password': hi,
            'email': data['email']
        }
    )



    return {'user inserted'}


@frappe.whitelist()
def member_login():
    #return frappe.session.user
    return frappe.session

@frappe.whitelist(allow_guest=True)
def dell_employee_login():
    data = json.loads(frappe.request.data)

    dell_user_email = frappe.db.get_value("Dell User", filters={"email": data["email"]})

    if dell_user_email:
        user = frappe.get_doc('User', data['email'])
        user.new_password = otp = ''.join(random.sample('0123456789', 5))
        user.save(ignore_permissions=True)

        frappe.sendmail(
            recipients=data['email'],
            subject='Your DELL Employee OTP',
            template='otp',
            args={
                'msg': 'Your OTP',
                'full_name': data['first_name'],
                'OTP': otp,
            }
        )

        return 'otp sent'
    else:
        return f"Unable to find email {data['email']}"



@frappe.whitelist(allow_guest=True)
def partner_login():
    data = json.loads(frappe.request.data)

    user = frappe.db.get_value("User", filters={"email": data["email"]})

    if data['email'].split('@')[1] in {'dell.com', 'vmware.com', 'rsa.com', 'yahoo.com'}:
        return {'invalid email domain'}

    if user:
        print('hello'*20)
        user = frappe.get_doc('User', data['email'])
        user.new_password = otp = ''.join(random.sample('0123456789', 5))
        user.save(ignore_permissions=True)

        frappe.sendmail(
            recipients=data['email'],
            subject='Your Partner OTP',
            template='otp',
            args={
                'msg': 'Your OTP',
                'full_name': data['email'],
                'OTP': otp,
            }
        )
    else:
        print('hi'*20)
        user = frappe.get_doc({
            "doctype": "User",
            "email": data['email'],
            "first_name": data['email'],
            "enabled": 1,
            "user_type": "System User",
        })
        user.new_password = otp = ''.join(random.sample('0123456789', 5))
        user.flags.no_welcome_mail = True
        user.flags.ignore_permissions = True
        user.insert(ignore_permissions=True)

        user.add_roles("Dell User")

        dell_user = frappe.get_doc({
            'doctype': 'Dell User',
            'email': data['email'],
            'first_name': data['first_name'],
            'last_name': data['last_name'],
            'user_type': 'Partner'
        })
        dell_user.insert(ignore_permissions=True)


        frappe.sendmail(
            recipients=data['email'],
            subject='Your Partner Account Created',
            template='welcome',
            args={
                'msg': 'Your Partner Account Created',
                'full_name': data['first_name'],
                'OTP': otp,
            }
        )

        return {'user inserted'}



@frappe.whitelist(allow_guest=True)
def dell_employee_signup():
    data = json.loads(frappe.request.data)

    if data['email'].split('@')[1] not in {'dell.com', 'vmware.com', 'rsa.com', 'yahoo.com'}:
        return {'invalid email domain'}

    user = frappe.get_doc({
        "doctype": "User",
        "email": data['email'],
        "enabled": 1,
        "username": data['first_name'],
        "first_name": data['first_name'],
        "user_type": "System User",
    })
    user.new_password = otp = ''.join(random.sample('0123456789', 5))
    user.flags.no_welcome_mail = True
    user.flags.ignore_permissions = True
    try:
        user.insert(ignore_permissions=True)
    except frappe.exceptions.DuplicateEntryError:
        return {'user already been created'}
    user.add_roles("Dell User")


    dell_user = frappe.get_doc({
        'doctype': 'Dell User',
        'email': data['email'],
        'badge_id': data['badge_id'],
        'first_name': data['first_name'],
        'last_name': data['last_name'],
        'user_type': 'Employee'
    })
    dell_user.insert(ignore_permissions=True)


    frappe.sendmail(
        recipients=data['email'],
        subject='Your DELL Employee Account Created',
        template='welcome',
        args={
            'msg': 'Your DELL Employee Account Created',
            'full_name': data['first_name'],
            'OTP': otp,
        }
    )

    return {'user inserted'}

