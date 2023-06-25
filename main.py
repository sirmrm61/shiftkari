import telepot
import threading
import time
import json
from model.membership import Membership
import os
from pprint import pprint
import msg
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
import db.mysqlconnector as msc
import uuid
import menu

last_update_ids = {}
# زمان حداکثر برای فعال بودن آخرین پیام دریافتی (به ثانیه)
MAX_IDLE_TIME = 600

mydb = msc.mysqlconnector()
idFromFile = None

bot = telepot.Bot('6012649808:AAGXWUsZJBtvWsFlYuvqg18tgIwo7ildPUs')


def handle_new_messages(user_id, userName):
    global last_update_ids
    # دریافت آخرین شناسه update_id برای کاربر
    # tempMember, last_update_time = last_update_ids.get(user_id, (Membership, 0))
    tempV = last_update_ids.get(user_id)
    tempMember = None if tempV is None else tempV[0]
    last_update_time = 0 if tempV is None else tempV[1]
    if tempMember is None:
        tempMember = mydb.load_member(userName)
        if tempMember is not None:
            last_update_id = tempMember.lastMessage
        else:
            tempMember = mydb.create_member(Membership(userName=userName))
            last_update_id = 0
    else:
        last_update_id = int(tempMember.lastMessage)

    # محاسبه زمان گذشته از آخرین پیام دریافتی
    elapsed_time = time.time() - last_update_time
    # اگر زمان گذشته بیشتر از حداکثر زمان مجاز باشد، آخرین شناسه update_id برای کاربر حذف می شود
    if elapsed_time > MAX_IDLE_TIME and last_update_time > 0:
        del last_update_ids[user_id]
        return
    # pprint('tempmember = {}'.format(tempMember.userName))
    # print('get last_message_id = {} where user is {}'.format(last_update_id, user_id))
    # دریافت پیام های جدید
    updates = bot.getUpdates(offset=last_update_id + 1, timeout=10)
    message = None
    for update in updates:
        print(update)
        if 'message' in update:
            message = update['message']
            if tempMember.register_progress == 0 and message['text'] == '/start':
                bot.sendMessage(message['chat']['id'], str(msg.messageLib.helloClient.value).format(
                    message['chat']['first_name']), reply_markup=menu.keyLib.kbWhoAreYou)
            elif tempMember.register_progress == 1:
                mydb.member_update('name', message['text'], message['chat']['username'])
                bot.sendMessage(message['chat']['id'],
                                str(msg.messageLib.enterLastName.value))
                mydb.member_update('registration_progress', 2, message['chat']['username'])
                tempMember.register_progress = 2
            elif tempMember.register_progress == 2:
                mydb.member_update('last_name', message['text'], message['chat']['username'])
                bot.sendMessage(message['chat']['id'],
                                str(msg.messageLib.enterPhoneNumber.value))
                mydb.member_update('registration_progress', 3, message['chat']['username'])
                tempMember.register_progress = 3
            elif tempMember.register_progress == 3:
                mydb.member_update('phone_number', message['text'], message['chat']['username'])
                if tempMember.membership_type == 1:
                    bot.sendMessage(message['chat']['id'],
                                    str(msg.messageLib.enterPharmacyName.value))
                elif tempMember.membership_type == 2 or tempMember.membership_type == 3:
                    bot.sendMessage(message['chat']['id'],
                                    str(msg.messageLib.enterNationCode.value))
                mydb.member_update('registration_progress', 4, message['chat']['username'])
                tempMember.register_progress = 4
            elif tempMember.register_progress == 4:
                if tempMember.membership_type == 1:
                    mydb.founder_update('pharmacy_name', message['text'], message['chat']['username'])
                    bot.sendMessage(message['chat']['id'],
                                    str(msg.messageLib.enterPharmacyType.value),
                                    reply_markup=menu.keyLib.kbTypePharmacy)
                    mydb.member_update('registration_progress', 5, message['chat']['username'])
                    tempMember.register_progress = 5
                elif tempMember.membership_type == 2:
                    mydb.technicalManager_update('national_code', message['text'], message['chat']['username'])
                    bot.sendMessage(message['chat']['id'],
                                    str(msg.messageLib.enetrcodePharmaceutical.value))
                    mydb.member_update('registration_progress', 5, message['chat']['username'])
                    tempMember.register_progress = 5
                elif tempMember.membership_type == 3:
                    mydb.student_update('national_code', message['text'], message['chat']['username'])
                    bot.sendMessage(message['chat']['id'],
                                    str(msg.messageLib.enterLicenseStartDate.value))
                    mydb.member_update('registration_progress', 5, message['chat']['username'])
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
                        mydb.member_update('registration_progress', 10, message['chat']['username'])
                        bot.sendMessage(message['chat']['id'],
                                        str(msg.messageLib.endRegisteration.value))
                    else:
                        bot.sendMessage(message['chat']['id'],
                                        str(msg.messageLib.errorSendFile.value))
                elif tempMember.membership_type == 3:
                    mydb.student_update('start_date', message['text'], message['chat']['username'])
                    bot.sendMessage(message['chat']['id'],
                                    str(msg.messageLib.enterLicenseEndDate.value))
                    mydb.member_update('registration_progress', 6, message['chat']['username'])
                    tempMember.register_progress = 6
            elif tempMember.register_progress == 6:
                if tempMember.membership_type == 1:
                    mydb.founder_update('pharmacy_address', message['text'], message['chat']['username'])
                    bot.sendMessage(message['chat']['id'],
                                    str(msg.messageLib.enterPharmacyLicensePhoto.value))
                    mydb.member_update('registration_progress', 7, message['chat']['username'])
                    tempMember.register_progress = 7
                elif tempMember.membership_type == 3:
                    mydb.student_update('end_date', message['text'], message['chat']['username'])
                    bot.sendMessage(message['chat']['id'],
                                    str(msg.messageLib.enterWorkoverPermitPhoto.value))
                    mydb.member_update('registration_progress', 7, message['chat']['username'])
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
                                            message['chat']['username'])
                        mydb.member_update('registration_progress', 10, message['chat']['username'])
                        bot.sendMessage(message['chat']['id'],
                                        str(msg.messageLib.endRegisteration.value))
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
                        mydb.member_update('registration_progress', 8, message['chat']['username'])
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
                        mydb.student_update('overtime_license_photo', '{0}{1}'.format(ufid, fileExtention),
                                            message['chat']['username'])
                        mydb.member_update('`personal_photo`', 9, message['chat']['username'])
                        tempMember.register_progress = 9
                        bot.sendMessage(message['chat']['id'],
                                        str(msg.messageLib.enterPermitActivity.value),
                                        reply_markup=menu.keyLib.kbTypeShift)
                    else:
                        bot.sendMessage(message['chat']['id'],
                                        str(msg.messageLib.errorSendFile.value))


        elif 'callback_query' in update:
            message = update['callback_query']['message']
            btn = update['callback_query']['data']
            if btn == 'btnFounder':
                tempMember.userName = update['callback_query']['from']['username']
                tempMember.lastMessage = update['update_id']
                tempMember.membership_type = 1
                tempMember.chatId = update['callback_query']['chat_instance']
                tempMember.register_progress = 1
                mydb.member_update('membership_type', 1, message['chat']['username'])
                pprint(mydb.member_update('registration_progress', 1, message['chat']['username']))
                bot.sendMessage(message['chat']['id'],
                                str(msg.messageLib.enterName.value))
            if btn == 'btnTechnicalResponsible':
                tempMember.userName = update['callback_query']['from']['username']
                tempMember.lastMessage = update['update_id']
                tempMember.membership_type = 2
                tempMember.chatId = update['callback_query']['chat_instance']
                tempMember.register_progress = 1
                mydb.member_update('membership_type', 2, message['chat']['username'])
                pprint(mydb.member_update('registration_progress', 1, message['chat']['username']))
                bot.sendMessage(message['chat']['id'],
                                str(msg.messageLib.enterName.value))
            if btn == 'btnStudent':
                tempMember.userName = update['callback_query']['from']['username']
                tempMember.lastMessage = update['update_id']
                tempMember.membership_type = 3
                tempMember.chatId = update['callback_query']['chat_instance']
                tempMember.register_progress = 1
                mydb.member_update('membership_type', 3, message['chat']['username'])
                pprint(mydb.member_update('registration_progress', 1, message['chat']['username']))
                bot.sendMessage(message['chat']['id'],
                                str(msg.messageLib.enterName.value))
            if btn == 'btNightDay':
                mydb.founder_update('pharmacy_type', 'شبانه روزی', message['chat']['username'])
                bot.sendMessage(message['chat']['id'],
                                str(msg.messageLib.enterPharmacyAddress.value))
                mydb.member_update('registration_progress', 6, message['chat']['username'])
                tempMember.register_progress = 6
            if btn == 'btnNormal':
                mydb.founder_update('pharmacy_type', 'عادی', message['chat']['username'])
                bot.sendMessage(message['chat']['id'],
                                str(msg.messageLib.enterPharmacyAddress.value))
                mydb.member_update('registration_progress', 6, message['chat']['username'])
                tempMember.register_progress = 6
            if btn == 'btShiftMorning':
                mydb.student_update('shift_access', 'صبح', message['chat']['username'])
                bot.sendMessage(message['chat']['id'],
                                str(msg.messageLib.endRegisteration.value))
                mydb.member_update('registration_progress', 10, message['chat']['username'])
                tempMember.register_progress = 10
            if btn == 'btShiftEvening':
                mydb.student_update('shift_access', 'عصر', message['chat']['username'])
                bot.sendMessage(message['chat']['id'],
                                str(msg.messageLib.endRegisteration.value))
                mydb.member_update('registration_progress', 10, message['chat']['username'])
                tempMember.register_progress = 10
            if btn == 'btShiftEveningNight':
                mydb.student_update('shift_access', 'عصر و شب', message['chat']['username'])
                bot.sendMessage(message['chat']['id'],
                                str(msg.messageLib.endRegisteration.value))
                mydb.member_update('registration_progress', 10, message['chat']['username'])
                tempMember.register_progress = 10
            if btn == 'btShiftMorningEvening':
                mydb.student_update('shift_access', 'صبح و عصر', message['chat']['username'])
                bot.sendMessage(message['chat']['id'],
                                str(msg.messageLib.endRegisteration.value))
                mydb.member_update('registration_progress', 10, message['chat']['username'])
                tempMember.register_progress = 10
            # پردازش پیام

        # بروزرسانی شناسه آخرین پیام دریافتی و زمان آن
        # print('last_message_id = {} where user is {}'.format(update['update_id'], user_id))
        print('test = {}'.format(tempMember.register_progress))
        last_update_ids[user_id] = (tempMember, update['update_id'])
        mydb.set_member_last_update_id(message['chat']['username'], update['update_id'])


# پردازش تمامی پیام های دریافتی
def handle_updates(updates):
    for update in updates:
        if 'message' in update:
            message = update['message']
        elif 'callback_query' in update:
            message = update['callback_query']['message']
        user_id = message['chat']['id']
        user_name = message['chat']['username']

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
