import threading
import traceback
import telepot
import time
from model.membership import Membership
from persiantools.jdatetime import JalaliDate
from dateutil.relativedelta import relativedelta
from datetime import timedelta,  datetime, time
import os
import msg
import db.mysqlconnector as msc
import uuid
import menu
import db.founderHelper as fh
from unidecode import unidecode
import pandas as pd
import re as reg

helper = fh.HelperFunder()

last_update_ids = {}
# زمان حداکثر برای فعال بودن آخرین پیام دریافتی (به ثانیه)
MAX_IDLE_TIME = 600

mydb = msc.mysqlconnector()
idFromFile = None
botKeyApi = mydb.get_property_domain('botkey')
bot = telepot.Bot(botKeyApi)


# splitDate = JalaliDate(datetime.now())
# print(JalaliDate(datetime.now() + timedelta(days=3)))
# helper.send_shift_to_technicalResponsible(29, bot )
# exit()
# admins = mydb.getAdmins()
# image = 'download/2c3809f7-8e48-4cbf-acb7-bc7b0c9d1cd4.jpg'
# pprint(admins)
# for admin in admins:
#     pprint(bot.sendPhoto(admin[0], open(image, 'rb')))
# date1 = datetime.combine(JalaliDate(1402, 6, 29).to_gregorian(),time())
# date2 = datetime.now()
# delta = date1 - date2
# diffDay = relativedelta(date1, date2)
# print("{0} - {1} = {2} hours ".format(date1, date2, (diffDay.days * 24)+ diffDay.hours))
# todayDate=datetime.date.today()
# jd=str(JalaliDate.to_jalali(todayDate.year,todayDate.month,todayDate.day)).split('-')
# sjd= "{0}{1}{2}".format(jd[0],jd[1],jd[2])
# print(sjd)
# dr =mydb.get_shift_property('dateRegiter',24)
# print(dr.day)
# print(JalaliDate.to_jalali(dr.year, dr.month, dr.day))
# splitDate = str(JalaliDate(datetime.now())).split('-')
# print(splitDate)
# dateEndMoth = JalaliDate(JalaliDate(1402, int(splitDate[1]) + 1, 1).to_gregorian() - timedelta(days=1))
# print(dateEndMoth)
# pprint(telepot.message_identifier(bot.sendMessage('6274361322', 'test3')))
# bot.deleteMessage((6274361322, 1725))
# bot.editMessageText((6274361322, 2336),'test3Edit')
# exit(0)


