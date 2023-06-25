from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
from enum import Enum


class keyLib(Enum):
    kbWhoAreYou = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='موسس هستم', callback_data='btnFounder'),
         InlineKeyboardButton(text='مسئول فنی هستم', callback_data='btnTechnicalResponsible'),
         InlineKeyboardButton(text='دانشجو هستم', callback_data='btnStudent')]]),
    kbTypePharmacy = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='شبانه روزی', callback_data='btNightDay'),
         InlineKeyboardButton(text='عادی', callback_data='btnNormal')]
    ]),
    kbTypeShift = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='صبح', callback_data='btShiftMorning'),
         InlineKeyboardButton(text='عصر', callback_data='btShiftEvening')],
        [InlineKeyboardButton(text='عصر و شب', callback_data='btShiftEveningNight'),
         InlineKeyboardButton(text='صبح و عصر', callback_data='btShiftMorningEvening')]
    ]),
    kbAdmin = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='کاربران', callback_data='btShiftMorning'),
         InlineKeyboardButton(text='درخواست ها', callback_data='btShiftEvening')]
    ]),
    kbAdminUsers = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='در انتظار تائید', callback_data='btShiftMorning'),
         InlineKeyboardButton(text='موسسان', callback_data='btShiftEvening')],
        [InlineKeyboardButton(text='مسئول فنی', callback_data='btShiftMorning'),
         InlineKeyboardButton(text='دانشجویان', callback_data='btShiftEvening')]
    ])
