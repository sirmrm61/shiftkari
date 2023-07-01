import telepot
import time
from model.membership import Membership
import os
from pprint import pprint
import msg
import db.mysqlconnector as msc
import uuid
import menu

last_update_ids = {}
# زمان حداکثر برای فعال بودن آخرین پیام دریافتی (به ثانیه)
MAX_IDLE_TIME = 600

mydb = msc.mysqlconnector()
idFromFile = None

bot = telepot.Bot('6012649808:AAGXWUsZJBtvWsFlYuvqg18tgIwo7ildPUs')


# admins = mydb.getAdmins()
# image = 'download/2c3809f7-8e48-4cbf-acb7-bc7b0c9d1cd4.jpg'
# pprint(admins)
# for admin in admins:
#     pprint(bot.sendPhoto(admin[0], open(image, 'rb')))
# exit()


def handle_new_messages(user_id, userName):
    global last_update_ids
    # دریافت آخرین شناسه update_id برای کاربر
    # tempMember, last_update_time = last_update_ids.get(user_id, (Membership, 0))
    tempV = last_update_ids.get(user_id)
    tempMember = None if tempV is None else tempV[0]
    last_update_time = 0 if tempV is None else tempV[1]
    if tempMember is None:
        tempMember = mydb.load_member(user_id)
        if tempMember is not None:
            last_update_id = tempMember.lastMessage
        else:
            print(user_id)
            tempMember = mydb.create_member(Membership(userName=userName, chatid=user_id))
            last_update_id = 0
    else:
        last_update_id = int(tempMember.lastMessage)

    # محاسبه زمان گذشته از آخرین پیام دریافتی
    elapsed_time = time.time() - last_update_time
    # اگر زمان گذشته بیشتر از حداکثر زمان مجاز باشد، آخرین شناسه update_id برای کاربر حذف می شود
    if elapsed_time > MAX_IDLE_TIME and last_update_time > 0:
        del last_update_ids[user_id]
        return
    # دریافت پیام های جدید
    updates = bot.getUpdates(offset=last_update_id + 1, timeout=10)
    message = None
    for update in updates:
        print(update)
        if 'message' in update:
            message = update['message']
            if message['text'] == '/myinfo':
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
                                str(msg.messageLib.duplicateregistration.value).format(titlePos))
            elif tempMember.register_progress == 0 and message['text'] == '/start':
                bot.sendMessage(message['chat']['id'], str(msg.messageLib.helloClient.value).format(
                    message['chat']['first_name']), reply_markup=menu.keyLib.kbWhoAreYou())
            elif tempMember.register_progress != 0 and message['text'] == '/start':
                titlePos = None
                if tempMember.membership_type == 1:
                    titlePos = 'موسس'
                elif tempMember.membership_type == 2:
                    titlePos = 'مسئول فنی'
                elif tempMember.membership_type == 3:
                    titlePos = 'دانشجو'
                elif tempMember.membership_type == 4:
                    titlePos = 'مدیر'
                bot.sendMessage(message['chat']['id'],
                                str(msg.messageLib.duplicateregistration.value).format(titlePos),
                                reply_markup=menu.keyLib.kbCreateDelKey(message['chat']['id']))
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
                    mydb.technicalManager_update('national_code', message['text'], message['chat']['id'])
                    bot.sendMessage(message['chat']['id'],
                                    str(msg.messageLib.enetrcodePharmaceutical.value))
                    mydb.member_update_chatid('registration_progress', 5, message['chat']['id'])
                    tempMember.register_progress = 5
                elif tempMember.membership_type == 3:
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
                        mydb.technicalManager_update('membership_card_photo', '{0}{1}'.format(ufid, fileExtention),
                                                     message['chat']['username'])
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
                                                                            message['chat']['username'])))
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
                                            message['chat']['username'])
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
                                            message['chat']['username'])
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
                    print(chatIdUser)
                    if chatIdUser is not None:
                        mydb.member_update_chatid('desc', message['text'], chatIdUser)
                        mydb.member_update_chatid('adminChatId', 'Deny', chatIdUser)
                        mydb.del_member_chatid(chatid=chatIdUser)
                        bot.sendMessage(chatIdUser, msg.messageLib.sorryDenyAdmin.value)
                        bot.sendMessage(chatIdUser, message['text'])
        elif 'callback_query' in update:
            message = update['callback_query']['message']
            btn = update['callback_query']['data']
            spBtn = btn.split('_')
            pprint(btn)
            if len(spBtn) > 1:
                if spBtn[1] == 'verify':
                    mydb.member_update_chatid('verifyAdmin', 1, spBtn[2])
                    bot.sendMessage(spBtn[2], msg.messageLib.congratulationsApproveAdmin.value)
                elif spBtn[1] == 'deny':
                    bot.sendMessage(message['chat']['id'],
                                    str(msg.messageLib.descDenyAdmin.value))
                    mydb.member_update_chatid('registration_progress', 15, spBtn[2])
                    mydb.member_update_chatid('adminChatId', message['chat']['id'], spBtn[2])

            if btn == 'btnFounder':
                tempMember.userName = update['callback_query']['from']['username']
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
                tempMember.userName = update['callback_query']['from']['username']
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
                tempMember.userName = update['callback_query']['from']['username']
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
                tempMember.userName = update['callback_query']['from']['username']
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
                                                                  message['chat']['username'])))
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
                                                                  message['chat']['username'])))
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
                                                                  message['chat']['username'])))
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
        elif 'my_chat_member' in update:
            continue
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
        elif 'my_chat_member' in update:
            continue
        user_id = message['chat']['id']
        user_name = None
        if 'username' in message['chat']:
            user_name = message['chat']['username']
        else:
            user_name = ' کاربر '
        # پردازش پیام جدید
        handle_new_messages(user_id, user_name)


# شروع برنامه
def main():
    while True:
        # دریافت تمامی پیام های دریافتی
        updates = bot.getUpdates(timeout=10)
        if updates:
            handle_updates(updates)


if __name__ == '__main__':
    main()
