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

    def kbCreateMenuFunder(self=None, chatId=None):
        return InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='ساخت شیفت', callback_data='btn_createSift_{}'.format(str(chatId))),
             InlineKeyboardButton(text='حذف شیفت', callback_data='btn_deleteShift_{}'.format(str(chatId)))]
        ])

    def kbCreateMenuResponsible(self=None, chatId=None):
        return InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='ساخت شیفت', callback_data='btn_createSift_{}'.format(str(chatId))),
             InlineKeyboardButton(text='حذف شیفت', callback_data='btn_deleteShift_{}'.format(str(chatId)))],
            [InlineKeyboardButton(text='شیفت های من', callback_data='btn_listSift_{}'.format(str(chatId))),
             InlineKeyboardButton(text='کنسل کردن شیفت', callback_data='btn_cancelShift_{}'.format(str(chatId)))],
            [InlineKeyboardButton(text='درخواست پر کردن شیفت', callback_data='btn_repShift_{}'.format(str(chatId)))]
        ])

    def kbCreateMenuStudent(self=None, chatId=None):
        return InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='ویرایش پروفایل', callback_data='btn_editProfile_{}'.format(str(chatId))),
             InlineKeyboardButton(text='حذف پروفایل', callback_data='btn_removeProfile_{}'.format(str(chatId))),
             InlineKeyboardButton(text='تغییر نوع کاربری', callback_data='btn_changeType_{}'.format(str(chatId)))],
            [InlineKeyboardButton(text='لیست شیفت', callback_data='btn_listSift_{}'.format(str(chatId))),
             InlineKeyboardButton(text='کنسل کردن شیفت', callback_data='btn_cancelShift_{}'.format(str(chatId)))],
        ])

    def kbCreateMenuManager(self=None, chatId=None):
        return InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='لیست شیفت', callback_data='btn_listSiftManager_{}'.format(str(chatId))),
             # InlineKeyboardButton(text='نیازمند تائید', callback_data='btn_listSiftDisApprove_{}'.format(str(chatId))),
             # InlineKeyboardButton(text='تائید شده', callback_data='btn_listSiftApprove_{}'.format(str(chatId))),
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
            [InlineKeyboardButton(text='مورد تائید است',
                                  callback_data='btn_approveShiftFunder_{}'.format(str(shiftId))),
             InlineKeyboardButton(text='مورد تائید نیست',
                                  callback_data='btn_disApproveShiftFunder_{}'.format(str(shiftId)))
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

    def kbCreateMenuConfirmDelete(self=None, shiftId=None):
        return InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='حذف کردن شیفت', callback_data='btn_confirmDelete_{}'.format(str(shiftId)))]
        ])

    def kbCreateMenuDayInMonth(tag=None):
        return InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='01', callback_data='btn_day_01_{}'.format(str(tag))),
             InlineKeyboardButton(text='02', callback_data='btn_day_02_{}'.format(str(tag))),
             InlineKeyboardButton(text='03', callback_data='btn_day_03_{}'.format(str(tag))),
             InlineKeyboardButton(text='04', callback_data='btn_day_04_{}'.format(str(tag))),
             InlineKeyboardButton(text='05', callback_data='btn_day_05_{}'.format(str(tag))),
             InlineKeyboardButton(text='06', callback_data='btn_day_06_{}'.format(str(tag)))],
            [InlineKeyboardButton(text='07', callback_data='btn_day_07_{}'.format(str(tag))),
             InlineKeyboardButton(text='08', callback_data='btn_day_08_{}'.format(str(tag))),
             InlineKeyboardButton(text='09', callback_data='btn_day_09_{}'.format(str(tag))),
             InlineKeyboardButton(text='10', callback_data='btn_day_10_{}'.format(str(tag))),
             InlineKeyboardButton(text='11', callback_data='btn_day_11_{}'.format(str(tag))),
             InlineKeyboardButton(text='12', callback_data='btn_day_12_{}'.format(str(tag)))],
            [InlineKeyboardButton(text='13', callback_data='btn_day_13_{}'.format(str(tag))),
             InlineKeyboardButton(text='14', callback_data='btn_day_14_{}'.format(str(tag))),
             InlineKeyboardButton(text='15', callback_data='btn_day_15_{}'.format(str(tag))),
             InlineKeyboardButton(text='16', callback_data='btn_day_16_{}'.format(str(tag))),
             InlineKeyboardButton(text='17', callback_data='btn_day_17_{}'.format(str(tag))),
             InlineKeyboardButton(text='18', callback_data='btn_day_18_{}'.format(str(tag)))],
            [InlineKeyboardButton(text='19', callback_data='btn_day_19_{}'.format(str(tag))),
             InlineKeyboardButton(text='20', callback_data='btn_day_20_{}'.format(str(tag))),
             InlineKeyboardButton(text='21', callback_data='btn_day_21_{}'.format(str(tag))),
             InlineKeyboardButton(text='22', callback_data='btn_day_22_{}'.format(str(tag))),
             InlineKeyboardButton(text='23', callback_data='btn_day_23_{}'.format(str(tag))),
             InlineKeyboardButton(text='24', callback_data='btn_day_24_{}'.format(str(tag)))],
            [InlineKeyboardButton(text='25', callback_data='btn_day_25_{}'.format(str(tag))),
             InlineKeyboardButton(text='26', callback_data='btn_day_26_{}'.format(str(tag))),
             InlineKeyboardButton(text='27', callback_data='btn_day_27_{}'.format(str(tag))),
             InlineKeyboardButton(text='28', callback_data='btn_day_28_{}'.format(str(tag))),
             InlineKeyboardButton(text='29', callback_data='btn_day_29_{}'.format(str(tag))),
             InlineKeyboardButton(text='30', callback_data='btn_day_30_{}'.format(str(tag)))],
            [InlineKeyboardButton(text='31', callback_data='btn_day_31_{}'.format(str(tag)))]
        ])

    def kbCreateMenuMonthInYear( tag):
        return InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='فروردین', callback_data='btn_month_01_{}'.format(str(tag))),
             InlineKeyboardButton(text='اردیبهشت', callback_data='btn_month_02_{}'.format(str(tag))),
             InlineKeyboardButton(text='خرداد', callback_data='btn_month_03_{}'.format(str(tag)))],
            [InlineKeyboardButton(text='تیر', callback_data='btn_month_04_{}'.format(str(tag))),
             InlineKeyboardButton(text='مرداد', callback_data='btn_month_05_{}'.format(str(tag))),
             InlineKeyboardButton(text='شهریور', callback_data='btn_month_06_{}'.format(str(tag)))],
            [InlineKeyboardButton(text='مهر', callback_data='btn_month_07_{}'.format(str(tag))),
             InlineKeyboardButton(text='آبان', callback_data='btn_month_08_{}'.format(str(tag))),
             InlineKeyboardButton(text='آذر', callback_data='btn_month_09_{}'.format(str(tag)))],
            [InlineKeyboardButton(text='دی', callback_data='btn_month_10_{}'.format(str(tag))),
             InlineKeyboardButton(text='بهمن', callback_data='btn_month_11_{}'.format(str(tag))),
             InlineKeyboardButton(text='اسفند', callback_data='btn_month_12_{}'.format(str(tag)))]])

    def kbCreateMenuYear(tag):
        return InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='سال جاری', callback_data='btn_year_currntYear_{}'.format(str(tag))),
             InlineKeyboardButton(text='سال بعد', callback_data='btn_year_nextYear_{}'.format(str(tag))),],
        ])
    def kbVerifyEditProfile(self,tag):
        return InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='ویرایش میکنم', callback_data='btn_yesEditProfile_{}'.format(str(tag))),
             InlineKeyboardButton(text='بازگشت', callback_data='btn_noBack_{}'.format(str(tag))), ],
        ])