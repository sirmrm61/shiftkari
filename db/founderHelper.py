import db.mysqlconnector as msc
import msg
import menu
from datetime import datetime as DT
from persiantools.jdatetime import JalaliDate
from dateutil.relativedelta import relativedelta
import datetime
from datetime import timedelta
from model.membership import Membership
import uuid
import os
from unidecode import unidecode

mydb = msc.mysqlconnector()
listDenyOP = [
    {"pr": 10, "op": 0, "msg": "عملیات نامعتبر است"},
    {"pr": 18, "op": 0, "msg": "عملیات نامعتبر است"},
    {"pr": 18, "op": 16, "msg": "عملیات نامعتبر است"}
]
listCommand = ['/myoperation', '/start', '/myinfo', '/changeHrStudent', '/changeMinWage', '/changeMinLicenss',
               '/CancelMessage', '/changeWFS','/changeShiftEmHr','/changePDEM','/changeTPDEM']


class HelperFunder:
    def __init__(self, op=0):
        self._op = op

    def checkStatus(self, bot, mem: Membership, update=None):
        if mem.register_progress >= 10:
            if mem.verifyAdmin == 0 and mem.register_progress != 18:
                bot.sendMessage(mem.chatId, msg.messageLib.notVerifyAdmin.value)
                return False
            txtMessage = None
            if 'message' in update and 'text' in update['message']:
                txtMessage = update['message']['text']
            res = [idx for idx in listCommand if idx.lower().startswith(str(txtMessage).split(" ")[0].lower())]
            if len(res) == 0 and not txtMessage in listCommand and not 'callback_query' in update:
                for item in listDenyOP:
                    if mem.register_progress == int(item["pr"]) and mem.op == int(item["op"]):
                        bot.sendMessage(mem.chatId, item["msg"])
                        return False
        return True

    def send_info_funder(self, chatid, funder_chatid, shiftId, bot):
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
            isExisting = os.path.exists(img)
            if isExisting:
                bot.sendPhoto(funder_chatid, open(img, 'rb'))
            else:
                bot.sendMessage(funder_chatid, 'فایل تصویر پیدا نشد')
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
            isExisting = os.path.exists(img)
            if isExisting:
                bot.sendPhoto(funder_chatid, open(img, 'rb'))
            else:
                bot.sendMessage(funder_chatid, 'فایل تصویر پیدا نشد')
            bot.sendMessage(funder_chatid,
                            str(msg.messageLib.labelPermitPhoto.value))
            img = 'download/{}'.format(
                mydb.get_student_property('overtime_license_photo', chatid))
            isExisting = os.path.exists(img)
            if isExisting:
                bot.sendPhoto(funder_chatid, open(img, 'rb'))
            else:
                bot.sendMessage(funder_chatid, 'فایل تصویر پیدا نشد')
            bot.sendMessage(funder_chatid, msg.messageLib.messAdminApprove.value,
                            reply_markup=menu.keyLib.kbCreateMenuShiftApproveFunder(shiftId=chatid))

    def send_operation(self, tempMember, bot, chatid):
        mydb.member_update('registration_progress', 10, chatid)
        mydb.member_update('op', 0, chatid)
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

    def formatShiftMessage(self, shiftRow, memberType=None):
        rowReq = 'درخواست دهنده: {}'.format(shiftRow[0])
        rowDate = 'تاریخ شروع : {}'.format(shiftRow[2])
        rowDateEnd = 'تاریخ پایان : {}'.format(shiftRow[10])
        rowStartTime = 'ساعت شروع  : {}'.format(shiftRow[3])
        rowEndTime = 'ساعت پایان  : {}'.format(shiftRow[4])
        if memberType != 3:
            rowWage = 'حق الزحمه  : {}'.format(shiftRow[5])
        elif memberType == 3:
            rowWage = 'حق الزحمه  : {}'.format(shiftRow[11])
        if memberType is None: rowWage += '{} حق الزحمه دانشجو  : {}'.format('\n', shiftRow[11])
        rowaddr = 'آدرس  : {}'.format(shiftRow[6])
        return '''
{0}
{1}
{6}
{2}
{3}
{4}
{5}
'''.format(rowReq, rowDate, rowStartTime, rowEndTime, rowWage, rowaddr, rowDateEnd)

    def send_list_shift_Cancel(self, chatId, bot, todayDate):
        shifts = mydb.get_all_shift_by_approver(chatId, todayDate)
        if len(shifts) == 0:
            bot.sendMessage(chatId, msg.messageLib.emptyList.value)
        else:
            for shiftRow in shifts:
                bot.sendMessage(chatId, self.formatShiftMessage(shiftRow, 0),
                                reply_markup=menu.keyLib.kbCreateMenuCancelShift(shiftId=shiftRow[9]))

    def validate_IR_national_id(self, national_id):
        # Check if national id has exactly 10 digits
        if not len(national_id) == 10:
            return False

        # Check if all characters in the national id are digits
        if not national_id.isdigit():
            return False
        return True

    def validate_IR_mobile_number(self=None, mobile_number=None):

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

    def send_shift_to_technicalResponsible(self, idShift, bot, creator=None):
        shiftRow = mydb.get_all_property_shift_byId(idShift)
        ts = mydb.get_all_ts_chatid(creator)
        for t in ts:
            bot.sendMessage(t[0], self.formatShiftMessage(shiftRow, 2),
                            reply_markup=menu.keyLib.kbCreateMenuApproveShift(shiftId=shiftRow[9]))

    def send_shift_to_studentEM(self, idShift, bot, creator=None):
        shiftRow = mydb.get_all_property_shift_byId(idShift)
        st = mydb.get_all_student_chatid()
        for s in st:
            bot.sendMessage(s[0], self.formatShiftMessage(shiftRow, 2),
                            reply_markup=menu.keyLib.kbCreateMenuApproveShift(shiftId=shiftRow[9]))
        mydb.shift_update_by_id('send', 1, idShift)

    def send_shift_to_student(self, bot):
        shiftRows = mydb.get_list_shift_for_student()  # shift's for student
        if len(shiftRows) > 0:
            students = mydb.get_all_student_chatid()  # 3 is tpe of student
            for shiftRow in shiftRows:
                for st in students:
                    mydb.shift_update_by_id(fieldName='send', fieldValue=1, idshift=shiftRow[9])
                    bot.sendMessage(st[0], self.formatShiftMessage(shiftRow, 3),
                                    reply_markup=menu.keyLib.kbCreateMenuApproveShift(shiftId=shiftRow[9]))

    def send_profile(self, chatid, bot, forUser=None):
        fuser = None
        if forUser is None:
            fuser = chatid
        else:
            fuser = forUser
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
            profileInfo += 'تصویر مجوز داروخانه:\t\n'
            img = 'download/{}'.format(mydb.get_funder_property('license_photo', chatid))
            bot.sendMessage(fuser, profileInfo)
            isExisting = os.path.exists(img)
            if isExisting:
                bot.sendPhoto(fuser, open(img, 'rb'))
            else:
                bot.sendMessage(fuser, 'فایل تصویر پیدا نشد')
        elif mem.membership_type == 2:
            profileInfo += 'نوع کاربری:\t{0}\n'.format('مسئول فنی')
            profileInfo += 'کد ملی:\t{0}\n'.format(
                mydb.get_technical_property(fieldName='national_code', chatid=chatid))
            profileInfo += 'تصویر مجوز نظام پزشکی:\t\n'
            img = 'download/{}'.format(mydb.get_technical_property('membership_card_photo', chatid))
            bot.sendMessage(fuser, profileInfo)
            isExisting = os.path.exists(img)
            if isExisting:
                bot.sendPhoto(fuser, open(img, 'rb'))
            else:
                bot.sendMessage(fuser, 'فایل تصویر پیدا نشد')
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
            bot.sendMessage(fuser, profileInfo)
            isExisting = os.path.exists(img)
            if isExisting:
                bot.sendPhoto(fuser, open(img, 'rb'))
            else:
                bot.sendMessage(fuser, 'فایل تصویر پیدا نشد')
            bot.sendMessage(fuser, ':تصویر پروفایل')
            img = 'download/{}'.format(mydb.get_student_property('personal_photo', chatid))
            isExisting = os.path.exists(img)
            if isExisting:
                bot.sendPhoto(fuser, open(img, 'rb'))
            else:
                bot.sendMessage(fuser, 'فایل تصویر پیدا نشد')
        elif mem.membership_type == 4:
            profileInfo += 'نوع کاربری:\t{0}\n'.format('ادمین')
            bot.sendMessage(fuser, profileInfo)

    def editProfile(self, bot, spBtn, mem: Membership):
        userId = mem.chatId
        mydb.member_update_chatid('opTime', DT.now(), userId)
        mydb.member_update_chatid('registration_progress', 18, userId)
        if spBtn[2] == 'nameEdit':  # edit registration_progress==18 && op==1
            mydb.member_update_chatid('op', 1, userId)
            bot.sendMessage(userId, msg.messageLib.enterName.value)

        elif spBtn[2] == 'familyEdit':
            mydb.member_update_chatid('op', 2, userId)
            bot.sendMessage(userId, msg.messageLib.enterLastName.value)
        elif spBtn[2] == 'phoneEdit':
            mydb.member_update_chatid('op', 4, userId)
            bot.sendMessage(userId, msg.messageLib.enterPhoneNumber.value)
        elif spBtn[2] == 'nationCodeEdit':
            mydb.member_update_chatid('op', 5, userId)
            bot.sendMessage(userId, msg.messageLib.enterNationCode.value)
        elif spBtn[2] == 'pharmacyNameEdit':
            mydb.member_update_chatid('op', 5, userId)
            bot.sendMessage(userId, msg.messageLib.enterPharmacyName.value)
        elif spBtn[2] == 'pharmacyTypeEdit':
            mydb.member_update_chatid('op', 6, userId)
            bot.sendMessage(userId, msg.messageLib.enterPharmacyType.value, reply_markup=menu.keyLib.kbTypePharmacy())
        elif spBtn[2] == 'pharmacyAddressEdit':
            mydb.member_update_chatid('op', 7, userId)
            bot.sendMessage(userId, msg.messageLib.enterPharmacyAddress.value)
        elif spBtn[2] == 'licensePhotoEdit':
            mydb.member_update_chatid('op', 8, userId)
            bot.sendMessage(userId, msg.messageLib.enterPharmacyLicensePhoto.value)
        elif spBtn[2] == 'membershipCardPhotoEdit':
            mydb.member_update_chatid('op', 9, userId)
            bot.sendMessage(userId, msg.messageLib.labelMembershipCardPhoto.value)
        elif spBtn[2] == 'dateStartEdit':
            mydb.member_update_chatid('op', 10, userId)
            bot.sendMessage(userId, msg.messageLib.enterLicenseStartDate.value)
            bot.sendMessage(chat_id=userId, text='سال را انتخاب کنید',
                            reply_markup=menu.keyLib.kbCreateMenuYear(tag=4))
        elif spBtn[2] == 'dateStartEdit':
            mydb.member_update_chatid('op', 11, userId)
            bot.sendMessage(userId, msg.messageLib.enterLicenseEndDate.value)
            bot.sendMessage(chat_id=userId, text='سال را انتخاب کنید',
                            reply_markup=menu.keyLib.kbCreateMenuYear(tag=5))
        elif spBtn[2] == 'hrPermitEdit':
            mydb.member_update_chatid('op', 12, userId)
            bot.sendMessage(userId, msg.messageLib.hrPermitTotal.value)
        elif spBtn[2] == 'shiftAccessEdit':
            mydb.member_update_chatid('op', 13, userId)
            bot.sendMessage(userId, str(msg.messageLib.enterPermitActivity.value),
                            reply_markup=menu.keyLib.kbTypeShift())
        elif spBtn[2] == 'overTimeLiccenssEdit':
            mydb.member_update_chatid('op', 14, userId)
            bot.sendMessage(userId, str(msg.messageLib.enterWorkoverPermitPhoto.value))
        elif spBtn[2] == 'personalPhotoEdit':
            mydb.member_update_chatid('op', 15, userId)
            bot.sendMessage(userId, str(msg.messageLib.enterSelfiPhoto.value))
        elif spBtn[2] == 'typeEdit':
            mydb.member_update_chatid('op', 16, userId)
            bot.sendMessage(userId, f'نوع کاربری جاری شما '
                                    f' <strong><u>{mem.getTextType()}</u></strong> '
                                    f'  می باشد برای تغییر آن روی یکی از کلید های زیر کلیک کنید.', parse_mode='html',
                            reply_markup=menu.keyLib.kbWhoAreYou(exclude=mem.membership_type))
        elif spBtn[2] == 'deactiveUser':
            mydb.member_update_chatid('del', 1, userId)
            bot.sendMessage(userId, f'نام کاربری شما غیر فعال گردید.')
        return None

    def regEditItem(self, mem: Membership, bot, newValue):
        userId = mem.chatId
        date1 = mem.opTime
        date2 = DT.now()
        diffDay = relativedelta(date2, date1)
        op = int(mydb.get_member_property_chatid('op', userId))
        # دریافت حداکثر زمان انتخاب مشخص تا تغییر مشخصه
        timeDiff = int(mydb.get_property_domain('timeDiff'))
        if diffDay.minutes > timeDiff:
            # return to end step registration & ready To register shift
            mydb.member_update_chatid('registration_progress', 10, userId)
            # return to end step register shift
            mydb.member_update_chatid('op', 0, userId)
            bot.sendMessage(userId, msg.messageLib.errorTimeEdit.value)
            return
        elif op == 1:
            mydb.member_update_chatid(fieldName='name', fieldValue=newValue['text'], chatid=userId)
        elif op == 2:
            mydb.member_update_chatid(fieldName='last_name', fieldValue=newValue['text'], chatid=userId)
        elif op == 4:
            phone = unidecode(newValue['text'])
            print(f'phoneNumber:{newValue["text"]}')
            if self.validate_IR_mobile_number(mobile_number=phone):
                mydb.member_update_chatid(fieldName='phone_number', fieldValue=phone, chatid=userId)
            else:
                bot.sendMessage(userId, msg.messageLib.errorPhoneNumber.value)
                return
        elif op == 5:
            if mem.membership_type == 2:
                nationCode = unidecode(newValue['text'])
                if self.validate_IR_national_id(nationCode):
                    mydb.technicalManager_update(fieldName='national_code', fieldValue=nationCode, chatid=userId)
                else:
                    bot.sendMessage(userId, msg.messageLib.errrorNation.value)
            elif mem.membership_type == 3:
                nationCode = unidecode(newValue['text'])
                if self.validate_IR_national_id(nationCode):
                    mydb.student_update(fieldName='national_code', fieldValue=nationCode, chatid=userId)
                else:
                    bot.sendMessage(userId, msg.messageLib.errrorNation.value)
            else:
                mydb.founder_update(fieldName='pharmacy_name', fieldValue=newValue['text'], chatid=userId)
        elif op == 7:
            mydb.founder_update(fieldName='pharmacy_address', fieldValue=newValue['text'], chatid=userId)
        elif op == 8:
            if 'photo' in newValue:
                file_id = newValue['photo'][-1]['file_id']
                file_path = bot.getFile(file_id)['file_path']
                fileName, fileExtention = os.path.splitext(file_path)
                ufid = uuid.uuid4()
                image_path = 'download/{0}{1}'.format(ufid, fileExtention)
                bot.download_file(file_id, image_path)
                mydb.founder_update('license_photo', '{0}{1}'.format(ufid, fileExtention),
                                    userId)
            else:
                bot.sendMessage(userId,
                                str(msg.messageLib.errorSendFile.value))
        elif op == 9:
            if 'photo' in newValue:
                file_id = newValue['photo'][-1]['file_id']
                file_path = bot.getFile(file_id)['file_path']
                fileName, fileExtention = os.path.splitext(file_path)
                ufid = uuid.uuid4()
                image_path = 'download/{0}{1}'.format(ufid, fileExtention)
                bot.download_file(file_id, image_path)
                mydb.technicalManager_update('membership_card_photo', '{0}{1}'.format(ufid, fileExtention),
                                             userId)
            else:
                bot.sendMessage(userId,
                                str(msg.messageLib.errorSendFile.value))
        elif op == 12:
            mydb.student_update(fieldName='hourPermit', fieldValue=newValue['text'], chatid=userId)
        elif op == 14:
            if 'photo' in newValue:
                file_id = newValue['photo'][-1]['file_id']
                file_path = bot.getFile(file_id)['file_path']
                fileName, fileExtention = os.path.splitext(file_path)
                ufid = uuid.uuid4()
                image_path = 'download/{0}{1}'.format(ufid, fileExtention)
                bot.download_file(file_id, image_path)
                mydb.student_update('overtime_license_photo', '{0}{1}'.format(ufid, fileExtention),
                                    userId)
            else:
                bot.sendMessage(userId,
                                str(msg.messageLib.errorSendFile.value))
        elif op == 15:
            if 'photo' in newValue:
                file_id = newValue['photo'][-1]['file_id']
                file_path = bot.getFile(file_id)['file_path']
                fileName, fileExtention = os.path.splitext(file_path)
                ufid = uuid.uuid4()
                image_path = 'download/{0}{1}'.format(ufid, fileExtention)
                bot.download_file(file_id, image_path)
                mydb.student_update('personal_photo', '{0}{1}'.format(ufid, fileExtention),
                                    userId)
            else:
                bot.sendMessage(userId,
                                str(msg.messageLib.errorSendFile.value))
        else:
            bot.sendMessage(userId, )

        mydb.member_update_chatid(fieldName='verifyAdmin', fieldValue=0, chatid=userId)
        # send message to user
        bot.sendMessage(userId, msg.messageLib.afterEdit.value,
                        reply_markup=menu.keyLib.kbVerifyEditProfile(self=None, tag=userId))

    def msg_get_all_shift_approve(self, chatId, bot):
        shiftRows = mydb.get_all_shift_managerApproved()
        if len(shiftRows) > 0:
            for shiftRow in shiftRows:
                listNotEmptyDay = mydb.getListDayIsNotEmpty(shiftRow[9])
                dateStr = '\nتاریخ های پر شده از این شیفت:\n'
                if len(listNotEmptyDay) > 0:
                    for item in listNotEmptyDay:
                        dateStr += item[1] + ','
                bot.sendMessage(chatId, self.formatShiftMessage(shiftRow) + dateStr,
                                reply_markup=menu.keyLib.kbCreateMenuApproveShift(shiftId=shiftRow[9]))
        else:
            bot.sendMessage(chatId, msg.messageLib.noShift.value)

    def endSelectionDayBtnClick(self, idShift, userId, bot):
        listDay = mydb.getListDaySelection(idShift, userId)
        if len(listDay) == 0:
            bot.sendMessage(userId, msg.messageLib.emptSelectedDay.value)
        else:
            bot.sendMessage(userId, msg.messageLib.selectedDay.value,
                            reply_markup=menu.keyLib.createMenuFromListDay(None, listDay, 2))
            bot.sendMessage(userId, msg.messageLib.sendForCreatorMessage.value,
                            reply_markup=menu.keyLib.kbCreateMenuSendForCreator(None, idShift))

    def send_shift_to_other(self, bot, idshift, userId, typeMember=2):
        shiftRow = mydb.get_all_property_shift_byId(idshift)  # shift's for student
        bot.sendMessage(userId, self.formatShiftMessage(shiftRow, typeMember),
                        reply_markup=menu.keyLib.kbCreateMenuShiftApproveManager(shiftId=shiftRow[9]))

    def yesApproveAllShift(self, idShift, userId, bot):
        mydb.shift_update_by_id('approver', userId, idShift)
        creator = mydb.get_shift_property('Creator', idShift)
        bot.sendMessage(creator, msg.messageLib.reqTitleMessageForCreator.value)
        self.send_profile(userId, bot, creator)
        self.send_shift_to_other(bot, idShift, creator)
        bot.sendMessage(userId, msg.messageLib.YourInfoToCreatorShift.value)

    def registerFullShiftDay(self, idShift, requester):
        dateStart = str(mydb.get_shift_property('DateShift', idShift)).split('-')
        dateEnd = str(mydb.get_shift_property('dateEndShift', idShift)).split('-')
        dsG = JalaliDate(int(dateStart[0]), int(dateStart[1]), int(dateStart[2])).to_gregorian()
        deG = JalaliDate(int(dateEnd[0]), int(dateEnd[1]), int(dateEnd[2])).to_gregorian()
        delta = deG - dsG
        listFullDay = mydb.getListDayIsNotEmpty(idShift)
        if len(listFullDay) > 0:
            listFullDay = list(zip(*listFullDay))[1]
        for i in range(delta.days + 1):
            day = dsG + timedelta(days=i)
            tmp = JalaliDate.to_jalali(day.year, day.month, day.day)
            txtTmp = str(tmp).replace('-', '.')
            mydb.registerDayShift(idShift, txtTmp, requester, 0, 2)

    def NOApproveAllShift(self, idShift, userID, bot):
        dateStart = str(mydb.get_shift_property('DateShift', idShift)).split('-')
        dateEnd = str(mydb.get_shift_property('dateEndShift', idShift)).split('-')
        dsG = JalaliDate(int(dateStart[0]), int(dateStart[1]), int(dateStart[2])).to_gregorian()
        deG = JalaliDate(int(dateEnd[0]), int(dateEnd[1]), int(dateEnd[2])).to_gregorian()
        delta = deG - dsG
        listFullDay = mydb.getListDayIsNotEmpty(idShift)
        if len(listFullDay) > 0:
            listFullDay = list(zip(*listFullDay))[1]
        listDay = []
        for i in range(delta.days + 1):
            tempDic = {}
            day = dsG + timedelta(days=i)
            tmp = JalaliDate.to_jalali(day.year, day.month, day.day)
            txtTmp = str(tmp).replace('-', '.')
            if txtTmp not in listFullDay:
                tempDic['text'] = str(tmp).replace('-', '.')
                tempDic['key'] = str(tmp).replace('-', '.') + f'={idShift}'
                listDay.append(tempDic)
        bot.sendMessage(userID,
                        msg.messageLib.shiftSelectDay.value
                        , reply_markup=menu.keyLib.createMenuFromList(listMenu=listDay))
        bot.sendMessage(userID, str(msg.messageLib.endShiftSelection.value),
                        reply_markup=menu.keyLib.kbCreateMenuEndSelection(idShift=idShift))

    def registerDay(self, idDay, bot, userId):
        statusDay = mydb.getShiftDayProperty('status', idDay)
        if statusDay == None:
            bot.sendMessage('6274361322', f'Can not find {idDay} in id to dayshift table')
            return None
        dateReq = mydb.getShiftDayProperty('dateShift', idDay)
        if mydb.isShiftDayFull(idDay, dateReq) > 0:
            bot.sendMessage(userId, msg.messageLib.invalidApproveDate.value)
            return None
        if (int(statusDay) != 2):
            mydb.updateShiftDay(fieldName='status', fieldValue=2, idDayShift=idDay)
            requesterShift = mydb.getShiftDayProperty('requster', idDay)
            bot.sendMessage(requesterShift, str(msg.messageLib.approvedDay.value).format(dateReq))
            return requesterShift
