import datetime

import mysql.connector
import db.env as helper
from model.membership import Founder, Membership
from datetime import datetime as DT
from persiantools.jdatetime import JalaliDate


class mysqlconnector:
    def __init__(self):
        self._ipDb = helper.ipServer
        self._portDb = helper.portServer
        self._userDb = helper.userDb
        self._passDb = helper.passDb

    @property
    def ipDb(self):
        return self._ipDb

    @ipDb.setter
    def ipDb(self, new_ipDb):
        self._ipDb = new_ipDb

    @property
    def portDb(self):
        return self._portDb

    @portDb.setter
    def portDb(self, new_portDb):
        self._portDb = new_portDb

    @property
    def userDb(self):
        return self._userDb

    @userDb.setter
    def userDb(self, new_userDb):
        self._userDb = new_userDb

    @property
    def passDb(self):
        return self._passDb

    @passDb.setter
    def passDb(self, new_passDb):
        self._passDb = new_passDb

    def connector(self):
        return mysql.connector.connect(host=self._ipDb, user=self._userDb, password=self._passDb, port=self._portDb,
                                       database=helper.dbName)

    def insert_Founder(self, member: Founder):
        sqlQuery = 'select * from `botshiftkari`.`membership` where chat_id = \'{}\''.format(member.chatId)
        mydb = self.connector()
        mydb.autocommit = True
        myCursor = mydb.cursor()
        myCursor.execute(sqlQuery)
        result = myCursor.fetchall()
        myCursor.reset()
        if len(result) == 0:
            sql = '''insert into membership (name,last_name,phone_number,membership_type,membership_fee_paid,
                registration_progress,username,chat_id,last_message_sent) VALUEs (%s,%s,%s,%s,%s,%s,%s,%s,%s)'''
            val = (
                member.name, member.last_name, member.phone_number, member.membership_type, member.membership_fee_paid,
                member.register_progress, member.userName, member.chatId, member.lastMessage)
            myCursor.execute(sql, val)
            myCursor.reset()
        else:
            sql = 'UPDATE `botshiftkari`.`membership` SET'
            updateExp = ''
            if member.name is not None: updateExp = '`name` = \'{}\''.format(member.name)
            if member.last_name is not None:
                if updateExp is not None:
                    updateExp = '`last_name` = \'{}\''.format(member.last_name)
                else:
                    updateExp = ', `last_name` = \'{}\''.format(member.last_name)
            if member.phone_number is not None:
                if updateExp is not None:
                    updateExp = '`phone_number` = \'{}\''.format(member.phone_number)
                else:
                    updateExp = ', `phone_number` = \'{}\''.format(member.phone_number)
            if member.membership_fee_paid is not None:
                if updateExp is not None:
                    updateExp = '`membership_fee_paid` = \'{}\''.format(member.membership_fee_paid)
                else:
                    updateExp = ', `membership_fee_paid` = \'{}\''.format(member.membership_fee_paid)
            if member.register_progress is not None:
                if updateExp is not None:
                    updateExp = '`registration_progress` = \'{}\''.format(member.register_progress)
                else:
                    updateExp = ', `registration_progress` = \'{}\''.format(member.register_progress)
            if member.chatId is not None:
                if updateExp is not None:
                    updateExp = '`username` = \'{}\''.format(member.userName)
                else:
                    updateExp = ', `username` = \'{}\''.format(member.userName)
            if member.lastMessage is not None:
                if updateExp is not None:
                    updateExp = '`last_message_sent` = \'{}\''.format(member.lastMessage)
                else:
                    updateExp = ', `last_message_sent` = \'{}\''.format(member.lastMessage)
            if len(updateExp) > 0:
                updateExp += ' WHERE `chat_id` = \'{0}\';'.format(member.chatId)
                sql += updateExp
                result = myCursor.execute(sql)
        myCursor.reset()
        mydb.close()

    def getAdmins(self):
        sqlQuery = '''select chat_id from `botshiftkari`.`membership` 
                            where membership_type = 4 and verifyAdmin =1 and del=0'''
        mydb = self.connector()
        myCursor = mydb.cursor()
        myCursor.execute(sqlQuery)
        result = myCursor.fetchall()
        myCursor.reset()
        return result

    def load_member(self, chatid):
        sqlQuery = 'select * from `botshiftkari`.`membership` where  chat_id = \'{}\''.format(chatid)
        mydb = self.connector()
        myCursor = mydb.cursor()
        myCursor.execute(sqlQuery)
        result = myCursor.fetchone()
        myCursor.reset()
        tempMember = Membership()
        if result is not None:
            tempMember.name = result[1]
            tempMember.last_name = result[2]
            tempMember.phone_number = result[3]
            tempMember.membership_type = result[4]
            tempMember.membership_fee_paid = result[5]
            tempMember.register_progress = result[6]
            tempMember.userName = result[7]
            tempMember.chatId = result[8]
            tempMember.lastMessage = result[9]
            tempMember.verifyAdmin = result[10]
            tempMember.op = result[13]
            tempMember.delf = result[14]
            tempMember.opTime = DT.strptime(str(result[15]), '%Y-%m-%d %H:%M:%S')

        else:
            tempMember = None
        return tempMember

    def member_update(self, fieldName, fieldValue, chatid):
        sqlQuery = 'UPDATE `botshiftkari`.`membership` SET `{0}` = \'{1}\'  where chat_id = \'{2}\''.format(fieldName,
                                                                                                            fieldValue,
                                                                                                            chatid)
        mydb = self.connector()
        mydb.autocommit = True
        myCursor = mydb.cursor()
        result = myCursor.execute(sqlQuery)
        myCursor.reset()
        return result

    def member_update_chatid(self, fieldName, fieldValue, chatid):
        sqlQuery = 'UPDATE `botshiftkari`.`membership` SET `{0}` = \'{1}\'  where chat_id = \'{2}\''.format(fieldName,
                                                                                                            fieldValue,
                                                                                                            chatid)
        mydb = self.connector()
        mydb.autocommit = True
        myCursor = mydb.cursor()
        result = myCursor.execute(sqlQuery)
        myCursor.reset()
        return result

    def set_member_last_update_id(self, chatid, last_uid):
        sqlQuery = 'UPDATE `botshiftkari`.`membership` SET last_message_sent = {1}  where chat_id = \'{0}\''.format(
            chatid, last_uid)
        mydb = self.connector()
        mydb.autocommit = True
        myCursor = mydb.cursor()
        result = myCursor.execute(sqlQuery)
        myCursor.reset()
        return result

    def reactive_member_chatid(self, chatid):
        sqlQuery = 'select id from `botshiftkari`.`membership` where chat_id=\'{0}\''.format(chatid)
        mydb = self.connector()
        mydb.autocommit = True
        myCursor = mydb.cursor()
        myCursor.execute(sqlQuery)
        result = myCursor.fetchone()
        if result is None:
            return None
        else:
            sqlQuery = '''update `botshiftkari`.`membership` set del=0 WHERE id={0};
                            update `botshiftkari`.`founder` set del=0 WHERE idMember={0};
                            update `botshiftkari`.`student` set del=0 WHERE idMember ={0};
                            update `botshiftkari`.`technicalmanager` set del=0 WHERE idMember={0};'''.format(result[0])
            myCursor.execute(sqlQuery)
            return result[0]

    def del_member_chatid(self, chatid):
        sqlQuery = 'select id from `botshiftkari`.`membership` where chat_id=\'{0}\''.format(chatid)
        mydb = self.connector()
        mydb.autocommit = True
        myCursor = mydb.cursor()
        myCursor.execute(sqlQuery)
        result = myCursor.fetchone()
        if result is None:
            return None
        else:
            sqlQuery = '''delete from `botshiftkari`.`membership`  WHERE id={0};
                          delete from  `botshiftkari`.`founder`  WHERE idMember={0};
                          delete from  `botshiftkari`.`student`  WHERE idMember ={0};
                          delete from  `botshiftkari`.`technicalmanager`  WHERE idMember={0};'''.format(result[0])
            myCursor.execute(sqlQuery)
            return result[0]

    def get_member_property_Adminchatid(self, fieldName, chatid):
        sqlQuery = 'select `{1}` from `botshiftkari`.`membership` where registration_progress = 15 and  adminChatId = ' \
                   '\'{0}\''.format(
            chatid,
            fieldName)
        mydb = self.connector()
        mydb.autocommit = True
        myCursor = mydb.cursor()
        myCursor.execute(sqlQuery)
        result = myCursor.fetchone()
        if result is None:
            return None
        else:
            return result[0]

    def get_member_property_chatid(self, fieldName, chatid):
        sqlQuery = 'select `{1}` from `botshiftkari`.`membership` where  chat_id = \'{0}\''.format(chatid, fieldName)
        mydb = self.connector()
        myCursor = mydb.cursor()
        myCursor.execute(sqlQuery)
        result = myCursor.fetchone()
        if result is None:
            return None
        else:
            return result[0]

    def get_member_property_id(self, fieldName, idMember):
        sqlQuery = 'select `{1}` from `botshiftkari`.`membership` where  id = \'{0}\''.format(idMember, fieldName)
        mydb = self.connector()
        mydb.autocommit = True
        myCursor = mydb.cursor()
        myCursor.execute(sqlQuery)
        result = myCursor.fetchone()
        if result is None:
            return None
        else:
            return result[0]

    def create_member(self, member: Membership):
        sqlQuery = 'select * from `botshiftkari`.`membership` where chat_id = \'{}\''.format(member.chatId)
        mydb = self.connector()
        mydb.autocommit = True
        myCursor = mydb.cursor()
        myCursor.execute(sqlQuery)
        result = myCursor.fetchall()
        myCursor.reset()
        if len(result) == 0:
            sql = '''insert into membership (name,last_name,phone_number,membership_type,membership_fee_paid,
            registration_progress,username,chat_id,last_message_sent) VALUEs (%s,%s,%s,%s,%s,%s,%s,%s,%s)'''
            val = (
                member.name, member.last_name, member.phone_number, member.membership_type, member.membership_fee_paid,
                member.register_progress, member.userName, member.chatId, member.lastMessage)
            result = myCursor.execute(sql, val)
            myCursor.reset()
        return member

    def get_funder_property(self, fieldName, chatid):
        sqlQuery = 'select id from `botshiftkari`.`membership` where  chat_id = \'{0}\''.format(chatid)
        mydb = self.connector()
        mydb.autocommit = True
        myCursor = mydb.cursor()
        myCursor.execute(sqlQuery)
        result = myCursor.fetchone()
        idMember = result[0]
        sqlQuery = 'select {0} from `botshiftkari`.`founder` where idMember={1}'.format(fieldName, idMember)
        myCursor.execute(sqlQuery)
        result = myCursor.fetchone()
        if result is None:
            return None
        else:
            return result[0]

    def founder_update(self, fieldName, fieldValue, chatid):
        sqlQuery = 'select id from `botshiftkari`.`membership` where  chat_id = \'{0}\''.format(chatid)
        mydb = self.connector()
        mydb.autocommit = True
        myCursor = mydb.cursor()
        myCursor.execute(sqlQuery)
        result = myCursor.fetchone()
        idMember = result[0]
        sqlQuery = 'select id from `botshiftkari`.`founder` where idMember={}'.format(idMember)
        myCursor.execute(sqlQuery)
        result = myCursor.fetchone()
        if result is None:
            sqlQuery = 'insert into `botshiftkari`.`founder` (idMember,{0}) values ({1},\'{2}\')'.format(fieldName,
                                                                                                         idMember,
                                                                                                         fieldValue)
        else:
            sqlQuery = 'UPDATE `botshiftkari`.`founder` SET `{0}` = \'{1}\'  where idMember = \'{2}\''.format(fieldName,
                                                                                                              fieldValue,
                                                                                                              idMember)
        myCursor.execute(sqlQuery)
        myCursor.reset()
        return result

    def get_student_property(self, fieldName, chatid):
        sqlQuery = 'select id from `botshiftkari`.`membership` where  chat_id = \'{0}\''.format(chatid)
        mydb = self.connector()
        mydb.autocommit = True
        myCursor = mydb.cursor()
        myCursor.reset()
        myCursor.execute(sqlQuery)
        result = myCursor.fetchone()
        idMember = result[0]
        myCursor.reset()
        sqlQuery = 'select {0} from `botshiftkari`.`student` where idMember={1}'.format(fieldName, idMember)
        myCursor.execute(sqlQuery)
        result = myCursor.fetchone()
        if result is None:
            return None
        else:
            return result[0]

    def student_update(self, fieldName, fieldValue, chatid):
        sqlQuery = 'select id from `botshiftkari`.`membership` where  chat_id = \'{0}\''.format(chatid)
        mydb = self.connector()
        mydb.autocommit = True
        myCursor = mydb.cursor()
        myCursor.execute(sqlQuery)
        result = myCursor.fetchone()
        idMember = result[0]
        sqlQuery = 'select id from `botshiftkari`.`student` where idMember={}'.format(idMember)
        myCursor.execute(sqlQuery)
        result = myCursor.fetchone()
        if result is None:
            sqlQuery = 'insert into `botshiftkari`.`student` (idMember,{0}) values ({1},\'{2}\')'.format(fieldName,
                                                                                                         idMember,
                                                                                                         fieldValue)
        else:
            sqlQuery = 'UPDATE `botshiftkari`.`student` SET `{0}` = \'{1}\'  where idMember = \'{2}\''.format(fieldName,
                                                                                                              fieldValue,
                                                                                                              idMember)
        myCursor.execute(sqlQuery)
        myCursor.reset()
        return result

    def get_technical_property(self, fieldName, chatid):
        sqlQuery = 'select id from `botshiftkari`.`membership` where  chat_id = \'{0}\''.format(chatid)
        mydb = self.connector()
        mydb.autocommit = True
        myCursor = mydb.cursor()
        myCursor.execute(sqlQuery)
        result = myCursor.fetchone()
        idMember = result[0]
        sqlQuery = 'select {0} from `botshiftkari`.`technicalmanager` where idMember={1}'.format(fieldName, idMember)
        myCursor.execute(sqlQuery)
        result = myCursor.fetchone()
        if result is None:
            return None
        else:
            return result[0]

    def technicalManager_update(self, fieldName, fieldValue, chatid):
        sqlQuery = 'select id from `botshiftkari`.`membership` where  chat_id = \'{0}\''.format(chatid)
        mydb = self.connector()
        mydb.autocommit = True
        myCursor = mydb.cursor()
        myCursor.execute(sqlQuery)
        result = myCursor.fetchone()
        idMember = result[0]
        sqlQuery = 'select id from `botshiftkari`.`technicalmanager` where idMember={}'.format(idMember)
        myCursor.execute(sqlQuery)
        result = myCursor.fetchone()
        if result is None:
            sqlQuery = 'insert into `botshiftkari`.`technicalmanager` (idMember,{0}) values ({1},\'{2}\')'.format(
                fieldName, idMember, fieldValue)
        else:
            sqlQuery = 'UPDATE `botshiftkari`.`technicalmanager` SET `{0}` = \'{1}\'  where idMember = \'{2}\''.format(
                fieldName, fieldValue, idMember)
        myCursor.execute(sqlQuery)
        myCursor.reset()
        return result

    def shift_update(self, fieldName, fieldValue, chatid):
        mydb = self.connector()
        mydb.autocommit = True
        myCursor = mydb.cursor()
        sqlQuery = 'select idshift from `botshiftkari`.`shift` where progress=0 and Creator={}'.format(chatid)
        myCursor.execute(sqlQuery)
        result = myCursor.fetchone()
        if result is None:
            sqlQuery = 'insert into `botshiftkari`.`shift` (Creator,{0}) values (\'{1}\',\'{2}\')'.format(fieldName,
                                                                                                          chatid,
                                                                                                          fieldValue)
            result = myCursor.lastrowid
        else:
            sqlQuery = 'UPDATE `botshiftkari`.`shift` SET `{0}` = \'{1}\'  where progress=0 and Creator = \'{2}\''.format(
                fieldName, fieldValue, chatid)
        myCursor.execute(sqlQuery)
        if not isinstance(result, int):
            result = result[0]
        myCursor.reset()
        return result

    def create_shift(self, userid):
        mydb = self.connector()
        mydb.autocommit = True
        myCursor = mydb.cursor()
        sqlQuery = 'insert into `botshiftkari`.`shift` (Creator) values (\'{0}\')'.format(userid)
        myCursor.execute(sqlQuery)
        result = myCursor.lastrowid
        return result

    def shift_update_by_id(self, fieldName, fieldValue, idshift):
        mydb = self.connector()
        mydb.autocommit = True
        myCursor = mydb.cursor()
        sqlQuery = 'UPDATE `botshiftkari`.`shift` SET `{0}` = \'{1}\'  where  idshift = \'{2}\''.format(
            fieldName, fieldValue, idshift)
        myCursor.execute(sqlQuery)
        myCursor.reset()
        return None

    def shift_reserve_by_id(self, idshift, chatid):
        mydb = self.connector()
        mydb.autocommit = True
        myCursor = mydb.cursor()
        sqlQuery = 'UPDATE `botshiftkari`.`shift` SET `progress` = 3,`approver`=\'{1}\'  where progress=2 and idshift = \'{0}\''.format(
            idshift, chatid)
        myCursor.execute(sqlQuery)
        myCursor.reset()
        return None

    def get_shift_property(self, fieldName, idShift):
        mydb = self.connector()
        mydb.autocommit = True
        myCursor = mydb.cursor()
        sqlQuery = 'select {0} from `botshiftkari`.`shift` where idshift={1}'.format(fieldName, idShift)
        myCursor.execute(sqlQuery)
        result = myCursor.fetchone()
        if result is None:
            return None
        else:
            return result[0]

    def get_all_shift(self=None, progress=1, creator=0):
        mydb = self.connector()
        mydb.autocommit = True
        myCursor = mydb.cursor()
        sqlQuery = '''SELECT concat(mem.name,mem.last_name) as fullname,creator,
                        DateShift,startTime,endTime,wage,pharmacyAddress,progress,approver,shi.idshift,
                        shi.dateEndShift
                        FROM botshiftkari.shift shi inner join botshiftkari.membership mem on
                         mem.chat_id = shi.Creator where not shi.creator = '{0}' and shi.progress={1}'''.format(creator,
                                                                                                                progress)
        myCursor.execute(sqlQuery)
        result = myCursor.fetchall()
        return result

    def get_shift_no_approve(self=None, progress=1, creator=0):
        mydb = self.connector()
        mydb.autocommit = True
        myCursor = mydb.cursor()
        sqlQuery = '''SELECT concat(mem.name,mem.last_name) as fullname,creator,
                         DateShift,startTime,endTime,wage,pharmacyAddress,progress,approver,shi.idshift,
                         shi.dateEndShift
                         FROM botshiftkari.shift shi inner join botshiftkari.membership mem on
                          mem.chat_id = shi.Creator where approver is null and not shi.creator = '{0}' and shi.progress={1}'''.format(
            creator, progress)
        myCursor.execute(sqlQuery)
        result = myCursor.fetchall()
        return result

    def get_all_shift_by_creator(self=None, creator=0):
        mydb = self.connector()
        mydb.autocommit = True
        myCursor = mydb.cursor()
        sqlQuery = '''SELECT concat(mem.name,mem.last_name) as fullname,creator,
                        DateShift,startTime,endTime,wage,pharmacyAddress,progress,approver,shi.idshift,
                        shi.dateEndShift,shi.wfStudent,shi.dateRegiter
                        FROM botshiftkari.shift shi inner join botshiftkari.membership mem on
                         mem.chat_id = shi.Creator where  shi.creator = '{0}' and (shi.progress=1 or shi.progress=2) and shi.del=0'''.format(
            creator)
        myCursor.execute(sqlQuery)
        result = myCursor.fetchall()
        return result

    def get_all_shift_manager(self=None):
        mydb = self.connector()
        mydb.autocommit = True
        myCursor = mydb.cursor()
        sqlQuery = '''SELECT concat(mem.name,mem.last_name) as fullname,creator,
                        DateShift,startTime,endTime,wage,pharmacyAddress,progress,approver,shi.idshift,
                        shi.dateEndShift,shi.wfStudent,shi.dateRegiter
                        FROM botshiftkari.shift shi inner join botshiftkari.membership mem on
                         mem.chat_id = shi.Creator and shi.del=0 '''
        myCursor.execute(sqlQuery)
        result = myCursor.fetchall()
        return result

    def get_all_shift_managerForApprove(self=None):
        mydb = self.connector()
        mydb.autocommit = True
        myCursor = mydb.cursor()
        sqlQuery = '''SELECT concat(mem.name,mem.last_name) as fullname,creator,
                        DateShift,startTime,endTime,wage,pharmacyAddress,progress,approver,shi.idshift,
                        shi.dateEndShift,shi.wfStudent,shi.dateRegiter
                        FROM botshiftkari.shift shi inner join botshiftkari.membership mem on
                         mem.chat_id = shi.Creator where progress = 1 and shi.del = 0'''
        myCursor.execute(sqlQuery)
        result = myCursor.fetchall()
        return result

    def get_all_shift_managerApproved(self=None):
        mydb = self.connector()
        mydb.autocommit = True
        myCursor = mydb.cursor()
        sqlQuery = '''SELECT concat(mem.name,mem.last_name) as fullname,creator,
                        DateShift,startTime,endTime,wage,pharmacyAddress,progress,approver,shi.idshift,
                        shi.dateEndShift,shi.wfStudent,shi.dateRegiter
                        FROM botshiftkari.shift shi inner join botshiftkari.membership mem on
                         mem.chat_id = shi.Creator where progress = 2 and shi.del = 0'''
        myCursor.execute(sqlQuery)
        result = myCursor.fetchall()
        return result

    def get_all_member(self=None, type=None):
        mydb = self.connector()
        mydb.autocommit = True
        myCursor = mydb.cursor()
        sqlQuery = None
        if type is None:
            sqlQuery = '''select concat(mem.name,mem.last_name) as fullname,
                            case 
                            when mem.membership_type = 1 then 'موسس'
                            when mem.membership_type = 2 then 'مسئول فنی'
                            when mem.membership_type = 3 then 'دانشجو'
                            when mem.membership_type = 4 then 'مدیر'
                            else 'نامشخص'
                            end as typeMember,
                            mem.phone_number
                            from  botshiftkari.membership as mem '''
        elif type == 1:
            sqlQuery = '''select concat(mem.name,' ',mem.last_name) as fn,
						    case 
                            when mem.membership_type = 1 then 'موسس'
                            when mem.membership_type = 2 then 'مسئول فنی'
                            when mem.membership_type = 3 then 'دانشجو'
                            when mem.membership_type = 4 then 'مدیر'
                            else 'نامشخص'
                            end as typeMember,
                            mem.phone_number,memf.pharmacy_name,pharmacy_type,pharmacy_address,
                            case when memf.del = 0 then 'فعال'
                            else 'غیر فعال' end as status
                            from botshiftkari.membership mem inner join botshiftkari.founder memf 
                            on mem.id=memf.idMember  where mem.membership_type={}'''.format(type)
        elif type == 2:
            sqlQuery = '''select concat(mem.name,' ',mem.last_name) as fn,
						    case 
                            when mem.membership_type = 1 then 'موسس'
                            when mem.membership_type = 2 then 'مسئول فنی'
                            when mem.membership_type = 3 then 'دانشجو'
                            when mem.membership_type = 4 then 'مدیر'
                            else 'نامشخص'
                            end as typeMember,
                            mem.phone_number,memT.national_code,
                            case when memT.del = 0 then 'فعال'
                            else 'غیر فعال' end as status
                            from botshiftkari.membership mem inner join botshiftkari.technicalmanager memT
                            on mem.id=memt.idMember  where mem.membership_type={}'''.format(type)
        elif type == 3:
            sqlQuery = '''select concat(mem.name,' ',mem.last_name) as fn,
					        case 
                            when mem.membership_type = 1 then 'موسس'
                            when mem.membership_type = 2 then 'مسئول فنی'
                            when mem.membership_type = 3 then 'دانشجو'
                            when mem.membership_type = 4 then 'مدیر'
                            else 'نامشخص'
                            end as typeMember,
                            mem.phone_number,mems.national_code,
                            mems.start_date,mems.end_date,mems.shift_access, mems.hourPermit,
                            mems.hourPermitUsed,
                            case when mems.del = 0 then 'فعال'
                            else 'غیر فعال' end as status
                            from botshiftkari.membership mem inner join botshiftkari.student mems 
                            on mem.id=mems.idMember  where mem.membership_type={}'''.format(type)

        myCursor.execute(sqlQuery)
        result = myCursor.fetchall()
        return result

    def get_all_shift_by_approver(self=None, creator='0', dateShift=''):
        mydb = self.connector()
        myCursor = mydb.cursor()
        sqlQuery = '''SELECT concat(mem.name,mem.last_name) as fullname,creator,
                        DateShift,startTime,endTime,wage,pharmacyAddress,progress,approver,shi.idshift,
                        shi.dateEndShift,shi.wfStudent,shi.dateRegiter
                        FROM botshiftkari.shift shi inner join botshiftkari.membership mem on
                         mem.chat_id = shi.Creator where  shi.approver = '{0}' and shi.DateShift> '{1}'
                          and (shi.progress=3 or shi.progress=4) and shi.del=0'''.format(creator, dateShift)
        myCursor.execute(sqlQuery)
        result = myCursor.fetchall()
        return result

    def get_all_property_shift_byId(self=None, idshift=0):
        mydb = self.connector()
        mydb.autocommit = True
        myCursor = mydb.cursor()
        sqlQuery = '''SELECT concat(mem.name,mem.last_name) as fullname,creator,
                        DateShift,startTime,endTime,wage,pharmacyAddress,progress,approver,shi.idshift,
                        shi.dateEndShift,shi.wfStudent,shi.dateRegiter
                        FROM botshiftkari.shift shi inner join botshiftkari.membership mem on
                         mem.chat_id = shi.Creator where  shi.idshift={0}'''.format(idshift)
        myCursor.execute(sqlQuery)
        result = myCursor.fetchone()
        return result

    def get_all_ts_chatid(self, creator=None):
        mydb = self.connector()
        mydb.autocommit = True
        myCursor = mydb.cursor()
        sqlQuery = None
        if creator is None:
            sqlQuery = '''SELECT mem.chat_id from botshiftkari.membership as mem where mem.del=0 and 
            mem.membership_type=2 '''
        else:
            sqlQuery = '''SELECT mem.chat_id from botshiftkari.membership as mem where mem.del=0 and 
                        mem.membership_type=2 and not mem.chat_id = \'{0}\''''.format(creator)
        myCursor.execute(sqlQuery)
        result = myCursor.fetchall()
        return result

    def get_property_domain(self, key):
        mydb = self.connector()
        mydb.autocommit = True
        myCursor = mydb.cursor()
        sqlQuery = '''SELECT value from `botshiftkari`.`domain` where `key` = \'{0}\''''.format(key)
        myCursor.execute(sqlQuery)
        result = myCursor.fetchone()
        return result[0]

    def domain_update_by_key(self, key, value):
        mydb = self.connector()
        mydb.autocommit = True
        myCursor = mydb.cursor()
        sqlQuery = 'UPDATE `botshiftkari`.`domain` SET `value` = \'{0}\'  where `key` = \'{1}\''.format(value, key)
        myCursor.execute(sqlQuery)
        myCursor.reset()
        return None

    def rep_nation_code(self, nationCode):
        mydb = self.connector()
        mydb.autocommit = True
        myCursor = mydb.cursor()
        sqlQuery = 'select count(*) from `botshiftkari`.`technicalmanager` where `national_code` = \'{0}\''.format(
            nationCode)
        myCursor.execute(sqlQuery)
        result = myCursor.fetchone()
        if int(result[0]) > 0:
            return True
        sqlQuery = 'select count(*) from `botshiftkari`.`student` where `national_code` = \'{0}\''.format(
            nationCode)
        myCursor.execute(sqlQuery)
        result = myCursor.fetchone()
        if int(result[0]) > 0:
            return True
        return False

    def getTotalShiftEM(self, dateStart, dateEnd, creator):
        mydb = self.connector()
        myCursor = mydb.cursor()
        sqlQuery = f'SELECT count(*) FROM botshiftkari.shift where Creator=\'{creator}\' and shiftIsEM = 1 and dateRegiter between' \
                   f' \'{dateStart}\' and \'{dateEnd}\' and progress = 2 '
        myCursor.execute(sqlQuery)
        result = myCursor.fetchone()
        return int(result[0])

    def get_list_shift_for_student(self):
        # send تعیین می کند که آیا برای دانشجویان ارسال شده اس قبلا
        mydb = self.connector()
        mydb.autocommit = True
        myCursor = mydb.cursor()
        sqlQuery = 'select `value` from `botshiftkari`.`domain` where `key` = \'hrStudent\''
        myCursor.execute(sqlQuery)
        result = myCursor.fetchone()
        sqlQuery = '''SELECT concat(mem.name,' ',mem.last_name) as fullname,creator,
                        DateShift,startTime,endTime,wage,pharmacyAddress,progress,approver,shi.idshift,
                        shi.dateEndShift,shi.wfStudent,shi.dateRegiter
                        FROM botshiftkari.shift shi inner join botshiftkari.membership mem on
                         mem.chat_id = shi.Creator where `progress` > '0'  and    `progress` < '3'  and 
                         `send` = 0 and  date_add(shi.dateRegiter,interval {0} HOUR)<now() and dateShift > \'{1}\''''.format(
            result[0], JalaliDate(datetime.datetime.now()))
        myCursor.execute(sqlQuery)
        result = myCursor.fetchall()
        return result

    def get_all_student_chatid(self, creator=None):
        mydb = self.connector()
        myCursor = mydb.cursor()
        sqlQuery = ''
        if creator is None:
            sqlQuery = 'SELECT mem.chat_id from botshiftkari.membership as mem where mem.del=0 ' \
                       'and mem.membership_type=3 and mem.verifyAdmin = 1 '
        else:
            sqlQuery = f'SELECT mem.chat_id from botshiftkari.membership as mem where mem.del=0 ' \
                       f'and mem.membership_type=3  and mem.verifyAdmin = 1 and not mem.chat_id = \'{creator}\' '
        myCursor.execute(sqlQuery)
        result = myCursor.fetchall()
        return result

    def get_all_student_idmeMember(self, creator=None):
        mydb = self.connector()
        myCursor = mydb.cursor()
        sqlQuery = ''
        if creator is None:
            sqlQuery = 'SELECT mem.chat_id,mem.id from botshiftkari.membership as mem where mem.del=0 ' \
                       'and mem.membership_type=3 and mem.verifyAdmin = 1 '
        else:
            sqlQuery = f'SELECT mem.chat_id,mem.id from botshiftkari.membership as mem where mem.del=0 ' \
                       f'and mem.membership_type=3  and mem.verifyAdmin = 1 and not mem.chat_id = \'{creator}\' '
        myCursor.execute(sqlQuery)
        result = myCursor.fetchall()
        return result

    def checkExsistDetail(self, mem: Membership, newType):
        mydb = self.connector()
        myCursor = mydb.cursor()
        sqlQuery = f'select id from botshiftkari.membership where chat_id = {mem.chatId}'
        myCursor.execute(sqlQuery)
        result = myCursor.fetchone()
        idMember = result[0]
        if newType == 1:
            sqlQuery = f'select count(*) from botshiftkari.founder where idMember = {idMember}'
        elif newType == 2:
            sqlQuery = f'select count(*) from botshiftkari.technicalmanager where idMember = {idMember}'
        elif newType == 3:
            sqlQuery = f'select count(*) from botshiftkari.student where idMember = {idMember}'
        else:
            return False
        myCursor.execute(sqlQuery)
        result = myCursor.fetchone()
        count = int(result[0])
        if count == 1:
            return True
        else:
            return False

    def registerDayShift(self, idShift, dateShift, requster, sendedForCreator, idDetailShift, status=None, ft=-1):
        tmpIdDayShift = self.getIdRegisterDayOfShift(idShift, dateShift, requster, idDetailShift, ft=ft)
        if tmpIdDayShift != 0:
            return 0
        mydb = self.connector()
        myCursor = mydb.cursor()
        mydb.autocommit = True
        if status is None:
            sqlQuery = f'''INSERT INTO `botshiftkari`.`dayshift`
(`idShift`,
`dateShift`,
`requster`,
`approveCreator`,
`sendedForCreator`,
`idDetailShift`,
`flagtime`)
VALUES({idShift},\'{dateShift}\',\'{requster}\',0,{sendedForCreator},{idDetailShift},{ft})'''
        else:
            sqlQuery = f'''INSERT INTO `botshiftkari`.`dayshift`
            (`idShift`,
            `dateShift`,
            `requster`,
            `approveCreator`,
            `sendedForCreator`,`status`,`idDetailShift`,`flagtime`)
            VALUES({idShift},\'{dateShift}\',\'{requster}\',0,{sendedForCreator},{status},{idDetailShift},{ft})'''
        myCursor.execute(sqlQuery)
        return myCursor.lastrowid

    def registerDetailShift(self, idShift, year, month, day):
        sqlQuery = f'insert into  `botshiftkari`.`detailshift` (idShift,year,month,day)values' \
                   f'({idShift},{year},{month},{day})'
        mydb = self.connector()
        myCursor = mydb.cursor()
        mydb.autocommit = True
        myCursor.execute(sqlQuery)
        return myCursor.lastrowid

    def updateDetailShift(self, fieldName, fieldValue, idDetailShift):
        mydb = self.connector()
        mydb.autocommit = True
        myCursor = mydb.cursor()
        if fieldValue is not None:
            sqlQuery = 'UPDATE `botshiftkari`.`detailshift` SET `{0}` = \'{1}\'  where `idDetailShift` = \'{2}\''.format(
                fieldName, fieldValue, idDetailShift)
        else:
            sqlQuery = 'UPDATE `botshiftkari`.`detailshift` SET `{0}` = null  where `idDetailShift` = \'{1}\''.format(
                fieldName, idDetailShift)
        myCursor.execute(sqlQuery)
        myCursor.reset()
        return None

    def updateShiftDay(self, fieldName, fieldValue, idDayShift):
        mydb = self.connector()
        mydb.autocommit = True
        myCursor = mydb.cursor()
        sqlQuery = 'UPDATE `botshiftkari`.`dayshift` SET `{0}` = \'{1}\'  where `iddayshift` = \'{2}\''.format(
            fieldName, fieldValue, idDayShift)
        myCursor.execute(sqlQuery)
        myCursor.reset()
        return None

    def getShiftDayProperty(self, fieldName, idDayShift):
        mydb = self.connector()
        myCursor = mydb.cursor()
        sqlQuery = f'SELECT {fieldName} from botshiftkari.dayshift  where  idDayShift={idDayShift}'
        myCursor.execute(sqlQuery)
        result = myCursor.fetchone()
        if result is None:
            return None
        else:
            return result[0]

    def getEmptyDayOfShift(self, idShift):
        mydb = self.connector()
        myCursor = mydb.cursor()
        sqlQuery = f'SELECT * from botshiftkari.dayshift  where  approveCreator=0 and idShift={idShift}'
        myCursor.execute(sqlQuery)
        result = myCursor.fetchall()
        return result

    def getIdRegisterDayOfShift(self, idShift, dateShift, requsterShift, idDetailShift, ft):
        mydb = self.connector()
        myCursor = mydb.cursor()
        sqlQuery = f'SELECT iddayShift from botshiftkari.dayshift  where  idShift={idShift} and dateShift=\'{dateShift}\'' + \
                   f' and requster=\'{requsterShift}\' and idDetailShift={idDetailShift} and flagtime={ft}'
        myCursor.execute(sqlQuery)
        result = myCursor.fetchone()
        if result is not None:
            return result[0]
        else:
            return 0

    def isShiftDayFull(self, idDetailShift, flagTime=0):
        mydb = self.connector()
        myCursor = mydb.cursor()
        sqlQuery = ''
        if int(flagTime) == 0:
            sqlQuery = f'SELECT count(*) from botshiftkari.detailshift  where  idDetailShift={idDetailShift} and status=1'
        elif int(flagTime) == 1:
            sqlQuery = f'SELECT count(*) from botshiftkari.detailshift  where  idDetailShift={idDetailShift} and status_e=1'
        elif int(flagTime) == 2:
            sqlQuery = f'SELECT count(*) from botshiftkari.detailshift  where  idDetailShift={idDetailShift} and status_n=1'
        elif int(flagTime) == 3:
            sqlQuery = f'SELECT count(*) from botshiftkari.detailshift  where  idDetailShift={idDetailShift} and status_f=1'
        myCursor.execute(sqlQuery)
        result = myCursor.fetchone()
        return result[0]

    def getListDaySelection(self, idShift, requsterShift):
        mydb = self.connector()
        myCursor = mydb.cursor()
        sqlQuery = f'SELECT iddayShift,dateShift,idDetailShift from botshiftkari.dayshift  where  idShift={idShift} and status= 0 ' + \
                   f' and requster=\'{requsterShift}\''
        myCursor.execute(sqlQuery)
        result = myCursor.fetchall()
        return result

    def getIdShiftFromDay(self, idDayShift):
        mydb = self.connector()
        myCursor = mydb.cursor()
        sqlQuery = f'SELECT idshift from botshiftkari.dayshift  where  iddayShift={idDayShift} '
        myCursor.execute(sqlQuery)
        result = myCursor.fetchone()
        if result is not None:
            return result[0]
        else:
            return None

    def removeFromSelection(self, idDayShift):
        mydb = self.connector()
        myCursor = mydb.cursor()
        mydb.autocommit = True
        sqlQuery = f'delete from botshiftkari.dayshift  where  iddayShift={idDayShift} and status = 0 '
        myCursor.execute(sqlQuery)

    def removeShiftFromTable(self, idShift):
        mydb = self.connector()
        myCursor = mydb.cursor()
        mydb.autocommit = True
        sqlQuery = f'delete from botshiftkari.shift  where  idshift={idShift}  '
        myCursor.execute(sqlQuery)

    def getListDayIsNotEmpty(self, idShift, status=2):
        mydb = self.connector()
        myCursor = mydb.cursor()
        sqlQuery = f'SELECT iddayShift,dateShift,requster,idDetailShift from botshiftkari.dayshift  where  idShift={idShift}'
        if status is not None:
            sqlQuery += f' and status= {status} '
        myCursor.execute(sqlQuery)
        result = myCursor.fetchall()
        return result

    def getListMember(self, sender, group=None):
        sqlQuery = ''
        if group is None:
            sqlQuery = f"SELECT chat_id FROM botshiftkari.membership where not chat_id = '{sender}'"
        else:
            sqlQuery = f"SELECT chat_id FROM botshiftkari.membership where not chat_id = '{sender}'  and membership_type = {group}"
        mydb = self.connector()
        myCursor = mydb.cursor()
        myCursor.execute(sqlQuery)
        result = myCursor.fetchall()
        return result

    def getListSelectedDay(self, idShift, status=-1):
        sqlQuery = f'''SELECT CONCAT(lpad(ds.year,4,\'0\'),\'-\',lpad(ds.month,2,\'0\'),\'-\',lpad(ds.day,2,\'0\')) as
                   dateS,ds.idDetailShift,ds.idShift, morning, evening, night, freeTime,
                    case 
                    when morning is  null and evening is null and night is null then 0
                    when morning is not null and evening is null and night is null then 1
                    when morning is  null and evening is not null  and night is null then 2
                    when morning is not null and evening is not null and night is null then 3
                    when morning is  null and evening is  null and night is not null then 4
                    when morning is not null and evening is  null and night is not null then 5
                    when morning is  null and evening is not null and night is not null then 6
                    when morning is not null and evening is not null and night is not null then 7
                    else 0 end selectStatus,
                    ds.status,
                    ds.status_e,
                    ds.status_n,
                    ds.status_f FROM  
                   botshiftkari.detailshift as ds   
                    where idShift = {idShift}  '''
        if status > -1:
            sqlQuery += f' and status = {status} order by ds.year,ds.month,ds.day'
        else:
            sqlQuery += ' order by ds.year,ds.month,ds.day'
        mydb = self.connector()
        myCursor = mydb.cursor()
        myCursor.execute(sqlQuery)
        result = myCursor.fetchall()
        return result

    def getIdDetailShift(self, idShift, year, month, day):
        sqlQuery = f'select idDetailShift from  botshiftkari.detailshift as ds where ds.idShift = {idShift} and ds.year={year} and' \
                   f' ds.month={month} and ds.day = {day}'
        mydb = self.connector()
        mydb.autocommit = True
        myCursor = mydb.cursor()
        myCursor.execute(sqlQuery)
        id = myCursor.fetchone()
        if id is not None:
            return id[0]
        else:
            return None

    def removeDay(self, idShift):
        sqlQuery = f'delete from  botshiftkari.detailshift as ds where ds.idDetailShift = {idShift} and ds.morning is ' \
                   f'null and ds.evening is null and ds.night is null and freeTime is null'
        mydb = self.connector()
        mydb.autocommit = True
        myCursor = mydb.cursor()
        myCursor.execute(sqlQuery)
        return

    def setMinMaxDate(self, idShift):
        sqlQuery = f'select * from  botshiftkari.detailshift where idShift= {idShift} order by year,month,day;'
        mydb = self.connector()
        myCursor = mydb.cursor()
        myCursor.execute(sqlQuery)
        result = myCursor.fetchall()
        startDate = endDate = '0001-01-01'
        if len(result) > 0:
            startDate = f'{str(result[0][2]).zfill(4)}-{str(result[0][3]).zfill(2)}-{str(result[0][4]).zfill(2)}'
            endDate = f'{str(result[-1][2]).zfill(4)}-{str(result[-1][3]).zfill(2)}-{str(result[-1][4]).zfill(2)}'
        self.shift_update_by_id('DateShift', startDate, idShift)
        self.shift_update_by_id('dateEndShift', endDate, idShift)

    def getTotalDayShift(self, idShift, status=0):
        sqlQuery = f'''SELECT  sum((case
 WHEN morning IS NOT NULL AND status = {status} THEN 1
 else 0
 end +
 case
 WHEN evening IS NOT NULL AND status_e = {status} THEN 1
 else 0
 end + case
 WHEN night IS NOT NULL AND status_n = {status} THEN 1
 else 0
 end  + case
 WHEN freeTime IS NOT NULL AND status_f = {status} THEN 1
 else 0
 end )) as ct
 FROM botshiftkari.detailshift where idshift = {idShift}; '''
        mydb = self.connector()
        myCursor = mydb.cursor()
        myCursor.execute(sqlQuery)
        result = myCursor.fetchone()
        return result[0]

    def detailShift_update_by_id(self, fieldName, fieldValue, idDetailShift):
        mydb = self.connector()
        mydb.autocommit = True
        myCursor = mydb.cursor()
        sqlQuery = 'UPDATE `botshiftkari`.`detailshift` SET `{0}` = \'{1}\'  where  idDetailShift = \'{2}\''.format(
            fieldName, fieldValue, idDetailShift)
        myCursor.execute(sqlQuery)
        myCursor.reset()
        return None

    def getShiftList(self, creator=None, requsterShift=None, startDate=None, endDate=None):
        sqlQuery = 'SELECT * FROM botshiftkari.myshift '
        condition = ''
        if creator is not None:
            condition = f'where creator = \'{creator}\''
        if requsterShift is not None:
            if len(condition) == 0:
                condition = f'where requster = \'{requsterShift}\''
            else:
                condition += f' and requster = \'{requsterShift}\''
        if startDate is not None:
            if len(condition) == 0:
                condition = f'where dateShift >= \'{startDate}\''
            else:
                condition += f' and dateShift >= \'{startDate}\''
        if endDate is not None:
            if len(condition) == 0:
                condition = f'where dateShift <= \'{endDate}\''
            else:
                condition += f' and dateShift <= \'{endDate}\''
        sqlQuery += condition
        mydb = self.connector()
        myCursor = mydb.cursor()
        myCursor.execute(sqlQuery)
        result = myCursor.fetchall()
        return result

    def insertLicense(self, textDetail, typeLicense, creator):
        sqlQuery = f'''insert into `botshiftkari`.`activity_license` (`detail`,`type`,`creator`)values(\'{textDetail}\',
                        {typeLicense},\'{creator}\')'''
        mydb = self.connector()
        mydb.autocommit = True
        myCursor = mydb.cursor()
        myCursor.execute(sqlQuery)
        return myCursor.lastrowid

    def removeReq(self, idReq):
        sqlQuery = f'''delete from `botshiftkari`.`activity_license` where `id_activity_license` = {idReq} '''
        mydb = self.connector()
        mydb.autocommit = True
        myCursor = mydb.cursor()
        myCursor.execute(sqlQuery)
        return None

    def getListLicenseEmpty(self, searchTerm=None):
        sqlQuery = f'''select id_activity_license, fn, phone_number, detail, date_register from 
                        `botshiftkari`.`vw_licenseempty`'''
        if searchTerm is not None:
            condition = f'''
                 where   fn like \'%{searchTerm}%\' or
                         phone_number like \'%{searchTerm}%\' or
                         detail like \'%{searchTerm}%\'
             '''
            sqlQuery += condition
        mydb = self.connector()
        myCursor = mydb.cursor()
        myCursor.execute(sqlQuery)
        result = myCursor.fetchall()
        return result

    def getListLicenseNeed(self, searchTerm=None):
        sqlQuery = f'''select id_activity_license, fn, phone_number, pharmacy_name, pharmacy_type, pharmacy_address,
        detail, date_register from `botshiftkari`.`vw_licenseneed` '''
        if searchTerm is not None:
            condition = f'''
                where   fn like \'%{searchTerm}%\' or
                        phone_number like \'%{searchTerm}%\' or
                        pharmacy_name like \'%{searchTerm}%\' or
                        pharmacy_type like \'%{searchTerm}%\' or
                        pharmacy_address like \'%{searchTerm}%\' or
                        detail like \'%{searchTerm}%\'
            '''
            sqlQuery += condition
        mydb = self.connector()
        myCursor = mydb.cursor()
        myCursor.execute(sqlQuery)
        result = myCursor.fetchall()
        return result

    def getMyListLicense(self, userId):
        sqlQuery = f'''select id_activity_license, type, detail, date_register, creator, del
         from `botshiftkari`.`activity_license` where del=0  and creator = \'{userId}\''''
        mydb = self.connector()
        myCursor = mydb.cursor()
        myCursor.execute(sqlQuery)
        result = myCursor.fetchall()
        return result

    def updateLisence(self, fieldName, fieldValue, idL):
        mydb = self.connector()
        mydb.autocommit = True
        myCursor = mydb.cursor()
        sqlQuery = 'UPDATE `botshiftkari`.`activity_license` SET `{0}` = \'{1}\'  where `id_activity_license` = {2}' \
            .format(fieldName, fieldValue, idL)
        myCursor.execute(sqlQuery)
        myCursor.reset()
        return None

    def delLisence(self, fieldValue, idL):
        mydb = self.connector()
        mydb.autocommit = True
        myCursor = mydb.cursor()
        sqlQuery = 'UPDATE `botshiftkari`.`activity_license` SET `del` = {0}  where `id_activity_license` = {1}' \
            .format(fieldValue, idL)
        myCursor.execute(sqlQuery)
        myCursor.reset()
        return None

    def searchFounder(self, searchVerb):
        sqlQuery = f'''select fn, phone_number, username, chat_id, vdmind, vf.desc, opTime, pharmacy_name, pharmacy_type,
         pharmacy_address, vdmin
         from `botshiftkari`.`vw_founder` vf where fn like \'%{searchVerb}%\' or  phone_number like\'%{searchVerb}%\' or 
         username like \'%{searchVerb}%\' or  vf.desc like\'%{searchVerb}%\' or pharmacy_name like \'%{searchVerb}%\' or 
         pharmacy_type like\'%{searchVerb}%\' or pharmacy_address like\'%{searchVerb}%\''''
        mydb = self.connector()
        myCursor = mydb.cursor()
        myCursor.execute(sqlQuery)
        result = myCursor.fetchall()
        return result

    def searchShift(self, searchVerb):
        sqlQuery = f'''SELECT concat(mem.name,mem.last_name) as fullname,creator,
                        DateShift,startTime,endTime,wage,pharmacyAddress,progress,approver,shi.idshift,
                        shi.dateEndShift,shi.wfStudent,shi.dateRegiter
                        FROM botshiftkari.shift shi inner join botshiftkari.membership mem on
                         mem.chat_id = shi.Creator where 
                         mem.name like \'%{searchVerb}%\' or
                         mem.last_name like \'%{searchVerb}%\' or
                         shi.DateShift like \'%{searchVerb}%\' or
                         shi.dateEndShift like \'%{searchVerb}%\' or
                         shi.pharmacyAddress like \'%{searchVerb}%\''''
        mydb = self.connector()
        myCursor = mydb.cursor()
        myCursor.execute(sqlQuery)
        result = myCursor.fetchall()
        return result

    def searchStudent(self, searchVerb):
        sqlQuery = f'''SELECT fn, phone_number, username, chat_id, vdmind, vs.desc,
                     opTime, national_code, start_date, end_date, shift_access,
                     hourPermit, vdmin FROM botshiftkari.vw_student vs
                     where fn like \'%{searchVerb}%\' or  phone_number like\'%{searchVerb}%\' or 
                     username like \'%{searchVerb}%\' or  vs.desc like\'%{searchVerb}%\' or 
                     national_code like\'%{searchVerb}%\' or start_date like\'%{searchVerb}%\' or
                     end_date like\'%{searchVerb}%\' or shift_access like\'%{searchVerb}%\' or
                     end_date like\'%{searchVerb}%\' or shift_access like\'%{searchVerb}%\' '''
        mydb = self.connector()
        myCursor = mydb.cursor()
        myCursor.execute(sqlQuery)
        result = myCursor.fetchall()
        return result

    def searchTecnician(self, searchVerb):
        sqlQuery = f'''SELECT fn, phone_number, username, chat_id, vdmind, vs.desc, opTime, national_code, vdmin
                     FROM botshiftkari.vw_tecnician vs
                     where fn like \'%{searchVerb}%\' or  phone_number like\'%{searchVerb}%\' or 
                     username like \'%{searchVerb}%\' or  vs.desc like\'%{searchVerb}%\' or 
                     national_code like\'%{searchVerb}%\'  '''
        mydb = self.connector()
        myCursor = mydb.cursor()
        myCursor.execute(sqlQuery)
        result = myCursor.fetchall()
        return result

    def searchAdmin(self, searchVerb):
        sqlQuery = f'''SELECT fn, phone_number, username, chat_id, vdmind, vs.desc, opTime
                     FROM botshiftkari.vw_admin vs
                     where fn like \'%{searchVerb}%\' or  phone_number like\'%{searchVerb}%\' or 
                     username like \'%{searchVerb}%\' or  vs.desc like\'%{searchVerb}%\'  '''
        mydb = self.connector()
        myCursor = mydb.cursor()
        myCursor.execute(sqlQuery)
        result = myCursor.fetchall()
        return result

    def checkNoneTimeDayInFreeTime(self, idShift):
        sqlQuery = f'select count(*) from `botshiftkari`.`detailshift` where idShift={idShift} and freeTime=\'?\''
        mydb = self.connector()
        myCursor = mydb.cursor()
        myCursor.execute(sqlQuery)
        result = myCursor.fetchone()
        return result[0]

    def checkTotalDayInShift(self, idShift):
        sqlQuery = f'select count(*) from `botshiftkari`.`detailshift` where idShift={idShift}'
        mydb = self.connector()
        myCursor = mydb.cursor()
        myCursor.execute(sqlQuery)
        result = myCursor.fetchone()
        return result[0]

    def deleteShift(self, idShift):
        try:
            mydb = self.connector()
            myCursor = mydb.cursor()
            mydb.autocommit = True
            sqlQuery = f'delete from botshiftkari.dayshift  where  idShift={idShift} '
            myCursor.execute(sqlQuery)
            sqlQuery = f'delete from botshiftkari.shift  where  idShift={idShift} '
            myCursor.execute(sqlQuery)
            sqlQuery = f"delete from botshiftkari.detailshift where idshift = {idShift} "
            myCursor.execute(sqlQuery)
            return 1
        except:
            return 0

    def insertSendMsg(self, chatId, msgId, typemsg, reqCode):
        sqlQuery = f'''insert into `botshiftkari`.`lstmsg` (`chatId`,`msgId`,`typemsg`,`reqCode`)values(\'{chatId}\',
                        \'{msgId}\',{typemsg},\'{reqCode}\')'''
        mydb = self.connector()
        mydb.autocommit = True
        myCursor = mydb.cursor()
        myCursor.execute(sqlQuery)
        return myCursor.lastrowid

    def getLstMsg(self, chatId, typemsg, reqCode):
        sqlQuery = f'select msgId from `botshiftkari`.`lstmsg` where typemsg={typemsg} and chatId = \'{chatId}\' and reqCode=\'{reqCode}\''
        mydb = self.connector()
        myCursor = mydb.cursor()
        myCursor.execute(sqlQuery)
        result = myCursor.fetchall()
        return result

    def delMsg(self, chatId, msgId):
        try:
            mydb = self.connector()
            myCursor = mydb.cursor()
            mydb.autocommit = True
            sqlQuery = f'delete from botshiftkari.lstmsg  where  msgId=\'{msgId}\' and chatId = \'{chatId}\' '
            myCursor.execute(sqlQuery)
            return 1
        except:
            return 0

    def getDayShiftForStudent(self, idMember, idShift):
        sqlQuery = f'call getDayShiftForStudent({idShift},{idMember})'
        mydb = self.connector()
        myCursor = mydb.cursor()
        myCursor.execute(sqlQuery)
        result = myCursor.fetchall()
        return result

    def delOldShift(self):
        datePersian = JalaliDate(datetime.datetime.now())
        sqlQuery = f"select idshift from botshiftkari.shift where dateEndShift < '{datePersian}'"
        mydb = self.connector()
        mydb.autocommit = True
        myCursor = mydb.cursor()
        myCursor.execute(sqlQuery)
        idsShift = myCursor.fetchall()
        for idShift in idsShift:
            sqlQuery = f"delete from botshiftkari.dayshift where idshift = {idShift[0]} "
            myCursor.execute(sqlQuery)
            sqlQuery = f"delete from botshiftkari.detailshift where idshift = {idShift[0]} "
            myCursor.execute(sqlQuery)
            sqlQuery = f"delete from botshiftkari.shift where idshift = {idShift[0]} "
            myCursor.execute(sqlQuery)
        return None
