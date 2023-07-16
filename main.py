import telepot
import time
from model.membership import Membership
from persiantools.jdatetime import JalaliDate
from dateutil.relativedelta import relativedelta
import datetime
import os
from pprint import pprint
import msg
import db.mysqlconnector as msc
import uuid
import menu
import db.founderHelper as fh
from telepot.loop import MessageLoop

last_update_ids = {}
# زمان حداکثر برای فعال بودن آخرین پیام دریافتی (به ثانیه)
MAX_IDLE_TIME = 600

mydb = msc.mysqlconnector()
idFromFile = None
# sirmrmco1
bot = telepot.Bot('409679224:AAHAWm_FaSNiuthByMxAESwqq4SFYR8CxZE')


# shiftkari
# bot = telepot.Bot('6012649808:AAGXWUsZJBtvWsFlYuvqg18tgIwo7ildPUs')


# admins = mydb.getAdmins()
# image = 'download/2c3809f7-8e48-4cbf-acb7-bc7b0c9d1cd4.jpg'
# pprint(admins)
# for admin in admins:
#     pprint(bot.sendPhoto(admin[0], open(image, 'rb')))
# date1 = JalaliDate(1402, 4, 18).to_gregorian()
# date2 = datetime.date.today()
# diffDay = relativedelta(date1, date2)
# print("{0} - {1} = {2} Day ".format(date1, date2, diffDay.days))
# todayDate=datetime.date.today()
# jd=str(JalaliDate.to_jalali(todayDate.year,todayDate.month,todayDate.day)).split('-')
# sjd= "{0}{1}{2}".format(jd[0],jd[1],jd[2])
# print(sjd)
# exit(0)

