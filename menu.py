import datetime

from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
import db.mysqlconnector as msc
from persiantools.jdatetime import JalaliDate

mydb = msc.mysqlconnector()
listTypeMember = [InlineKeyboardButton(text='موسسان', callback_data='btnFounder'),
                  InlineKeyboardButton(text='مسئولان فنی', callback_data='btnTechnicalResponsible'),
                  InlineKeyboardButton(text='دانشجویان', callback_data='btnStudent'),
                  InlineKeyboardButton(text='مدیران', callback_data='btnMananger')]


class keyLib:
    def kbWhoAreYou(self=None, exclude=None):
        ltm = []
        if exclude == None:
            ltm = listTypeMember
        else:
            for idx, item in enumerate(listTypeMember):
                if not idx == int(exclude) - 1:
                    ltm.append(item)
        return InlineKeyboardMarkup(inline_keyboard=[ltm])

    def kbTypePharmacy(self=None):
        return InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='شبانه روزی', callback_data='btNightDay'),
             InlineKeyboardButton(text='عادی', callback_data='btnNormal')]
        ])

    def kbTypePharmacyCS(self=None, idShift=0):
        return InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='شبانه روزی', callback_data=f'btn_btNightDayCS_{idShift}'),
             InlineKeyboardButton(text='عادی', callback_data=f'btn_btnNormalCS_{idShift}')]
        ])
    def kbTypePharmacyTime(self=None, idShift=0):
        return InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='زمان آزاد', callback_data=f'btn_freeTime_{idShift}'),
             InlineKeyboardButton(text='زمان استاندارد', callback_data=f'btn_timeStandard_{idShift}')]
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
            [InlineKeyboardButton(text='حذف شیفت', callback_data='btn_deleteShift_{}'.format(str(chatId))),
             InlineKeyboardButton(text='شیفت های من', callback_data='btn_listSift_{}'.format(str(chatId)))],
            [InlineKeyboardButton(text='ثبت شیفت اضطراری', callback_data='btn_createShiftEm_{}'.format(str(chatId))),
             InlineKeyboardButton(text='ثبت شیفت', callback_data='btn_createShift_{}'.format(str(chatId)))],
            [InlineKeyboardButton(text='ویرایش پروفایل', callback_data='btn_epf_{}'.format(str(chatId))),
             InlineKeyboardButton(text='غیر فعال', callback_data='btn_removeProfile_{}'.format(str(chatId)))],
            [InlineKeyboardButton(text='شیفت هایی که پر کرده ام',
                                  callback_data='btn_ownerShift_{}'.format(str(chatId)))],
            [InlineKeyboardButton(text='ثبت نیاز به پروانه',
                                  callback_data='btn_licenseNeed_{}'.format(str(chatId)))],
            [InlineKeyboardButton(text='پروانه ها با ساعات خالی',
                                  callback_data='btn_listLicenseEmpty_{}'.format(str(chatId)))],
            [InlineKeyboardButton(text='پروانه ها درخواستی من',
                                  callback_data='btn_myListLicense_{}'.format(str(chatId)))]
        ])

    def kbCreateMenuResponsible(self=None, chatId=None):
        return InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='شیفت های من', callback_data='btn_listSift_{}'.format(str(chatId))),
             InlineKeyboardButton(text='کنسل کردن شیفت', callback_data='btn_cancelShift_{}'.format(str(chatId)))],
            [InlineKeyboardButton(text='درخواست پر کردن شیفت', callback_data='btn_repShift_{}'.format(str(chatId)))],
            [InlineKeyboardButton(text='حذف شیفت', callback_data='btn_deleteShift_{}'.format(str(chatId))),
             InlineKeyboardButton(text='ویرایش پروفایل', callback_data='btn_epf_{}'.format(str(chatId)))],
            [InlineKeyboardButton(text='ثبت شیفت اضطراری', callback_data='btn_createShiftEm_{}'.format(str(chatId))),
             InlineKeyboardButton(text='ثبت شیفت', callback_data='btn_createShift_{}'.format(str(chatId)))],
            [InlineKeyboardButton(text='غیر فعال', callback_data='btn_removeProfile_{}'.format(str(chatId)))],
            [InlineKeyboardButton(text='شیفت هایی که پر کرده ام',
                                  callback_data='btn_ownerShift_{}'.format(str(chatId))), ],
            [InlineKeyboardButton(text='ثبت ساعات خالی پروانه',
                                  callback_data='btn_licenseEmpty_{}'.format(str(chatId)))],
            [InlineKeyboardButton(text='لیست درخواست پروانه ',
                                  callback_data='btn_listLicenseNeed_{}'.format(str(chatId)))],
            [InlineKeyboardButton(text='ساعات خالی پروانه من ',
                                  callback_data='btn_myListLicense_{}'.format(str(chatId)))]
        ])

    def kbCreateMenuStudent(self=None, chatId=None):
        return InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='درخواست پر کردن شیفت', callback_data='btn_repShift_{}'.format(str(chatId)))],
            [InlineKeyboardButton(text='کنسل کردن شیفت', callback_data='btn_cancelShift_{}'.format(str(chatId))),
             InlineKeyboardButton(text='لیست شیفت', callback_data='btn_listSift_{}'.format(str(chatId))), ],
            [InlineKeyboardButton(text='ثبت شیفت اضطراری', callback_data='btn_createShiftEm_{}'.format(str(chatId))),
             InlineKeyboardButton(text='ثبت شیفت', callback_data='btn_createShift_{}'.format(str(chatId)))],
            [InlineKeyboardButton(text='غیر فعال', callback_data='btn_removeProfile_{}'.format(str(chatId))),
             InlineKeyboardButton(text='ویرایش پروفایل', callback_data='btn_epf_{}'.format(str(chatId))), ],
            [InlineKeyboardButton(text='شیفت هایی که پر کرده ام',
                                  callback_data='btn_ownerShift_{}'.format(str(chatId))), ]
        ])

    def kbCreateMenuManager(self=None, chatId=None):
        return InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='لیست موسسان', callback_data='btn_listFunderManager_{}'.format(str(chatId))),
             InlineKeyboardButton(text='لیست مسئولان فنی', callback_data='btn_listresponsible_{}'.format(str(chatId))),
             InlineKeyboardButton(text='لیست دانشجویان', callback_data='btn_listStudent_{}'.format(str(chatId)))],
            [InlineKeyboardButton(text='زمان مسئول', callback_data='btn_hr_{}'.format(str(chatId))),
             InlineKeyboardButton(text='حداقل دستمزد', callback_data='btn_minWage_{}'.format(str(chatId))), ],
            [InlineKeyboardButton(text='حداقل دستمزد دانشجو', callback_data='btn_minWFStudent_{}'.format(str(chatId))),
             InlineKeyboardButton(text='قیمت مصوبه پروانه', callback_data='btn_licenss_{}'.format(str(chatId)))],
            [InlineKeyboardButton(text='ساعت تشخیص شیفت اضطراری',
                                  callback_data='btn_shiftEMHr_{}'.format(str(chatId)))],
            [InlineKeyboardButton(text='دوره شیفت اضطراری', callback_data='btn_shiftPD_{}'.format(str(chatId)))],
            [InlineKeyboardButton(text='تعداد شیفت اضطراری', callback_data='btn_shiftPD_{}'.format(str(chatId)))],
            [InlineKeyboardButton(text='ارسال پیام', callback_data='btn_sendMessage_{}'.format(str(chatId))),
             InlineKeyboardButton(text='لیست شیفت', callback_data='btn_listSiftManager_{}'.format(str(chatId))),
             InlineKeyboardButton(text='ویرایش پروفایل', callback_data='btn_epf_{}'.format(str(chatId)))],
            [InlineKeyboardButton(text='جستجو',
                                  callback_data='btn_searchMenu_{}'.format(str(chatId)))],
        ])

    def kbCreateSearchMenu(self=None):
        return InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='مدیر', callback_data='btn_search_manager'),
             InlineKeyboardButton(text='دانشجو', callback_data='btn_search_student'),
             InlineKeyboardButton(text=' مسئول فنی', callback_data='btn_search_responsible'),
             InlineKeyboardButton(text='موسس', callback_data='btn_search_founder')],
            [InlineKeyboardButton(text='شیفت ', callback_data='btn_search_shift'),
             InlineKeyboardButton(text=' داروخانه ', callback_data='btn_search_pharmacy'),
             InlineKeyboardButton(text='پروانه', callback_data='btn_search_license'),
             InlineKeyboardButton(text='آمار استفاده', callback_data='btn_search_used')],
        ])

    def kbCreateCancelSearchMenu(self=None):
        return InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='کنسل کردن جستجو',
                                                                           callback_data='btn_cancelSearch')]])

    def kbCreateOperateSearchMenu(self=None, chatId=None, op=None):
        return InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='عملیات',
                                                                           callback_data='btn_operate_{0}_{1}'.format(
                                                                               chatId, op))]])

    def kbcreateSendMessage(self=None, chatId=None):
        return InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='مدیران', callback_data='btn_SM_0_{}'.format(str(chatId))),
             InlineKeyboardButton(text='موسسان', callback_data='btn_SM_1_{}'.format(str(chatId)))],
            [InlineKeyboardButton(text='مسئولان فنی', callback_data='btn_SM_2_{}'.format(str(chatId))),
             InlineKeyboardButton(text='دانشجویان', callback_data='btn_SM_3_{}'.format(str(chatId)))],
            [InlineKeyboardButton(text='همه', callback_data='btn_SM_4_{}'.format(str(chatId)))]
        ])

    def kbCreateMenuYesNO(self=None, chatId=None):
        return InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='بله', callback_data='btn_yes_{}'.format(str(chatId))),
             InlineKeyboardButton(text='خیر', callback_data='btn_NO_{}'.format(str(chatId)))]
        ])

    def kbApproveAllShiftYesNO(self=None, shiftId=None):
        return InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='خیر', callback_data='btn_NOApproveAllShift_{}'.format(str(shiftId))),
             InlineKeyboardButton(text='بله', callback_data='btn_yesApproveAllShift_{}'.format(str(shiftId)))]
        ])

    def kbCreateMenuDeleteShift(self=None, shiftId=None):
        return InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='بله', callback_data='btn_DeleteShiftList_{}'.format(str(shiftId))),
             InlineKeyboardButton(text='خیر', callback_data='btn_noDeleteShiftList_{}'.format(str(shiftId)))]
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

    def kbCreateLicenseMenu(self=None, idL=None):
        return InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='تمدید', callback_data='btn_Extension_{}'.format(str(idL))),
             InlineKeyboardButton(text='حذف', callback_data='btn_delLicense_{}'.format(str(idL)))]
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

    def kbCreateMenuMonthInYear(tag):
        return InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='خرداد', callback_data='btn_month_03_{}'.format(str(tag))),
             InlineKeyboardButton(text='اردیبهشت', callback_data='btn_month_02_{}'.format(str(tag))),
             InlineKeyboardButton(text='فروردین', callback_data='btn_month_01_{}'.format(str(tag))), ],
            [InlineKeyboardButton(text='شهریور', callback_data='btn_month_06_{}'.format(str(tag))),
             InlineKeyboardButton(text='مرداد', callback_data='btn_month_05_{}'.format(str(tag))),
             InlineKeyboardButton(text='تیر', callback_data='btn_month_04_{}'.format(str(tag)))],
            [InlineKeyboardButton(text='آذر', callback_data='btn_month_09_{}'.format(str(tag))),
             InlineKeyboardButton(text='آبان', callback_data='btn_month_08_{}'.format(str(tag))),
             InlineKeyboardButton(text='مهر', callback_data='btn_month_07_{}'.format(str(tag)))],
            [InlineKeyboardButton(text='اسفند', callback_data='btn_month_12_{}'.format(str(tag))),
             InlineKeyboardButton(text='بهمن', callback_data='btn_month_11_{}'.format(str(tag))),
             InlineKeyboardButton(text='دی', callback_data='btn_month_10_{}'.format(str(tag)))]])

    def kbCreateMenuYear(tag):
        return InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='سال جاری', callback_data='btn_year_currntYear_{}'.format(str(tag))),
             InlineKeyboardButton(text='سال بعد', callback_data='btn_year_nextYear_{}'.format(str(tag))), ],
        ])

    def kbVerifyEditProfile(self, tag):
        return InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='ویرایش میکنم', callback_data='btn_yesEditProfile_{}'.format(str(tag))),
             InlineKeyboardButton(text='تائید نهایی', callback_data='btn_noBack_{}'.format(str(tag))), ],
        ])

    def kbEditProfile(self=None, chatId=None):
        mem = mydb.load_member(chatid=chatId)
        if mem.membership_type == 1:
            return InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text='نوع کاربری',
                                      callback_data='btn_editProfile_typeEdit_{}'.format(str(chatId))),
                 InlineKeyboardButton(text='شماره تلفن',
                                      callback_data='btn_editProfile_phoneEdit_{}'.format(str(chatId))),
                 InlineKeyboardButton(text='نام خانوادگی',
                                      callback_data='btn_editProfile_familyEdit_{}'.format(str(chatId))),
                 InlineKeyboardButton(text='نام', callback_data='btn_editProfile_nameEdit_{}'.format(str(chatId))), ],
                [InlineKeyboardButton(text='تصویر مجوز',
                                      callback_data='btn_editProfile_licensePhotoEdit_{}'.format(str(chatId))),
                 InlineKeyboardButton(text='آدرس داوخانه',
                                      callback_data='btn_editProfile_pharmacyAddressEdit_{}'.format(str(chatId))),
                 InlineKeyboardButton(text='نوع داروخانه',
                                      callback_data='btn_editProfile_pharmacyTypeEdit_{}'.format(str(chatId))),
                 InlineKeyboardButton(text='نام داروخانه',
                                      callback_data='btn_editProfile_pharmacyNameEdit_{}'.format(str(chatId))), ],
                [InlineKeyboardButton(text='حذف کاربر',
                                      callback_data='btn_editProfile_deactiveUser_{}'.format(str(chatId))), ]
            ])
        elif mem.membership_type == 2:
            return InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text='نوع کاربری',
                                      callback_data='btn_editProfile_typeEdit_{}'.format(str(chatId))),
                 InlineKeyboardButton(text='شماره تلفن',
                                      callback_data='btn_editProfile_phoneEdit_{}'.format(str(chatId))),
                 InlineKeyboardButton(text='نام خانوادگی',
                                      callback_data='btn_editProfile_familyEdit_{}'.format(str(chatId))),
                 InlineKeyboardButton(text='نام', callback_data='btn_editProfile_nameEdit_{}'.format(str(chatId))), ],
                [InlineKeyboardButton(text='تصویر نظام پزشکی',
                                      callback_data='btn_editProfile_membershipCardPhotoEdit_{}'.format(str(chatId))),
                 InlineKeyboardButton(text='کد ملی',
                                      callback_data='btn_editProfile_nationCodeEdit_{}'.format(str(chatId))), ]
            ])
        elif mem.membership_type == 3:
            return InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text='نوع کاربری',
                                      callback_data='btn_editProfile_typeEdit_{}'.format(str(chatId))),
                 InlineKeyboardButton(text='شماره تلفن',
                                      callback_data='btn_editProfile_phoneEdit_{}'.format(str(chatId))),
                 InlineKeyboardButton(text='نام خانوادگی',
                                      callback_data='btn_editProfile_familyEdit_{}'.format(str(chatId))),
                 InlineKeyboardButton(text='نام', callback_data='btn_editProfile_nameEdit_{}'.format(str(chatId))),
                 ],
                [InlineKeyboardButton(text='ساعت مجوز',
                                      callback_data='btn_editProfile_hrPermitEdit_{}'.format(str(chatId))),
                 InlineKeyboardButton(text='پایان مجوز',
                                      callback_data='btn_editProfile_dateEndEdit_{}'.format(str(chatId))),
                 InlineKeyboardButton(text='شروع مجوز',
                                      callback_data='btn_editProfile_dateStartEdit_{}'.format(str(chatId))),
                 InlineKeyboardButton(text='کد ملی',
                                      callback_data='btn_editProfile_nationCodeEdit_{}'.format(str(chatId))), ],
                [InlineKeyboardButton(text='تصویر مجوز',
                                      callback_data='btn_editProfile_overTimeLiccenssEdit_{}'.format(str(chatId))),
                 InlineKeyboardButton(text='عکس پرسنلی',
                                      callback_data='btn_editProfile_personalPhotoEdit_{}'.format(str(chatId))),
                 InlineKeyboardButton(text='شیفت مجوز',
                                      callback_data='btn_editProfile_shiftAccessEdit_{}'.format(str(chatId))), ],
            ])
        elif mem.membership_type == 4:
            return InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text='نوع کاربری',
                                      callback_data='btn_editProfile_typeEdit_{}'.format(str(chatId))),
                 InlineKeyboardButton(text='شماره تلفن',
                                      callback_data='btn_editProfile_phoneEdit_{}'.format(str(chatId))),
                 InlineKeyboardButton(text='نام خانوادگی',
                                      callback_data='btn_editProfile_familyEdit_{}'.format(str(chatId))),
                 InlineKeyboardButton(text='نام', callback_data='btn_editProfile_nameEdit_{}'.format(str(chatId))),
                 ],
            ])

    def createMenuFromList(self=None, listMenu=[], totalInRow=2):
        lk = []
        for item in listMenu:
            lk.append(InlineKeyboardButton(text=item['text'],
                                           callback_data='btn_dayShift_{}'.format(str(item['key']))))
        N = totalInRow
        res = []
        mod = 0
        if (len(lk) % N) > 0: mod = 1
        for idx in range(0, (len(lk) // N) + mod):
            res.append(lk[idx * N: (idx + 1) * N])  # ToDo: check day is empty
        return InlineKeyboardMarkup(inline_keyboard=res)

    def kbCreateMenuEndSelection(self=None, idShift=None):
        return InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='پایان انتخاب', callback_data='btn_endSelection_{}'.format(str(idShift)))]
        ])

    def createMenuFromListDay(self, listDay, totalInRow=2):
        lk = []
        for item in listDay:
            lk.append(InlineKeyboardButton(text=item[1],
                                           callback_data='btn_daySelectedRemove_{}'.format(str(item[0]))))
        N = totalInRow
        res = []
        mod = 0
        if (len(lk) % N) > 0: mod = 1
        for idx in range(0, (len(lk) // N) + mod):
            res.append(lk[idx * N: (idx + 1) * N])  # ToDo: check day is empty
        return InlineKeyboardMarkup(inline_keyboard=res)

    def kbCreateMenuSendForCreator(self=None, idShift=None):
        return InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='ارسال', callback_data='btn_sendToCreator_{}'.format(str(idShift)))]
        ])

    def kbCreateMenuTypePharmacy(self=None, idShift=None):
        return InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='شبانه روزی', callback_data='btn_pharmacyType_{}'.format(str(idShift)))],
            [InlineKeyboardButton(text='عادی', callback_data='btn_pharmacyType_{}'.format(str(idShift)))]
        ])

    def createMenuFromListDayForApproveCreator(self, listDay, totalInRow=2):
        lk = []
        listIdDay = ''
        print(listDay)
        for item in listDay:
            listIdDay += str(item[0]) + '=' + str(item[2]) + '#'
            lk.append(InlineKeyboardButton(text=item[1],
                                           callback_data='btn_dayApproveCreator_{}'.format(
                                               str(item[0]) + '=' + str(item[2]))))
        listIdDay = listIdDay[:-1]
        if len(lk) > 1: lk.append(InlineKeyboardButton(text="همه روزها",
                                                       callback_data='btn_approveAllDay_{}'.format(listIdDay)))
        N = totalInRow
        res = []
        mod = 0
        if (len(lk) % N) > 0: mod = 1
        for idx in range(0, (len(lk) // N) + mod):
            res.append(lk[idx * N: (idx + 1) * N])  # ToDo: check day is empty
        return InlineKeyboardMarkup(inline_keyboard=res)

    def createMenuForSelectDay(self, year, month, startDay, endDay, idShift=0, totalInRow=7, isEM=2, typeShift=0,
                               isMorning=0):
        selectedDay = []
        sdFullData = None
        if idShift != 0:
            sdFullData = mydb.getListSelectedDay(idShift)
            selectedDay = [item[0] for item in sdFullData]
        currentDate = str(JalaliDate(datetime.datetime.now() + datetime.timedelta(days=int(isEM)))).split('-')
        dayValid = int(currentDate[2])
        if int(currentDate[1]) < month:
            dayValid = 0
        elif int(currentDate[1]) > month:
            if int(month) < 7:
                dayValid = 32
            else:
                dayValid = 31
        else:
            startDay = int(currentDate[2])
        listDay = [InlineKeyboardButton(text=f'شنبه', callback_data='spare'),
                   InlineKeyboardButton(text=f'1شنبه', callback_data='spare'),
                   InlineKeyboardButton(text=f'2شنبه', callback_data='spare'),
                   InlineKeyboardButton(text=f'3شنبه', callback_data='spare'),
                   InlineKeyboardButton(text=f'4شنبه', callback_data='spare'),
                   InlineKeyboardButton(text=f'5شنبه', callback_data='spare'),
                   InlineKeyboardButton(text=f'جمعه', callback_data='spare')]
        monthList = ['فروردین', 'اردیبهشت', 'خرداد',
                     'تیر', 'مرداد', 'شهریور',
                     'مهر', 'آبان', 'آذر',
                     'دی', 'بهمن', 'اسفند']
        dayList = ["0", "شنبه", "یکشنه", "دوشنبه", "سه شنبه", "چهارشنبه", "پنج شنبه", "جمعه"]
        dateStartMonth = JalaliDate(year, month, 1).to_gregorian()
        dateEndMonth = JalaliDate(year, month, endDay).to_gregorian()
        dayStart = dateStartMonth.isoweekday()
        dayEnd = dateEndMonth.isoweekday()
        if dayStart > 5:
            dayStart -= 5
        else:
            dayStart += 2
        if dayEnd > 5:
            dayEnd -= 5
        else:
            dayEnd += 2
        print(f'dayValid={dayValid}')
        if dayValid == 0:
            startDay = 1
            endDay += 1
        elif dayValid == 32 or dayValid == 31:
            startDay = dayValid
        else:
            endDay += 1
        for idx in range(1, dayStart):
            listDay.append(InlineKeyboardButton(text='-', callback_data='spare'))
        for idx in range(1, startDay):
            listDay.append(InlineKeyboardButton(text=f'🙅{idx}', callback_data='spare'))
        for day in range(startDay, endDay):
            if f'{str(year).zfill(4)}-{str(month).zfill(2)}-{str(day).zfill(2)}' in selectedDay:
                itemDay = [item for item in sdFullData if
                           item[0] == f'{str(year).zfill(4)}-{str(month).zfill(2)}-{str(day).zfill(2)}']
                emoji = None
                action = 'removeDay'
                if int(itemDay[0][7]) == 1:
                    if int(isMorning) == 1 or int(isMorning) == 2:
                        action = 'newDaySelect'
                    emoji = '🌞'
                elif int(itemDay[0][7]) == 2:
                    if int(isMorning) == 0 or int(isMorning) == 2:
                        action = 'newDaySelect'
                    emoji = '🌝'
                elif int(itemDay[0][7]) == 3:
                    if int(isMorning) == 2:
                        action = 'newDaySelect'
                    emoji = '🌓'
                elif int(itemDay[0][7]) == 4:
                    if int(isMorning) == 0 or int(isMorning) == 1:
                        action = 'newDaySelect'
                    emoji = '🌑'
                elif int(itemDay[0][7]) == 5:
                    if int(isMorning) == 1:
                        action = 'newDaySelect'
                    emoji = '🌖'
                elif int(itemDay[0][7]) == 6:
                    if int(isMorning) == 0:
                        action = 'newDaySelect'
                    emoji = '🌘'
                elif int(itemDay[0][7]) == 7:
                    emoji = '🥮'
                listDay.append(InlineKeyboardButton(text=f'{emoji}{day}',
                                                    callback_data=f'btn_{action}_{year}#{month}#{day}_{idShift}_{startDay}_{endDay}_{isEM}_{typeShift}_{isMorning}'))
            else:
                listDay.append(InlineKeyboardButton(text=f'👍{day}',
                                                    callback_data=f'btn_newDaySelect_{year}#{month}#{day}_{idShift}_{startDay}_{endDay}_{isEM}_{typeShift}_{isMorning}'))
        for idx in range(dayEnd, 7):
            listDay.append(InlineKeyboardButton(text='-', callback_data='spare'))
        N = totalInRow
        res = [[InlineKeyboardButton(text=f'{monthList[month - 1]}-{year}', callback_data='spare')]]
        mod = 0
        if (len(listDay) % N) > 0: mod = 1
        for idx in range(0, (len(listDay) // N) + mod):
            res.append(listDay[idx * N: (idx + 1) * N])  # ToDo: check day is empty
        res.append(
            [InlineKeyboardButton(text='ماه قبل >>',
                                  callback_data=f'btn_previousMonth_{year}#{month}#{startDay}_{idShift}_{typeShift}_{isEM}_{isMorning}'),
             InlineKeyboardButton(text='<< ماه بعد',
                                  callback_data=f'btn_nextMonth_{year}#{month}#{startDay}_{idShift}_{typeShift}_{isEM}_{isMorning}')])
        print(f'menu-isMorning={isMorning}')
        if int(typeShift) == 2:
            res.append(
                [InlineKeyboardButton(text='پایان انتخاب روز ها برای شیفت صبح',
                                      callback_data=f'btn_endSelectDay_{idShift}_{isMorning}')])
        elif int(typeShift) == 3:
            res.append(
                [InlineKeyboardButton(text='بازگشت به انتخاب شیفت های صبح',
                                      callback_data=f'btn_backwardToMorning_{idShift}_{year}#{month}#{startDay}_{isEM}')])
            res.append(
                [InlineKeyboardButton(text='پایان انتخاب روز ها برای شیفت عصر',
                                      callback_data=f'btn_endSelectDay_{idShift}_{isMorning}')])
        elif int(typeShift) == 4:
            res.append(
                [InlineKeyboardButton(text='بازگشت به انتخاب شیفت های عصر',
                                      callback_data=f'btn_backwardToEvening_{idShift}_{year}#{month}#{startDay}_{isEM}')])
            res.append(
                [InlineKeyboardButton(text='پایان انتخاب تاریخ ها برای شیفت شب',
                                      callback_data=f'btn_endSelectDay_{idShift}_{isMorning}')])
        elif int(typeShift) == 1:
            res.append(
                [InlineKeyboardButton(text='پایان انتخاب روز های شیفت',
                                      callback_data=f'btn_endSelectDay_{idShift}_{isMorning}')])
        return InlineKeyboardMarkup(inline_keyboard=res)

    def createMenuFromListDayForApproveCreatorNew(self, idShift, totalInRow=2, ability=0):
        lk = []
        listIdDay = ''
        listDay = mydb.getListSelectedDay(idShift)
        for item in listDay:
            listIdDay += str(item[1]) + '#'
            actionText = 'spare'
            if ability == 1:
                actionText = f'btn_dayApproveNew_{str(item[1])}'
            if item[3] is not None:
                lk.append(InlineKeyboardButton(text=f'{item[0]}<=>{item[3]}',
                                               callback_data=actionText))
            if item[4] is not None:
                lk.append(InlineKeyboardButton(text=f'{item[0]}<=>{item[4]}',
                                               callback_data=actionText))
            if item[5] is not None:
                lk.append(InlineKeyboardButton(text=f'{item[0]}<=>{item[5]}',
                                               callback_data=actionText))
            if item[6] is not None:
                lk.append(InlineKeyboardButton(text=f'{item[0]}<=>{item[6]}',
                                               callback_data=actionText))
        listIdDay = listIdDay[:-1]
        if len(lk) > 1 and ability == 1: lk.append(InlineKeyboardButton(text="همه روزها",
                                                                        callback_data='btn_approveAllDayNew_{}'.format(
                                                                            listIdDay)))
        N = totalInRow
        res = []
        mod = 0
        if (len(lk) % N) > 0: mod = 1
        for idx in range(0, (len(lk) // N) + mod):
            res.append(lk[idx * N: (idx + 1) * N])  # ToDo: check day is empty
        if len(res) > 1 and ability == 2:
            res.append([InlineKeyboardButton(text='شیفت را می پذیرم',
                                             callback_data='btn_shiftApprove_{}'.format(str(idShift)))])
        return InlineKeyboardMarkup(inline_keyboard=res)

    def kbCreateMenuApproveShift(self=None, shiftId=None):
        return InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='شیفت را می پذیرم', callback_data='btn_shiftApprove_{}'.format(str(shiftId)))]
        ])
