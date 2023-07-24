import db.mysqlconnector as msc
import msg
import menu

mydb = msc.mysqlconnector()


class helperFunder:
    def __init__(self):
        return

        allShift = mydb.get_shift_no_approve(progress=2, creator=message['chat']["id"])
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
              msg.messageLib.doYouLike.value), reply_markup=menu.keyLib.kbCreateMenuApproveShift(shiftId=shiftRow[9]))

    def send_info_funder(chatid, funder_chatid, shiftId, bot):
        tempMember = mydb.load_member(chatid)
        if tempMember.membership_type == 2:
            bot.sendMessage(funder_chatid,
                            str(msg.messageLib.messAdminApproveTechnical.value))
        elif tempMember.membership_type == 3:
            bot.sendMessage(funder_chatid,
                            str(msg.messageLib.messAdminApproveStudent.value))
        bot.sendMessage(funder_chatid,
                        str(msg.messageLib.labeName.value).format(tempMember.name,
                                                                  tempMember.last_name))
        bot.sendMessage(funder_chatid,
                        str(msg.messageLib.labelPhoneNumber.value).format(tempMember.phone_number))
        if tempMember.membership_type == 2:
            bot.sendMessage(funder_chatid,
                            str(msg.messageLib.labelNationCode.value).format(
                                mydb.get_technical_property('national_code',
                                                            chatid)))
            bot.sendMessage(funder_chatid,
                            str(msg.messageLib.labelMembershipCardPhoto.value))
            img = 'download/{}'.format(
                mydb.get_technical_property('membership_card_photo', chatid))
            bot.sendPhoto(funder_chatid, open(img, 'rb'))
            bot.sendMessage(funder_chatid, msg.messageLib.messAdminApprove.value,
                            reply_markup=menu.keyLib.kbCreateMenuShiftApproveFunder(shiftId=shiftId))
        elif tempMember.membership_type == 3:
            bot.sendMessage(funder_chatid,
                            str(msg.messageLib.labelNationCode.value).format(
                                mydb.get_student_property('national_code',
                                                          chatid)))
            bot.sendMessage(funder_chatid,
                            str(msg.messageLib.labelDateStartPermit.value).format(
                                mydb.get_student_property('start_date',
                                                          chatid)))
            bot.sendMessage(funder_chatid,
                            str(msg.messageLib.labelDateEndPermit.value).format(
                                mydb.get_student_property('end_date', chatid)))
            bot.sendMessage(funder_chatid,
                            str(msg.messageLib.labelShift.value).format(
                                mydb.get_student_property('shift_access', chatid)))
            bot.sendMessage(funder_chatid,
                            str(msg.messageLib.labelSelfiPhoto.value))
            img = 'download/{}'.format(mydb.get_student_property('personal_photo', chatid))
            print(
                'download/{}'.format(mydb.get_student_property('personal_photo', chatid)))
            bot.sendPhoto(funder_chatid, open(img, 'rb'))
            bot.sendMessage(funder_chatid,
                            str(msg.messageLib.labelPermitPhoto.value))
            img = 'download/{}'.format(
                mydb.get_student_property('overtime_license_photo', chatid))
            bot.sendPhoto(chatid, open(img, 'rb'))
            bot.sendMessage(chatid, msg.messageLib.messAdminApprove.value,
                            reply_markup=menu.keyLib.kbCreateMenuShiftApproveFunder(shiftId=chatid))

    def send_operation(tempMember, bot, chatid):
        if tempMember.membership_type == 1:
            bot.sendMessage(chatid, msg.messageLib.yourOperation.value,
                            reply_markup=menu.keyLib.kbCreateMenuFunder(chatId=chatid))
        elif tempMember.membership_type == 2:
            bot.sendMessage(chatid, msg.messageLib.yourOperation.value,
                            reply_markup=menu.keyLib.kbCreateMenuResponsible(chatId=chatid))
        elif tempMember.membership_type == 3:
            bot.sendMessage(chatid, msg.messageLib.yourOperation.value,
                            reply_markup=menu.keyLib.kbCreateMenuStudent(chatId=chatid))
        elif tempMember.membership_type == 4:
            bot.sendMessage(chatid, msg.messageLib.yourOperation.value,
                            reply_markup=menu.keyLib.kbCreateMenuManager(chatId=chatid))

    def send_list_shift_Cancel(chatId, bot, todayDate):
        shifts = mydb.get_all_shift_by_approver(chatId, todayDate)
        if len(shifts) == 0:
            bot.sendMessage(chatId, msg.messageLib.emptyList.value)
        else:
            for shiftRow in shifts:
                rowReq = 'درخواست دهنده: {}'.format(shiftRow[0])
                rowDate = 'تاریخ  : {}'.format(shiftRow[2])
                rowStartTime = 'ساعت شروع  : {}'.format(shiftRow[3])
                rowEndTime = 'ساعت پایان  : {}'.format(shiftRow[4])
                rowWage = 'حق الزحمه  : {}'.format(shiftRow[5])
                rowaddr = 'آدرس  : {}'.format(shiftRow[6])
                bot.sendMessage(chatId, '''
{0}
{1}
{2}
{3}
{4}
{5}
{6}'''.format(rowReq, rowDate, rowStartTime, rowEndTime, rowWage, rowaddr,
              msg.messageLib.doYouLike.value),
                                reply_markup=menu.keyLib.kbCreateMenuCancelShift(shiftId=shiftRow[9]))

    def validate_IR_national_id(national_id):
        # Check if national id has exactly 10 digits
        if not len(national_id) == 10:
            return False

        # Check if all characters in the national id are digits
        if not national_id.isdigit():
            return False
        return True

    def validate_IR_mobile_number(mobile_number):

        # Check if mobile number has exactly 11 digits
        if not len(mobile_number) == 11:
            return False

        # Check if mobile number starts with 09
        if not mobile_number.startswith('09'):
            return False

        # Check if all characters in the mobile number are digits
        if not mobile_number.isdigit():
            return False

        # If all conditions are met, return True
        return True

    def send_shift_to_technicalResponsible(idshift, bot):
        shiftRow = mydb.get_all_property_shift_byId(idshift)
        ts = mydb.get_all_ts_chatid()
        for t in ts:
            rowReq = 'درخواست دهنده: {}'.format(shiftRow[0])
            rowDate = 'تاریخ  : {}'.format(shiftRow[2])
            rowStartTime = 'ساعت شروع  : {}'.format(shiftRow[3])
            rowEndTime = 'ساعت پایان  : {}'.format(shiftRow[4])
            rowWage = 'حق الزحمه  : {}'.format(shiftRow[5])
            rowaddr = 'آدرس  : {}'.format(shiftRow[6])
            bot.sendMessage(t[0], '''
{0}
{1}
{2}
{3}
{4}
{5}
{6}'''.format(rowReq, rowDate, rowStartTime, rowEndTime, rowWage, rowaddr,
              msg.messageLib.doYouLike.value),
                            reply_markup=menu.keyLib.kbCreateMenuCancelShift(shiftId=shiftRow[9]))

    def send_shift_to_student(self=None, bot=None):
        shiftRows = mydb.get_list_shift_for_student()  # shift's for student
        students = mydb.get_all_student_chatid()  # 3 is tpe of student
        for shiftRow in shiftRows:
            for st in students:
                # todo: delete print
                print('student ={0}'.format(st[0]))
                mydb.shift_update_by_id(fieldName='send', fieldValue=1, idshift=shiftRow[9])
                rowReq = 'درخواست دهنده: {}'.format(shiftRow[0])
                rowDate = 'تاریخ  : {}'.format(shiftRow[2])
                rowStartTime = 'ساعت شروع  : {}'.format(shiftRow[3])
                rowEndTime = 'ساعت پایان  : {}'.format(shiftRow[4])
                rowWage = 'حق الزحمه  : {}'.format(shiftRow[5])
                rowaddr = 'آدرس  : {}'.format(shiftRow[6])
                bot.sendMessage(st[0], '''
{0}
{1}
{2}
{3}
{4}
{5}
{6}'''.format(rowReq, rowDate, rowStartTime, rowEndTime, rowWage, rowaddr,
              msg.messageLib.doYouLike.value),
                                reply_markup=menu.keyLib.kbCreateMenuApproveShift(shiftId=shiftRow[9]))

    def send_profile(self=None, chatid=None, bot=None):
        mem = mydb.load_member(chatid=chatid)
        profileInfo = 'نام:\t{0}\n'.format(mem.name)
        profileInfo += 'نام خانوادگی:\t{0}\n'.format(mem.last_name)
        profileInfo += 'تلفن همراه:\t{0}\n'.format(mem.phone_number)
        if mem.membership_type == 1:
            profileInfo += 'نوع کاربری:\t{0}\n'.format('موسس')
            profileInfo += 'نام داروخانه:\t{0}\n'.format(
                mydb.get_funder_property(fieldName='pharmacy_name', chatid=chatid))
            profileInfo += 'نوع  داروخانه:\t{0}\n'.format(
                mydb.get_funder_property(fieldName='pharmacy_type', chatid=chatid))
            profileInfo += 'تصویر مجوز داروخانه:\t{0}\n'
            img = 'download/{}'.format(mydb.get_student_property('personal_photo', chatid))
            bot.sendMessage(chatid, profileInfo)
            bot.sendPhoto(chatid, open(img, 'rb'))
        elif mem.membership_type == 2:
            profileInfo += 'نوع کاربری:\t{0}\n'.format('مسئول فنی')
            profileInfo += 'کد ملی:\t{0}\n'.format(
                mydb.get_technical_property(fieldName='national_code', chatid=chatid))
            profileInfo += 'تصویر مجوز نظام پزشکی:\t{0}\n'
            img = 'download/{}'.format(mydb.get_technical_property('membership_card_photo', chatid))
            bot.sendMessage(chatid, profileInfo)
            bot.sendPhoto(chatid, open(img, 'rb'))
        elif mem.membership_type == 3:
            profileInfo += 'نوع کاربری:\t{0}\n'.format('دانشجو')
            profileInfo += 'کد ملی:\t{0}\n'.format(mydb.get_student_property(fieldName='national_code', chatid=chatid))
            profileInfo += 'تاریخ شروع مجوز:\t{0}\n'.format(
                mydb.get_student_property(fieldName='start_date', chatid=chatid))
            profileInfo += 'تاریخ پایان مجوز:\t{0}\n'.format(
                mydb.get_student_property(fieldName='end_date', chatid=chatid))
            profileInfo += 'شیفت مجوز:\t{0}\n'.format(
                mydb.get_student_property(fieldName='shift_access', chatid=chatid))
            profileInfo += 'میزان ساعت مجوز:\t{0}\n'.format(
                mydb.get_student_property(fieldName='shift_access', chatid=chatid))
            profileInfo += 'تصویر مجوز نظام پزشکی:'
            img = 'download/{}'.format(mydb.get_student_property('overtime_license_photo', chatid))
            bot.sendMessage(chatid, profileInfo)
            bot.sendPhoto(chatid, open(img, 'rb'))
            bot.sendMessage(chatid, 'تصویر پروفایل')
            img = 'download/{}'.format(mydb.get_student_property('personal_photo', chatid))
            bot.sendPhoto(chatid, open(img, 'rb'))
        elif mem.membership_type == 4:
            profileInfo += 'نوع کاربری:\t{0}\n'.format('ادمین')
