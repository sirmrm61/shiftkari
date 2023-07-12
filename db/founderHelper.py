import db.mysqlconnector as msc
import msg
import menu
mydb=msc.mysqlconnector()
class helperFunder:
    def msg_get_all_shift_approve(self=None,message=None,bot=None):
        allShift=mydb.get_shift_no_approve(progress=2,creator=message['chat']["id"])
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
    def send_info_funder(chatid,funder_chatid,shiftId,bot):
        tempMember=mydb.load_member(chatid)
        if tempMember.membership_type == 2 :
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
    def send_operation(tempMember,bot,chatid):
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
    def send_list_shift_Cancel(chatId,bot,todayDate):
        shifts = mydb.get_all_shift_by_approver(chatId,todayDate)
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
