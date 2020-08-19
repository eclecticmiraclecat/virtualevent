import frappe
import json
import random
from frappe import _
from frappe.utils import nowdate, add_days, now_datetime


@frappe.whitelist()
def get_schedules(start, end):
        #if not frappe.has_permission("Meeting", "read"):
        #        raise frappe.PermissionError

        return frappe.db.sql("""select
                timestamp(`date`, from_time) as start,
                timestamp(`date`, to_time) as end,
                naming_series,
                title,
                0 as all_day
        from `tabDell Meeting Schedule`
        where `date` between %(start)s and %(end)s""", {
                "start": start,
                "end": end
        }, as_dict=True)



@frappe.whitelist(allow_guest=True)
def dell_employee_signup():
    data = json.loads(frappe.request.data)

    #if data['email'].split('@')[1] not in {'dell.com', 'vmware.com', 'rsa.com', 'yahoo.com', 'framemotion.net', 'gmail.com'}:
    #    return {'invalid email domain'}


    dell_user_badge_id = frappe.db.get_value("Dell User", filters={"badge_id": data["badge_id"]})

    if dell_user_badge_id:
        return {'badge id already exists'}

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
        'sign_up_type': 'Onsite Registered',
        'sing_up_date': now_datetime(),
        'user_type': 'Employee'
    })
    dell_user.insert(ignore_permissions=True)


    frappe.sendmail(
        recipients=data['email'],
        subject='Registration OTP - Dell Quality Connect:Virtual 2020',
        template='welcome',
        args={
            'msg': f'Thank you for registering for Quality Connect:Virtual 2020. Your authorization OTP is {otp}',
        }
    )

    return {'user inserted'}


@frappe.whitelist()
def first_login():
    #print('x'*50, frappe.session.user)
    user = frappe.get_doc('User', frappe.session.user)
    dell_user = frappe.db.get_value("Dell User", filters={"email": user.email})
    dell_user = frappe.get_doc('Dell User', dell_user)
    user.new_password = dell_user.badge_id
    user.save(ignore_permissions=True)


@frappe.whitelist(allow_guest=True)
def partner_login():
    data = json.loads(frappe.request.data)

    user = frappe.db.get_value("User", filters={"email": data["email"]})

#    if data['email'].split('@')[1] in {'dell.com', 'vmware.com', 'rsa.com', 'yahoo.com'}:
#        return {'invalid email domain'}

    if user:
        user = frappe.get_doc('User', data['email'])
        user.new_password = otp = ''.join(random.sample('0123456789', 5))
        user.save(ignore_permissions=True)
        frappe.sendmail(
            recipients=data['email'],
            subject='Registration OTP - Dell Quality Connect:Virtual 2020',
            template='welcome',
            args={
                'msg': f'Thank you for registering for Quality Connect:Virtual 2020. Your authorization OTP is {otp}',
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
            'first_name': data['email'],
            'user_type': 'Partner',
            'sing_up_date': now_datetime(),
        })
        dell_user.insert(ignore_permissions=True)

        frappe.sendmail(
            recipients=data['email'],
            subject='Registration OTP - Dell Quality Connect:Virtual 2020',
            template='welcome',
            args={
                'msg': f'Thank you for registering for Quality Connect:Virtual 2020. Your authorization OTP is {otp}',
            }
        )

        return {'user inserted'}

