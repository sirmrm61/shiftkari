from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
from enum import Enum


class keyLib:
    def kbWhoAreYou(self=None):
        return InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='موسسان', callback_data='btnFounder'),
             InlineKeyboardButton(text='مسئولان فنی', callback_data='btnTechnicalResponsible'),
             InlineKeyboardButton(text='دانشجویان', callback_data='btnStudent'),
             InlineKeyboardButton(text='مدیران', callback_data='btnMananger')]])

    def kbTypePharmacy(self=None):
        return InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='شبانه روزی', callback_data='btNightDay'),
             InlineKeyboardButton(text='عادی', callback_data='btnNormal')]
        ])

    def kbTypeShift(self=None):
        return InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='صبح', callback_data='btShiftMorning'),
             InlineKeyboardButton(text='عصر', callback_data='btShiftEvening')],
            [InlineKeyboardButton(text='عصر و شب', callback_data='btShiftEveningNight'),
             InlineKeyboardButton(text='صبح و عصر', callback_data='btShiftMorningEvening')]
        ])

    def kbAdmin(self=None):
        return InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='موسسان', callback_data='btListFunder'),
             InlineKeyboardButton(text='مسئولان فنی', callback_data='btListTechninal'),
             InlineKeyboardButton(text='دانشجویان', callback_data='btListStudent')],
            [InlineKeyboardButton(text='درخواست ها', callback_data='btListRequest'),
             InlineKeyboardButton(text='درخواست های تائید شده', callback_data='btListApprovedRequest'),
             InlineKeyboardButton(text='آمار', callback_data='btListTotal')]
        ])

    def kbAdminUsers(self=None):
        return InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='در انتظار تائید', callback_data='btShiftMorning'),
             InlineKeyboardButton(text='موسسان', callback_data='btShiftEvening')],
            [InlineKeyboardButton(text='مسئولان فنی', callback_data='btShiftMorning'),
             InlineKeyboardButton(text='دانشجویان', callback_data='btShiftEvening')]
        ])

    def kbCreateApproveKey(self=None, chat_id=None):
        return InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='تائید', callback_data='btn_verify_{}'.format(str(chat_id))),
             InlineKeyboardButton(text='عدم تائید', callback_data='btn_deny_{}'.format(str(chat_id)))]
        ])
    def kbCreateDelKey(self=None, chat_id=None):
        return InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='بلی', callback_data='btn_Del_{}'.format(str(chat_id))),
             InlineKeyboardButton(text='خیر', callback_data='btn_NoDel_{}'.format(str(chat_id)))]
        ])
    def kbCreateMenuFunder(self=None,chatId=None):
        return InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='ساخت شیفت', callback_data='btn_createSift_{}'.format(str(chatId))),
             InlineKeyboardButton(text='حذف شیفت', callback_data='btn_deleteShift_{}'.format(str(chatId)))]
        ])
    def kbCreateMenuResponsible(self=None,chatId=None):
        return InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='ساخت شیفت', callback_data='btn_createSift_{}'.format(str(chatId))),
             InlineKeyboardButton(text='حذف شیفت', callback_data='btn_deleteShift_{}'.format(str(chatId)))],
            [InlineKeyboardButton(text='شیفت های من', callback_data='btn_listSift_{}'.format(str(chatId))),
             InlineKeyboardButton(text='کنسل کردن شیفت', callback_data='btn_cancelShift_{}'.format(str(chatId)))],
            [InlineKeyboardButton(text='درخواست پر کردن شیفت', callback_data='btn_repShift_{}'.format(str(chatId)))]
        ])
    def kbCreateMenuStudent(self=None,chatId=None):
        return InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='لیست شیفت', callback_data='btn_listSift_{}'.format(str(chatId))),
             InlineKeyboardButton(text='کنسل مردن شیفت', callback_data='btn_cancelShift_{}'.format(str(chatId)))]
        ])

    def kbCreateMenuManager(self=None, chatId=None):
        return InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='لیست شیفت', callback_data='btn_listSiftManager_{}'.format(str(chatId))),
             InlineKeyboardButton(text='نیازمند تائید', callback_data='btn_listSiftDisApprove_{}'.format(str(chatId))),
             InlineKeyboardButton(text='تائید شده', callback_data='btn_listSiftApprove_{}'.format(str(chatId))),
             ],
            [InlineKeyboardButton(text='لیست موسسان', callback_data='btn_listFunderManager_{}'.format(str(chatId))),
             InlineKeyboardButton(text='لیست مسئولان فنی', callback_data='btn_listresponsible_{}'.format(str(chatId))),
             InlineKeyboardButton(text='لیست دانشجویان', callback_data='btn_listStudent_{}'.format(str(chatId)))],

            [InlineKeyboardButton(text='زمان مسئول', callback_data='btn_hr_{}'.format(str(chatId))),
             InlineKeyboardButton(text='حداقل دستمزد', callback_data='btn_minWage_{}'.format(str(chatId))),
             InlineKeyboardButton(text='قیمت مصوبه پروانه', callback_data='btn_licenss_{}'.format(str(chatId)))]
        ])
    def kbCreateMenuYesNO(self=None, chatId=None):
        return InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='بله', callback_data='btn_yes_{}'.format(str(chatId))),
             InlineKeyboardButton(text='خیر', callback_data='btn_NO_{}'.format(str(chatId)))]
        ])
    def kbCreateMenuApproveShift(self=None, shiftId=None):
        return InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='شیفت را می پذیرم', callback_data='btn_shiftApprove_{}'.format(str(shiftId)))]
        ])
    def kbCreateMenuDeleteShift(self=None, shiftId=None):
        return InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='بله'
                                       ' ', callback_data='btn_DeleteShiftList_{}'.format(str(shiftId)))]
        ])
    def kbCreateMenuShiftApproveManager(self=None, shiftId=None):
        return InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='بله', callback_data='btn_approveShiftManager_{}'.format(str(shiftId))),
             InlineKeyboardButton(text='خیر', callback_data='btn_disApproveShiftManager_{}'.format(str(shiftId)))
              ]
        ])
    def kbCreateMenuShiftApproveFunder(self=None, shiftId=None):
        return InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='مورد تائید است', callback_data='btn_approveShiftFunder_{}'.format(str(shiftId))),
             InlineKeyboardButton(text='مورد تائید نیست', callback_data='btn_disApproveShiftFunder_{}'.format(str(shiftId)))
              ]
        ])
    def kbCreateMenuCancelShift(self=None, shiftId=None):
        return InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='کنسل می کنم'
                                       ' ', callback_data='btn_cancelShiftBtnList_{}'.format(str(shiftId)))]
        ])
    def kbCreateMenuReactive(self=None, memberId=None):
        return InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='فعال کن', callback_data='btn_reactive_{}'.format(str(memberId)))]
        ])