def handle_new_messages(user_id, userName, update):
    tempMember = mydb.load_member(user_id)
    if tempMember is None:
        tempMember = mydb.create_member(Membership(userName=userName, chatid=user_id))
        last_update_id = 0
    else:
        last_update_id = int(tempMember.lastMessage)
    # **********************************************************************************************************
    print(f"register_progress = {tempMember.register_progress} && op = {tempMember.op} ")
    if not helper.checkStatus(bot=bot, mem=tempMember, update=update):
        return
    message = None
    if 'message' in update:
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
            helper.myInfo(tempMember, bot, message, user_id)
        elif 'text' in message and str(message['text']).lower().startswith('/emday '.lower()):
            if tempMember.membership_type is None or tempMember.membership_type != 4:
                bot.sendMessage(user_id, msg.messageLib.userIsNotAdmin.value)
                return
            totalDay = str(message['text']).lower().split(' ')
            if len(totalDay) != 2:
                bot(user_id, msg.messageLib.noBussiness.value)
            else:
                mydb.domain_update_by_key('emDay', totalDay[1])
                bot.sendMessage(user_id, str(msg.messageLib.changeEmDay.value).format(totalDay[1]))

        elif 'text' in message and str(message['text']).lower().startswith('/changeHrStudent'.lower()):
            if tempMember.membership_type is None or tempMember.membership_type != 4:
                bot.sendMessage(user_id, msg.messageLib.userIsNotAdmin.value)
                return
            hr = None
            try:
                hr = int(str(message['text'])[16:])
            except:
                bot.sendMessage(user_id, msg.messageLib.erroCommand.value)
                return
            mydb.domain_update_by_key('hrStudent', hr)
            bot.sendMessage(user_id, str(msg.messageLib.changeHourSuccess.value).format(hr))
        elif 'text' in message and str(message['text']).lower().startswith('/changeMinWage'.lower()):
            if tempMember.membership_type is None or tempMember.membership_type != 4:
                bot.sendMessage(user_id, msg.messageLib.userIsNotAdmin.value)
                return
            wage = None
            try:
                wage = int(str(message['text'])[14:])
            except:
                bot.sendMessage(user_id, msg.messageLib.erroCommand.value)
                return
            mydb.domain_update_by_key('wage', wage)
            bot.sendMessage(user_id, str(msg.messageLib.changeWageSuccess.value).format(wage))
        elif 'text' in message and str(message['text']).lower().startswith('/changeWFS'.lower()):
            if tempMember.membership_type is None or tempMember.membership_type != 4:
                bot.sendMessage(user_id, msg.messageLib.userIsNotAdmin.value)
                return
            wage = None
            try:
                wage = int(str(message['text'])[10:])
            except:
                bot.sendMessage(user_id, msg.messageLib.erroCommand.value)
                return
            mydb.domain_update_by_key('studentWage', wage)
            bot.sendMessage(user_id, str(msg.messageLib.changeWageSuccess.value).format(wage))
        elif 'text' in message and str(message['text']).lower().startswith('/changeShiftEmHr'.lower()):
            if tempMember.membership_type is None or tempMember.membership_type != 4:
                bot.sendMessage(user_id, msg.messageLib.userIsNotAdmin.value)
                return
            emhr = None
            try:
                emhr = int(str(message['text'])[16:])
            except:
                bot.sendMessage(user_id, msg.messageLib.erroCommand.value)
                return
            mydb.domain_update_by_key('hrEmShift', emhr)
            bot.sendMessage(user_id, str(msg.messageLib.changeShiftEmHr.value).format(emhr))
        elif 'text' in message and str(message['text']).lower().startswith('/changePDEM'.lower()):
            if tempMember.membership_type is None or tempMember.membership_type != 4:
                bot.sendMessage(user_id, msg.messageLib.userIsNotAdmin.value)
                return
            PDEM = None
            try:
                PDEM = int(str(message['text'])[11:])
            except:
                bot.sendMessage(user_id, msg.messageLib.erroCommand.value)
                return
            mydb.domain_update_by_key('PDEM', PDEM)
            bot.sendMessage(user_id, str(msg.messageLib.chandePDEM.value).format(PDEM))
        elif 'text' in message and str(message['text']).lower().startswith('/changeTPDEM'.lower()):
            if tempMember.membership_type is None or tempMember.membership_type != 4:
                bot.sendMessage(user_id, msg.messageLib.userIsNotAdmin.value)
                return
            TSPDEM = None
            try:
                TSPDEM = int(str(message['text'])[12:])
            except:
                bot.sendMessage(user_id, msg.messageLib.erroCommand.value)
                return
            mydb.domain_update_by_key('TSPDEM', TSPDEM)
            bot.sendMessage(user_id, str(msg.messageLib.chageTSPDEM.value).format(TSPDEM))
        elif 'text' in message and str(message['text']).lower().startswith('/changeMinLicenss'.lower()):
            if tempMember.membership_type is None or tempMember.membership_type != 4:
                bot.sendMessage(user_id, msg.messageLib.userIsNotAdmin.value)
                return
            licenssRent = None
            try:
                licenssRent = int(str(message['text'])[17:])
            except:
                bot.sendMessage(user_id, msg.messageLib.erroCommand.value)
                return
            mydb.domain_update_by_key('licenss', licenssRent)
            bot.sendMessage(user_id, str(msg.messageLib.changeLicenssSuccess.value).format(licenssRent))
        elif 'text' in message and message['text'] == '/CancelMessage':
            mydb.member_update_chatid('registration_progress', 10, user_id)
            mydb.member_update_chatid('op', 0, user_id)
            bot.sendMessage(user_id, msg.messageLib.cancelMsg.value)
        elif 'text' in message and message['text'] == '/myoperation':
            if tempMember.register_progress < 10:
                bot.sendMessage(user_id, msg.messageLib.noRegisterUser.value)
                bot.sendMessage(user_id, msg.messageLib.noForRegisterUser.value)
                return
            helper.send_operation(tempMember=tempMember, bot=bot, chatid=message['chat']['id'])
        elif 'text' in message and tempMember.register_progress == 0 and message['text'] == '/start':
            bot.sendMessage(message['chat']['id'], str(msg.messageLib.helloClient.value).format(
                message['chat']['first_name']), reply_markup=menu.keyLib.kbWhoAreYou())
        elif 'text' in message and tempMember.register_progress > 9 and message['text'] == '/start':
            helper.myInfo(tempMember, bot, message, user_id)
            # titlePos = None
            # if tempMember.membership_type == 1:
            #     titlePos = 'موسس'
            # elif tempMember.membership_type == 2:
            #     titlePos = 'مسئول فنی'
            # elif tempMember.membership_type == 3:
            #     titlePos = 'دانشجو'
            # elif tempMember.membership_type == 4:
            #     titlePos = 'مدیر'
            # if tempMember.register_progress < 10:
            #     bot.sendMessage(user_id, msg.messageLib.userNotCompelete.value,
            #                     reply_markup=menu.keyLib.kbCreateMenuNotCompelete())
            #     return
            # try:
            #     bot.sendMessage(message['chat']['id'],
            #                     str(msg.messageLib.duplicateregistration.value).format(titlePos),
            #                     reply_markup=menu.keyLib.kbCreateDelKey(message['chat']['id']))
            # except:  #
            #     bot.sendMessage('6274361322', '{0}:{1}'.format(message['chat']['id'], message['text']))
        elif tempMember.register_progress == 1:
            if message['text'] == '/start':
                bot.sendMessage(message['chat']['id'],
                                str(msg.messageLib.enterName.value))
                return
            mydb.member_update_chatid('name', message['text'], message['chat']['id'])
            bot.sendMessage(message['chat']['id'],
                            str(msg.messageLib.enterLastName.value))
            mydb.member_update_chatid('registration_progress', 2, message['chat']['id'])
            tempMember.register_progress = 2
        elif tempMember.register_progress == 2:
            if message['text'] == '/start':
                bot.sendMessage(message['chat']['id'],
                                str(msg.messageLib.enterLastName.value))
                return
            mydb.member_update_chatid('last_name', message['text'], message['chat']['id'])
            bot.sendMessage(message['chat']['id'],
                            str(msg.messageLib.enterPhoneNumber.value))
            mydb.member_update_chatid('registration_progress', 3, message['chat']['id'])
            tempMember.register_progress = 3
        elif tempMember.register_progress == 3:
            phone = unidecode(message['text'])
            if not helper.validate_IR_mobile_number(mobile_number=phone):
                bot.sendMessage(message['chat']['id'], msg.messageLib.errorPhoneNumber.value)
                return
            mydb.member_update_chatid('phone_number', unidecode(message['text']), message['chat']['id'])
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
        elif tempMember.register_progress == 4:
            if tempMember.membership_type == 1:
                if message['text'] == '/start':
                    bot.sendMessage(message['chat']['id'],
                                    str(msg.messageLib.enterPharmacyName.value))
                    return
                mydb.founder_update('pharmacy_name', message['text'], message['chat']['id'])
                bot.sendMessage(message['chat']['id'],
                                str(msg.messageLib.enterPharmacyType.value),
                                reply_markup=menu.keyLib.kbTypePharmacy())
                mydb.member_update_chatid('registration_progress', 5, message['chat']['id'])
                tempMember.register_progress = 5
            elif tempMember.membership_type == 2:
                nationCode = unidecode(message['text'])
                repNation = False
                if tempMember.op == 0:
                    repNation = mydb.rep_nation_code(nationCode)
                if repNation:
                    bot.sendMessage(user_id, msg.messageLib.repNationCode.value)
                    return
                if not helper.validate_IR_national_id(nationCode):
                    bot.sendMessage(message['chat']['id'], msg.messageLib.errrorNation.value)
                    return
                mydb.technicalManager_update('national_code', unidecode(message['text']), message['chat']['id'])
                bot.sendMessage(message['chat']['id'],
                                str(msg.messageLib.enetrcodePharmaceutical.value))
                mydb.member_update_chatid('registration_progress', 5, message['chat']['id'])
                tempMember.register_progress = 5
            elif tempMember.membership_type == 3:
                nationCode = unidecode(message['text'])
                repNation = mydb.rep_nation_code(nationCode)
                if repNation:
                    bot.sendMessage(user_id, msg.messageLib.repNationCode.value)
                    return
                if not helper.validate_IR_national_id(nationCode):
                    bot.sendMessage(message['chat']['id'], msg.messageLib.errrorNation.value)
                    return
                mydb.student_update('national_code', unidecode(message['text']), message['chat']['id'])
                bot.sendMessage(message['chat']['id'],
                                str(msg.messageLib.enterLicenseStartDate.value))
                bot.sendMessage(chat_id=user_id, parse_mode='HTML', text='سال را انتخاب کنید',
                                reply_markup=menu.keyLib.kbCreateMenuYear(tag=4))
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
                        isExisting = os.path.exists(img)
                        if isExisting:
                            bot.sendPhoto(admin[0], open(img, 'rb'))
                        else:
                            bot.sendMessage(admin[0], 'فایل تصویر پیدا نشد')
                        bot.sendMessage(admin[0], msg.messageLib.messAdminApprove.value,
                                        reply_markup=menu.keyLib.kbCreateApproveKey(chat_id=message['chat']['id']))
                    mydb.member_update_chatid('registration_progress', 10, message['chat']['id'])
                    tempMember.register_progress = 10
                else:
                    bot.sendMessage(message['chat']['id'],
                                    str(msg.messageLib.errorSendFile.value))
            elif tempMember.membership_type == 3:
                #todo: check number
                mydb.student_update('hourPermit', unidecode(message['text']), user_id)
                bot.sendMessage(message['chat']['id'],
                                str(msg.messageLib.enterWorkoverPermitPhoto.value))
                mydb.member_update_chatid('registration_progress', 7, message['chat']['id'])
                tempMember.register_progress = 7
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
                        isExisting = os.path.exists(img)
                        if isExisting:
                            bot.sendPhoto(admin[0], open(img, 'rb'))
                        else:
                            bot.sendMessage(admin[0], 'فایل تصویر پیدا نشد')
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
        # elif tempMember.register_progress == 10:
        #     if tempMember.membership_type == 4 and message['text'] == '/start':
        #         bot.sendMessage(message['chat']['id'],
        #                         str(msg.messageLib.helloAdmin.value).format(
        #                             tempMember.name + ' ' + tempMember.last_name),
        #                         reply_markup=menu.keyLib.kbAdmin())
        elif tempMember.register_progress == 11:
            op = mydb.get_member_property_chatid('op', user_id)
            if op is not None:
                if op == 0:
                    try:
                        yearIn = int(str(message['text'])[0:4])
                        monthIn = int(str(message['text'])[4:6])
                        dayIn = int(str(message['text'])[6:])
                        dateMiladiIn = JalaliDate(yearIn, monthIn, dayIn).to_gregorian()
                        todayDate = datetime.today()
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
                    minWage = mydb.get_property_domain('wage')
                    if str(message['text']).isnumeric():
                        if int(minWage) > int(message['text']):
                            bot.sendMessage(user_id, str(msg.messageLib.minWage.value).format(minWage),
                                            parse_mode='HTML')
                            bot.sendMessage(user_id, msg.messageLib.shiftWage.value, parse_mode='HTML')
                            return
                    else:
                        bot.sendMessage(user_id, msg.messageLib.errorNumber.value)
                        return
                    mydb.member_update('op', 7, message['chat']['id'])
                    idShift = mydb.get_member_property_chatid('lastShiftId', user_id)
                    mydb.shift_update_by_id('wage', unidecode(message['text']), idShift)
                    bot.sendMessage(message['chat']['id'],
                                    'آیا مبلغ {0} ریال بعنوان حق الزحمه صحیح است؟'.format(message['text']),
                                    reply_markup=menu.keyLib.kbCreateMenuYesNO(
                                        chatId='{}'.format(op)))
                if op == 8:
                    minWage = mydb.get_property_domain('studentWage')
                    if str(message['text']).isnumeric():
                        if int(minWage) > int(message['text']):
                            bot.sendMessage(user_id, str(msg.messageLib.minWFStudent.value).format(minWage))
                            bot.sendMessage(user_id, msg.messageLib.shiftWageStudent.value)
                            return
                    else:
                        bot.sendMessage(user_id, msg.messageLib.errorNumber.value)
                        return
                    mydb.member_update('op', 9, message['chat']['id'])
                    idShift = mydb.get_member_property_chatid('lastShiftId', user_id)
                    mydb.shift_update_by_id('wfStudent', unidecode(message['text']), idShift)
                    bot.sendMessage(message['chat']['id'],
                                    'آیا مبلغ {0} ریال بعنوان حق الزحمه دانشجو صحیح است؟'.format(message['text']),
                                    reply_markup=menu.keyLib.kbCreateMenuYesNO(
                                        chatId='{}'.format(op)))
                if op == 10:
                    mydb.member_update('op', 11, message['chat']['id'])
                    idShift = mydb.get_member_property_chatid('lastShiftId', user_id)
                    rs = mydb.shift_update_by_id('pharmacyAddress', message['text'], idShift)
                    bot.sendMessage(message['chat']['id'],
                                    'آیا آدرس {0} برای داروخانه صحیح است؟'.format(message['text']),
                                    reply_markup=menu.keyLib.kbCreateMenuYesNO(
                                        chatId='{0}_{1}'.format(11, idShift)))
        elif tempMember.register_progress == 15:
            if tempMember.membership_type == 4:
                chatIdUser = mydb.get_member_property_Adminchatid(fieldName='chat_id', chatid=message['chat']['id'])
                if chatIdUser is not None:
                    mydb.member_update_chatid('desc', message['text'], chatIdUser)
                    mydb.member_update_chatid('adminChatId', user_id, chatIdUser)
                    # mydb.del_member_chatid(chatid=chatIdUser)
                    mydb.member_update_chatid('registration_progress', 18, chatIdUser)
                    bot.sendMessage(chatIdUser, msg.messageLib.sorryDenyAdmin.value)
                    bot.sendMessage(chatIdUser, message['text'])
                    bot.sendMessage(chatIdUser, msg.messageLib.selectPropertyForEdit.value,
                                    reply_markup=menu.keyLib.kbEditProfile(chatId=chatIdUser))
            mydb.member_update_chatid('registration_progress', 10, user_id)
        elif tempMember.register_progress == 18:
            helper.regEditItem(mem=tempMember, bot=bot, newValue=message)
        elif tempMember.register_progress == 19:
            listReciver = None
            if tempMember.op == 20:  # مدیران
                listReciver = mydb.getListMember(user_id, 4)
            elif tempMember.op == 21:  # موسسان
                listReciver = mydb.getListMember(user_id, 1)
            elif tempMember.op == 22:  # مسئولان فنی
                listReciver = mydb.getListMember(user_id, 2)
            elif tempMember.op == 23:  # دانشجویان
                listReciver = mydb.getListMember(user_id, 3)
            elif tempMember.op == 24:  # همه
                listReciver = mydb.getListMember(user_id)
            for item in listReciver:
                bot.sendMessage(item[0], message['text'])
            mydb.member_update_chatid('registration_progress', 10, user_id)
            mydb.member_update_chatid('op', 0, user_id)
            bot.sendMessage(user_id, msg.messageLib.sendedMessage.value)
        elif tempMember.register_progress in (201, 202):
            typeRequest = tempMember.register_progress - 201
            result = mydb.insertLicense(message['text'], typeRequest, user_id)
            if result > 0:
                if typeRequest == 0:
                    bot.sendMessage(user_id, msg.messageLib.msgRegistedlicenseNeed.value)
                else:
                    bot.sendMessage(user_id, msg.messageLib.msgRegistedlicenseEmpty.value)
            else:
                bot.sendMessage(user_id, msg.messageLib.errorRegisterLicense.value)
            mydb.member_update_chatid('registration_progress', 10, user_id)
        elif tempMember.register_progress == 306:
            listEmpty = mydb.getListLicenseEmpty(searchTerm=message['text'])
            if len(listEmpty) == 0:
                bot.sendMessage(user_id, msg.messageLib.emptyList.value)
                return
            for item in listEmpty:
                bot.sendMessage(user_id, helper.formatLicenseEmpty(item),
                                reply_markup=menu.keyLib.kbRemoveRequest(idReq=item[0]))

        elif tempMember.register_progress == 307:
            listNeed = mydb.getListLicenseNeed(searchTerm=message['text'])
            if len(listNeed) == 0:
                bot.sendMessage(user_id, msg.messageLib.emptyList.value)
                return
            for item in listNeed:
                bot.sendMessage(user_id, helper.formatLicenseNeed(item),
                                reply_markup=menu.keyLib.kbRemoveRequest(idReq=item[0]))
        elif tempMember.register_progress == 305:
            resultSearch = []
            resultSearch = mydb.searchShift(message['text'])
            if len(resultSearch) == 0:
                bot.sendMessage(user_id, msg.messageLib.searchEmptyList.value,
                                reply_markup=menu.keyLib.kbCreateCancelSearchMenu())
                return
            for shiftRow in resultSearch:
                bot.sendMessage(message['chat']["id"], helper.formatShiftMessage(shiftRow),
                                reply_markup=menu.keyLib.kbDelShift(shiftId=shiftRow[9]))
            mydb.member_update_chatid('registration_progress', 10, user_id)
        elif tempMember.register_progress in (304, 301, 302, 303):
            resultSearch = []
            if tempMember.register_progress == 304:
                resultSearch = mydb.searchFounder(message['text'])
            elif tempMember.register_progress == 301:
                resultSearch = mydb.searchStudent(message['text'])
            elif tempMember.register_progress == 303:
                resultSearch = mydb.searchTecnician(message['text'])
            elif tempMember.register_progress == 302:
                resultSearch = mydb.searchAdmin(message['text'])

            if len(resultSearch) == 0:
                bot.sendMessage(user_id, msg.messageLib.searchEmptyList.value,
                                reply_markup=menu.keyLib.kbCreateCancelSearchMenu())
                return
            for item in resultSearch:
                bot.sendMessage(user_id, helper.formatSearchFounder(item, tempMember.register_progress),
                                reply_markup=menu.keyLib.kbCreateOperateSearchMenu(chatId=item[3],
                                                                                   op=tempMember.register_progress))
            mydb.member_update_chatid('registration_progress', 10, user_id)
        elif tempMember.register_progress == 400:
            idDetailShift = mydb.get_member_property_chatid('editMsgId', user_id)
            txtInput = unidecode(message['text'])
            idShift = mydb.get_member_property_chatid('lastShiftId', user_id)
            msgId = mydb.get_shift_property('messageID', idShift)
            if reg.match(r'^([01]\d|2[0-3]):([0-5]\d)-([01]\d|2[0-3]):([0-5]\d)$', txtInput):
                mydb.updateDetailShift('freeTime', txtInput, idDetailShift)
                bot.editMessageText((user_id, msgId), msg.messageLib.freeTimeMsg.value, parse_mode='HTML',
                                    reply_markup=menu.keyLib.createMenuFromListDayForApproveCreatorNew(self=None,
                                                                                                       idShift=idShift,
                                                                                                       ability=3))
                bot.deleteMessage((user_id, message['message_id']))
                mydb.member_update_chatid('registration_progress', 10, user_id)
            else:
                msgInfo = bot.editMessageText((user_id, msgId),
                                              text=f'{txtInput} \n {msg.messageLib.errorFormatTime.value}')
                mydb.shift_update_by_id('messageID', msgInfo['message_id'], idShift)
                bot.deleteMessage((user_id, message['message_id']))
        else:
            bot.deleteMessage((user_id, update['message']['message_id']))
            bot.sendMessage(user_id, msg.messageLib.noBussiness.value)

    elif 'callback_query' in update:
        message = update['callback_query']['message']
        btn = update['callback_query']['data']
        spBtn = btn.split('_')
        print(spBtn)
        if len(spBtn) > 1:
            if spBtn[1] == 'verify':
                verification = mydb.get_member_property_chatid('verifyAdmin', spBtn[2])
                if not (verification == 1 or verification == 3):
                    mydb.member_update_chatid('verifyAdmin', 1, spBtn[2])
                    mydb.member_update_chatid('adminChatId', message['chat']['id'], spBtn[2])
                    bot.sendMessage(spBtn[2], msg.messageLib.congratulationsApproveAdmin.value)
                    mem = mydb.load_member(chatid=spBtn[2])
                    helper.send_operation(tempMember=mem, bot=bot, chatid=spBtn[2])
                    mem = mydb.load_member(spBtn[2])
                    bot.sendMessage(user_id, str(msg.messageLib.verifyMsg.value).format(mem.name + " " + mem.last_name))
                else:
                    bot.sendMessage(user_id, msg.messageLib.doseVerify.value)
            elif spBtn[1] == 'searchMenu':
                bot.sendMessage(user_id, msg.messageLib.searchMessage.value,
                                reply_markup=menu.keyLib.kbCreateSearchMenu())
            elif spBtn[1] == 'regFromFirstStep':
                tempMember.register_progress = 0
                mydb.member_update('registration_progress', 0, user_id)
                bot.sendMessage(user_id, msg.messageLib.noForRegisterUser.value)
            elif spBtn[1] == 'search':
                if spBtn[2] == 'student':
                    mydb.member_update_chatid('registration_progress', 301, user_id)
                    bot.sendMessage(user_id, msg.messageLib.searchMessageStudent.value,
                                    reply_markup=menu.keyLib.kbCreateCancelSearchMenu())
                elif spBtn[2] == 'manager':
                    mydb.member_update_chatid('registration_progress', 302, user_id)
                    bot.sendMessage(user_id, msg.messageLib.searchMessageAdmin.value,
                                    reply_markup=menu.keyLib.kbCreateCancelSearchMenu())
                elif spBtn[2] == 'responsible':
                    mydb.member_update_chatid('registration_progress', 303, user_id)
                    bot.sendMessage(user_id, msg.messageLib.searchMessageTechnician.value,
                                    reply_markup=menu.keyLib.kbCreateCancelSearchMenu())
                elif spBtn[2] == 'founder':
                    mydb.member_update_chatid('registration_progress', 304, user_id)
                    bot.sendMessage(user_id, msg.messageLib.searchMessageFounder.value,
                                    reply_markup=menu.keyLib.kbCreateCancelSearchMenu())
                elif spBtn[2] == 'shift':
                    mydb.member_update_chatid('registration_progress', 305, user_id)
                    bot.sendMessage(user_id, msg.messageLib.searchMessageShift.value,
                                    reply_markup=menu.keyLib.kbCreateCancelSearchMenu())
                elif spBtn[2] == 'licenseEmpty':
                    mydb.member_update_chatid('registration_progress', 306, user_id)
                    bot.sendMessage(user_id, msg.messageLib.searchMessageLicenseEmpty.value,
                                    reply_markup=menu.keyLib.kbCreateCancelSearchMenu())
                elif spBtn[2] == 'licenseNeed':
                    mydb.member_update_chatid('registration_progress', 307, user_id)
                    bot.sendMessage(user_id, msg.messageLib.searchMessageLicenseNeed.value,
                                    reply_markup=menu.keyLib.kbCreateCancelSearchMenu())
            elif spBtn[1] == 'cancelSearch':
                mydb.member_update_chatid('registration_progress', 10, user_id)
                bot.sendMessage(user_id, msg.messageLib.searchCancel.value)
            elif spBtn[1] == 'removeReq':
                mydb.removeReq(idReq=spBtn[2])
                bot.sendMessage(user_id, msg.messageLib.msgRemoveLicense.value)
            elif spBtn[1] == 'licenseNeed':
                mydb.member_update_chatid('registration_progress', 201, user_id)
                bot.sendMessage(user_id, msg.messageLib.licenseNeed.value)
            elif spBtn[1] == 'licenseEmpty':
                mydb.member_update_chatid('registration_progress', 202, user_id)
                bot.sendMessage(user_id, msg.messageLib.licenseEmpty.value)
            elif spBtn[1] == 'listLicenseNeed':
                listNeed = mydb.getListLicenseNeed()
                for item in listNeed:
                    bot.sendMessage(user_id, helper.formatLicenseNeed(item))
                if len(listNeed) == 0:
                    bot.sendMessage(user_id, msg.messageLib.emptyList.value)
            elif spBtn[1] == 'listLicenseEmpty':
                listEmpty = mydb.getListLicenseEmpty()
                for item in listEmpty:
                    bot.sendMessage(user_id, helper.formatLicenseEmpty(item))
                if len(listEmpty) == 0:
                    bot.sendMessage(user_id, msg.messageLib.emptyList.value)
            elif spBtn[1] == 'myListLicense':
                myList = mydb.getMyListLicense(user_id)
                for item in myList:
                    bot.sendMessage(user_id, helper.formatMyLicense(item),
                                    reply_markup=menu.keyLib.kbCreateLicenseMenu(idL=item[0]))
                if len(myList) == 0:
                    bot.sendMessage(user_id, msg.messageLib.emptyList.value)
            elif spBtn[1] == 'Extension':
                mydb.updateLisence('dateExtension', datetime.now(), spBtn[2])
                bot.sendMessage(user_id, msg.messageLib.extensionLicensed.value)
            elif spBtn[1] == 'delLicense':
                mydb.delLisence(1, spBtn[2])
                bot.sendMessage(user_id, msg.messageLib.delLicensed.value)
            elif spBtn[1] == 'noApproveCreator':

                bot.sendMessage(spBtn[3], msg.messageLib.disAcceptShift.value)
                tmr = mydb.get_member_property_chatid('membership_type', spBtn[3])
                helper.send_shift_to_other(bot, spBtn[2], spBtn[3], tmr, 1)
                lstmsg = mydb.getLstMsg(user_id, spBtn[2], spBtn[3])
                if lstmsg is not None:
                    for item in lstmsg:
                        bot.deleteMessage((user_id, item[0]))
                        mydb.delMsg(user_id, item[0])
            elif spBtn[1] == 'sendToCreator':
                creatorChatID = mydb.get_shift_property(fieldName='Creator', idShift=spBtn[2])
                listDayAccept = mydb.getListDaySelection(idShift=spBtn[2], requsterShift=user_id)
                fname = mydb.get_member_property_chatid('name', user_id)
                lname = mydb.get_member_property_chatid('last_name', user_id)
                fullName = fname + ' ' + lname
                if len(listDayAccept) > 0:
                    msgInfo = bot.sendMessage(creatorChatID,
                                              str(msg.messageLib.sendDayForApproveCreator.value).format(fullName))
                    mydb.insertSendMsg(creatorChatID, msgInfo['message_id'], spBtn[2], user_id)
                    helper.send_profile(user_id, bot, creatorChatID, idShift=spBtn[2])
                    msgInfo = bot.sendMessage(creatorChatID,
                                              msg.messageLib.msgCreatror.value,
                                              reply_markup=menu.keyLib.createMenuFromListDayForApproveCreator(None,
                                                                                                              listDayAccept,
                                                                                                              1,
                                                                                                              idShift=
                                                                                                              spBtn[2],
                                                                                                              reqUser=user_id))
                    mydb.insertSendMsg(creatorChatID, msgInfo['message_id'], spBtn[2], user_id)
                else:
                    bot.sendMessage(creatorChatID, str(msg.messageLib.senndAcceptAllDayInShift.value).format(fullName),
                                    reply_markup=menu.keyLib.kbCreateMenuShiftApproveManager(shiftId=spBtn[2]))
            elif spBtn[1] == 'dayApproveCreator':
                ids = str(spBtn[2]).split('=')
                requsterSift = helper.registerDay(ids[0], bot, user_id, ids[1])
                if requsterSift is not None:
                    # bot.sendMessage(requsterSift, msg.messageLib.propertyShiftCreator.value)
                    # helper.send_profile(user_id, bot, requsterSift)
                    bot.sendMessage(user_id, msg.messageLib.requesterNotify.value)

            elif spBtn[1] == 'sendInfoCreator':
                helper.send_profile(spBtn[2], bot, user_id)
            elif spBtn[1] == 'approveAllDay':
                listIdDay = str(spBtn[2]).split('#')
                requsterSift = None
                for item in listIdDay:
                    ids = str(item).split('=')
                    requsterSift = helper.registerDay(ids[0], bot, user_id, ids[1])
                bot.sendMessage(user_id, msg.messageLib.requesterNotify.value)
            elif spBtn[1] == 'editProfile':
                # آماده‌سازی دریافت اطلاعات کاربر جهت ویرایش
                helper.editProfile(bot=bot, spBtn=spBtn, mem=tempMember)
            elif spBtn[1] == 'yesEditProfile':
                bot.sendMessage(user_id, msg.messageLib.selectPropertyForEdit.value,
                                reply_markup=menu.keyLib.kbEditProfile(chatId=user_id))
            elif spBtn[1] == 'noBack':
                # return to end step registration & ready To register shift
                mydb.member_update_chatid('registration_progress', 10, user_id)
                # return to end step register shift
                mydb.member_update_chatid('op', 0, user_id)
                admins = mydb.getAdmins()
                for admin in admins:
                    # senf profile For Admin
                    helper.send_profile(chatid=user_id, bot=bot, forUser=admin[0])
                    # send info for verify Admin
                    bot.sendMessage(admin[0], msg.messageLib.sendAdminAfterEdit.value,
                                    reply_markup=menu.keyLib.kbCreateApproveKey(chat_id=user_id))
                bot.sendMessage(user_id, msg.messageLib.sendToAdminMessage.value)
                # todo: send To Admin
            elif spBtn[1] == 'shiftEMHr':
                hrEmShift = mydb.get_property_domain('hrEmShift')
                bot.sendMessage(user_id, str(msg.messageLib.shiftEMHrLabel.value).format(hrEmShift))
            elif spBtn[1] == 'shiftEmCycle':
                emDay = mydb.get_property_domain('emDay')
                bot.sendMessage(user_id, str(msg.messageLib.shiftEmCycle.value).format(emDay))
            elif spBtn[1] == 'shiftPD':
                TSPDEM = mydb.get_property_domain('TSPDEM')
                PDEM = mydb.get_property_domain('PDEM')
                bot.sendMessage(user_id, str(msg.messageLib.pdLabel.value).format(PDEM, TSPDEM))
            elif spBtn[1] == 'minWFStudent':
                studentWage = mydb.get_property_domain('studentWage')
                bot.sendMessage(user_id, str(msg.messageLib.wfStudenMessage.value).format(studentWage))
            elif spBtn[1] == 'hr':
                hr = mydb.get_property_domain('hrStudent')
                bot.sendMessage(user_id, str(msg.messageLib.changeHour.value).format(hr))
                return None
            elif spBtn[1] == 'minWage':
                wage = mydb.get_property_domain('wage')
                bot.sendMessage(user_id, str(msg.messageLib.changeWage.value).format(wage))
                return None
            elif spBtn[1] == 'licenss':
                licenss = mydb.get_property_domain('wage')
                bot.sendMessage(user_id, str(msg.messageLib.changeLicenss.value).format(licenss))
                return None
            elif spBtn[1] == 'repShift':
                # todo: write function
                helper.msg_get_all_shift_approve(user_id, bot)
            elif spBtn[1] == 'reactive':
                tempMember.delf = 0
                mydb.member_update(fieldName='del', fieldValue=0, chatid=user_id)
                mydb.member_update(fieldName='registration_progress', fieldValue=10, chatid=user_id)
                bot.sendMessage(user_id, msg.messageLib.reActive.value)
                helper.send_profile(user_id, bot)
                helper.send_operation(tempMember, bot, user_id)
            elif spBtn[1] == 'sendMessage':
                bot.sendMessage(user_id, msg.messageLib.whoDoYouSend.value,
                                reply_markup=menu.keyLib.kbcreateSendMessage(chatId=user_id))
            elif spBtn[1] == 'SM':
                if spBtn[2] == '0':  # مدیران
                    mydb.member_update_chatid('registration_progress', 19, user_id)
                    mydb.member_update_chatid('op', 20, user_id)
                elif spBtn[2] == '1':  # موسسان
                    mydb.member_update_chatid('registration_progress', 19, user_id)
                    mydb.member_update_chatid('op', 21, user_id)
                elif spBtn[2] == '2':  # مسئولان فنی
                    mydb.member_update_chatid('registration_progress', 19, user_id)
                    mydb.member_update_chatid('op', 22, user_id)
                elif spBtn[2] == '3':  # دانشجویان
                    mydb.member_update_chatid('registration_progress', 19, user_id)
                    mydb.member_update_chatid('op', 23, user_id)
                elif spBtn[2] == '4':  # همه
                    mydb.member_update_chatid('registration_progress', 19, user_id)
                    mydb.member_update_chatid('op', 24, user_id)
                bot.sendMessage(user_id, msg.messageLib.msgSend.value)
            elif spBtn[1] == 'deny':
                verification = mydb.get_member_property_chatid('verifyAdmin', spBtn[2])
                if not (verification == 1 or verification == 3):
                    bot.sendMessage(message['chat']['id'],
                                    str(msg.messageLib.descDenyAdmin.value))
                    mydb.member_update_chatid('registration_progress', 15, user_id)
                    mydb.member_update_chatid('registration_progress', 15, spBtn[2])
                    mydb.member_update_chatid('adminChatId', user_id, spBtn[2])
                else:
                    bot.sendMessage(user_id, msg.messageLib.doseVerify.value)
            elif spBtn[1] == 'NoDel':
                helper.send_operation(tempMember=tempMember, bot=bot, chatid=message['chat']['id'])
            elif spBtn[1] == 'removeProfile':
                mydb.del_member_chatid(user_id)
                mydb.member_update_chatid('registration_progress', 12, spBtn[2])  # 12 mean is deactivate
                bot.sendMessage(user_id, msg.messageLib.afterDelete.value)
            elif spBtn[1] == 'Del':
                tempMember.delf = 1
                mydb.del_member_chatid(user_id)
                mydb.member_update_chatid('registration_progress', 12, spBtn[2])  # 12 mean is deactivate
                bot.sendMessage(user_id, msg.messageLib.afterDelete.value)
            elif spBtn[1] == 'createShiftEm':
                dateNow = datetime.now()
                date7ago = dateNow - timedelta(days=7)
                TSPDEM = mydb.get_property_domain('TSPDEM')  # تعداد مجاز شیفت در هردوره اضطراری
                PDEM = mydb.get_property_domain('PDEM')  # دوره شیفت اضطراری هر چند روز
                bot.sendMessage(user_id, str(msg.messageLib.emShiftMsgCreate.value).format(PDEM, TSPDEM))
                totalEM = mydb.getTotalShiftEM(date7ago, dateNow, user_id)
                if int(totalEM) < int(TSPDEM):
                    idShift = mydb.create_shift(user_id)
                    mydb.shift_update_by_id('shiftIsEM', 1, idShift)
                    if tempMember.membership_type != 1:
                        msgInfo = bot.sendMessage(user_id, msg.messageLib.promptChoseTypePharmacy.value,
                                                  reply_markup=menu.keyLib.kbTypePharmacyCS(idShift=idShift))
                    else:
                        pharmacyTypeTmp = mydb.get_funder_property('pharmacy_type', user_id)
                        if pharmacyTypeTmp == 'شبانه روزی':
                            mydb.shift_update_by_id('pharmacyType', 1, idShift)
                            msgInfo = helper.send_createShift(bot, user_id, idShift, 1, None, 3, 0)
                            # داروخانه های شبانه روزی با فقط با زمانهای آزاد کار کنند
                            # morning = mydb.get_property_domain('morning')
                            # evening = mydb.get_property_domain('evening')
                            # night = mydb.get_property_domain('night')
                            # msgInfo = bot.sendMessage(user_id,
                            #                           str(msg.messageLib.promptStandardShift.value).format(morning,
                            #                                                                                evening,
                            #                                                                                night),
                            #                           reply_markup=menu.keyLib.kbTypePharmacyTime(idShift=idShift))
                        else:
                            mydb.shift_update_by_id('pharmacyType', 2, idShift)
                            msgInfo = helper.send_createShift(bot, user_id, idShift, 2, None)
                    mydb.shift_update_by_id('messageID', msgInfo['message_id'], idShift)
                    mydb.member_update_chatid('lastShiftId', idShift, user_id)
                else:
                    bot.sendMessage(user_id, msg.messageLib.emShiftFull.value)
                    return
            elif spBtn[1] == 'backwardToEvening':
                idShift = int(spBtn[2])
                sd = str(spBtn[3]).split('#')
                yearC = int(sd[0])
                monthC = int(sd[1])
                dayC = int(sd[2])
                dateEndMonth = None
                if monthC < 12:
                    dateEndMonth = JalaliDate(
                        JalaliDate(yearC, monthC + 1, 1).to_gregorian() - timedelta(days=1))
                else:
                    dateEndMonth = JalaliDate(
                        JalaliDate(yearC + 1, 1, 1).to_gregorian() - timedelta(days=1))
                sde = str(dateEndMonth).split('-')
                getMsgId = mydb.get_shift_property('messageID', spBtn[2])
                msgInfo = helper.sendCalendar(bot, user_id, getMsgId, yearC, monthC, dayC, int(sde[2]), idShift=idShift,
                                              isEm=spBtn[4], typeShift=3, isMorning=0)
            elif spBtn[1] == 'backwardToMorning':
                idShift = int(spBtn[2])
                sd = str(spBtn[3]).split('#')
                yearC = int(sd[0])
                monthC = int(sd[1])
                dayC = int(sd[2])
                dateEndMonth = None
                if monthC < 12:
                    dateEndMonth = JalaliDate(
                        JalaliDate(yearC, monthC + 1, 1).to_gregorian() - timedelta(days=1))
                else:
                    dateEndMonth = JalaliDate(
                        JalaliDate(yearC + 1, 1, 1).to_gregorian() - timedelta(days=1))
                sde = str(dateEndMonth).split('-')
                getMsgId = mydb.get_shift_property('messageID', spBtn[2])
                msgInfo = helper.sendCalendar(bot, user_id, getMsgId, yearC, monthC, dayC, int(sde[2]), idShift=idShift,
                                              isEm=spBtn[4], typeShift=2, isMorning=0)
            elif spBtn[1] == 'createShift':
                idShift = mydb.create_shift(user_id)
                msgInfo = None
                if tempMember.membership_type != 1:
                    msgInfo = bot.sendMessage(user_id, msg.messageLib.promptChoseTypePharmacy.value,
                                              reply_markup=menu.keyLib.kbTypePharmacyCS(idShift=idShift))
                else:
                    pharmacyTypeTmp = mydb.get_funder_property('pharmacy_type', user_id)
                    if pharmacyTypeTmp == 'شبانه روزی':
                        mydb.shift_update_by_id('pharmacyType', 1, idShift)
                        msgInfo = helper.send_createShift(bot, user_id, idShift, 1, None, 3, 2)
                        # داروخانه های شبانه روزی با فقط با زمانهای آزاد کار کنند
                        # helper.send_createShift(bot, user_id, idShift, 2, None, 3, 2)
                        # morning = mydb.get_property_domain('morning')
                        # evening = mydb.get_property_domain('evening')
                        # night = mydb.get_property_domain('night')
                        # msgInfo = bot.sendMessage(user_id,
                        #                           str(msg.messageLib.promptStandardShift.value).format(morning, evening,
                        #                                                                                night),
                        #                           reply_markup=menu.keyLib.kbTypePharmacyTime(idShift=idShift))
                    else:
                        mydb.shift_update_by_id('pharmacyType', 2, idShift)
                        msgInfo = helper.send_createShift(bot, user_id, idShift, 2, None)
                    # msgInfo = mydb.shift_update_by_id('pharmacyType', 1, idShift)
                    # helper.send_createShift(bot, user_id)
                mydb.shift_update_by_id('messageID', msgInfo['message_id'], idShift)
                mydb.member_update_chatid('lastShiftId', idShift, user_id)
            elif spBtn[1] == 'btNightDayCS':
                idShift = spBtn[2]
                mydb.shift_update_by_id('pharmacyType', 1, idShift)
                msgId = mydb.get_shift_property('messageID', idShift)
                isEM = mydb.get_shift_property('shiftIsEM', idShift)
                if isEM == 0:
                    helper.send_createShift(bot, user_id, idShift, 1, msgId, 3, 2)
                elif isEM == 1:
                    helper.send_createShift(bot, user_id, idShift, 1, msgId, 3, 0)
                # idShift = spBtn[2]
                # msgId = mydb.get_shift_property('messageID', idShift)
                # morning = mydb.get_property_domain('morning')
                # evening = mydb.get_property_domain('evening')
                # night = mydb.get_property_domain('night')
                # bot.editMessageText((user_id, msgId),
                #                     str(msg.messageLib.promptStandardShift.value).format(morning, evening, night),
                #                     reply_markup=menu.keyLib.kbTypePharmacyTime(idShift=idShift))
            elif spBtn[1] == 'backToSelectDay':
                idShift = spBtn[2]
                msgId = mydb.get_shift_property('messageID', idShift)
                isEM = mydb.get_shift_property('shiftIsEM', idShift)
                if isEM == 0:
                    helper.send_createShift(bot, user_id, idShift, 2, msgId, 3, 2)
                elif isEM == 1:
                    helper.send_createShift(bot, user_id, idShift, 2, msgId, 3, 0)
            elif spBtn[1] == 'freeTime':
                idShift = spBtn[2]
                mydb.shift_update_by_id('pharmacyType', 1, idShift)
                msgId = mydb.get_shift_property('messageID', idShift)
                isEM = mydb.get_shift_property('shiftIsEM', idShift)
                if isEM == 0:
                    helper.send_createShift(bot, user_id, idShift, 2, msgId, 3, 2)
                elif isEM == 1:
                    helper.send_createShift(bot, user_id, idShift, 2, msgId, 3, 0)
            elif spBtn[1] == 'timeStandard':
                idShift = spBtn[2]
                mydb.shift_update_by_id('pharmacyType', 1, idShift)
                msgId = mydb.get_shift_property('messageID', idShift)
                isEM = mydb.get_shift_property('shiftIsEM', idShift)
                if isEM == 0:
                    helper.send_createShift(bot, user_id, idShift, 2, msgId, 0, 2)
                elif isEM == 1:
                    helper.send_createShift(bot, user_id, idShift, 2, msgId, 0, 0)
            elif spBtn[1] == 'btnNormalCS':
                idShift = spBtn[2]
                mydb.shift_update_by_id('pharmacyType', 2, idShift)
                msgId = mydb.get_shift_property('messageID', idShift)
                isEM = mydb.get_shift_property('shiftIsEM', idShift)
                if isEM == 0:
                    helper.send_createShift(bot, user_id, idShift, 2, msgId, 0, 2)
                elif isEM == 1:
                    helper.send_createShift(bot, user_id, idShift, 2, msgId, 0, 0)
            elif spBtn[1] == 'nextMonth':
                sd = str(spBtn[2]).split('#')
                yearC = int(sd[0])
                monthC = int(sd[1])
                dayC = int(sd[2])
                if monthC == 12:
                    monthC = 1
                    yearC += 1
                else:
                    monthC += 1
                dateEndMonth = None
                if monthC < 12:
                    dateEndMonth = JalaliDate(
                        JalaliDate(yearC, monthC + 1, 1).to_gregorian() - timedelta(days=1))
                else:
                    dateEndMonth = JalaliDate(
                        JalaliDate(yearC + 1, 1, 1).to_gregorian() - timedelta(days=1))
                sde = str(dateEndMonth).split('-')
                getMsgId = mydb.get_shift_property('messageID', spBtn[3])
                msgInfo = helper.sendCalendar(bot, user_id, getMsgId, yearC, monthC, dayC, int(sde[2]), spBtn[3],
                                              isEm=spBtn[5], typeShift=spBtn[4], isMorning=spBtn[6])
                if msgInfo is not None:
                    mydb.shift_update_by_id('messageID', msgInfo["message_id"], spBtn[3])
            elif spBtn[1] == 'previousMonth':
                sd = str(spBtn[2]).split('#')
                yearC = int(sd[0])
                monthC = int(sd[1])
                dayC = int(sd[2])
                if monthC == 1:
                    monthC = 12
                    yearC -= 1
                else:
                    monthC -= 1
                dateEndMonth = None
                if monthC == 12:
                    dateEndMonth = JalaliDate(
                        JalaliDate(yearC + 1, 1, 1).to_gregorian() - timedelta(days=1))
                else:
                    dateEndMonth = JalaliDate(
                        JalaliDate(yearC, monthC + 1, 1).to_gregorian() - timedelta(days=1))
                sde = str(dateEndMonth).split('-')
                getMsgId = mydb.get_shift_property('messageID', spBtn[3])
                msgInfo = helper.sendCalendar(bot, user_id, getMsgId, yearC, monthC, dayC, int(sde[2]), spBtn[3],
                                              isEm=spBtn[5], typeShift=spBtn[4], isMorning=spBtn[6])
                if msgInfo is not None:
                    mydb.shift_update_by_id('messageID', msgInfo["message_id"], spBtn[3])
            elif spBtn[1] == 'newDaySelect':
                idShift = int(spBtn[3])
                selectiveDate = str(spBtn[2]).split('#')
                yearC = int(selectiveDate[0])
                monthC = int(selectiveDate[1])
                dayC = int(selectiveDate[2])
                startDay = int(spBtn[4])
                isEm = int(spBtn[6])
                typeShift = int(spBtn[7])
                isMorning = int(spBtn[8])
                dateEndMonth = None
                if int(monthC) < 12:
                    dateEndMonth = JalaliDate(
                        JalaliDate(yearC, monthC + 1, 1).to_gregorian() - timedelta(days=1))
                else:
                    dateEndMonth = JalaliDate(
                        JalaliDate(yearC + 1, 1, 1).to_gregorian() - timedelta(days=1))
                sde = str(dateEndMonth).split('-')
                fname = ''
                fvalue = ''
                if int(isMorning) == 0:
                    fname = 'morning'
                    fvalue = mydb.get_property_domain('morning')
                elif int(isMorning) == 1:
                    fname = 'evening'
                    fvalue = mydb.get_property_domain('evening')
                elif int(isMorning) == 2:
                    fname = 'night'
                    fvalue = mydb.get_property_domain('night')
                elif int(isMorning) == 3:
                    fname = 'freeTime'
                    fvalue = '?'
                endDay = int(sde[2])
                if idShift == 0:
                    idShift = mydb.shift_update('send', 0, user_id)
                re = mydb.getIdDetailShift(idShift, selectiveDate[0], selectiveDate[1], selectiveDate[2])
                if re is None:
                    re = mydb.registerDetailShift(idShift, selectiveDate[0], selectiveDate[1], selectiveDate[2])
                mydb.updateDetailShift(fname, fvalue, re)
                getMsgId = mydb.get_shift_property('messageID', spBtn[3])
                msgInfo = helper.sendCalendar(bot, user_id, getMsgId, yearC, monthC, startDay, int(endDay), idShift,
                                              isEm, typeShift, isMorning)
                if msgInfo is not None:
                    mydb.shift_update_by_id('messageID', msgInfo["message_id"], spBtn[3])
            elif spBtn[1] == 'removeDay':
                idShift = int(spBtn[3])
                selectiveDate = str(spBtn[2]).split('#')
                yearC = int(selectiveDate[0])
                monthC = int(selectiveDate[1])
                dayC = int(selectiveDate[2])
                startDay = int(spBtn[4])
                isEm = int(spBtn[6])
                typeShift = int(spBtn[7])
                isMorning = int(spBtn[8])
                dateEndMonth = None
                if int(monthC) < 12:
                    dateEndMonth = JalaliDate(
                        JalaliDate(yearC, monthC + 1, 1).to_gregorian() - timedelta(days=1))
                else:
                    dateEndMonth = JalaliDate(
                        JalaliDate(yearC + 1, 1, 1).to_gregorian() - timedelta(days=1))
                sde = str(dateEndMonth).split('-')
                endDay = int(sde[2])
                fname = ''
                if int(isMorning) == 0:
                    fname = 'morning'
                elif int(isMorning) == 1:
                    fname = 'evening'
                elif int(isMorning) == 2:
                    fname = 'night'
                elif int(isMorning) == 3:
                    fname = 'freeTime'

                idDS = mydb.getIdDetailShift(idShift, selectiveDate[0], selectiveDate[1], selectiveDate[2])
                mydb.updateDetailShift(fname, None, idDS)
                mydb.removeDay(idDS)
                getMsgId = mydb.get_shift_property('messageID', spBtn[3])
                msgInfo = helper.sendCalendar(bot, user_id, getMsgId, yearC, monthC, startDay, int(endDay), idShift,
                                              isEm, typeShift, isMorning)
                if msgInfo is not None:
                    mydb.shift_update_by_id('messageID', msgInfo["message_id"], idShift)
            elif spBtn[1] == 'endSelectDay':
                idShift = int(spBtn[2])
                isMorning = int(spBtn[3])
                dateStr = spBtn[4]
                isEm = spBtn[5]
                typeShift = spBtn[6]
                totalDay = mydb.checkTotalDayInShift(idShift)
                typePh = mydb.get_shift_property('pharmacyType', idShift)
                msgId = mydb.get_shift_property('messageID', idShift)
                if isMorning == 0:
                    msgInfo = helper.send_createShift(bot, user_id, idShift, 3, msgId, 1, isEM=isEm)
                    if msgInfo is not None:
                        mydb.shift_update_by_id('messageID', msgInfo["message_id"], idShift)
                elif isMorning == 1 and int(typePh) == 1:
                    msgInfo = helper.send_createShift(bot, user_id, idShift, 4, msgId, 2, isEM=isEm)
                    if msgInfo is not None:
                        mydb.shift_update_by_id('messageID', msgInfo["message_id"], idShift)
                elif isMorning == 3:
                    if totalDay > 0:
                        bot.editMessageText((user_id, msgId), msg.messageLib.freeTimeMsg.value, parse_mode='HTML',
                                            reply_markup=menu.keyLib.createMenuFromListDayForApproveCreatorNew(
                                                self=None,
                                                idShift=idShift,
                                                ability=3))
                    else:
                        bot.editMessageText((user_id, msgId), msg.messageLib.errorTotalDay.value,
                                            reply_markup=menu.keyLib.kbCreateMenuCancelShiftReg(
                                                idShift=f'{idShift}_{isMorning}_{dateStr}_{isEm}_{typeShift}'))
                else:
                    if totalDay > 0:
                        minWag = mydb.get_property_domain('wage')
                        bot.editMessageText((user_id, msgId), f'''{str(msg.messageLib.minWage.value).format(minWag)}\n
                        {msg.messageLib.shiftWage.value}''', parse_mode='HTML')
                        mydb.member_update('lastShiftId', idShift, user_id)
                        mydb.member_update('op', 6, user_id)
                        mydb.member_update('registration_progress', 11, user_id)
                    else:
                        bot.editMessageText((user_id, msgId), msg.messageLib.errorTotalDay.value,
                                            reply_markup=menu.keyLib.kbCreateMenuCancelShiftReg(
                                                idShift=f'{idShift}_{isMorning}_{dateStr}_{isEm}_{typeShift}'))
            elif spBtn[1] == 'ContiReg':
                idShift = spBtn[2]
                sd = str(spBtn[4]).split('#')
                yearC = int(sd[0])
                monthC = int(sd[1])
                dayC = int(sd[2])
                isEM = spBtn[5]
                isMorning = spBtn[3]
                typeShift = spBtn[6]
                dateEndMonth = None
                if monthC < 12:
                    dateEndMonth = JalaliDate(
                        JalaliDate(yearC, monthC + 1, 1).to_gregorian() - timedelta(days=1))
                else:
                    dateEndMonth = JalaliDate(
                        JalaliDate(yearC + 1, 1, 1).to_gregorian() - timedelta(days=1))
                sde = str(dateEndMonth).split('-')
                getMsgId = mydb.get_shift_property('messageID', idShift)
                msgInfo = helper.sendCalendar(bot, user_id, getMsgId, yearC, monthC, dayC, int(sde[2]), idShift,
                                              isEm=isEM, typeShift=typeShift, isMorning=isMorning)
            elif spBtn[1] == 'cancelReg':
                idShift = spBtn[2]
                getMsgId = mydb.get_shift_property('messageID', idShift)
                mydb.deleteShift(idShift)
                bot.editMessageText((user_id, getMsgId), msg.messageLib.cancelShiftMsg.value)
                helper.send_operation(tempMember, bot, user_id)
            elif spBtn[1] == 'continueRegShif':
                idShift = int(spBtn[2])
                totalEmptyDay = mydb.checkNoneTimeDayInFreeTime(idShift)
                msgId = mydb.get_shift_property('messageID', idShift)
                if totalEmptyDay > 0:
                    bot.editMessageText((user_id, msgId), str(msg.messageLib.errorConti.value).format(totalEmptyDay),
                                        reply_markup=menu.keyLib.kbCreateMenuErrorConti(idShift=idShift))
                else:
                    minWag = mydb.get_property_domain('wage')
                    bot.editMessageText((user_id, msgId), f'''{str(msg.messageLib.minWage.value).format(minWag)}\n
{msg.messageLib.shiftWage.value}''', parse_mode='HTML')
                    mydb.member_update('lastShiftId', idShift, user_id)
                    mydb.member_update('op', 6, user_id)
                    mydb.member_update('registration_progress', 11, user_id)
            elif spBtn[1] == 'erroConti':
                idShift = int(spBtn[2])
                msgId = mydb.get_shift_property('messageID', idShift)
                bot.editMessageText((user_id, msgId), msg.messageLib.freeTimeMsg.value, parse_mode='HTML',
                                    reply_markup=menu.keyLib.createMenuFromListDayForApproveCreatorNew(self=None,
                                                                                                       idShift=idShift,
                                                                                                       ability=3))
            elif spBtn[1] == 'enterTime':
                idShift = int(spBtn[2])
                msgId = mydb.get_shift_property('messageID', idShift)
                dateDetail = spBtn[4]
                msgInfo = bot.editMessageText((user_id, msgId), str(msg.messageLib.enterTime.value).format(dateDetail),
                                              parse_mode='HTML')
                mydb.shift_update_by_id('messageID', msgInfo['message_id'], idShift)
                mydb.member_update_chatid('registration_progress', 400, user_id)
                mydb.member_update_chatid('editMsgId', spBtn[3], user_id)
            elif spBtn[1] == 'year':
                if tempMember.register_progress not in (11, 5):
                    bot.sendMessage(user_id, msg.messageLib.noBussiness.value)
                    return
                yearTemp = None
                todayDate = datetime.today()
                jd = str(JalaliDate.to_jalali(todayDate.year, todayDate.month, todayDate.day)).split('-')
                if spBtn[2] == 'currntYear':
                    yearTemp = int(jd[0])
                else:
                    yearTemp = int(jd[0]) + 1
                if spBtn[3] == '1':
                    rowid = mydb.shift_update('DateShift', yearTemp, user_id)
                    bot.sendMessage(chat_id=user_id, parse_mode='HTML', text='ماه انتخاب کنید',
                                    reply_markup=menu.keyLib.kbCreateMenuMonthInYear(tag='1_{}'.format(rowid)))
                elif spBtn[3] == '6':
                    rowid = mydb.shift_update('DateShift', yearTemp, user_id)
                    mydb.shift_update_by_id('shiftIsEM', 1, rowid)
                    bot.sendMessage(chat_id=user_id, parse_mode='HTML', text='ماه انتخاب کنید',
                                    reply_markup=menu.keyLib.kbCreateMenuMonthInYear(tag='1_{}'.format(rowid)))
                elif spBtn[3] == '2':
                    mydb.shift_update_by_id('dateEndShift', yearTemp, spBtn[4])
                    bot.sendMessage(chat_id=user_id, parse_mode='HTML', text='ماه انتخاب کنید',
                                    reply_markup=menu.keyLib.kbCreateMenuMonthInYear(tag='2_{}'.format(spBtn[4])))
                elif spBtn[3] == '4':
                    mydb.student_update('start_date', yearTemp, user_id)
                    bot.sendMessage(chat_id=user_id, parse_mode='HTML', text='ماه انتخاب کنید',
                                    reply_markup=menu.keyLib.kbCreateMenuMonthInYear(tag='4_{}'.format(user_id)))
                elif spBtn[3] == '5':
                    mydb.student_update('end_date', yearTemp, user_id)
                    bot.sendMessage(chat_id=user_id, parse_mode='HTML', text='ماه انتخاب کنید',
                                    reply_markup=menu.keyLib.kbCreateMenuMonthInYear(tag='5_{}'.format(user_id)))
            elif spBtn[1] == 'month':
                if tempMember.register_progress not in (11, 5):
                    bot.sendMessage(user_id, msg.messageLib.noBussiness.value)
                    return
                if spBtn[3] == '1':
                    year = mydb.get_shift_property(fieldName='DateShift', idShift=spBtn[4])
                    if len(year) != 4:
                        bot.sendMessage(user_id, msg.messageLib.noBussiness.value)
                        return
                    mydb.shift_update_by_id('DateShift', '{0}-{1}'.format(year, spBtn[2]), spBtn[4])
                    bot.sendMessage(chat_id=user_id, parse_mode='HTML', text='روز انتخاب کنید',
                                    reply_markup=menu.keyLib.kbCreateMenuDayInMonth(tag='1_{}'.format(spBtn[4])))
                elif spBtn[3] == '2':
                    year = mydb.get_shift_property(fieldName='dateEndShift', idShift=spBtn[4])
                    if len(year) != 4:
                        bot.sendMessage(user_id, msg.messageLib.noBussiness.value)
                        return
                    mydb.shift_update_by_id('dateEndShift', '{0}-{1}'.format(year, spBtn[2]), spBtn[4])
                    bot.sendMessage(chat_id=user_id, parse_mode='HTML', text='روز انتخاب کنید',
                                    reply_markup=menu.keyLib.kbCreateMenuDayInMonth(tag='2_{}'.format(spBtn[4])))
                elif spBtn[3] == '4':
                    year = mydb.get_student_property(fieldName='start_date', chatid=user_id)
                    if len(year) != 4:
                        bot.sendMessage(user_id, msg.messageLib.noBussiness.value)
                        return
                    mydb.student_update('start_date', '{0}{1}'.format(year, spBtn[2]), user_id)
                    bot.sendMessage(chat_id=user_id, parse_mode='HTML', text='روز انتخاب کنید',
                                    reply_markup=menu.keyLib.kbCreateMenuDayInMonth(tag='4_{}'.format(user_id)))
                elif spBtn[3] == '5':
                    year = mydb.get_student_property(fieldName='end_date', chatid=user_id)
                    if len(year) != 4:
                        bot.sendMessage(user_id, msg.messageLib.noBussiness.value)
                        return
                    mydb.student_update('end_date', '{0}{1}'.format(year, spBtn[2]), user_id)
                    bot.sendMessage(chat_id=user_id, parse_mode='HTML', text='روز انتخاب کنید',
                                    reply_markup=menu.keyLib.kbCreateMenuDayInMonth(tag='5_{}'.format(user_id)))
            elif spBtn[1] == 'day':
                if tempMember.register_progress not in (11, 5):
                    bot.sendMessage(user_id, msg.messageLib.noBussiness.value)
                    return
                if spBtn[3] == '1':
                    year = mydb.get_shift_property(fieldName='DateShift', idShift=spBtn[4])
                    if len(year) > 7:
                        bot.sendMessage(user_id, msg.messageLib.noBussiness.value)
                        return
                    mydb.shift_update('DateShift', '{0}-{1}'.format(year, spBtn[2]), user_id)
                    yearIn = int(str(year)[0:4])
                    monthIn = int(str(year)[5:7])
                    dayIn = int(str(spBtn[2]))
                    dateMiladiIn = JalaliDate(yearIn, monthIn, dayIn).to_gregorian()
                    todayDate = datetime.today()
                    diffDay = relativedelta(dateMiladiIn, todayDate).days
                    if diffDay >= 0:
                        mydb.member_update('op', 1, message['chat']['id'])
                        mydb.shift_update('DateShift', '{0}-{1}'.format(year, spBtn[2]), message['chat']['id'])
                        bot.sendMessage(message['chat']['id'],
                                        'آیا {0} بعنوان تاریخ آغاز شیفت صحیح است؟'.format(
                                            '{0}-{1}'.format(year, spBtn[2])),
                                        reply_markup=menu.keyLib.kbCreateMenuYesNO(
                                            chatId='{}'.format(spBtn[4])))
                    else:
                        bot.sendMessage(message['chat']['id'], msg.messageLib.invalidDate.value)
                        bot.sendMessage(message['chat']['id'], msg.messageLib.dateShift.value)
                        bot.sendMessage(chat_id=user_id, parse_mode='HTML', text='سال را کنید',
                                        reply_markup=menu.keyLib.kbCreateMenuYear(tag=1))
                elif spBtn[3] == '2':
                    year = mydb.get_shift_property(fieldName='dateEndShift', idShift=spBtn[4])
                    if len(year) > 7:
                        bot.sendMessage(user_id, msg.messageLib.noBussiness.value)
                        return
                    mydb.shift_update_by_id('dateEndShift', '{0}-{1}'.format(year, spBtn[2]), spBtn[4])
                    yearIn = int(str(year)[0:4])
                    monthIn = int(str(year)[5:7])
                    dayIn = int(str(spBtn[2]))
                    dateMiladiIn = JalaliDate(yearIn, monthIn, dayIn).to_gregorian()
                    todayDate = datetime.today()
                    diffDay = relativedelta(dateMiladiIn, todayDate).days
                    if diffDay >= 0:
                        mydb.member_update('op', 13, message['chat']['id'])
                        mydb.shift_update('dateEndShift', '{0}-{1}'.format(year, spBtn[2]), message['chat']['id'])
                        bot.sendMessage(message['chat']['id'],
                                        'آیا {0} بعنوان تاریخ پایان شیفت صحیح است؟'.format(
                                            '{0}-{1}'.format(year, spBtn[2])),
                                        reply_markup=menu.keyLib.kbCreateMenuYesNO(
                                            chatId='{}'.format(spBtn[4])))
                    else:
                        bot.sendMessage(message['chat']['id'], msg.messageLib.invalidDate.value)
                        bot.sendMessage(message['chat']['id'], msg.messageLib.dateShift.value)
                        bot.sendMessage(chat_id=user_id, parse_mode='HTML', text='سال را کنید',
                                        reply_markup=menu.keyLib.kbCreateMenuYear(tag=2))
                elif spBtn[3] == '4':
                    year = mydb.get_student_property(fieldName='start_date', chatid=user_id)
                    if len(year) > 7:
                        bot.sendMessage(user_id, msg.messageLib.noBussiness.value)
                        return
                    mydb.student_update('start_date', '{0}{1}'.format(year, spBtn[2]), user_id)
                    if tempMember.register_progress != 18:  # 18 is Edit Mode
                        bot.sendMessage(message['chat']['id'],
                                        str(msg.messageLib.enterLicenseEndDate.value))
                        bot.sendMessage(chat_id=user_id, parse_mode='HTML', text='سال را انتخاب کنید',
                                        reply_markup=menu.keyLib.kbCreateMenuYear(tag=5))
                        mydb.member_update_chatid('registration_progress', 5, user_id)
                        tempMember.register_progress = 5
                    else:
                        mydb.member_update_chatid(fieldName='verifyAdmin', fieldValue=0, chatid=user_id)
                        # send message to user
                        bot.sendMessage(user_id, msg.messageLib.afterEdit.value,
                                        reply_markup=menu.keyLib.kbVerifyEditProfile(self=None, tag=user_id))
                elif spBtn[3] == '5':
                    year = mydb.get_student_property(fieldName='end_date', chatid=user_id)
                    if len(year) > 7:
                        bot.sendMessage(user_id, msg.messageLib.noBussiness.value)
                        return
                    mydb.student_update('end_date', '{0}{1}'.format(year, spBtn[2]), user_id)
                    # bot.sendMessage(message['chat']['id'],
                    #                 str(msg.messageLib.enterWorkoverPermitPhoto.value))

                    if tempMember.register_progress != 18:  # 18 is Edit Mode
                        bot.sendMessage(user_id, msg.messageLib.hrPermitTotal.value)
                        mydb.member_update_chatid('registration_progress', 5, user_id)
                        tempMember.register_progress = 5
                    else:
                        mydb.member_update_chatid(fieldName='verifyAdmin', fieldValue=0, chatid=user_id)
                        # send message to user
                        bot.sendMessage(user_id, msg.messageLib.afterEdit.value,
                                        reply_markup=menu.keyLib.kbVerifyEditProfile(self=None, tag=user_id))
            elif spBtn[1] == 'yes':
                if tempMember.register_progress != 11:
                    bot.sendMessage(user_id, msg.messageLib.noBussiness.value)
                    return
                opBtn = int(spBtn[2])
                op = mydb.get_member_property_chatid('op', message['chat']['id'])
                if (int(op) - int(opBtn)) > 1:
                    bot.sendMessage(user_id, msg.messageLib.erroOnBack.value)
                if int(op) == 1:
                    dateStartShift = mydb.get_shift_property('DateShift', spBtn[2])
                    dateStart = JalaliDate(int(dateStartShift[:4]), int(dateStartShift[5:7]),
                                           int(dateStartShift[8:])).to_gregorian()
                    dateStart = datetime.combine(dateStart, time())
                    dateNow = datetime.now()
                    diffDay = relativedelta(dateStart, dateNow)
                    hrEmShift = mydb.get_property_domain(
                        'hrEmShift')  # از این زمان برای تشخیص شیفت اضطراری استفاده می شود
                    # todo: Remove Print command
                    if ((diffDay.days * 24) + diffDay.hours) <= int(hrEmShift):
                        date7ago = dateNow - timedelta(days=7)
                        TSPDEM = mydb.get_property_domain('TSPDEM')  # تعداد مجاز شیفت در هردوره اضطراری
                        PDEM = mydb.get_property_domain('PDEM')  # دوره شیفت اضطراری هر چند روز
                        bot.sendMessage(user_id, str(msg.messageLib.emShiftMsg.value).format(PDEM, TSPDEM))
                        helper.send_operation(tempMember, bot, user_id)
                        mydb.removeShiftFromTable(spBtn[2])
                        mydb.member_update('op', 0, user_id)
                        mydb.member_update('registration_progress', 10, message['chat']['id'])
                        return
                    else:
                        bot.sendMessage(message['chat']['id'], msg.messageLib.enterDateEnd.value)
                        bot.sendMessage(chat_id=user_id, parse_mode='HTML', text='سال را کنید',
                                        reply_markup=menu.keyLib.kbCreateMenuYear(tag='2_{}'.format(spBtn[2])))
                        mydb.member_update('op', 13, message['chat']['id'])
                if int(op) == 13:
                    bot.sendMessage(message['chat']['id'], msg.messageLib.shiftStartTime.value)
                    mydb.member_update('op', 2, message['chat']['id'])
                if int(op) == 3:
                    bot.sendMessage(message['chat']['id'], msg.messageLib.shiftEndTime.value)
                    mydb.member_update('op', 4, message['chat']['id'])
                if int(op) == 5:
                    minWage = mydb.get_property_domain('wage')
                    bot.sendMessage(user_id, str(msg.messageLib.minWage.value).format(minWage))
                    bot.sendMessage(message['chat']['id'], msg.messageLib.shiftWage.value)
                    mydb.member_update('op', 6, message['chat']['id'])
                if int(op) == 7:
                    minWage = mydb.get_property_domain('studentWage')
                    bot.sendMessage(user_id, str(msg.messageLib.minWFStudent.value).format(minWage))
                    bot.sendMessage(message['chat']['id'], msg.messageLib.shiftWageStudent.value)
                    mydb.member_update('op', 8, message['chat']['id'])
                if int(op) == 9:
                    bot.sendMessage(message['chat']['id'], msg.messageLib.pharmacyAddress.value)
                    addressPharmacy = None
                    if tempMember.membership_type == 1:
                        addressPharmacy = mydb.get_funder_property('pharmacy_address', message['chat']['id'])
                        idShift = mydb.get_member_property_chatid('lastShiftId', user_id)
                        rs = mydb.shift_update_by_id('pharmacyAddress', addressPharmacy, idShift)
                    if addressPharmacy is not None:
                        bot.sendMessage(message['chat']['id'],
                                        'آیا آدرس {0} برای داروخانه صحیح است؟'.format(addressPharmacy),
                                        reply_markup=menu.keyLib.kbCreateMenuYesNO(
                                            chatId='{0}_{1}'.format(11, idShift)))
                        mydb.member_update('op', 11, message['chat']['id'])
                    else:
                        mydb.member_update('op', 10, message['chat']['id'])
                if int(op) == 11:
                    # Send Shift to All Technical Responsible
                    idShift = mydb.get_member_property_chatid('lastShiftId', user_id)
                    mydb.setMinMaxDate(idShift)
                    hrSendToStudent = mydb.get_property_domain('hrStudent')
                    helper.send_shift_to_technicalResponsible(idShift, bot, user_id, 2)
                    isShiftEm = mydb.get_shift_property('shiftIsEM', idShift)
                    if int(isShiftEm) == 1:
                        helper.send_shift_to_studentEM(spBtn[3], bot, user_id)
                        bot.sendMessage(user_id,
                                        str(msg.messageLib.msgIsEm.value))
                    else:
                        bot.sendMessage(user_id,
                                        str(msg.messageLib.endRegisterShift.value).format(hrSendToStudent))
                    mydb.member_update('registration_progress', 10, user_id)
                    mydb.member_update('op', 0, user_id)
                    mydb.member_update('editMsgId', '', user_id)
                    mydb.shift_update_by_id('progress', 2, idShift)
            elif spBtn[1] == 'NO':
                if tempMember.register_progress != 11:
                    bot.sendMessage(user_id, msg.messageLib.noBussiness.value)
                    return
                opBtn = int(spBtn[2])
                op = mydb.get_member_property_chatid('op', message['chat']['id'])
                if (int(op) - int(opBtn)) > 1:
                    bot.sendMessage(user_id, msg.messageLib.erroOnBack.value)
                    return
                if int(op) == 1:
                    mydb.member_update('op', 0, message['chat']['id'])
                    bot.sendMessage(message['chat']['id'], msg.messageLib.dateShift.value)
                    bot.sendMessage(chat_id=user_id, parse_mode='HTML', text='سال را کنید',
                                    reply_markup=menu.keyLib.kbCreateMenuYear(tag=1))
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
                    bot.sendMessage(message['chat']['id'], msg.messageLib.shiftWageStudent.value)
                if int(op) == 11:
                    mydb.member_update('op', 10, message['chat']['id'])
                    bot.sendMessage(message['chat']['id'], msg.messageLib.enterPharmacyAddress.value)
            elif spBtn[1] == 'ownerShift':
                dateF = JalaliDate.today().strftime("%Y.%m.%d")
                listShift = mydb.getShiftList(requsterShift=user_id, startDate=dateF)
                for item in listShift:
                    bot.sendMessage(user_id, helper.formatMyShift(item))
                if len(listShift) == 0:    bot.sendMessage(user_id, msg.messageLib.emptyList.value)
            elif spBtn[1] == 'listSift':
                allShift = mydb.get_all_shift_by_creator(creator=user_id)
                if len(allShift) == 0:
                    bot.sendMessage(user_id, msg.messageLib.emptyList.value)
                else:
                    for shiftRow in allShift:
                        bot.sendMessage(user_id, helper.formatShiftMessage(shiftRow),
                                        reply_markup=menu.keyLib.createMenuFromListDayForApproveCreatorNew(
                                            self=None,
                                            idShift=shiftRow[9]))
            elif spBtn[1] == 'epf':
                bot.sendMessage(user_id, msg.messageLib.editMessag.value)
                helper.send_profile(chatid=user_id, bot=bot)
                bot.sendMessage(user_id, msg.messageLib.confirmEdit.value,
                                reply_markup=menu.keyLib.kbEditProfile(self=None, chatId=user_id))
            # پذیرش شخصی که شیفت را رزرو کرده است
            elif spBtn[1] == 'approveShiftFunder':
                requester = mydb.get_shift_property(fieldName='approver', idShift=spBtn[2])
                shiftRow = mydb.get_all_property_shift_byId(spBtn[2])
                mydb.shift_update_by_id('progress', 4, spBtn[2])
                bot.sendMessage(requester, msg.messageLib.acceptShift.value)
                bot.sendMessage(requester, helper.formatShiftMessage(shiftRow))
                bot.sendMessage(user_id, msg.messageLib.requesterNotify.value)
                # آپدیت کردن شیف
            elif spBtn[1] == 'cancelShift':
                # ارسال شیفت هایی که شخص قبول کرده و تاریخ آنها نرسیده
                todayDate = datetime.today()
                jd = str(JalaliDate.to_jalali(todayDate.year, todayDate.month, todayDate.day)).split('-')
                sjd = "{0}{1}{2}".format(jd[0], jd[1], jd[2])
                helper.send_list_shift_Cancel(chatId=message['chat']['id'], bot=bot, todayDate=sjd)
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
                tmr = mydb.get_member_property_chatid('membership_type', requester)
                bot.sendMessage(requester, msg.messageLib.disAcceptShift.value)
                helper.send_shift_to_other(bot, spBtn[2], requester, tmr, 1)
                lstMsg = mydb.getLstMsg(user_id, spBtn[2], requester)
                for item in lstMsg:
                    try:
                        bot.deleteMessage((user_id, item[0]))
                        mydb.delMsg(user_id, item[0])
                    except:
                        print(f'error item:{item}')
                        continue
            # آپدیت کردن شیفت
            #             پس از فشردن کلید شیفت را می پذیرم اجرا می شود
            elif spBtn[1] == 'shiftApprove':
                shiftIsFull = mydb.get_shift_property('progress', spBtn[2])
                if int(shiftIsFull) == 4:
                    bot.sendMessage(user_id, msg.messageLib.shiftIsFull.value)
                    return
                # todo: new approve shift
                tds = mydb.getTotalDayShift(spBtn[2], 1)
                emptyDay = mydb.getTotalDayShift(spBtn[2], 0)
                if emptyDay > 0:
                    # if tds == 0:
                    #     bot.sendMessage(user_id, str(msg.messageLib.shiftTotalDay.value).format(emptyDay),
                    #                     reply_markup=menu.keyLib.kbApproveAllShiftYesNO(shiftId=spBtn[2]))
                    # else:
                    helper.NOApproveAllShift(spBtn[2], user_id, bot)
                else:
                    mydb.shift_update_by_id('progress', 4, spBtn[2])
                    bot.sendMessage(user_id, msg.messageLib.shiftIsFull.value)
                    return
            elif spBtn[1] == 'endSelection':
                helper.endSelectionDayBtnClick(spBtn[2], user_id, bot)
            elif spBtn[1] == 'daySelectedRemove':
                idShift = mydb.getIdShiftFromDay(spBtn[2])
                mydb.removeFromSelection(spBtn[2])
                helper.endSelectionDayBtnClick(idShift, user_id, bot)
            elif spBtn[1] == 'dayShift':
                idShift = spBtn[2]
                dateStr = spBtn[4]
                idDetailShift = spBtn[3]
                ft = spBtn[5]
                if mydb.isShiftDayFull(idDetailShift, ft) > 0:
                    bot.sendMessage(user_id, str(msg.messageLib.shiftDayIsFull.value))
                    return
                tmpRes = mydb.registerDayShift(idShift, dateStr, user_id, 0, idDetailShift, ft=ft)
                if tmpRes != 0:
                    bot.sendMessage(user_id, str(msg.messageLib.afterDaySelction.value).format(dateStr))
                else:
                    bot.sendMessage(user_id, str(msg.messageLib.repeatedDay.value))
            elif spBtn[1] == 'NOApproveAllShift':
                helper.NOApproveAllShift(spBtn[2], user_id, bot)
            elif spBtn[1] == 'yesApproveAllShift':
                shiftIsFull = mydb.get_shift_property('progress', spBtn[2])
                if int(shiftIsFull) != 4:
                    helper.yesApproveAllShift(spBtn[2], user_id, bot)
                else:
                    bot.sendMessage(user_id, msg.messageLib.shiftIsFull.value)
            elif spBtn[1] == 'confirmSendToAll':
                creator = mydb.get_shift_property('Creator', spBtn[2])
                helper.send_shift_to_technicalResponsible(int(spBtn[2]), bot, creator, 2)
                bot.sendMessage(user_id, msg.messageLib.msgSendToTechnician.value)
                helper.send_shift_to_studentEM(spBtn[2], bot, creator)
                bot.sendMessage(user_id, msg.messageLib.msgSendToStudent.value)
            elif spBtn[1] == 'confirmSendToStudent':
                creator = mydb.get_shift_property('Creator', spBtn[2])
                helper.send_shift_to_studentEM(spBtn[2], bot, creator)
                bot.sendMessage(user_id, msg.messageLib.msgSendToStudent.value)
            elif spBtn[1] == 'confirmSendToTechnician':
                creator = mydb.get_shift_property('Creator', spBtn[2])
                helper.send_shift_to_technicalResponsible(int(spBtn[2]), bot, creator, 2)
                bot.sendMessage(user_id, msg.messageLib.msgSendToTechnician.value)
            elif spBtn[1] == 'DelShiftAdmin':
                if tempMember.membership_type != 4:
                    bot.sendMessage(user_id, msg.messageLib.userIsNotAdmin.value)
                    return
                if mydb.deleteShift(idShift=spBtn[2]) == 1:
                    bot.sendMessage(user_id, msg.messageLib.delShiftAdminMsg.value)
                else:
                    print('error')
            elif spBtn[1] == 'deleteShift':
                allShift = mydb.get_all_shift_by_creator(creator=message['chat']["id"])
                if len(allShift) == 0:
                    bot.sendMessage(message['chat']["id"], msg.messageLib.emptyList.value)
                else:
                    for shiftRow in allShift:
                        bot.sendMessage(message['chat']["id"], helper.formatShiftMessage(shiftRow) +
                                        msg.messageLib.deleteMessage.value,
                                        reply_markup=menu.keyLib.kbCreateMenuDeleteShift(shiftId=shiftRow[9]))
            elif spBtn[1] == 'DeleteShiftList':  # فشردن دکمه حذف شیفت
                # todo: اگر شیفت پر است برای افرادی که شیف را پر کرده اند پیام بفرستد
                bot.sendMessage(user_id, msg.messageLib.confirmDeleteShift.value,
                                reply_markup=menu.keyLib.kbCreateMenuConfirmDelete(shiftId=spBtn[2]))

            elif spBtn[1] == 'confirmDelete':  # تائیدیه پاک کردن شیفت توسط مدیر سیستم
                mydb.shift_update_by_id(fieldName='del', fieldValue='1', idshift=spBtn[2])
                listDay = mydb.getListDayIsNotEmpty(spBtn[2], None)

                for item in listDay:
                    bot.sendMessage(item[2], str(msg.messageLib.cancelShiftFromCreator.value).format(item[1]))
                bot.sendMessage(user_id, msg.messageLib.delShiftMessage.value)
            elif spBtn[1] == 'listSiftManager':
                allShift = mydb.get_all_shift_manager()
                if len(allShift) == 0:
                    bot.sendMessage(message['chat']["id"], msg.messageLib.emptyList.value)
                else:
                    df = pd.DataFrame(allShift,
                                      columns=['ایجاد کننده شیفت', 'کد', 'تاریخ شروع', 'ساعت شروع', 'ساعت پایان',
                                               'دستمزد',
                                               'آدرس داروخانه', 'پیشرفت', 'تائید کننده', 'شناسه شیفت', 'تایخ پایان',
                                               'دسمزد دانشجو', 'تاریخ ثبت'])
                    df1 = df.iloc[:, [0, 12, 2, 10, 3, 4, 5, 11, 6]]
                    df1.to_excel('list.xlsx', sheet_name='لیست شیفت ها')
                    doc = 'list.xlsx'
                    isExisting = os.path.exists(doc)
                    if isExisting:
                        bot.sendDocument(user_id, open(doc, 'rb'))
                    bot.sendMessage(message['chat']["id"], msg.messageLib.diver.value)
                    for shiftRow in allShift:
                        bot.sendMessage(message['chat']["id"], helper.formatShiftMessage(shiftRow))
            elif spBtn[1] == 'approveShiftManager':
                mydb.shift_update_by_id(fieldName='progress', fieldValue=2, idshift=spBtn[2])
                approver = mydb.get_shift_property('approver', spBtn[2])
                if approver is not None:
                    bot.sendMessage(approver, msg.messageLib.shiftApprovedByManager.value)
                    helper.registerFullShiftDay(spBtn[2], approver)
                    bot.sendMessage(user_id, msg.messageLib.requesterNotify.value)
            elif spBtn[1] == 'disApproveShiftManager':
                approver = mydb.get_shift_property('approver', spBtn[2])
                bot.sendMessage(approver, msg.messageLib.shiftDisApprovedByManager.value)
                bot.sendMessage(user_id, msg.messageLib.requesterNotify.value)
            elif spBtn[1] == 'listFunderManager':
                result = mydb.get_all_member(type=1)
                df = pd.DataFrame(result,
                                  columns=['نام', 'نوع عضویت', 'شماره همراه', 'نام داروخانه', 'نام داروخانه', 'آدرس',
                                           'وضعیت'])
                df.to_excel('list.xlsx', sheet_name='لیست موسسان')
                doc = 'list.xlsx'
                isExisting = os.path.exists(doc)
                if isExisting:
                    bot.sendDocument(user_id, open(doc, 'rb'))
                if len(result) > 0:
                    for item in result:
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
                result = mydb.get_all_member(type=2)
                df = pd.DataFrame(result, columns=['نام', 'نوع عضویت', 'شماره همراه', 'شماره ملی', 'وضعیت'])
                df.to_excel('list.xlsx', sheet_name='لیست مسئولان فنی')
                doc = 'list.xlsx'
                isExisting = os.path.exists(doc)
                if isExisting:
                    bot.sendDocument(user_id, open(doc, 'rb'))
                if len(result) > 0:
                    for item in result:
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
                result = mydb.get_all_member(type=3)
                df = pd.DataFrame(result,
                                  columns=['نام', 'نوع عضویت', 'شماره همراه', 'کدملی', 'تاریخ شروع', 'تاریخ پایان',
                                           'نوع داروخانه',
                                           'میزان مجوز ساعت', 'ساعت استفاده شده', 'وضعیت'])
                df.to_excel('list.xlsx', sheet_name='لیست دانشجویان')
                doc = 'list.xlsx'
                isExisting = os.path.exists(doc)
                if isExisting:
                    bot.sendDocument(user_id, open(doc, 'rb'))
                if len(result) > 0:
                    for item in result:
                        itemRow1 = 'نام و نام خانوادگی:{}'.format(item[0])
                        itemRow2 = 'نوع عضویت:{}'.format(item[1])
                        itemRow3 = 'شماره همراه:{}'.format(item[2])
                        bot.sendMessage(message['chat']['id'], '''
{0}
{1}
{2}'''.format(itemRow1, itemRow2, itemRow3))
                else:
                    bot.sendMessage(message['chat']['id'], msg.messageLib.emptyList.value)
            elif spBtn[1] == 'operateAdmin':
                if spBtn[2] == 'disable':
                    mydb.member_update_chatid('del', 1, spBtn[3])
                    bot.sendMessage(user_id, msg.messageLib.disableUser.value)
                elif spBtn[2] == 'enable':
                    mydb.member_update_chatid('del', 0, spBtn[3])
                    bot.sendMessage(user_id, msg.messageLib.enableUser.value)
                elif spBtn[2] == 'remove':
                    mydb.del_member_chatid(spBtn[3])
                    bot.sendMessage(user_id, msg.messageLib.removeUser.value)
            elif spBtn[1] == 'operate':
                helper.send_profile(spBtn[2], bot, user_id)
                bot.sendMessage(user_id, 'عملیات در دسترس',
                                reply_markup=menu.keyLib.kbCreateOperateAdminForUser(chatId=spBtn[2]))
        if btn == 'btnFounder':
            if tempMember.register_progress == 18 and tempMember.op == 16:
                mydb.member_update_chatid('membership_type', 1, user_id)
                mydb.member_update_chatid(fieldName='verifyAdmin', fieldValue=0, chatid=user_id)
                # send message to user
                if not mydb.checkExsistDetail(tempMember, 1):
                    bot.sendMessage(user_id, msg.messageLib.enterPharmacyName.value)
                    mydb.member_update_chatid('registration_progress', 4, user_id)
                else:
                    bot.sendMessage(user_id, msg.messageLib.oldInfo.value)
                    helper.send_profile(chatid=user_id, bot=bot)
                    bot.sendMessage(user_id, msg.messageLib.confirmEdit.value,
                                    reply_markup=menu.keyLib.kbEditProfile(self=None, chatId=user_id))
            elif tempMember.register_progress == 0 and tempMember.op == 0:
                tempMember.userName = userName
                tempMember.lastMessage = update['update_id']
                tempMember.membership_type = 1
                tempMember.chatId = update['callback_query']['chat_instance']
                tempMember.register_progress = 1
                mydb.member_update_chatid('membership_type', 1, message['chat']['id'])
                mydb.member_update_chatid('chat_id', user_id, message['chat']['id'])
                mydb.member_update_chatid('registration_progress', 1, message['chat']['id'])
                bot.sendMessage(message['chat']['id'],
                                str(msg.messageLib.enterName.value))
        if btn == 'btnTechnicalResponsible':
            if tempMember.register_progress == 18 and tempMember.op == 16:
                mydb.member_update_chatid('membership_type', 2, user_id)
                mydb.member_update_chatid(fieldName='verifyAdmin', fieldValue=0, chatid=user_id)
                # send message to user
                if not mydb.checkExsistDetail(tempMember, 2):
                    bot.sendMessage(user_id, msg.messageLib.enterNationCode.value)
                    mydb.member_update_chatid('registration_progress', 4, user_id)
                else:
                    bot.sendMessage(user_id, msg.messageLib.oldInfo.value)
                    helper.send_profile(chatid=user_id, bot=bot)
                    bot.sendMessage(user_id, msg.messageLib.confirmEdit.value,
                                    reply_markup=menu.keyLib.kbEditProfile(self=None, chatId=user_id))
            elif tempMember.register_progress == 0 and tempMember.op == 0:
                tempMember.userName = userName
                tempMember.lastMessage = update['update_id']
                tempMember.membership_type = 2
                tempMember.chatId = update['callback_query']['chat_instance']
                tempMember.register_progress = 1
                mydb.member_update_chatid('membership_type', 2, message['chat']['id'])
                mydb.member_update_chatid('chat_id', user_id, message['chat']['id'])
                mydb.member_update_chatid('registration_progress', 1, message['chat']['id'])
                bot.sendMessage(message['chat']['id'],
                                str(msg.messageLib.enterName.value))
        if btn == 'btnStudent':
            if tempMember.register_progress == 18 and tempMember.op == 16:
                mydb.member_update_chatid('membership_type', 3, user_id)
                mydb.member_update_chatid(fieldName='verifyAdmin', fieldValue=0, chatid=user_id)
                # send message to user
                if not mydb.checkExsistDetail(tempMember, 3):
                    bot.sendMessage(user_id, msg.messageLib.enterNationCode.value)
                    mydb.member_update_chatid('registration_progress', 4, user_id)
                else:
                    bot.sendMessage(user_id, msg.messageLib.oldInfo.value)
                    helper.send_profile(chatid=user_id, bot=bot)
                    bot.sendMessage(user_id, msg.messageLib.confirmEdit.value,
                                    reply_markup=menu.keyLib.kbEditProfile(self=None, chatId=user_id))
            elif tempMember.register_progress == 0 and tempMember.op == 0:
                tempMember.userName = userName
                tempMember.lastMessage = update['update_id']
                tempMember.membership_type = 3
                tempMember.chatId = update['callback_query']['chat_instance']
                tempMember.register_progress = 1
                mydb.member_update_chatid('membership_type', 3, user_id)
                mydb.member_update_chatid('chat_id', user_id, user_id)
                mydb.member_update_chatid('registration_progress', 1, user_id)
                bot.sendMessage(user_id,
                                str(msg.messageLib.enterName.value))
            else:
                bot.sendMessage(user_id, 'عملیات نامعتبر است')
        if btn == 'btnMananger':
            if tempMember.register_progress == 18 and tempMember.op == 16:
                mydb.member_update_chatid('membership_type', 4, user_id)
                mydb.member_update_chatid(fieldName='verifyAdmin', fieldValue=0, chatid=user_id)
                # send message to user
                bot.sendMessage(user_id, msg.messageLib.afterEdit.value,
                                reply_markup=menu.keyLib.kbVerifyEditProfile(self=None, tag=user_id))
            elif tempMember.register_progress == 0 and tempMember.op == 0:
                tempMember.userName = userName
                tempMember.lastMessage = update['update_id']
                tempMember.membership_type = 4
                tempMember.chatId = update['callback_query']['chat_instance']
                tempMember.register_progress = 1
                mydb.member_update_chatid('membership_type', 4, user_id)
                mydb.member_update_chatid('chat_id', user_id, user_id)
                mydb.member_update_chatid('registration_progress', 1, user_id)
                bot.sendMessage(user_id,
                                str(msg.messageLib.enterName.value))
            else:
                bot.sendMessage(user_id, 'عملیات نامعتبر است')
        if btn == 'btNightDay':
            if tempMember.register_progress == 18:
                mydb.founder_update('pharmacy_type', 'شبانه روزی', message['chat']['id'])
                mydb.member_update_chatid(fieldName='verifyAdmin', fieldValue=0, chatid=user_id)
                bot.sendMessage(user_id, msg.messageLib.afterEdit.value,
                                reply_markup=menu.keyLib.kbVerifyEditProfile(self=None, tag=user_id))
            else:
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
            mydb.student_update('timePermit', '06:00-14:00', message['chat']['id'])
            if tempMember.register_progress != 18:
                bot.sendMessage(message['chat']['id'],
                                str(msg.messageLib.endRegisteration.value))
            else:
                mydb.member_update_chatid(fieldName='verifyAdmin', fieldValue=0, chatid=user_id)
                # send message to user
                bot.sendMessage(user_id, msg.messageLib.afterEdit.value,
                                reply_markup=menu.keyLib.kbVerifyEditProfile(self=None, tag=user_id))
                return

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
                isExisting = os.path.exists(img)
                if isExisting:
                    bot.sendPhoto(admin[0], open(img, 'rb'))
                else:
                    bot.sendMessage(admin[0], 'فایل تصویر پیدا نشد')
                bot.sendMessage(admin[0],
                                str(msg.messageLib.labelPermitPhoto.value))
                img = 'download/{}'.format(
                    mydb.get_student_property('overtime_license_photo', message['chat']['id']))
                isExisting = os.path.exists(img)
                if isExisting:
                    bot.sendPhoto(admin[0], open(img, 'rb'))
                else:
                    bot.sendMessage(admin[0], 'فایل تصویر پیدا نشد')
                bot.sendMessage(admin[0], msg.messageLib.messAdminApprove.value,
                                reply_markup=menu.keyLib.kbCreateApproveKey(chat_id=message['chat']['id']))
            mydb.member_update_chatid('registration_progress', 10, message['chat']['id'])
            tempMember.register_progress = 10
        if btn == 'btShiftEvening':
            mydb.student_update('shift_access', 'عصر', message['chat']['id'])
            mydb.student_update('timePermit', '14:00-22:00', message['chat']['id'])
            if tempMember.register_progress != 18:
                bot.sendMessage(message['chat']['id'],
                                str(msg.messageLib.endRegisteration.value))
            else:
                mydb.member_update_chatid(fieldName='verifyAdmin', fieldValue=0, chatid=user_id)
                # send message to user
                bot.sendMessage(user_id, msg.messageLib.afterEdit.value,
                                reply_markup=menu.keyLib.kbVerifyEditProfile(self=None, tag=user_id))
                return
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
                isExisting = os.path.exists(img)
                if isExisting:
                    bot.sendPhoto(admin[0], open(img, 'rb'))
                else:
                    bot.sendMessage(admin[0], 'فایل تصویر پیدا نشد')
                bot.sendMessage(admin[0],
                                str(msg.messageLib.labelPermitPhoto.value))
                img = 'download/{}'.format(
                    mydb.get_student_property('overtime_license_photo', message['chat']['id']))
                isExisting = os.path.exists(img)
                if isExisting:
                    bot.sendPhoto(admin[0], open(img, 'rb'))
                else:
                    bot.sendMessage(admin[0], 'فایل تصویر پیدا نشد')
                bot.sendMessage(admin[0], msg.messageLib.messAdminApprove.value,
                                reply_markup=menu.keyLib.kbCreateApproveKey(chat_id=message['chat']['id']))
            mydb.member_update_chatid('registration_progress', 10, message['chat']['id'])
            tempMember.register_progress = 10
        if btn == 'btShiftEveningNight':
            mydb.student_update('shift_access', 'عصر و شب', message['chat']['id'])
            mydb.student_update('timePermit', '14:00-06:00', message['chat']['id'])
            if tempMember.register_progress != 18:
                bot.sendMessage(message['chat']['id'],
                                str(msg.messageLib.endRegisteration.value))
            else:
                mydb.member_update_chatid(fieldName='verifyAdmin', fieldValue=0, chatid=user_id)
                # send message to user
                bot.sendMessage(user_id, msg.messageLib.afterEdit.value,
                                reply_markup=menu.keyLib.kbVerifyEditProfile(self=None, tag=user_id))
                return
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
                isExisting = os.path.exists(img)
                if isExisting:
                    bot.sendPhoto(admin[0], open(img, 'rb'))
                else:
                    bot.sendMessage(admin[0], 'فایل تصویر پیدا نشد')
                bot.sendMessage(admin[0],
                                str(msg.messageLib.labelPermitPhoto.value))
                img = 'download/{}'.format(
                    mydb.get_student_property('overtime_license_photo', message['chat']['id']))
                isExisting = os.path.exists(img)
                if isExisting:
                    bot.sendPhoto(admin[0], open(img, 'rb'))
                else:
                    bot.sendMessage(admin[0], 'فایل تصویر پیدا نشد')
                bot.sendMessage(admin[0], msg.messageLib.messAdminApprove.value,
                                reply_markup=menu.keyLib.kbCreateApproveKey(chat_id=message['chat']['id']))
            mydb.member_update_chatid('registration_progress', 10, message['chat']['id'])
            tempMember.register_progress = 10
        if btn == 'btShiftMorningEvening':
            mydb.student_update('shift_access', 'صبح و عصر', message['chat']['id'])
            mydb.student_update('timePermit', '06:00-22:00', message['chat']['id'])
            if tempMember.register_progress != 18:
                bot.sendMessage(message['chat']['id'],
                                str(msg.messageLib.endRegisteration.value))
            else:
                mydb.member_update_chatid(fieldName='verifyAdmin', fieldValue=0, chatid=user_id)
                # send message to user
                bot.sendMessage(user_id, msg.messageLib.afterEdit.value,
                                reply_markup=menu.keyLib.kbVerifyEditProfile(self=None, tag=user_id))
                return
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
                isExisting = os.path.exists(img)
                if isExisting:
                    bot.sendPhoto(admin[0], open(img, 'rb'))
                else:
                    bot.sendMessage(admin[0], 'فایل تصویر پیدا نشد')
                bot.sendMessage(admin[0],
                                str(msg.messageLib.labelPermitPhoto.value))
                img = 'download/{}'.format(
                    mydb.get_student_property('overtime_license_photo', message['chat']['id']))
                isExisting = os.path.exists(img)
                if isExisting:
                    bot.sendPhoto(admin[0], open(img, 'rb'))
                else:
                    bot.sendMessage(admin[0], 'فایل تصویر پیدا نشد')
                bot.sendMessage(admin[0], msg.messageLib.messAdminApprove.value,
                                reply_markup=menu.keyLib.kbCreateApproveKey(chat_id=message['chat']['id']))
            mydb.member_update_chatid('registration_progress', 10, message['chat']['id'])
            tempMember.register_progress = 10
        if btn == 'btShiftAllTime':
            mydb.student_update('shift_access', 'صبح و عصر', message['chat']['id'])
            mydb.student_update('timePermit', '00:00-23:59', message['chat']['id'])
            if tempMember.register_progress != 18:
                bot.sendMessage(message['chat']['id'],
                                str(msg.messageLib.endRegisteration.value))
            else:
                mydb.member_update_chatid(fieldName='verifyAdmin', fieldValue=0, chatid=user_id)
                # send message to user
                bot.sendMessage(user_id, msg.messageLib.afterEdit.value,
                                reply_markup=menu.keyLib.kbVerifyEditProfile(self=None, tag=user_id))
                return
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
                isExisting = os.path.exists(img)
                if isExisting:
                    bot.sendPhoto(admin[0], open(img, 'rb'))
                else:
                    bot.sendMessage(admin[0], 'فایل تصویر پیدا نشد')
                bot.sendMessage(admin[0],
                                str(msg.messageLib.labelPermitPhoto.value))
                img = 'download/{}'.format(
                    mydb.get_student_property('overtime_license_photo', message['chat']['id']))
                isExisting = os.path.exists(img)
                if isExisting:
                    bot.sendPhoto(admin[0], open(img, 'rb'))
                else:
                    bot.sendMessage(admin[0], 'فایل تصویر پیدا نشد')
                bot.sendMessage(admin[0], msg.messageLib.messAdminApprove.value,
                                reply_markup=menu.keyLib.kbCreateApproveKey(chat_id=message['chat']['id']))
            mydb.member_update_chatid('registration_progress', 10, message['chat']['id'])
            tempMember.register_progress = 10
        if btn == 'btShiftNight':
            mydb.student_update('shift_access', 'شب', message['chat']['id'])
            mydb.student_update('timePermit', '22:00-06:00', message['chat']['id'])
            if tempMember.register_progress != 18:
                bot.sendMessage(message['chat']['id'],
                                str(msg.messageLib.endRegisteration.value))
            else:
                mydb.member_update_chatid(fieldName='verifyAdmin', fieldValue=0, chatid=user_id)
                # send message to user
                bot.sendMessage(user_id, msg.messageLib.afterEdit.value,
                                reply_markup=menu.keyLib.kbVerifyEditProfile(self=None, tag=user_id))
                return
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
                isExisting = os.path.exists(img)
                if isExisting:
                    bot.sendPhoto(admin[0], open(img, 'rb'))
                else:
                    bot.sendMessage(admin[0], 'فایل تصویر پیدا نشد')
                bot.sendMessage(admin[0],
                                str(msg.messageLib.labelPermitPhoto.value))
                img = 'download/{}'.format(
                    mydb.get_student_property('overtime_license_photo', message['chat']['id']))
                isExisting = os.path.exists(img)
                if isExisting:
                    bot.sendPhoto(admin[0], open(img, 'rb'))
                else:
                    bot.sendMessage(admin[0], 'فایل تصویر پیدا نشد')
                bot.sendMessage(admin[0], msg.messageLib.messAdminApprove.value,
                                reply_markup=menu.keyLib.kbCreateApproveKey(chat_id=message['chat']['id']))
            mydb.member_update_chatid('registration_progress', 10, message['chat']['id'])
            tempMember.register_progress = 10
        if btn == 'btShiftMorningNight':
            mydb.student_update('shift_access', 'صبح و شب', message['chat']['id'])
            mydb.student_update('timePermit', '22:00-14:00', message['chat']['id'])
            if tempMember.register_progress != 18:
                bot.sendMessage(message['chat']['id'],
                                str(msg.messageLib.endRegisteration.value))
            else:
                mydb.member_update_chatid(fieldName='verifyAdmin', fieldValue=0, chatid=user_id)
                # send message to user
                bot.sendMessage(user_id, msg.messageLib.afterEdit.value,
                                reply_markup=menu.keyLib.kbVerifyEditProfile(self=None, tag=user_id))
                return
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
                isExisting = os.path.exists(img)
                if isExisting:
                    bot.sendPhoto(admin[0], open(img, 'rb'))
                else:
                    bot.sendMessage(admin[0], 'فایل تصویر پیدا نشد')
                bot.sendMessage(admin[0],
                                str(msg.messageLib.labelPermitPhoto.value))
                img = 'download/{}'.format(
                    mydb.get_student_property('overtime_license_photo', message['chat']['id']))
                isExisting = os.path.exists(img)
                if isExisting:
                    bot.sendPhoto(admin[0], open(img, 'rb'))
                else:
                    bot.sendMessage(admin[0], 'فایل تصویر پیدا نشد')
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


