import frappe
import json
import random
from frappe import _
from frappe.utils import nowdate, add_days, now_datetime, validate_email_address


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

    if frappe.session['user'] != 'Guest':
        pass

    user = frappe.db.get_value("User", filters={"email": data["email"]})
    dell_user = frappe.db.get_value("Dell User", filters={"email": data["email"]})

    check_badge_id = frappe.db.sql("""select name, user_type, badge_id, first_name, last_name, email from `tabDell User` where `badge_id`=%(badge_id)s and first_login='1'""",{'badge_id': data['badge_id']})

    check_pre_badge_id = frappe.db.sql("""select name, user_type, badge_id, first_name, last_name, email from `tabDell User` where `badge_id`=%(badge_id)s and sign_up_type='Pre-Registered'""",{'badge_id': data['badge_id']})


    if user:
        dell_user = frappe.get_doc('Dell User', dell_user)

        if dell_user.sign_up_type == 'Pre Registered':
            return {'Please login with badge id'}

        if dell_user.sign_up_type == 'Onsite Registered' and dell_user.first_login == '1':
            return {'Please login with badge id'}

        if check_badge_id or check_pre_badge_id:
            return {'badge id has been already registered'}

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
        dell_user.first_name = data['first_name']
        dell_user.last_name = data['last_name']
        dell_user.badge_id = data['badge_id']
        dell_user.sing_up_date = now_datetime()
        dell_user.save(ignore_permissions=True)
    else:
        user = frappe.get_doc({
            "doctype": "User",
            "email": data['email'],
            "enabled": 1,
            "username": data['first_name'],
            "first_name": data['first_name'],
            "last_name": data['last_name'],
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

    return {'mail sent'}


#@frappe.whitelist()
#def first_login():
#    #print('x'*50, frappe.session.user)
#    user = frappe.get_doc('User', frappe.session.user)
#    dell_user = frappe.db.get_value("Dell User", filters={"email": user.email})
#    dell_user = frappe.get_doc('Dell User', dell_user)
#    user.new_password = dell_user.badge_id
#    user.save(ignore_permissions=True)


@frappe.whitelist(allow_guest=True)
def partner_login():

    data = json.loads(frappe.request.data)

    if not validate_email_address(data["email"]):
        return {'invalid email address'}


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


@frappe.whitelist()
def track_activity():
    data = json.loads(frappe.request.data)

    room = data['room']


#    print(frappe.cache().get_value('blue'))
    frappe.cache().get_value('room').append(room)


#    print('data'*10, frappe.session)
#    print('data'*10, frappe.session['data'])

#    if 'room' not in frappe.session['data']:
#        frappe.session['data'].update({'room':[]})

#    print('old'*10, frappe.session['data']['room'])

#    frappe.session['data']['room'].append(room)

#    print('new'*10, frappe.session['data']['room'])

    user = frappe.get_doc('User', frappe.session.user)
    dell_user = frappe.db.get_value("Dell User", filters={"email": user.email})

#    if len(frappe.session['data']['room']) > 1:
#        prev, current = frappe.session['data']['room'][-2:]

    # add checkout time
    if len(frappe.cache().get_value('room')) > 1:
        prev, current = frappe.session['data']['room'][-2:]
        get_doc = frappe.db.get_value(prev, filters={'user_id': dell_user})

        doc = frappe.get_doc(prev, get_doc)
        doc.check_out = now_datetime()

        print(doc.check_out)
        print(doc.check_in)

        #doc.duration = doc.check_out - doc.check_in
        doc.save(ignore_permissions=True)

    act = frappe.get_doc({
            "doctype": "Dell User Act Main Entry",
            "user_id": dell_user,
            "check_in": now_datetime(),
            "activity": 'Click'
    })
    act.insert(ignore_permissions=True)

@frappe.whitelist(allow_guest=True)
def validate_params():
    data = json.loads(frappe.request.data)

    email = data['email']
    #badge_id = data['badge_id']
    pwd = data.get('pwd')
    otp = data.get('otp')

    #check_badge_id = frappe.db.sql("""select name, user_type, badge_id, first_name, last_name, email from `tabDell User` where `badge_id`=%(badge_id)s and first_login='1'""",{'badge_id': badge_id]})

    #if check_badge_id:
    #    return {'badge id has been already registered'}

    user = frappe.db.get_value("User", filters={"email": data["email"]})

    if not user:
        return 'no email id'

    dell_user = frappe.db.get_value("Dell User", filters={"email": data["email"]})
    dell_user = frappe.get_doc('Dell User', dell_user)

    from frappe.utils.password import update_password, check_password, passlibctx

    #auth = frappe.db.sql(f"""select `name`, `password` from `__Auth` where `doctype`='User' and `name`={email}""", as_dict=True)
    auth = frappe.db.sql("""select `name`, `password` from `__Auth` where `doctype`='User' and `name`=%(email)s""",{'email': email}, as_dict=True)

    if otp:
        if not passlibctx.verify(otp, auth[0].password):
            return {'wrong otp'}
        return [{'first name': dell_user.first_name, 'email': dell_user.email}]

    if pwd:
        if not passlibctx.verify(pwd, auth[0].password):
            return {'wrong password'}
        return [{'first name': dell_user.first_name, 'email': dell_user.email}]


@frappe.whitelist()
def whoami():
    
    #return frappe.local.response
    print(frappe.local.response)
    return frappe.session.user


@frappe.whitelist()
def setup_log():

    frappe.cache().set_value('room', ['Dell User Act Main Entry'])

    #frappe.cache().get_value('room').append('blue')

    user = frappe.get_doc('User', frappe.session.user)
    dell_user = frappe.db.get_value("Dell User", filters={"email": user.email})
    dell_log = frappe.db.get_value("Dell User Journey Log", filters={"user_id": dell_user})

    #if dell_user:
    #    act = frappe.get_doc("Dell User Journey Log", dell_user)
    #    act.append("log_detail", {"check_in": now_datetime(), "activity": 'Login', "d_room": "R-016"})
    #    act.save()

    #else:
    #    act = frappe.get_doc({
    #            "doctype": "Dell User Journey Log",
    #            "user_id": dell_user,
    #            "log_detail": [{"check_in": now_datetime(), "activity": 'Login', "d_room": "R-016"}],
    #    })
    #    act.insert(ignore_permissions=True)

        
    if dell_user:
        dell_user = frappe.get_doc('Dell User', dell_user)
        if dell_user.sign_up_type == 'Onsite Registered' and dell_user.first_login == '0':
            print('syncing'*20)
            dell_user.first_login = 1
            user.new_password = dell_user.badge_id
            user.save(ignore_permissions=True)
            dell_user.save(ignore_permissions=True)
        

@frappe.whitelist(allow_guest=True)
def user_info():

    data = json.loads(frappe.request.data)

    #user = frappe.get_doc('User', frappe.session.user)
    #dell_user = frappe.db.get_value("Dell User", filters={"email": user.email})

    dell_user = frappe.db.get_value("Dell User", filters={"email": data['email']})

    return frappe.db.sql("""select name, user_type, badge_id, first_name, last_name, email from `tabDell User` where `name`=%(name)s""",{'name': dell_user}, as_dict=True)


@frappe.whitelist()
def schedule_meeting():

    print(frappe.session.user)

    user = frappe.get_doc('User', frappe.session.user)
    dell_user = frappe.db.get_value("Dell User", filters={"email": user.email})
    #dell_user = frappe.get_doc('Dell User', dell_user)

    print(dell_user)

    data = json.loads(frappe.request.data)

    print(data)

    check_meeting = frappe.db.sql("""select * from `tabEvent` where `booth_id`=%(booth_id)s and `starts_on`<=%(starts_on)s and `ends_on`>=%(ends_on)s""",{'booth_id': data['booth_id'], 'starts_on': data['starts_on'], 'ends_on': data['ends_on']})


    print(check_meeting)

    if check_meeting:
        return {'meeting already exists'}
    else:
        meeting = frappe.get_doc({
            "doctype": "Event",
            "subject": data['subject'],
            "starts_on": data['starts_on'],
            "ends_on": data['ends_on'],
            "booth_id": data['booth_id'],
            "even_parts": [{"user_id": dell_user}],
        })
        meeting.insert(ignore_permissions=True)

        return {'meeting been created'}