def handle_new_messages(user_id, userName, update):
    global last_update_ids
    # دریافت آخرین شناسه update_id برای کاربر
    # tempMember, last_update_time = last_update_ids.get(user_id, (Membership, 0))
    tempV = last_update_ids.get(user_id)
    tempMember = None if tempV is None else tempV[0]
    last_update_time = 0 if tempV is None else tempV[1]
    # If the user is not in the list, it will be loaded from the database, if it is not there, it will be created
    if tempMember is None:
        tempMember = mydb.load_member(user_id)
        if tempMember is None:
            tempMember = mydb.create_member(Membership(userName=userName, chatid=user_id))
            last_update_id = 0
    else:
        last_update_id = int(tempMember.lastMessage)
    # **********************************************************************************************************

    # محاسبه زمان گذشته از آخرین پیام دریافتی
    elapsed_time = time.time() - last_update_time
    # اگر زمان گذشته بیشتر از حداکثر زمان مجاز باشد، آخرین شناسه update_id برای کاربر حذف می شود
    # if elapsed_time > MAX_IDLE_TIME and last_update_time > 0:
    #     del last_update_ids[user_id]
    #     return
    # دریافت پیام های جدید
    # updates = bot.getUpdates(offset=last_update_id + 1, timeout=10)
    # message = None
    # for update in updates:
    #     print(update)
    message = None;
    if 'message' in update:
        print('tempMember.delf={}'.format(tempMember.delf))
        if tempMember.delf == 0:
            last_update_id = tempMember.lastMessage
        elif tempMember.delf == 1 or tempMember.delf == 3:
            last_update_id = tempMember.lastMessage
            tempMember.delf = 3
            mydb.member_update('del', 3, user_id)
            bot.sendMessage(user_id, msg.messageLib.oldDel.value,
                            reply_markup=menu.keyLib.kbCreateMenuReactive(memberId=user_id))
            return

        message = update['message']
        if 'text' in message and message['text'] == '/myinfo':
            titlePos = None
            if tempMember.membership_type == 1:
                titlePos = 'موسس'
            elif tempMember.membership_type == 2:
                titlePos = 'مسئول فنی'
            elif tempMember.membership_type == 3:
                titlePos = 'دانشجو'
            elif tempMember.membership_type == 4:
                titlePos = 'مدیر'
            else:
                titlePos = 'نا مشخص'
            bot.sendMessage(message['chat']['id'],
                            str(msg.messageLib.myInfo.value).format(titlePos))
            bot.sendMessage(message['chat']['id'],
                            str(msg.messageLib.labeName.value).format(tempMember.name, tempMember.last_name))
            bot.sendMessage(message['chat']['id'],
                            str(msg.messageLib.labelPhoneNumber.value).format(tempMember.phone_number))
            if tempMember.membership_type == 1:
                bot.sendMessage(message['chat']['id'], msg.messageLib.yourOperation.value,
                                reply_markup=menu.keyLib.kbCreateMenuFunder(chatId=message['chat']['id']))
            elif tempMember.membership_type == 2:
                bot.sendMessage(message['chat']['id'], msg.messageLib.yourOperation.value,
                                reply_markup=menu.keyLib.kbCreateMenuResponsible(chatId=message['chat']['id']))
            elif tempMember.membership_type == 3:
                bot.sendMessage(message['chat']['id'], msg.messageLib.yourOperation.value,
                                reply_markup=menu.keyLib.kbCreateMenuStudent(chatId=message['chat']['id']))
            elif tempMember.membership_type == 4:
                bot.sendMessage(message['chat']['id'], msg.messageLib.yourOperation.value,
                                reply_markup=menu.keyLib.kbCreateMenuManager(chatId=message['chat']['id']))
        elif 'text' in message and message['text'] == '/myoperation':
            fh.helperFunder.send_operation(tempMember=tempMember, bot=bot, chatid=message['chat']['id'])
        elif 'text' in message and tempMember.register_progress == 0 and message['text'] == '/start':
            bot.sendMessage(message['chat']['id'], str(msg.messageLib.helloClient.value).format(
                message['chat']['first_name']), reply_markup=menu.keyLib.kbWhoAreYou())
        elif 'text' in message and tempMember.register_progress != 0 and message[
            'text'] == '/start':
            titlePos = None
            if tempMember.membership_type == 1:
                titlePos = 'موسس'
            elif tempMember.membership_type == 2:
                titlePos = 'مسئول فنی'
            elif tempMember.membership_type == 3:
                titlePos = 'دانشجو'
            elif tempMember.membership_type == 4:
                titlePos = 'مدیر'
            try:
                bot.sendMessage(message['chat']['id'],
                                str(msg.messageLib.duplicateregistration.value).format(titlePos),
                                reply_markup=menu.keyLib.kbCreateDelKey(message['chat']['id']))
            except:
                bot.sendMessage('6274361322', '{0}:{1}'.format(message['chat']['id'], message['text']))
        elif tempMember.register_progress == 1:
            mydb.member_update_chatid('name', message['text'], message['chat']['id'])
            bot.sendMessage(message['chat']['id'],
                            str(msg.messageLib.enterLastName.value))
            mydb.member_update_chatid('registration_progress', 2, message['chat']['id'])
            tempMember.register_progress = 2
        elif tempMember.register_progress == 2:
            mydb.member_update_chatid('last_name', message['text'], message['chat']['id'])
            bot.sendMessage(message['chat']['id'],
                            str(msg.messageLib.enterPhoneNumber.value))
            mydb.member_update_chatid('registration_progress', 3, message['chat']['id'])
            tempMember.register_progress = 3
        elif tempMember.register_progress == 3:
            phone = message['text']
            if not fh.helperFunder.validate_IR_mobile_number(phone):
                bot.sendMessage(message['chat']['id'], msg.messageLib.errorPhoneNumber.value)
                return
            mydb.member_update_chatid('phone_number', message['text'], message['chat']['id'])
            tempMember.phone_number = message['text']
            if tempMember.membership_type == 1:
                bot.sendMessage(message['chat']['id'],
                                str(msg.messageLib.enterPharmacyName.value))
                mydb.member_update_chatid('registration_progress', 4, message['chat']['id'])
                tempMember.register_progress = 4
            elif tempMember.membership_type == 2 or tempMember.membership_type == 3:
                bot.sendMessage(message['chat']['id'],
                                str(msg.messageLib.enterNationCode.value))
                mydb.member_update_chatid('registration_progress', 4, message['chat']['id'])
                tempMember.register_progress = 4
            elif tempMember.membership_type == 4:
                bot.sendMessage(message['chat']['id'],
                                str(msg.messageLib.endRegisteration.value))
                admins = mydb.getAdmins()
                for admin in admins:
                    bot.sendMessage(admin[0],
                                    str(msg.messageLib.messAdminApproveAdmin.value))
                    bot.sendMessage(admin[0],
                                    str(msg.messageLib.labeName.value).format(tempMember.name,
                                                                              tempMember.last_name))
                    bot.sendMessage(admin[0],
                                    str(msg.messageLib.labelPhoneNumber.value).format(tempMember.phone_number))
                    bot.sendMessage(admin[0], msg.messageLib.messAdminApprove.value,
                                    reply_markup=menu.keyLib.kbCreateApproveKey(chat_id=message['chat']['id']))
                mydb.member_update_chatid('registration_progress', 10, message['chat']['id'])
                tempMember.register_progress = 10
                mydb.member_update_chatid('registration_progress', 10, message['chat']['id'])
                tempMember.register_progress = 10
        elif tempMember.register_progress == 4:
            if tempMember.membership_type == 1:
                mydb.founder_update('pharmacy_name', message['text'], message['chat']['id'])
                bot.sendMessage(message['chat']['id'],
                                str(msg.messageLib.enterPharmacyType.value),
                                reply_markup=menu.keyLib.kbTypePharmacy())
                mydb.member_update_chatid('registration_progress', 5, message['chat']['id'])
                tempMember.register_progress = 5
            elif tempMember.membership_type == 2:
                nationCode = message['text']
                if not fh.helperFunder.validate_IR_national_id(nationCode):
                    bot.sendMessage(message['chat']['id'],msg.messageLib.errrorNation.value)
                    return
                mydb.technicalManager_update('national_code', message['text'], message['chat']['id'])
                bot.sendMessage(message['chat']['id'],
                                str(msg.messageLib.enetrcodePharmaceutical.value))
                mydb.member_update_chatid('registration_progress', 5, message['chat']['id'])
                tempMember.register_progress = 5
            elif tempMember.membership_type == 3:
                nationCode = message['text']
                if not fh.helperFunder.validate_IR_national_id(nationCode):
                    bot.sendMessage(message['chat']['id'],msg.messageLib.errrorNation.value)
                    return
                mydb.student_update('national_code', message['text'], message['chat']['id'])
                bot.sendMessage(message['chat']['id'],
                                str(msg.messageLib.enterLicenseStartDate.value))
                mydb.member_update_chatid('registration_progress', 5, message['chat']['id'])
                tempMember.register_progress = 5
        elif tempMember.register_progress == 5:
            if tempMember.membership_type == 2:
                if 'photo' in message:
                    file_id = message['photo'][-1]['file_id']
                    file_path = bot.getFile(file_id)['file_path']
                    fileName, fileExtention = os.path.splitext(file_path)
                    ufid = uuid.uuid4()
                    image_path = 'download/{0}{1}'.format(ufid, fileExtention)
                    bot.download_file(file_id, image_path)
                    print()
                    mydb.technicalManager_update('membership_card_photo', '{0}{1}'.format(ufid, fileExtention),
                                                 message['chat']['id'])
                    bot.sendMessage(message['chat']['id'],
                                    str(msg.messageLib.endRegisteration.value))
                    admins = mydb.getAdmins()
                    for admin in admins:
                        bot.sendMessage(admin[0],
                                        str(msg.messageLib.messAdminApproveTechnical.value))
                        bot.sendMessage(admin[0],
                                        str(msg.messageLib.labeName.value).format(tempMember.name,
                                                                                  tempMember.last_name))
                        bot.sendMessage(admin[0],
                                        str(msg.messageLib.labelPhoneNumber.value).format(tempMember.phone_number))
                        bot.sendMessage(admin[0],
                                        str(msg.messageLib.labelNationCode.value).format(
                                            mydb.get_technical_property('national_code',
                                                                        message['chat']['id'])))
                        bot.sendMessage(admin[0],
                                        str(msg.messageLib.labelMembershipCardPhoto.value))
                        img = 'download/{}'.format(
                            mydb.get_technical_property('membership_card_photo', message['chat']['id']))
                        bot.sendPhoto(admin[0], open(img, 'rb'))
                        bot.sendMessage(admin[0], msg.messageLib.messAdminApprove.value,
                                        reply_markup=menu.keyLib.kbCreateApproveKey(chat_id=message['chat']['id']))
                    mydb.member_update_chatid('registration_progress', 10, message['chat']['id'])
                    tempMember.register_progress = 10
                else:
                    bot.sendMessage(message['chat']['id'],
                                    str(msg.messageLib.errorSendFile.value))
            elif tempMember.membership_type == 3:
                mydb.student_update('start_date', message['text'], message['chat']['id'])
                bot.sendMessage(message['chat']['id'],
                                str(msg.messageLib.enterLicenseEndDate.value))
                mydb.member_update_chatid('registration_progress', 6, message['chat']['id'])
                tempMember.register_progress = 6
        elif tempMember.register_progress == 6:
            if tempMember.membership_type == 1:
                mydb.founder_update('pharmacy_address', message['text'], message['chat']['id'])
                bot.sendMessage(message['chat']['id'],
                                str(msg.messageLib.enterPharmacyLicensePhoto.value))
                mydb.member_update_chatid('registration_progress', 7, message['chat']['id'])
                tempMember.register_progress = 7
            elif tempMember.membership_type == 3:
                mydb.student_update('end_date', message['text'], message['chat']['id'])
                bot.sendMessage(message['chat']['id'],
                                str(msg.messageLib.enterWorkoverPermitPhoto.value))
                mydb.member_update_chatid('registration_progress', 7, message['chat']['id'])
                tempMember.register_progress = 7
        elif tempMember.register_progress == 7:
            if tempMember.membership_type == 1:
                if 'photo' in message:
                    file_id = message['photo'][-1]['file_id']
                    file_path = bot.getFile(file_id)['file_path']
                    fileName, fileExtention = os.path.splitext(file_path)
                    ufid = uuid.uuid4()
                    image_path = 'download/{0}{1}'.format(ufid, fileExtention)
                    bot.download_file(file_id, image_path)
                    mydb.founder_update('license_photo', '{0}{1}'.format(ufid, fileExtention),
                                        message['chat']['id'])
                    bot.sendMessage(message['chat']['id'],
                                    str(msg.messageLib.endRegisteration.value))
                    admins = mydb.getAdmins()
                    for admin in admins:
                        bot.sendMessage(admin[0],
                                        str(msg.messageLib.messAdminApproveFunder.value))
                        bot.sendMessage(admin[0],
                                        str(msg.messageLib.labeName.value).format(tempMember.name,
                                                                                  tempMember.last_name))
                        bot.sendMessage(admin[0],
                                        str(msg.messageLib.labelPhoneNumber.value).format(tempMember.phone_number))
                        bot.sendMessage(admin[0],
                                        str(msg.messageLib.labelPharmacyName.value).format(
                                            mydb.get_funder_property('pharmacy_name',
                                                                     message['chat']['id'])))
                        bot.sendMessage(admin[0],
                                        str(msg.messageLib.labelPharmacyType.value).format(
                                            mydb.get_funder_property('pharmacy_type', message['chat']['id'])))
                        bot.sendMessage(admin[0],
                                        str(msg.messageLib.labelPharmacyAddress.value).format(
                                            mydb.get_funder_property('pharmacy_address',
                                                                     message['chat']['id'])))
                        bot.sendMessage(admin[0],
                                        str(msg.messageLib.labelPermitPhoto.value))
                        img = 'download/{}'.format(
                            mydb.get_funder_property('license_photo', message['chat']['id']))
                        bot.sendPhoto(admin[0], open(img, 'rb'))
                        bot.sendMessage(admin[0], msg.messageLib.messAdminApprove.value,
                                        reply_markup=menu.keyLib.kbCreateApproveKey(chat_id=message['chat']['id']))
                    mydb.member_update_chatid('registration_progress', 10, message['chat']['id'])
                    tempMember.register_progress = 10
                else:
                    bot.sendMessage(message['chat']['id'],
                                    str(msg.messageLib.errorSendFile.value))
            if tempMember.membership_type == 3:
                if 'photo' in message:
                    file_id = message['photo'][-1]['file_id']
                    file_path = bot.getFile(file_id)['file_path']
                    fileName, fileExtention = os.path.splitext(file_path)
                    ufid = uuid.uuid4()
                    image_path = 'download/{0}{1}'.format(ufid, fileExtention)
                    bot.download_file(file_id, image_path)
                    mydb.student_update('overtime_license_photo', '{0}{1}'.format(ufid, fileExtention),
                                        user_id)
                    mydb.member_update_chatid('registration_progress', 8, message['chat']['id'])
                    tempMember.register_progress = 8
                    bot.sendMessage(message['chat']['id'],
                                    str(msg.messageLib.enterSelfiPhoto.value))
                else:
                    bot.sendMessage(message['chat']['id'],
                                    str(msg.messageLib.errorSendFile.value))
        elif tempMember.register_progress == 8:
            if tempMember.membership_type == 3:
                if 'photo' in message:
                    file_id = message['photo'][-1]['file_id']
                    file_path = bot.getFile(file_id)['file_path']
                    fileName, fileExtention = os.path.splitext(file_path)
                    ufid = uuid.uuid4()
                    image_path = 'download/{0}{1}'.format(ufid, fileExtention)
                    bot.download_file(file_id, image_path)
                    mydb.student_update('personal_photo', '{0}{1}'.format(ufid, fileExtention),
                                        message['chat']['id'])
                    tempMember.register_progress = 9
                    bot.sendMessage(message['chat']['id'],
                                    str(msg.messageLib.enterPermitActivity.value),
                                    reply_markup=menu.keyLib.kbTypeShift())
                else:
                    bot.sendMessage(message['chat']['id'],
                                    str(msg.messageLib.errorSendFile.value))
        elif tempMember.register_progress == 10:
            if tempMember.membership_type == 4 and message['text'] == '/start':
                bot.sendMessage(message['chat']['id'],
                                str(msg.messageLib.helloAdmin.value).format(
                                    tempMember.name + ' ' + tempMember.last_name),
                                reply_markup=menu.keyLib.kbAdmin())
            elif tempMember.membership_type == 4:
                chatIdUser = mydb.get_member_property_Adminchatid(fieldName='chat_id', chatid=message['chat']['id'])
                if chatIdUser is not None:
                    mydb.member_update_chatid('desc', message['text'], chatIdUser)
                    mydb.member_update_chatid('adminChatId', 'Deny', chatIdUser)
                    mydb.del_member_chatid(chatid=chatIdUser)
                    bot.sendMessage(chatIdUser, msg.messageLib.sorryDenyAdmin.value)
                    bot.sendMessage(chatIdUser, message['text'])
            elif tempMember.membership_type == 2 or tempMember.membership_type == 1:
                print('text={}'.format(message['text']))
                op = mydb.get_member_property_chatid('op', message['chat']['id'])
                if op is not None:
                    if op == 0:
                        try:
                            yearIn = int(str(message['text'])[0:4])
                            monthIn = int(str(message['text'])[4:6])
                            dayIn = int(str(message['text'])[6:])
                            dateMiladiIn = JalaliDate(yearIn, monthIn, dayIn).to_gregorian()
                            todayDate = datetime.date.today()
                            diffDay = relativedelta(dateMiladiIn, todayDate).days
                            if diffDay > 0:
                                mydb.member_update('op', 1, message['chat']['id'])
                                mydb.shift_update('DateShift', message['text'], message['chat']['id'])
                                bot.sendMessage(message['chat']['id'],
                                                'آیا {0} بعنوان تاریخ شیفت صحیح است؟'.format(message['text']),
                                                reply_markup=menu.keyLib.kbCreateMenuYesNO(
                                                    chatId='{}'.format(op)))
                            else:
                                bot.sendMessage(message['chat']['id'], msg.messageLib.invalidDate.value)
                                bot.sendMessage(message['chat']['id'], msg.messageLib.dateShift.value)
                        except:
                            bot.sendMessage(message['chat']['id'], msg.messageLib.invalidDate.value)
                            bot.sendMessage(message['chat']['id'], msg.messageLib.dateShift.value)
                    if op == 2:
                        try:
                            hr, mi = map(int, str(message['text']).split(':'))
                            if (0 <= hr <= 23) and (0 <= mi <= 59):
                                mydb.member_update('op', 3, message['chat']['id'])
                                mydb.shift_update('startTime', message['text'], message['chat']['id'])
                                bot.sendMessage(message['chat']['id'],
                                                'آیا {0} بعنوان ساعت شروع شیفت صحیح است؟'.format(message['text']),
                                                reply_markup=menu.keyLib.kbCreateMenuYesNO(
                                                    chatId='{}'.format(op)))
                            else:
                                bot.sendMessage(message['chat']['id'], msg.messageLib.invalidTime.value)
                                bot.sendMessage(message['chat']['id'], msg.messageLib.shiftStartTime.value)
                        except:
                            bot.sendMessage(message['chat']['id'], msg.messageLib.invalidTime.value)
                            bot.sendMessage(message['chat']['id'], msg.messageLib.shiftStartTime.value)
                    if op == 4:
                        try:
                            hr, mi = map(int, str(message['text']).split(':'))
                            if (0 <= hr <= 23) and (0 <= mi <= 59):
                                mydb.member_update('op', 5, message['chat']['id'])
                                mydb.shift_update('endTime', message['text'], message['chat']['id'])
                                bot.sendMessage(message['chat']['id'],
                                                'آیا {0} بعنوان ساعت پایان شیفت صحیح است؟'.format(message['text']),
                                                reply_markup=menu.keyLib.kbCreateMenuYesNO(
                                                    chatId='{}'.format(op)))
                            else:
                                bot.sendMessage(message['chat']['id'], msg.messageLib.invalidTime.value)
                                bot.sendMessage(message['chat']['id'], msg.messageLib.shiftEndTime.value)
                        except:
                            bot.sendMessage(message['chat']['id'], msg.messageLib.invalidTime.value)
                            bot.sendMessage(message['chat']['id'], msg.messageLib.shiftEndTime.value)
                    if op == 6:
                        mydb.member_update('op', 7, message['chat']['id'])
                        mydb.shift_update('wage', message['text'], message['chat']['id'])
                        bot.sendMessage(message['chat']['id'],
                                        'آیا مبلغ {0} ریال بعنوان حق الزحمه صحیح است؟'.format(message['text']),
                                        reply_markup=menu.keyLib.kbCreateMenuYesNO(
                                            chatId='{}'.format(op)))
                    if op == 8:
                        mydb.member_update('op', 9, message['chat']['id'])
                        mydb.shift_update('pharmacyAddress', message['text'], message['chat']['id'])
                        bot.sendMessage(message['chat']['id'],
                                        'آیا آدرس {0} برای داروخانه صحیح است؟'.format(message['text']),
                                        reply_markup=menu.keyLib.kbCreateMenuYesNO(
                                            chatId='{}'.format(op)))

    elif 'callback_query' in update:
        message = update['callback_query']['message']
        btn = update['callback_query']['data']
        spBtn = btn.split('_')
        pprint(btn)
        if len(spBtn) > 1:
            if spBtn[1] == 'verify':
                mydb.member_update_chatid('verifyAdmin', 1, spBtn[2])
                bot.sendMessage(spBtn[2], msg.messageLib.congratulationsApproveAdmin.value)
            elif spBtn[1] == 'repShift':
                fh.helperFunder.msg_get_all_shift_approve(message=message, bot=bot);
            elif spBtn[1] == 'reactive':
                tempMember.delf = 0
                mydb.member_update(fieldName='del', fieldValue=0, chatid=spBtn[2])
                bot.sendMessage(spBtn[2], msg.messageLib.reActive.value)
            elif spBtn[1] == 'deny':
                bot.sendMessage(message['chat']['id'],
                                str(msg.messageLib.descDenyAdmin.value))
                mydb.member_update_chatid('registration_progress', 15, spBtn[2])
                mydb.member_update_chatid('adminChatId', message['chat']['id'], spBtn[2])
            elif spBtn[1] == 'NoDel':
                fh.helperFunder.send_operation(tempMember=tempMember, bot=bot, chatid=message['chat']['id'])
            elif spBtn[1] == 'reactive':
                mydb.del_member_chatid(message['chat']['id'])
                bot.sendMessage(message['chat']['id'], msg.messageLib.reActive.value)
            elif spBtn[1] == 'Del':
                tempMember.delf = 1
                mydb.del_member_chatid(user_id)
                bot.sendMessage(user_id, msg.messageLib.afteDelete.value)
            elif spBtn[1] == 'createSift':
                if tempMember.membership_type == 1 or tempMember.membership_type == 2:
                    bot.sendMessage(message['chat']['id'], msg.messageLib.dateShift.value)
                    mydb.member_update('op', 0, message['chat']['id'])
                else:
                    bot.sendMessage(message['chat']['id'], msg.messageLib.notAccess.value)
            elif spBtn[1] == 'yes':
                opBtn = int(spBtn[2])
                op = mydb.get_member_property_chatid('op', message['chat']['id'])
                print('{0} - {1} = {2}'.format(int(op), int(opBtn), int(op) - int(opBtn)))
                if (int(op) - int(opBtn)) > 1:
                    bot.sendMessage(user_id, msg.messageLib.erroOnBack.value)
                if int(op) == 1:
                    bot.sendMessage(message['chat']['id'], msg.messageLib.shiftStartTime.value)
                    mydb.member_update('op', 2, message['chat']['id'])
                if int(op) == 3:
                    bot.sendMessage(message['chat']['id'], msg.messageLib.shiftEndTime.value)
                    mydb.member_update('op', 4, message['chat']['id'])

                if int(op) == 5:
                    bot.sendMessage(message['chat']['id'], msg.messageLib.shiftWage.value)
                    mydb.member_update('op', 6, message['chat']['id'])

                if int(op) == 7:
                    bot.sendMessage(message['chat']['id'], msg.messageLib.pharmacyAddress.value)
                    addressPharmacy = None
                    if tempMember.membership_type == 1:
                        addressPharmacy = mydb.get_funder_property('pharmacy_address', message['chat']['id'])
                        mydb.shift_update('pharmacyAddress', addressPharmacy, user_id)
                    if addressPharmacy is not None:
                        bot.sendMessage(message['chat']['id'],
                                        'آیا آدرس {0} برای داروخانه صحیح است؟'.format(addressPharmacy),
                                        reply_markup=menu.keyLib.kbCreateMenuYesNO(
                                            chatId='{}'.format(9)))
                        mydb.member_update('op', 9, message['chat']['id'])
                    else:
                        mydb.member_update('op', 8, message['chat']['id'])
                if int(op) == 9:
                    bot.sendMessage(message['chat']['id'], msg.messageLib.endRegisterShift.value)
                    mydb.member_update('op', 0, message['chat']['id'])
                    # mydb.shift_update('pharmacyAddress', spBtn[3], spBtn[2])
                    mydb.shift_update('progress', 1, message['chat']['id'])
            elif spBtn[1] == 'NO':
                opBtn = int(spBtn[2])
                op = mydb.get_member_property_chatid('op', message['chat']['id'])
                if (int(op) - int(opBtn)) > 1:
                    bot.sendMessage(user_id, msg.messageLib.erroOnBack.value)
                    return
                if int(op) == 1:
                    mydb.member_update('op', 0, message['chat']['id'])
                    bot.sendMessage(message['chat']['id'], msg.messageLib.dateShift.value)
                if int(op) == 3:
                    mydb.member_update('op', 2, message['chat']['id'])
                    bot.sendMessage(message['chat']['id'], msg.messageLib.shiftStartTime.value)
                if int(op) == 5:
                    mydb.member_update('op', 4, message['chat']['id'])
                    bot.sendMessage(message['chat']['id'], msg.messageLib.shiftEndTime.value)
                if int(op) == 7:
                    mydb.member_update('op', 6, message['chat']['id'])
                    bot.sendMessage(message['chat']['id'], msg.messageLib.shiftWage.value)
                if int(op) == 9:
                    mydb.member_update('op', 8, message['chat']['id'])
                    bot.sendMessage(message['chat']['id'], msg.messageLib.shiftWage.value)
            elif spBtn[1] == 'listSift':
                allShift = mydb.get_all_shift(creator=message['chat']["id"])
                if len(allShift) == 0:
                    bot.sendMessage(message['chat']["id"], msg.messageLib.emptyList.value)
                else:
                    for shiftRow in allShift:
                        rowReq = 'درخواست دهنده: {}'.format(shiftRow[0])
                        rowDate = 'تاریخ  : {}'.format(shiftRow[2])
                        rowStartTime = 'ساعت شروع  : {}'.format(shiftRow[3])
                        rowEndTime = 'ساعت پایان  : {}'.format(shiftRow[4])
                        rowWage = 'حق الزحمه  : {}'.format(shiftRow[5])
                        rowaddr = 'آدرس  : {}'.format(shiftRow[6])
                        bot.sendMessage(message['chat']["id"], '''
{0}
{1}
{2}
{3}
{4}
{5}
{6}'''.format(rowReq, rowDate, rowStartTime, rowEndTime, rowWage, rowaddr,
              msg.messageLib.doYouLike.value), reply_markup=menu.keyLib.kbCreateMenuApproveShift(shiftRow[9]))
            # پذیرش شخصی که شیفت را رزرو کرده است
            elif spBtn[1] == 'approveShiftFunder':
                requester = mydb.get_shift_property(fieldName='approver', idShift=spBtn[2])
                mydb.shift_update('progress', 4, spBtn[2])
                bot.sendMessage(requester, msg.messageLib.acceptShift.value)
                rowDate = 'تاریخ  : {}'.format(mydb.get_shift_property('DateShift', spBtn[2]))
                rowStartTime = 'ساعت شروع  : {}'.format(mydb.get_shift_property('startTime', spBtn[2]))
                rowEndTime = 'ساعت پایان  : {}'.format(mydb.get_shift_property('endTime', spBtn[2]))
                rowWage = 'حق الزحمه  : {}'.format(mydb.get_shift_property('wage', spBtn[2]))
                rowaddr = 'آدرس  : {}'.format(mydb.get_shift_property('pharmacyAddress', spBtn[2]))
                bot.sendMessage(requester, '''
{0}
{1}
{2}
{3}
{4}'''.format(rowDate, rowStartTime, rowEndTime, rowWage, rowaddr))
                # آپدیت کردن شیف
            elif spBtn[1] == 'cancelShift':
                # ارسال شیفت هایی که شخص قبول کرده و تاریخ آنها نرسیده
                todayDate = datetime.date.today()
                jd = str(JalaliDate.to_jalali(todayDate.year, todayDate.month, todayDate.day)).split('-')
                sjd = "{0}{1}{2}".format(jd[0], jd[1], jd[2])
                fh.helperFunder.send_list_shift_Cancel(chatId=message['chat']['id'], bot=bot, todayDate=sjd)
            #     cancel approved Shift
            elif spBtn[1] == 'cancelShiftBtnList':
                mydb.shift_update_by_id(fieldName='progress', fieldValue=2, idshift=spBtn[2])
                creator = mydb.get_shift_property(fieldName='Creator', idShift=spBtn[2])
                dateShift = mydb.get_shift_property(fieldName='DateShift', idShift=spBtn[2])
                fullName = mydb.get_member_property_chatid(fieldName='last_name',
                                                           chatid=message['chat']['id'])
                bot.sendMessage(message['chat']['id'], str(msg.messageLib.youCanceled.value).format(dateShift))
                bot.sendMessage(creator, str(msg.messageLib.cancelShift.value).format(fullName, dateShift))
            elif spBtn[1] == 'disApproveShiftFunder':
                requester = mydb.get_shift_property(fieldName='approver', idShift=spBtn[2])
                mydb.shift_update('progress', 4, spBtn[2])
                bot.sendMessage(requester, msg.messageLib.disAcceptShift.value)
                rowDate = 'تاریخ  : {}'.format(mydb.get_shift_property('DateShift', spBtn[2]))
                rowStartTime = 'ساعت شروع  : {}'.format(mydb.get_shift_property('startTime', spBtn[2]))
                rowEndTime = 'ساعت پایان  : {}'.format(mydb.get_shift_property('endTime', spBtn[2]))
                rowWage = 'حق الزحمه  : {}'.format(mydb.get_shift_property('wage', spBtn[2]))
                rowaddr = 'آدرس  : {}'.format(mydb.get_shift_property('pharmacyAddress', spBtn[2]))
                bot.sendMessage(requester, '''
{0}
{1}
{2}
{3}
{4}'''.format(rowDate, rowStartTime, rowEndTime, rowWage, rowaddr))
            # آپدیت کردن شیفت
            #             پس از فشردن کلید شیفت را می پذیرم اجرا می شود
            elif spBtn[1] == 'shiftApprove':
                mydb.shift_reserve_by_id(spBtn[2], message['chat']['id'])
                bot.sendMessage(message['chat']['id'], msg.messageLib.reserveShift.value)
                creator = mydb.get_shift_property('Creator', spBtn[2]);
                fh.helperFunder.send_info_funder(chatid=message['chat']["id"], funder_chatid=creator,
                                                 shiftId=spBtn[2], bot=bot)
            elif spBtn[1] == 'deleteShift':
                print(message['chat']["id"])
                allShift = mydb.get_all_shift_by_creator(creator=message['chat']["id"])
                if len(allShift) == 0:
                    bot.sendMessage(message['chat']["id"], msg.messageLib.emptyList.value)
                else:
                    for shiftRow in allShift:
                        rowReq = 'درخواست دهنده: {}'.format(shiftRow[0])
                        rowDate = 'تاریخ  : {}'.format(shiftRow[2])
                        rowStartTime = 'ساعت شروع  : {}'.format(shiftRow[3])
                        rowEndTime = 'ساعت پایان  : {}'.format(shiftRow[4])
                        rowWage = 'حق الزحمه  : {}'.format(shiftRow[5])
                        rowaddr = 'آدرس  : {}'.format(shiftRow[6])
                        approveManager = None
                        if int(shiftRow[7]) == 1:
                            approveManager = 'ندارد'
                        else:
                            approveManager = 'دارد'
                        rowApprove = 'تائید مدیر: {}'.format(approveManager)
                        bot.sendMessage(message['chat']["id"], '''
{0}
{1}
{2}
{3}
{4}
{5}
{6}
{7}'''.format(rowReq, rowDate, rowStartTime, rowEndTime, rowWage, rowaddr, rowApprove,
              msg.messageLib.doYouLikeDelete.value),
                                        reply_markup=menu.keyLib.kbCreateMenuDeleteShift(shiftId=shiftRow[9]))
            elif spBtn[1] == 'DeleteShiftList':
                mydb.shift_update_by_id(fieldName='del', fieldValue='1', idshift=spBtn[2])
                bot.sendMessage(message['chat']['id'], msg.messageLib.delShiftMessage.value)
            elif spBtn[1] == 'listSiftManager':
                allShift = mydb.get_all_shift_manager()
                if len(allShift) == 0:
                    bot.sendMessage(message['chat']["id"], msg.messageLib.emptyList.value)
                else:
                    bot.sendMessage(message['chat']["id"], msg.messageLib.diver.value)
                    for shiftRow in allShift:
                        rowReq = 'درخواست دهنده: {}'.format(shiftRow[0])
                        rowDate = 'تاریخ  : {}'.format(shiftRow[2])
                        rowStartTime = 'ساعت شروع  : {}'.format(shiftRow[3])
                        rowEndTime = 'ساعت پایان  : {}'.format(shiftRow[4])
                        rowWage = 'حق الزحمه  : {}'.format(shiftRow[5])
                        rowaddr = 'آدرس  : {}'.format(shiftRow[6])
                        approveManager = None
                        if int(shiftRow[7]) == 1:
                            approveManager = 'ندارد'
                        else:
                            approveManager = 'دارد'
                        rowApprove = 'تائید مدیر: {}'.format(approveManager)
                        bot.sendMessage(message['chat']["id"], '''
{0}
{1}
{2}
{3}
{4}
{5}
{6}
{7}'''.format(rowReq, rowDate, rowStartTime, rowEndTime, rowWage, rowaddr, rowApprove,
              msg.messageLib.doYouLikeDelete.value),
                                        reply_markup=menu.keyLib.kbCreateMenuDeleteShift(shiftId=shiftRow[9]))
            elif spBtn[1] == 'listSiftDisApprove':
                allShift = mydb.get_all_shift_managerForApprove()
                if len(allShift) == 0:
                    bot.sendMessage(message['chat']["id"], msg.messageLib.emptyList.value)
                else:
                    for shiftRow in allShift:
                        rowReq = 'درخواست دهنده: {}'.format(shiftRow[0])
                        rowDate = 'تاریخ  : {}'.format(shiftRow[2])
                        rowStartTime = 'ساعت شروع  : {}'.format(shiftRow[3])
                        rowEndTime = 'ساعت پایان  : {}'.format(shiftRow[4])
                        rowWage = 'حق الزحمه  : {}'.format(shiftRow[5])
                        rowaddr = 'آدرس  : {}'.format(shiftRow[6])
                        approveManager = None
                        if int(shiftRow[7]) == 1:
                            approveManager = 'ندارد'
                        else:
                            approveManager = 'دارد'
                        rowApprove = 'تائید مدیر: {}'.format(approveManager)
                        bot.sendMessage(message['chat']["id"], '''
{0}
{1}
{2}
{3}
{4}
{5}
{6}
{7}'''.format(rowReq, rowDate, rowStartTime, rowEndTime, rowWage, rowaddr, rowApprove,
              msg.messageLib.doYouLikeApprove.value),
                                        reply_markup=menu.keyLib.kbCreateMenuShiftApproveManager(
                                            shiftId=shiftRow[9]))
            elif spBtn[1] == 'listSiftApprove':
                allShift = mydb.get_all_shift_managerApproved()
                if len(allShift) == 0:
                    bot.sendMessage(message['chat']["id"], msg.messageLib.emptyList.value)
                else:
                    for shiftRow in allShift:
                        rowReq = 'درخواست دهنده: {}'.format(shiftRow[0])
                        rowDate = 'تاریخ  : {}'.format(shiftRow[2])
                        rowStartTime = 'ساعت شروع  : {}'.format(shiftRow[3])
                        rowEndTime = 'ساعت پایان  : {}'.format(shiftRow[4])
                        rowWage = 'حق الزحمه  : {}'.format(shiftRow[5])
                        rowaddr = 'آدرس  : {}'.format(shiftRow[6])
                        approveManager = None
                        if int(shiftRow[7]) == 1:
                            approveManager = 'ندارد'
                        else:
                            approveManager = 'دارد'
                        rowApprove = 'تائید مدیر: {}'.format(approveManager)
                        bot.sendMessage(message['chat']["id"], '''
{0}
{1}
{2}
{3}
{4}
{5}
{6}
{7}'''.format(rowReq, rowDate, rowStartTime, rowEndTime, rowWage, rowaddr, rowApprove,
              msg.messageLib.doYouLikeApprove.value),
                                        reply_markup=menu.keyLib.kbCreateMenuShiftApproveManager(
                                            shiftId=shiftRow[9]))
            elif spBtn[1] == 'approveShiftManager':
                print(spBtn)
                mydb.shift_update_by_id('progress', 2, spBtn[2])
                cr = mydb.get_shift_property('creator', spBtn[2])
                bot.sendMessage(cr, msg.messageLib.shiftApprovedByManager.value)
            elif spBtn[1] == 'disApproveShiftManager':
                mydb.shift_update_by_id('progress', 3, spBtn[2])
                cr = mydb.get_shift_property('creator', spBtn[2])
                bot.sendMessage(cr, msg.messageLib.shiftDisApprovedByManager.value)
            elif spBtn[1] == 'listFunderManager':
                resualt = mydb.get_all_member(tye=1)
                print(resualt);
                txtResualt = None
                if len(resualt) > 0:
                    for item in resualt:
                        itemRow1 = 'نام و نام خانوادگی:{}'.format(item[0])
                        itemRow2 = 'نوع عضویت:{}'.format(item[1])
                        itemRow3 = 'شماره همراه:{}'.format(item[2])
                        bot.sendMessage(message['chat']['id'], '''
{0}
{1}
{2}'''.format(itemRow1, itemRow2, itemRow3))
                else:
                    bot.sendMessage(message['chat']['id'], msg.messageLib.emptyList.value)
            elif spBtn[1] == 'listresponsible':
                resualt = mydb.get_all_member(tye=2)
                txtResualt = None
                if len(resualt) > 0:
                    for item in resualt:
                        itemRow1 = 'نام و نام خانوادگی:{}'.format(item[0])
                        itemRow2 = 'نوع عضویت:{}'.format(item[1])
                        itemRow3 = 'شماره همراه:{}'.format(item[2])
                        bot.sendMessage(message['chat']['id'], '''
{0}
{1}
{2}'''.format(itemRow1, itemRow2, itemRow3))
                else:
                    bot.sendMessage(message['chat']['id'], msg.messageLib.emptyList.value)
            elif spBtn[1] == 'listStudent':
                resualt = mydb.get_all_member(tye=3)
                txtResualt = None
                if len(resualt) > 0:
                    for item in resualt:
                        itemRow1 = 'نام و نام خانوادگی:{}'.format(item[0])
                        itemRow2 = 'نوع عضویت:{}'.format(item[1])
                        itemRow3 = 'شماره همراه:{}'.format(item[2])
                        bot.sendMessage(message['chat']['id'], '''
{0}
{1}
{2}'''.format(itemRow1, itemRow2, itemRow3))
                else:
                    bot.sendMessage(message['chat']['id'], msg.messageLib.emptyList.value)
        if btn == 'btnFounder':
            tempMember.userName = userName
            tempMember.lastMessage = update['update_id']
            tempMember.membership_type = 1
            tempMember.chatId = update['callback_query']['chat_instance']
            tempMember.register_progress = 1
            mydb.member_update_chatid('membership_type', 1, message['chat']['id'])
            mydb.member_update_chatid('chat_id', user_id, message['chat']['id'])
            pprint(mydb.member_update_chatid('registration_progress', 1, message['chat']['id']))
            bot.sendMessage(message['chat']['id'],
                            str(msg.messageLib.enterName.value))
        if btn == 'btnTechnicalResponsible':
            tempMember.userName = userName
            tempMember.lastMessage = update['update_id']
            tempMember.membership_type = 2
            tempMember.chatId = update['callback_query']['chat_instance']
            tempMember.register_progress = 1
            mydb.member_update_chatid('membership_type', 2, message['chat']['id'])
            mydb.member_update_chatid('chat_id', user_id, message['chat']['id'])
            pprint(mydb.member_update_chatid('registration_progress', 1, message['chat']['id']))
            bot.sendMessage(message['chat']['id'],
                            str(msg.messageLib.enterName.value))
        if btn == 'btnStudent':
            tempMember.userName = userName
            tempMember.lastMessage = update['update_id']
            tempMember.membership_type = 3
            tempMember.chatId = update['callback_query']['chat_instance']
            tempMember.register_progress = 1
            mydb.member_update_chatid('membership_type', 3, message['chat']['id'])
            mydb.member_update_chatid('chat_id', user_id, message['chat']['id'])
            pprint(mydb.member_update_chatid('registration_progress', 1, message['chat']['id']))
            bot.sendMessage(message['chat']['id'],
                            str(msg.messageLib.enterName.value))
        if btn == 'btnMananger':
            tempMember.userName = userName
            tempMember.lastMessage = update['update_id']
            tempMember.membership_type = 4
            tempMember.chatId = update['callback_query']['chat_instance']
            tempMember.register_progress = 1
            mydb.member_update_chatid('membership_type', 4, message['chat']['id'])
            mydb.member_update_chatid('chat_id', user_id, message['chat']['id'])
            pprint(mydb.member_update_chatid('registration_progress', 1, message['chat']['id']))
            bot.sendMessage(message['chat']['id'],
                            str(msg.messageLib.enterName.value))
        if btn == 'btNightDay':
            mydb.founder_update('pharmacy_type', 'شبانه روزی', message['chat']['id'])
            bot.sendMessage(message['chat']['id'],
                            str(msg.messageLib.enterPharmacyAddress.value))
            mydb.member_update_chatid('registration_progress', 6, message['chat']['id'])
            tempMember.register_progress = 6
        if btn == 'btnNormal':
            mydb.founder_update('pharmacy_type', 'عادی', message['chat']['id'])
            bot.sendMessage(message['chat']['id'],
                            str(msg.messageLib.enterPharmacyAddress.value))
            mydb.member_update_chatid('registration_progress', 6, message['chat']['id'])
            tempMember.register_progress = 6
        if btn == 'btShiftMorning':
            mydb.student_update('shift_access', 'صبح', message['chat']['id'])
            bot.sendMessage(message['chat']['id'],
                            str(msg.messageLib.endRegisteration.value))

            admins = mydb.getAdmins()
            for admin in admins:
                bot.sendMessage(admin[0],
                                str(msg.messageLib.messAdminApproveStudent.value))
                bot.sendMessage(admin[0],
                                str(msg.messageLib.labeName.value).format(tempMember.name, tempMember.last_name))
                bot.sendMessage(admin[0],
                                str(msg.messageLib.labelNationCode.value).format(
                                    mydb.get_student_property('national_code', message['chat']['id'])))
                bot.sendMessage(admin[0],
                                str(msg.messageLib.labelPhoneNumber.value).format(tempMember.phone_number))
                bot.sendMessage(admin[0],
                                str(msg.messageLib.labelDateStartPermit.value).format(
                                    mydb.get_student_property('start_date',
                                                              message['chat']['id'])))
                bot.sendMessage(admin[0],
                                str(msg.messageLib.labelDateEndPermit.value).format(
                                    mydb.get_student_property('end_date', message['chat']['id'])))
                bot.sendMessage(admin[0],
                                str(msg.messageLib.labelShift.value).format(
                                    mydb.get_student_property('shift_access', message['chat']['id'])))
                bot.sendMessage(admin[0],
                                str(msg.messageLib.labelSelfiPhoto.value))
                img = 'download/{}'.format(mydb.get_student_property('personal_photo', message['chat']['id']))
                print(
                    'download/{}'.format(mydb.get_student_property('personal_photo', message['chat']['id'])))
                bot.sendPhoto(admin[0], open(img, 'rb'))
                bot.sendMessage(admin[0],
                                str(msg.messageLib.labelPermitPhoto.value))
                img = 'download/{}'.format(
                    mydb.get_student_property('overtime_license_photo', message['chat']['id']))
                bot.sendPhoto(admin[0], open(img, 'rb'))
                bot.sendMessage(admin[0], msg.messageLib.messAdminApprove.value,
                                reply_markup=menu.keyLib.kbCreateApproveKey(chat_id=message['chat']['id']))
            mydb.member_update_chatid('registration_progress', 10, message['chat']['id'])
            tempMember.register_progress = 10
        if btn == 'btShiftEvening':
            mydb.student_update('shift_access', 'عصر', message['chat']['id'])
            bot.sendMessage(message['chat']['id'],
                            str(msg.messageLib.endRegisteration.value))
            admins = mydb.getAdmins()
            for admin in admins:
                bot.sendMessage(admin[0],
                                str(msg.messageLib.messAdminApproveStudent.value))
                bot.sendMessage(admin[0],
                                str(msg.messageLib.labeName.value).format(tempMember.name, tempMember.last_name))
                bot.sendMessage(admin[0],
                                str(msg.messageLib.labelNationCode.value).format(
                                    mydb.get_student_property('national_code', message['chat']['id'])))
                bot.sendMessage(admin[0],
                                str(msg.messageLib.labelPhoneNumber.value).format(tempMember.phone_number))
                bot.sendMessage(admin[0],
                                str(msg.messageLib.labelDateStartPermit.value).format(
                                    mydb.get_student_property('start_date', message['chat']['id'])))
                bot.sendMessage(admin[0],
                                str(msg.messageLib.labelDateEndPermit.value).format(
                                    mydb.get_student_property('end_date', message['chat']['id'])))
                bot.sendMessage(admin[0],
                                str(msg.messageLib.labelShift.value).format(
                                    mydb.get_student_property('shift_access', message['chat']['id'])))
                bot.sendMessage(admin[0],
                                str(msg.messageLib.labelSelfiPhoto.value))
                img = 'download/{}'.format(mydb.get_student_property('personal_photo', message['chat']['id']))
                print(
                    'download/{}'.format(mydb.get_student_property('personal_photo', message['chat']['id'])))
                bot.sendPhoto(admin[0], open(img, 'rb'))
                bot.sendMessage(admin[0],
                                str(msg.messageLib.labelPermitPhoto.value))
                img = 'download/{}'.format(
                    mydb.get_student_property('overtime_license_photo', message['chat']['id']))
                bot.sendPhoto(admin[0], open(img, 'rb'))
                bot.sendMessage(admin[0], msg.messageLib.messAdminApprove.value,
                                reply_markup=menu.keyLib.kbCreateApproveKey(chat_id=message['chat']['id']))
            mydb.member_update_chatid('registration_progress', 10, message['chat']['id'])
            tempMember.register_progress = 10
        if btn == 'btShiftEveningNight':
            mydb.student_update('shift_access', 'عصر و شب', message['chat']['id'])
            bot.sendMessage(message['chat']['id'],
                            str(msg.messageLib.endRegisteration.value))
            admins = mydb.getAdmins()
            for admin in admins:
                bot.sendMessage(admin[0],
                                str(msg.messageLib.messAdminApproveStudent.value))
                bot.sendMessage(admin[0],
                                str(msg.messageLib.labeName.value).format(tempMember.name, tempMember.last_name))
                bot.sendMessage(admin[0],
                                str(msg.messageLib.labelNationCode.value).format(
                                    mydb.get_student_property('national_code', message['chat']['id'])))
                bot.sendMessage(admin[0],
                                str(msg.messageLib.labelPhoneNumber.value).format(tempMember.phone_number))
                bot.sendMessage(admin[0],
                                str(msg.messageLib.labelDateStartPermit.value).format(
                                    mydb.get_student_property('start_date',
                                                              message['chat']['id'])))
                bot.sendMessage(admin[0],
                                str(msg.messageLib.labelDateEndPermit.value).format(
                                    mydb.get_student_property('end_date', message['chat']['id'])))
                bot.sendMessage(admin[0],
                                str(msg.messageLib.labelShift.value).format(
                                    mydb.get_student_property('shift_access', message['chat']['id'])))
                bot.sendMessage(admin[0],
                                str(msg.messageLib.labelSelfiPhoto.value))
                img = 'download/{}'.format(mydb.get_student_property('personal_photo', message['chat']['id']))
                print(
                    'download/{}'.format(mydb.get_student_property('personal_photo', message['chat']['id'])))
                bot.sendPhoto(admin[0], open(img, 'rb'))
                bot.sendMessage(admin[0],
                                str(msg.messageLib.labelPermitPhoto.value))
                img = 'download/{}'.format(
                    mydb.get_student_property('overtime_license_photo', message['chat']['id']))
                bot.sendPhoto(admin[0], open(img, 'rb'))
                bot.sendMessage(admin[0], msg.messageLib.messAdminApprove.value,
                                reply_markup=menu.keyLib.kbCreateApproveKey(chat_id=message['chat']['id']))
            mydb.member_update_chatid('registration_progress', 10, message['chat']['id'])
            tempMember.register_progress = 10
        if btn == 'btShiftMorningEvening':
            mydb.student_update('shift_access', 'صبح و عصر', message['chat']['id'])
            bot.sendMessage(message['chat']['id'],
                            str(msg.messageLib.endRegisteration.value))
            admins = mydb.getAdmins()
            for admin in admins:
                bot.sendMessage(admin[0],
                                str(msg.messageLib.messAdminApproveStudent.value))
                bot.sendMessage(admin[0],
                                str(msg.messageLib.labeName.value).format(tempMember.name, tempMember.last_name))
                bot.sendMessage(admin[0],
                                str(msg.messageLib.labelNationCode.value).format(
                                    mydb.get_student_property('national_code', message['chat']['id'])))
                bot.sendMessage(admin[0],
                                str(msg.messageLib.labelPhoneNumber.value).format(tempMember.phone_number))
                bot.sendMessage(admin[0],
                                str(msg.messageLib.labelDateStartPermit.value).format(
                                    mydb.get_student_property('start_date',
                                                              message['chat']['id'])))
                bot.sendMessage(admin[0],
                                str(msg.messageLib.labelDateEndPermit.value).format(
                                    mydb.get_student_property('end_date', message['chat']['id'])))
                bot.sendMessage(admin[0],
                                str(msg.messageLib.labelShift.value).format(
                                    mydb.get_student_property('shift_access', message['chat']['id'])))
                bot.sendMessage(admin[0],
                                str(msg.messageLib.labelSelfiPhoto.value))
                img = 'download/{}'.format(mydb.get_student_property('personal_photo', message['chat']['id']))
                print(
                    'download/{}'.format(mydb.get_student_property('personal_photo', message['chat']['id'])))
                bot.sendPhoto(admin[0], open(img, 'rb'))
                bot.sendMessage(admin[0],
                                str(msg.messageLib.labelPermitPhoto.value))
                img = 'download/{}'.format(
                    mydb.get_student_property('overtime_license_photo', message['chat']['id']))
                bot.sendPhoto(admin[0], open(img, 'rb'))
                bot.sendMessage(admin[0], msg.messageLib.messAdminApprove.value,
                                reply_markup=menu.keyLib.kbCreateApproveKey(chat_id=message['chat']['id']))
            mydb.member_update_chatid('registration_progress', 10, message['chat']['id'])
            tempMember.register_progress = 10
        # پردازش پیام
    # elif 'my_chat_member' in update:
    #     continue
    # بروزرسانی شناسه آخرین پیام دریافتی و زمان آن
    # print('last_message_id = {} where user is {}'.format(update['update_id'], user_id))
    last_update_ids[user_id] = (tempMember, update['update_id'])
    mydb.set_member_last_update_id(message['chat']['id'], update['update_id'])
    # mydb.member_update_chatid(fieldName='last_message_sent', fieldValue=update['update_id'],
    #                           chatid=message['chat']['id'])


# پردازش تمامی پیام های دریافتی
def handle_updates(updates):
    message = None
    user_id = None
    for update in updates:
        if 'message' in update:
            message = update['message']
        elif 'callback_query' in update:
            message = update['callback_query']['message']
        else:
            continue
        user_id = message['chat']['id']
        user_name = None
        if 'username' in message['chat']:
            user_name = message['chat']['username']
        else:
            user_name = ' کاربر '
        # پردازش پیام جدید
        handle_new_messages(user_id, user_name, update)


# شروع برنامه
def main():
    lui = 0
    try:
     while True:
        # دریافت تمامی پیام های دریافتی
        updates = bot.getUpdates(timeout=10, offset=lui)
        if updates:
            lui = int(updates[-1]['update_id']) + 1
            handle_updates(updates)
    except Exception as e:
     bot.sendMessage('6274361322',str(e))
     main()


if __name__ == '__main__':
    main()