def delOldData():
    while True:
        now = datetime.now()
        if now.hour == 0 and now.minute <= 2:
            mydb.delOldShift()
        if not threadCallTelegram.isAlive():
            threadCallTelegram.start()


def callTelegram(luiIn):
    ut = datetime.now()
    last_ut = datetime.now()
    lui = luiIn
    try:
        while True:
            td = last_ut - ut
            if last_ut is None or td.total_seconds() > 1:
                ut = datetime.now()
                # دریافت تمامی پیام های دریافتی
                helper.send_shift_to_student(bot=bot)
                updates = bot.getUpdates(offset=lui)
                if updates:
                    lui = int(updates[-1]['update_id']) + 1
                    handle_updates(updates)
            last_ut = datetime.now()
    except Exception as e:
        lui = lui + 1
        if type(e).__name__ in ('MaxRetryError', 'ProtocolError'):
            print(type(e).__name__)
        else:
            bot.sendMessage('6274361322', traceback.format_exc())
            print(traceback.format_exc())
            threadCallTelegram = threading.Thread(target=callTelegram(lui + 1))
            threadCallTelegram.start()


threadCallTelegram = threading.Thread(target=callTelegram(0))
threadDelOldData = threading.Thread(target=delOldData)


def main():
    threadDelOldData.start()
    threadCallTelegram.start()


if __name__ == '__main__':
    # helper.send_shift_to_technicalResponsible(125, bot, '6274361322',2)
    main()
