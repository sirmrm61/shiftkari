class Membership:
    def __init__(self, name = None, last_name = None, phone_number = None, userName = None,chatid=None):
        self._name = None
        self._last_name = None
        self._phone_number = phone_number
        self._membership_type = 0
        self._membership_fee_paid = None
        self._register_progress = 0
        self._userName = userName
        self._chatId = chatid
        self._lastMessage = 0
        self._lastActivity = None
        self._chatid = None
        self._delf = 0

    @property
    def delf(self):
        return int(self._delf)

    @delf.setter
    def delf(self, new_delf):
        self._delf = int(new_delf)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, new_name):
        self._name = new_name

    @property
    def last_name(self):
        return self._last_name

    @last_name.setter
    def last_name(self, new_last_name):
        self._last_name = new_last_name

    @property
    def phone_number(self):
        return self._phone_number

    @phone_number.setter
    def phone_number(self, new_phone_number):
        self._phone_number = new_phone_number

    @property
    def membership_type(self):
        return int(self._membership_type)

    @membership_type.setter
    def membership_type(self, new_membership_type):
        self._membership_type = int(new_membership_type)

    @property
    def membership_fee_paid(self):
        return self._membership_fee_paid

    @membership_fee_paid.setter
    def membership_fee_paid(self, new_membership_fee_paid):
        self._membership_fee_paid = new_membership_fee_paid

    @property
    def register_progress(self):
        return int(self._register_progress)

    @register_progress.setter
    def register_progress(self, new_register_progress):
        self._register_progress = int(new_register_progress)

    @property
    def userName(self):
        return self._userName

    @userName.setter
    def userName(self, new_userName):
        self._userName = new_userName

    @property
    def chatId(self):
        return self._chatId

    @chatId.setter
    def chatId(self, new_chatId):
        self._chatId=new_chatId

    @property
    def lastMessage(self):
        return self._lastMessage

    @lastMessage.setter
    def lastMessage(self, new_lastMessage):
        self._lastMessage=new_lastMessage

    @property
    def lastActivity(self):
        return self._lastActivity

    @lastActivity.setter
    def lastActivity(self, new_lastActivity):
        self._lastActivity=new_lastActivity

class Founder(Membership):
    def __init__(self,name = None, last_name = None, phone_number = None,  membership_fee_paid = None,userName = None,
                 pharmacy_name = None, pharmacy_type = None, pharmacy_address = None, license_photo = None):
        super().__init__(name = name, last_name = last_name, phone_number = phone_number, membership_type = 1,
                         membership_fee_paid = membership_fee_paid,userName = userName)
        self._pharmacy_name = pharmacy_name
        self._pharmacy_type = pharmacy_type
        self._pharmacy_address = pharmacy_address
        self._license_photo = license_photo

    @property
    def pharmacy_name(self):
        return self._pharmacy_name

    @pharmacy_name.setter
    def pharmacy_name(self, new_pharmacy_name):
        self._pharmacy_name = new_pharmacy_name

    @property
    def pharmacy_type(self):
        return self._pharmacy_type

    @pharmacy_type.setter
    def pharmacy_type(self, new_pharmacy_type):
        self._pharmacy_type = new_pharmacy_type

    @property
    def pharmacy_address(self):
        return self._pharmacy_address

    @pharmacy_address.setter
    def pharmacy_address(self, new_pharmacy_address):
        self._pharmacy_address = new_pharmacy_address

    @property
    def license_photo(self):
        return self._license_photo

    @license_photo.setter
    def license_photo(self, new_license_photo):
        self._license_photo = new_license_photo


class TechnicalManager(Membership):
    def __init__(self, name = None, last_name = None, phone_number = None,  membership_fee_paid = None, national_id = None, pharmacy_membership_card_photo = None):
        super().__init__(name = None, last_name = None, phone_number = None, membership_type = 2, membership_fee_paid = None,userName = None)
        self._national_id = national_id
        self._pharmacy_membership_card_photo = pharmacy_membership_card_photo

    @property
    def national_id(self):
        return self._national_id

    @national_id.setter
    def national_id(self, new_national_id):
        self._national_id = new_national_id

    @property
    def pharmacy_membership_card_photo(self):
        return self._pharmacy_membership_card_photo

    @pharmacy_membership_card_photo.setter
    def pharmacy_membership_card_photo(self, new_pharmacy_membership_card_photo):
        self._pharmacy_membership_card_photo = new_pharmacy_membership_card_photo



class Student(Membership):
    def __init__(self, name = None, last_name = None, phone_number = None,
                  membership_fee_paid = None, national_id = None, permit_start_date = None, permit_end_date = None,
                 overtime_permit_photo = None, personal_photo = None, shift_permission = None, shift_fee_paid = None):
        super().__init__(name = None, last_name = None, phone_number = None, membership_type = 3, membership_fee_paid = None,userName = None)
        self._national_id = national_id
        self._permit_start_date = permit_start_date
        self._permit_end_date = permit_end_date
        self._overtime_permit_photo = overtime_permit_photo
        self._personal_photo = personal_photo
        self._shift_permission = shift_permission
        self._shift_fee_paid = shift_fee_paid

    @property
    def national_id(self):
        return self._national_id

    @national_id.setter
    def national_id(self, new_national_id):
        self._national_id = new_national_id

    @property
    def permit_start_date(self):
        return self._permit_start_date

    @permit_start_date.setter
    def permit_start_date(self, new_permit_start_date):
        self._permit_start_date = new_permit_start_date

    @property
    def permit_end_date(self):
        return self._permit_end_date

    @permit_end_date.setter
    def permit_end_date(self,new_permit_end_date):
        self._permit_end_date = new_permit_end_date

    @property
    def permit_end_date(self):
        return self._permit_end_date

    @permit_end_date.setter
    def permit_end_date(self,new_permit_end_date):
        self._permit_end_date = new_permit_end_date

    @property
    def overtime_permit_photo(self):
        return self._overtime_permit_photo

    @overtime_permit_photo.setter
    def overtime_permit_photo(self,new_overtime_permit_photo):
        self._overtime_permit_photo = new_overtime_permit_photo

    @property
    def personal_photo(self):
        return self._personal_photo

    @permit_end_date.setter
    def personal_photo(self,new_personal_photo):
        self._personal_photo = new_personal_photo

    @property
    def shift_permission(self):
        return self._shift_permission

    @shift_permission.setter
    def shift_permission(self,new_shift_permission):
        self._shift_permission = new_shift_permission

    @property
    def shift_fee_paid(self):
        return self._shift_fee_paid

    @shift_fee_paid.setter
    def shift_fee_paid(self, new_shift_fee_paid):
        self._shift_fee_paid = new_shift_fee_paid
