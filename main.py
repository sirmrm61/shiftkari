import telepot
import time
from model.membership import Membership
from persiantools.jdatetime import JalaliDate
from dateutil.relativedelta import relativedelta
import datetime
from datetime import timedelta
import os
from pprint import pprint
import msg
import db.mysqlconnector as msc
import uuid
import menu
import db.founderHelper as fh
from unidecode import unidecode

helper = fh.HelperFunder()
from telepot.loop import MessageLoop

last_update_ids = {}
# زمان حداکثر برای فعال بودن آخرین پیام دریافتی (به ثانیه)
MAX_IDLE_TIME = 600

mydb = msc.mysqlconnector()
idFromFile = None
botKeyApi = mydb.get_property_domain('botkey')
bot = telepot.Bot(botKeyApi)


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
        elif 'text' in message and str(message['text']).lower().startswith('/changeHrStudent'.lower()):
            hr = None
            try:
                hr = int(str(message['text'])[16:])
            except:
                bot.sendMessage(user_id, msg.messageLib.erroCommand.value)
                return
            mydb.domain_update_by_key('hrStudent', hr)
            bot.sendMessage(user_id, str(msg.messageLib.changeHourSuccess.value).format(hr))
        elif 'text' in message and str(message['text']).lower().startswith('/changeMinWage'.lower()):
            wage = None
            try:
                wage = int(str(message['text'])[14:])
            except:
                bot.sendMessage(user_id, msg.messageLib.erroCommand.value)
                return
            mydb.domain_update_by_key('wage', wage)
            bot.sendMessage(user_id, str(msg.messageLib.changeWageSuccess.value).format(wage))
        elif 'text' in message and str(message['text']).lower().startswith('/changeMinLicenss'.lower()):
            licenssRent = None
            try:
                licenssRent = int(str(message['text'])[17:])
            except:
                bot.sendMessage(user_id, msg.messageLib.erroCommand.value)
                return
            mydb.domain_update_by_key('licenss', licenssRent)
            bot.sendMessage(user_id, str(msg.messageLib.changeLicenssSuccess.value).format(licenssRent))
        elif 'text' in message and message['text'] == '/myoperation':
            helper.send_operation(tempMember=tempMember, bot=bot, chatid=message['chat']['id'])

        elif 'text' in message and tempMember.register_progress == 0 and message['text'] == '/start':
            bot.sendMessage(message['chat']['id'], str(msg.messageLib.helloClient.value).format(
                message['chat']['first_name']), reply_markup=menu.keyLib.kbWhoAreYou())
        elif 'text' in message and tempMember.register_progress != 0 and message['text'] == '/start':
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
            except:  # TODO: عوض کردن کد admin
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
                # todo: check number
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
        elif tempMember.register_progress == 10:
            if tempMember.membership_type == 4 and message['text'] == '/start':
                bot.sendMessage(message['chat']['id'],
                                str(msg.messageLib.helloAdmin.value).format(
                                    tempMember.name + ' ' + tempMember.last_name),
                                reply_markup=menu.keyLib.kbAdmin())
        elif tempMember.register_progress == 11:
            if tempMember.membership_type == 2 or tempMember.membership_type == 1:
                op = mydb.get_member_property_chatid('op', user_id)
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
                        minWage = mydb.get_property_domain('wage')
                        if str(message['text']).isnumeric():
                            if int(minWage) > int(message['text']):
                                bot.sendMessage(user_id, str(msg.messageLib.minWage.value).format(minWage))
                                bot.sendMessage(user_id, msg.messageLib.shiftWage.value)
                                return
                        else:
                            bot.sendMessage(user_id, msg.messageLib.errorNumber.value)
                            return
                        mydb.member_update('op', 7, message['chat']['id'])
                        mydb.shift_update('wage', message['text'], message['chat']['id'])
                        bot.sendMessage(message['chat']['id'],
                                        'آیا مبلغ {0} ریال بعنوان حق الزحمه صحیح است؟'.format(message['text']),
                                        reply_markup=menu.keyLib.kbCreateMenuYesNO(
                                            chatId='{}'.format(op)))
                    if op == 8:
                        mydb.member_update('op', 9, message['chat']['id'])
                        rs = mydb.shift_update('pharmacyAddress', message['text'], message['chat']['id'])
                        bot.sendMessage(message['chat']['id'],
                                        'آیا آدرس {0} برای داروخانه صحیح است؟'.format(message['text']),
                                        reply_markup=menu.keyLib.kbCreateMenuYesNO(
                                            chatId='{0}_{1}'.format(9, rs[0])))
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
            elif spBtn[1] == 'sendToCreator':
                creatorChatID = mydb.get_shift_property(fieldName='Creator', idShift=spBtn[2])
                listDayAccept = mydb.getListDaySelection(idShift=spBtn[2], requsterShift=user_id)
                fname = mydb.get_member_property_chatid('name', user_id)
                lname = mydb.get_member_property_chatid('last_name', user_id)
                fullName = fname + ' ' + lname

                if len(listDayAccept) > 0:
                    bot.sendMessage(creatorChatID, str(msg.messageLib.sendDayForApproveCreator.value).format(fullName))
                    helper.send_profile(user_id, bot, creatorChatID)
                    bot.sendMessage(creatorChatID, 'روز های مورد تائید را نتخاب نمائید',
                                    reply_markup=menu.keyLib.createMenuFromListDayForApproveCreator(None, listDayAccept,
                                                                                                    2))
                else:
                    bot.sendMessage(creatorChatID, str(msg.messageLib.senndAcceptAllDayInShift.value).format(fullName),
                                    reply_markup=menu.keyLib.kbCreateMenuShiftApproveManager(shiftId=spBtn[2]))
            elif spBtn[1] == 'dayApproveCreator':
                helper.registerDay(spBtn[2], bot, user_id)
            elif spBtn[1] == 'approveAllDay':
                listIdDay = str(spBtn[2]).split('#')
                for item in listIdDay:
                    helper.registerDay(item, bot, user_id)
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
            elif spBtn[1] == 'deny':
                verification = mydb.get_member_property_chatid('verifyAdmin', spBtn[2])
                print(f'verification={verification}')
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
            elif spBtn[1] == 'createSift':
                bot.sendMessage(message['chat']['id'], msg.messageLib.dateShift.value)
                bot.sendMessage(chat_id=user_id, parse_mode='HTML', text='سال را انتخاب کنید',
                                reply_markup=menu.keyLib.kbCreateMenuYear(tag=1))
                mydb.member_update('registration_progress', 11, user_id)
                mydb.member_update('op', 0, message['chat']['id'])
            elif spBtn[1] == 'year':
                if tempMember.register_progress not in (11, 5):
                    bot.sendMessage(user_id, msg.messageLib.noBussiness.value)
                    return
                yearTemp = None
                todayDate = datetime.date.today()
                jd = str(JalaliDate.to_jalali(todayDate.year, todayDate.month, todayDate.day)).split('-')
                if spBtn[2] == 'currntYear':
                    yearTemp = int(jd[0])
                else:
                    yearTemp = int(jd[0]) + 1
                if spBtn[3] == '1':
                    rowid = mydb.shift_update('DateShift', yearTemp, user_id)
                    bot.sendMessage(chat_id=user_id, parse_mode='HTML', text='ماه انتخاب کنید',
                                    reply_markup=menu.keyLib.kbCreateMenuMonthInYear(tag='1_{}'.format(rowid[0])))
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
                    mydb.shift_update_by_id('DateShift', '{0}-{1}'.format(year, spBtn[2]), spBtn[4])
                    bot.sendMessage(chat_id=user_id, parse_mode='HTML', text='روز انتخاب کنید',
                                    reply_markup=menu.keyLib.kbCreateMenuDayInMonth(tag='1_{}'.format(spBtn[4])))
                elif spBtn[3] == '2':
                    year = mydb.get_shift_property(fieldName='dateEndShift', idShift=spBtn[4])
                    mydb.shift_update_by_id('dateEndShift', '{0}-{1}'.format(year, spBtn[2]), spBtn[4])
                    bot.sendMessage(chat_id=user_id, parse_mode='HTML', text='روز انتخاب کنید',
                                    reply_markup=menu.keyLib.kbCreateMenuDayInMonth(tag='2_{}'.format(spBtn[4])))
                elif spBtn[3] == '4':
                    year = mydb.get_student_property(fieldName='start_date', chatid=user_id)
                    mydb.student_update('start_date', '{0}{1}'.format(year, spBtn[2]), user_id)
                    bot.sendMessage(chat_id=user_id, parse_mode='HTML', text='روز انتخاب کنید',
                                    reply_markup=menu.keyLib.kbCreateMenuDayInMonth(tag='4_{}'.format(user_id)))
                elif spBtn[3] == '5':
                    year = mydb.get_student_property(fieldName='end_date', chatid=user_id)
                    mydb.student_update('end_date', '{0}{1}'.format(year, spBtn[2]), user_id)
                    bot.sendMessage(chat_id=user_id, parse_mode='HTML', text='روز انتخاب کنید',
                                    reply_markup=menu.keyLib.kbCreateMenuDayInMonth(tag='5_{}'.format(user_id)))
            elif spBtn[1] == 'day':
                if tempMember.register_progress not in (11, 5):
                    bot.sendMessage(user_id, msg.messageLib.noBussiness.value)
                    return
                if spBtn[3] == '1':
                    year = mydb.get_shift_property(fieldName='DateShift', idShift=spBtn[4])
                    mydb.shift_update('DateShift', '{0}-{1}'.format(year, spBtn[2]), user_id)
                    yearIn = int(str(year)[0:4])
                    monthIn = int(str(year)[5:7])
                    dayIn = int(str(spBtn[2]))
                    dateMiladiIn = JalaliDate(yearIn, monthIn, dayIn).to_gregorian()
                    todayDate = datetime.date.today()
                    diffDay = relativedelta(dateMiladiIn, todayDate).days
                    if diffDay > 0:
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
                    mydb.shift_update_by_id('dateEndShift', '{0}-{1}'.format(year, spBtn[2]), spBtn[4])
                    yearIn = int(str(year)[0:4])
                    monthIn = int(str(year)[5:7])
                    dayIn = int(str(spBtn[2]))
                    dateMiladiIn = JalaliDate(yearIn, monthIn, dayIn).to_gregorian()
                    todayDate = datetime.date.today()
                    diffDay = relativedelta(dateMiladiIn, todayDate).days
                    if diffDay > 0:
                        mydb.member_update('op', 11, message['chat']['id'])
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
                if int(op) == 1:  # تاریخ پایان شیفت بعدا اضافه شد
                    bot.sendMessage(message['chat']['id'], msg.messageLib.enterDateEnd.value)
                    bot.sendMessage(chat_id=user_id, parse_mode='HTML', text='سال را کنید',
                                    reply_markup=menu.keyLib.kbCreateMenuYear(tag='2_{}'.format(spBtn[2])))
                    mydb.member_update('op', 11, message['chat']['id'])
                if int(op) == 11:
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
                    bot.sendMessage(message['chat']['id'], msg.messageLib.pharmacyAddress.value)
                    addressPharmacy = None
                    if tempMember.membership_type == 1:
                        addressPharmacy = mydb.get_funder_property('pharmacy_address', message['chat']['id'])
                        rs = mydb.shift_update('pharmacyAddress', addressPharmacy, user_id)
                    if addressPharmacy is not None:
                        bot.sendMessage(message['chat']['id'],
                                        'آیا آدرس {0} برای داروخانه صحیح است؟'.format(addressPharmacy),
                                        reply_markup=menu.keyLib.kbCreateMenuYesNO(
                                            chatId='{0}_{1}'.format(9, rs[0])))
                        mydb.member_update('op', 9, message['chat']['id'])
                    else:
                        mydb.member_update('op', 8, message['chat']['id'])
                if int(op) == 9:
                    # Send Shift to All Technical Responsible
                    hrSendToStudent = mydb.get_property_domain('hrStudent')
                    bot.sendMessage(message['chat']['id'],
                                    str(msg.messageLib.endRegisterShift.value).format(hrSendToStudent))
                    helper.send_shift_to_technicalResponsible(spBtn[3], bot, user_id)
                    mydb.member_update('registration_progress', 10, user_id)
                    mydb.member_update('op', 0, user_id)
                    mydb.shift_update('progress', 2, user_id)
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
                    bot.sendMessage(message['chat']['id'], msg.messageLib.enterPharmacyAddress.value)
            elif spBtn[1] == 'listSift':
                allShift = mydb.get_all_shift_by_creator(creator=message['chat']["id"])
                if len(allShift) == 0:
                    bot.sendMessage(message['chat']["id"], msg.messageLib.emptyList.value)
                else:
                    for shiftRow in allShift:
                        rowReq = 'درخواست دهنده: {}'.format(shiftRow[0])
                        rowDate = 'تاریخ شروع : {}'.format(shiftRow[2])
                        rowDateEnd = 'تاریخ پایان : {}'.format(shiftRow[10])
                        rowStartTime = 'ساعت شروع  : {}'.format(shiftRow[3])
                        rowEndTime = 'ساعت پایان  : {}'.format(shiftRow[4])
                        rowWage = 'حق الزحمه  : {}'.format(shiftRow[5])
                        rowaddr = 'آدرس  : {}'.format(shiftRow[6])
                        bot.sendMessage(message['chat']["id"], '''
{0}
{1}
{6}
{2}
{3}
{4}
{5}
'''.format(rowReq, rowDate, rowStartTime, rowEndTime, rowWage, rowaddr,
           rowDateEnd), )
            elif spBtn[1] == 'epf':
                bot.sendMessage(user_id, msg.messageLib.editMessag.value)
                helper.send_profile(chatid=user_id, bot=bot)
                bot.sendMessage(user_id, msg.messageLib.confirmEdit.value,
                                reply_markup=menu.keyLib.kbEditProfile(self=None, chatId=user_id))
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
                # todo: new approve shift
                listDayFull = mydb.getListDayIsNotEmpty(spBtn[2])
                if len(listDayFull) == 0:
                    dateStart = str(mydb.get_shift_property('DateShift', spBtn[2])).split('-')
                    dateEnd = str(mydb.get_shift_property('dateEndShift', spBtn[2])).split('-')
                    dsG = JalaliDate(int(dateStart[0]), int(dateStart[1]), int(dateStart[2])).to_gregorian()
                    deG = JalaliDate(int(dateEnd[0]), int(dateEnd[1]), int(dateEnd[2])).to_gregorian()
                    diffDay = relativedelta(deG, dsG)
                    bot.sendMessage(user_id, str(msg.messageLib.shiftTotalDay.value).format(diffDay.days + 1),
                                    reply_markup=menu.keyLib.kbApproveAllShiftYesNO(shiftId=spBtn[2]))
                else:
                    helper.NOApproveAllShift(spBtn[2], user_id, bot)

            elif spBtn[1] == 'endSelection':
                helper.endSelectionDayBtnClick(spBtn[2], user_id, bot)
            elif spBtn[1] == 'daySelectedRemove':
                idShift = mydb.getIdShiftFromDay(spBtn[2])
                mydb.removeFromSelection(spBtn[2])
                helper.endSelectionDayBtnClick(idShift, user_id, bot)
            elif spBtn[1] == 'dayShift':
                tmp = str(spBtn[2]).split('=')
                dateStr = tmp[0]
                idShiftStr = tmp[1]
                if mydb.isShiftDayFull(idShiftStr, dateStr) > 0:
                    bot.sendMessage(user_id, str(msg.messageLib.shiftDayIsFull.value))
                    return
                tmpRes = mydb.registerDayShift(idShiftStr, dateStr, user_id, 0)
                if tmpRes == 0:
                    bot.sendMessage(user_id, str(msg.messageLib.afterDaySelction.value).format(dateStr))
                else:
                    bot.sendMessage(user_id, str(msg.messageLib.repeatedDay.value))
            elif spBtn[1] == 'NOApproveAllShift':
                helper.NOApproveAllShift(spBtn[2], user_id, bot)
            elif spBtn[1] == 'yesApproveAllShift':
                helper.yesApproveAllShift(spBtn[2], user_id, bot)
            elif spBtn[1] == 'deleteShift':
                allShift = mydb.get_all_shift_by_creator(creator=message['chat']["id"])
                if len(allShift) == 0:
                    bot.sendMessage(message['chat']["id"], msg.messageLib.emptyList.value)
                else:
                    for shiftRow in allShift:
                        rowReq = 'درخواست دهنده: {}'.format(shiftRow[0])
                        rowDate = 'تاریخ شروع : {}'.format(shiftRow[2])
                        rowDateEnd = 'تاریخ پایان : {}'.format(shiftRow[10])
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
{7}
{2}
{3}
{4}
{5}
{6}
{7}'''.format(rowReq, rowDate, rowStartTime, rowEndTime, rowWage, rowaddr, rowApprove,
              msg.messageLib.doYouLikeDelete.value, rowDateEnd),
                                        reply_markup=menu.keyLib.kbCreateMenuDeleteShift(shiftId=shiftRow[9]))
            elif spBtn[1] == 'DeleteShiftList':  # فشردن دکمه حذف شیفت
                print(spBtn)
                bot.sendMessage(user_id, msg.messageLib.confirmDeleteShift.value,
                                reply_markup=menu.keyLib.kbCreateMenuConfirmDelete(shiftId=spBtn[2]))
            elif spBtn[1] == 'confirmDelete':  # تائیدیه پاک کردن شیفت توسط مدیر سیستم
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
                        rowDate = 'تاریخ شروع : {}'.format(shiftRow[2])
                        rowDateEnd = 'تاریخ پایان : {}'.format(shiftRow[10])
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
{8}
{2}
{3}
{4}
{5}
{6}
{7}'''.format(rowReq, rowDate, rowStartTime, rowEndTime, rowWage, rowaddr, rowApprove,
              msg.messageLib.doYouLikeDelete.value, rowDateEnd),
                                        reply_markup=menu.keyLib.kbCreateMenuDeleteShift(shiftId=shiftRow[9]))
            elif spBtn[1] == 'approveShiftManager':
                mydb.shift_update_by_id('progress', 2, spBtn[2])
                approver = mydb.get_shift_property('approver', spBtn[2])
                bot.sendMessage(approver, msg.messageLib.shiftApprovedByManager.value)
                helper.registerFullShiftDay(spBtn[2], approver)
            elif spBtn[1] == 'disApproveShiftManager':
                approver = mydb.get_shift_property('approver', spBtn[2])
                bot.sendMessage(approver, msg.messageLib.shiftDisApprovedByManager.value)
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
                pprint(mydb.member_update_chatid('registration_progress', 1, message['chat']['id']))
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
                pprint(mydb.member_update_chatid('registration_progress', 1, message['chat']['id']))
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
                pprint(mydb.member_update_chatid('registration_progress', 1, user_id))
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
                pprint(mydb.member_update_chatid('registration_progress', 1, user_id))
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
                # todo: print delete command
                print(
                    'download/{}'.format(mydb.get_student_property('personal_photo', message['chat']['id'])))
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
                print(
                    'download/{}'.format(mydb.get_student_property('personal_photo', message['chat']['id'])))
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
                print(
                    'download/{}'.format(mydb.get_student_property('personal_photo', message['chat']['id'])))
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
                print(
                    'download/{}'.format(mydb.get_student_property('personal_photo', message['chat']['id'])))
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


# شروع برنامه
def main():
    lui = 0
    # HTML کد پیام
    # html_message = '<table><tr><th>نام</th><th>سن</th></tr>''<tr><td>علی</td><td>30</td></tr><tr><td>محمد</td><td>25</td></tr></table>'
    try:
        while True:
            # دریافت تمامی پیام های دریافتی
            helper.send_shift_to_student(bot=bot)
            updates = bot.getUpdates(timeout=10, offset=lui)
            if updates:
                lui = int(updates[-1]['update_id']) + 1
                handle_updates(updates)
    except Exception as e:
        print(e)
        lui = lui + 1
        bot.sendMessage('6274361322', str(e))
        main()


if __name__ == '__main__':
    main()
