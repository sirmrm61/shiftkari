import mysql.connector
import db.env as helper
from pprint import pprint
from model.membership import Founder, Membership, Student, TechnicalManager
from datetime import datetime as DT


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

    @portDb.setter
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
        mydb.autocommit = True;
        mycursor = mydb.cursor()
        mycursor.execute(sqlQuery)
        resualt = mycursor.fetchall()
        mycursor.reset()
        if len(resualt) == 0:
            sql = '''insert into membership (name,last_name,phone_number,membership_type,membership_fee_paid,
                registration_progress,username,chat_id,last_message_sent) VALUEs (%s,%s,%s,%s,%s,%s,%s,%s,%s)'''
            val = (
                member.name, member.last_name, member.phone_number, member.membership_type, member.membership_fee_paid,
                member.register_progress, member.userName, member.chatId, member.lastMessage)
            resualt = mycursor.execute(sql, val)
            mycursor.reset()
        else:
            sql = 'UPDATE `botshiftkari`.`membership` SET'
            updateExp = ''
            if member.name != None: updateExp = '`name` = \'{}\''.format(member.name)
            if member.last_name != None:
                if updateExp != None:
                    updateExp = '`last_name` = \'{}\''.format(member.last_name)
                else:
                    updateExp = ', `last_name` = \'{}\''.format(member.last_name)
            if member.phone_number != None:
                if updateExp != None:
                    updateExp = '`phone_number` = \'{}\''.format(member.phone_number)
                else:
                    updateExp = ', `phone_number` = \'{}\''.format(member.phone_number)
            if member.membership_fee_paid != None:
                if updateExp != None:
                    updateExp = '`membership_fee_paid` = \'{}\''.format(member.membership_fee_paid)
                else:
                    updateExp = ', `membership_fee_paid` = \'{}\''.format(member.membership_fee_paid)
            if member.register_progress != None:
                if updateExp != None:
                    updateExp = '`registration_progress` = \'{}\''.format(member.register_progress)
                else:
                    updateExp = ', `registration_progress` = \'{}\''.format(member.register_progress)
            if member.chatId != None:
                if updateExp != None:
                    updateExp = '`username` = \'{}\''.format(member.userName)
                else:
                    updateExp = ', `username` = \'{}\''.format(member.userName)
            if member.lastMessage != None:
                if updateExp != None:
                    updateExp = '`last_message_sent` = \'{}\''.format(member.lastMessage)
                else:
                    updateExp = ', `last_message_sent` = \'{}\''.format(member.lastMessage)
            print(updateExp)
            if len(updateExp) > 0:
                updateExp += ' WHERE `chat_id` = \'{0}\';'.format(member.chatId)
                sql += updateExp
                resualt = mycursor.execute(sql)
        mycursor.reset()
        mydb.close()

    def getAdmins(self):
        sqlQuery = '''select chat_id from `botshiftkari`.`membership` 
                            where membership_type = 4 and verifyAdmin =1 and del=0'''
        mydb = self.connector()
        mycursor = mydb.cursor()
        mycursor.execute(sqlQuery)
        resualt = mycursor.fetchall()
        mycursor.reset()
        return resualt

    def load_member(self, chatid):
        sqlQuery = 'select * from `botshiftkari`.`membership` where  chat_id = \'{}\''.format(chatid)
        mydb = self.connector()
        mycursor = mydb.cursor()
        mycursor.execute(sqlQuery)
        resualt = mycursor.fetchone()
        mycursor.reset()
        tempMember = Membership()
        if resualt != None:
            tempMember.name = resualt[1]
            tempMember.last_name = resualt[2]
            tempMember.phone_number = resualt[3]
            tempMember.membership_type = resualt[4]
            tempMember.membership_fee_paid = resualt[5]
            tempMember.register_progress = resualt[6]
            tempMember.userName = resualt[7]
            tempMember.chatId = resualt[8]
            tempMember.lastMessage = resualt[9]
            tempMember.verifyAdmin = resualt[10]
            tempMember.op = resualt[13]
            tempMember.delf = resualt[14]
            tempMember.opTime = DT.strptime(str(resualt[15]), '%Y-%m-%d %H:%M:%S')

        else:
            tempMember = None
        return tempMember

    def member_update(self, fieldName, fieldValue, chatid):
        sqlQuery = 'UPDATE `botshiftkari`.`membership` SET `{0}` = \'{1}\'  where chat_id = \'{2}\''.format(fieldName,
                                                                                                            fieldValue,
                                                                                                            chatid)
        mydb = self.connector()
        mydb.autocommit = True
        mycursor = mydb.cursor()
        resualt = mycursor.execute(sqlQuery)
        mycursor.reset()
        return resualt

    def member_update_chatid(self, fieldName, fieldValue, chatid):
        sqlQuery = 'UPDATE `botshiftkari`.`membership` SET `{0}` = \'{1}\'  where chat_id = \'{2}\''.format(fieldName,
                                                                                                            fieldValue,
                                                                                                            chatid)
        mydb = self.connector()
        mydb.autocommit = True
        mycursor = mydb.cursor()
        resualt = mycursor.execute(sqlQuery)
        mycursor.reset()
        return resualt

    def set_member_last_update_id(self, chatid, last_uid):
        sqlQuery = 'UPDATE `botshiftkari`.`membership` SET last_message_sent = {1}  where chat_id = \'{0}\''.format(
            chatid, last_uid)
        mydb = self.connector()
        mydb.autocommit = True
        mycursor = mydb.cursor()
        resualt = mycursor.execute(sqlQuery)
        mycursor.reset()
        return resualt

    def reactive_member_chatid(self, chatid):
        sqlQuery = 'select id from `botshiftkari`.`membership` where chat_id=\'{0}\''.format(chatid)
        mydb = self.connector()
        mydb.autocommit = True
        mycursor = mydb.cursor()
        mycursor.execute(sqlQuery)
        resualt = mycursor.fetchone();
        print(chatid)
        print(resualt[0])
        if resualt is None:
            return None
        else:
            sqlQuery = '''update `botshiftkari`.`membership` set del=0 WHERE id={0};
                            update `botshiftkari`.`founder` set del=0 WHERE idMember={0};
                            update `botshiftkari`.`student` set del=0 WHERE idMember ={0};
                            update `botshiftkari`.`technicalmanager` set del=0 WHERE idMember={0};'''.format(resualt[0])
            mycursor.execute(sqlQuery)
            return resualt[0]

    def del_member_chatid(self, chatid):
        sqlQuery = 'select id from `botshiftkari`.`membership` where chat_id=\'{0}\''.format(chatid)
        mydb = self.connector()
        mydb.autocommit = True
        mycursor = mydb.cursor()
        mycursor.execute(sqlQuery)
        resualt = mycursor.fetchone();
        if resualt is None:
            return None
        else:
            sqlQuery = '''update `botshiftkari`.`membership` set del=1 WHERE id={0};
                          update `botshiftkari`.`founder` set del=1 WHERE idMember={0};
                          update `botshiftkari`.`student` set del=1 WHERE idMember ={0};
                          update `botshiftkari`.`technicalmanager` set del=1 WHERE idMember={0};'''.format(resualt[0])
            mycursor.execute(sqlQuery)
            return resualt[0]

    def get_member_property_Adminchatid(self, fieldName, chatid):
        sqlQuery = 'select `{1}` from `botshiftkari`.`membership` where registration_progress = 15 and  adminChatId = \'{0}\''.format(
            chatid,
            fieldName)
        mydb = self.connector()
        mydb.autocommit = True
        mycursor = mydb.cursor()
        mycursor.execute(sqlQuery)
        resualt = mycursor.fetchone();
        if resualt is None:
            return None
        else:
            return resualt[0]

    def get_member_property_chatid(self, fieldName, chatid):
        sqlQuery = 'select `{1}` from `botshiftkari`.`membership` where  chat_id = \'{0}\''.format(chatid, fieldName)
        print(sqlQuery)
        mydb = self.connector()
        mydb.autocommit = True
        mycursor = mydb.cursor()
        mycursor.execute(sqlQuery)
        resualt = mycursor.fetchone();
        if resualt is None:
            return None
        else:
            return resualt[0]

    def create_member(self, member: Membership):
        sqlQuery = 'select * from `botshiftkari`.`membership` where chat_id = \'{}\''.format(member.chatId)
        mydb = self.connector()
        mydb.autocommit = True;
        mycursor = mydb.cursor()
        mycursor.execute(sqlQuery)
        resualt = mycursor.fetchall()
        mycursor.reset()
        if len(resualt) == 0:
            sql = '''insert into membership (name,last_name,phone_number,membership_type,membership_fee_paid,
            registration_progress,username,chat_id,last_message_sent) VALUEs (%s,%s,%s,%s,%s,%s,%s,%s,%s)'''
            val = (
                member.name, member.last_name, member.phone_number, member.membership_type, member.membership_fee_paid,
                member.register_progress, member.userName, member.chatId, member.lastMessage)
            resualt = mycursor.execute(sql, val)
            mycursor.reset()
        return member;

    def get_funder_property(self, fieldName, chatid):
        sqlQuery = 'select id from `botshiftkari`.`membership` where  chat_id = \'{0}\''.format(chatid)
        mydb = self.connector()
        mydb.autocommit = True
        mycursor = mydb.cursor()
        mycursor.execute(sqlQuery)
        resualt = mycursor.fetchone();
        idMember = resualt[0]
        sqlQuery = 'select {0} from `botshiftkari`.`founder` where idMember={1}'.format(fieldName, idMember)
        mycursor.execute(sqlQuery)
        resualt = mycursor.fetchone()
        if resualt is None:
            return None
        else:
            return resualt[0]

    def founder_update(self, fieldName, fieldValue, chatid):
        sqlQuery = 'select id from `botshiftkari`.`membership` where  chat_id = \'{0}\''.format(chatid)
        mydb = self.connector()
        mydb.autocommit = True
        mycursor = mydb.cursor()
        mycursor.execute(sqlQuery)
        resualt = mycursor.fetchone();
        idMember = resualt[0]
        sqlQuery = 'select id from `botshiftkari`.`founder` where idMember={}'.format(idMember)
        mycursor.execute(sqlQuery)
        resualt = mycursor.fetchone()
        if resualt is None:
            sqlQuery = 'insert into `botshiftkari`.`founder` (idMember,{0}) values ({1},\'{2}\')'.format(fieldName,
                                                                                                         idMember,
                                                                                                         fieldValue)
        else:
            sqlQuery = 'UPDATE `botshiftkari`.`founder` SET `{0}` = \'{1}\'  where idMember = \'{2}\''.format(fieldName,
                                                                                                              fieldValue,
                                                                                                              idMember)
        mycursor.execute(sqlQuery)
        mycursor.reset()
        return resualt

    def get_student_property(self, fieldName, chatid):
        sqlQuery = 'select id from `botshiftkari`.`membership` where  chat_id = \'{0}\''.format(chatid)
        mydb = self.connector()
        mydb.autocommit = True
        mycursor = mydb.cursor()
        mycursor.execute(sqlQuery)
        resualt = mycursor.fetchone()
        idMember = resualt[0]
        sqlQuery = 'select {0} from `botshiftkari`.`student` where idMember={1}'.format(fieldName, idMember)
        mycursor.execute(sqlQuery)
        resualt = mycursor.fetchone()
        if resualt is None:
            return None
        else:
            return resualt[0]

    def student_update(self, fieldName, fieldValue, chatid):
        sqlQuery = 'select id from `botshiftkari`.`membership` where  chat_id = \'{0}\''.format(chatid)
        mydb = self.connector()
        mydb.autocommit = True
        mycursor = mydb.cursor()
        mycursor.execute(sqlQuery)
        resualt = mycursor.fetchone();
        idMember = resualt[0]
        sqlQuery = 'select id from `botshiftkari`.`student` where idMember={}'.format(idMember)
        mycursor.execute(sqlQuery)
        resualt = mycursor.fetchone()
        if resualt is None:
            sqlQuery = 'insert into `botshiftkari`.`student` (idMember,{0}) values ({1},\'{2}\')'.format(fieldName,
                                                                                                         idMember,
                                                                                                         fieldValue)
        else:
            sqlQuery = 'UPDATE `botshiftkari`.`student` SET `{0}` = \'{1}\'  where idMember = \'{2}\''.format(fieldName,
                                                                                                              fieldValue,
                                                                                                              idMember)
        mycursor.execute(sqlQuery)
        mycursor.reset()
        return resualt

    def get_technical_property(self, fieldName, chatid):
        sqlQuery = 'select id from `botshiftkari`.`membership` where  chat_id = \'{0}\''.format(chatid)
        mydb = self.connector()
        mydb.autocommit = True
        mycursor = mydb.cursor()
        mycursor.execute(sqlQuery)
        resualt = mycursor.fetchone();
        idMember = resualt[0]
        sqlQuery = 'select {0} from `botshiftkari`.`technicalmanager` where idMember={1}'.format(fieldName, idMember)
        mycursor.execute(sqlQuery)
        resualt = mycursor.fetchone()
        if resualt is None:
            return None
        else:
            return resualt[0]

    def technicalManager_update(self, fieldName, fieldValue, chatid):
        sqlQuery = 'select id from `botshiftkari`.`membership` where  chat_id = \'{0}\''.format(chatid)
        mydb = self.connector()
        mydb.autocommit = True
        mycursor = mydb.cursor()
        mycursor.execute(sqlQuery)
        resualt = mycursor.fetchone();
        idMember = resualt[0]
        sqlQuery = 'select id from `botshiftkari`.`technicalmanager` where idMember={}'.format(idMember)
        mycursor.execute(sqlQuery)
        resualt = mycursor.fetchone()
        if resualt is None:
            sqlQuery = 'insert into `botshiftkari`.`technicalmanager` (idMember,{0}) values ({1},\'{2}\')'.format(
                fieldName, idMember, fieldValue)
        else:
            sqlQuery = 'UPDATE `botshiftkari`.`technicalmanager` SET `{0}` = \'{1}\'  where idMember = \'{2}\''.format(
                fieldName, fieldValue, idMember)
        mycursor.execute(sqlQuery)
        mycursor.reset()
        return resualt

    def shift_update(self, fieldName, fieldValue, chatid):
        mydb = self.connector()
        mydb.autocommit = True
        mycursor = mydb.cursor()
        sqlQuery = 'select idshift from `botshiftkari`.`shift` where progress=0 and Creator={}'.format(chatid)
        mycursor.execute(sqlQuery)
        resualt = mycursor.fetchone()
        if resualt is None:
            sqlQuery = 'insert into `botshiftkari`.`shift` (Creator,{0}) values (\'{1}\',\'{2}\')'.format(fieldName,
                                                                                                          chatid,
                                                                                                          fieldValue)
            resualt = mycursor.lastrowid
        else:
            sqlQuery = 'UPDATE `botshiftkari`.`shift` SET `{0}` = \'{1}\'  where progress=0 and Creator = \'{2}\''.format(
                fieldName, fieldValue, chatid)
        mycursor.execute(sqlQuery)
        mycursor.reset()
        return resualt

    def shift_update_by_id(self, fieldName, fieldValue, idshift):
        mydb = self.connector()
        mydb.autocommit = True
        mycursor = mydb.cursor()
        sqlQuery = 'UPDATE `botshiftkari`.`shift` SET `{0}` = \'{1}\'  where  idshift = \'{2}\''.format(
            fieldName, fieldValue, idshift)
        mycursor.execute(sqlQuery)
        mycursor.reset()
        return None

    def shift_reserve_by_id(self, idshift, chatid):
        mydb = self.connector()
        mydb.autocommit = True
        mycursor = mydb.cursor()
        sqlQuery = 'UPDATE `botshiftkari`.`shift` SET `progress` = 3,`approver`=\'{1}\'  where progress=2 and idshift = \'{0}\''.format(
            idshift, chatid)
        print(sqlQuery)
        mycursor.execute(sqlQuery)
        mycursor.reset()
        return None

    def get_shift_property(self, fieldName, idShift):
        mydb = self.connector()
        mydb.autocommit = True
        mycursor = mydb.cursor()
        sqlQuery = 'select {0} from `botshiftkari`.`shift` where idshift={1}'.format(fieldName, idShift)
        mycursor.execute(sqlQuery)
        resualt = mycursor.fetchone()
        if resualt is None:
            return None
        else:
            return resualt[0]

    def get_all_shift(self=None, progress=1, creator=0):
        mydb = self.connector()
        mydb.autocommit = True
        mycursor = mydb.cursor()
        sqlQuery = '''SELECT concat(mem.name,mem.last_name) as fullname,creator,
                        DateShift,startTime,endTime,wage,pharmacyAddress,progress,approver,shi.idshift,
                        shi.dateEndShift
                        FROM botshiftkari.shift shi inner join botshiftkari.membership mem on
                         mem.chat_id = shi.Creator where not shi.creator = '{0}' and shi.progress={1}'''.format(creator,
                                                                                                                progress)
        mycursor.execute(sqlQuery)
        resualt = mycursor.fetchall()
        return resualt;

    def get_shift_no_approve(self=None, progress=1, creator=0):
        mydb = self.connector()
        mydb.autocommit = True
        mycursor = mydb.cursor()
        sqlQuery = '''SELECT concat(mem.name,mem.last_name) as fullname,creator,
                         DateShift,startTime,endTime,wage,pharmacyAddress,progress,approver,shi.idshift,
                         shi.dateEndShift
                         FROM botshiftkari.shift shi inner join botshiftkari.membership mem on
                          mem.chat_id = shi.Creator where approver is null and not shi.creator = '{0}' and shi.progress={1}'''.format(
            creator, progress)
        print(sqlQuery)
        mycursor.execute(sqlQuery)
        resualt = mycursor.fetchall()
        return resualt

    def get_all_shift_by_creator(self=None, creator=0):
        mydb = self.connector()
        mydb.autocommit = True
        mycursor = mydb.cursor()
        sqlQuery = '''SELECT concat(mem.name,mem.last_name) as fullname,creator,
                        DateShift,startTime,endTime,wage,pharmacyAddress,progress,approver,shi.idshift,
                        shi.dateEndShift,shi.wfStudent
                        FROM botshiftkari.shift shi inner join botshiftkari.membership mem on
                         mem.chat_id = shi.Creator where  shi.creator = '{0}' and (shi.progress=1 or shi.progress=2) and shi.del=0'''.format(
            creator)
        mycursor.execute(sqlQuery)
        resualt = mycursor.fetchall()
        return resualt

    def get_all_shift_manager(self=None):
        mydb = self.connector()
        mydb.autocommit = True
        mycursor = mydb.cursor()
        sqlQuery = '''SELECT concat(mem.name,mem.last_name) as fullname,creator,
                        DateShift,startTime,endTime,wage,pharmacyAddress,progress,approver,shi.idshift,
                        shi.dateEndShift,shi.wfStudent
                        FROM botshiftkari.shift shi inner join botshiftkari.membership mem on
                         mem.chat_id = shi.Creator and shi.del=0 '''
        mycursor.execute(sqlQuery)
        resualt = mycursor.fetchall()
        return resualt

    def get_all_shift_managerForApprove(self=None):
        mydb = self.connector()
        mydb.autocommit = True
        mycursor = mydb.cursor()
        sqlQuery = '''SELECT concat(mem.name,mem.last_name) as fullname,creator,
                        DateShift,startTime,endTime,wage,pharmacyAddress,progress,approver,shi.idshift,
                        shi.dateEndShift,shi.wfStudent
                        FROM botshiftkari.shift shi inner join botshiftkari.membership mem on
                         mem.chat_id = shi.Creator where progress = 1 and shi.del = 0'''
        mycursor.execute(sqlQuery)
        resualt = mycursor.fetchall()
        return resualt

    def get_all_shift_managerApproved(self=None):
        mydb = self.connector()
        mydb.autocommit = True
        mycursor = mydb.cursor()
        sqlQuery = '''SELECT concat(mem.name,mem.last_name) as fullname,creator,
                        DateShift,startTime,endTime,wage,pharmacyAddress,progress,approver,shi.idshift,
                        shi.dateEndShift,shi.wfStudent
                        FROM botshiftkari.shift shi inner join botshiftkari.membership mem on
                         mem.chat_id = shi.Creator where progress = 2 and shi.del = 0'''
        mycursor.execute(sqlQuery)
        resualt = mycursor.fetchall()
        return resualt;

    def get_all_member(self=None, tye=None):
        mydb = self.connector()
        mydb.autocommit = True
        mycursor = mydb.cursor()
        sqlQuery = None
        if tye is None:
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
        else:
            sqlQuery = '''select concat(mem.name,mem.last_name) as fullname,
                                        case 
                                        when mem.membership_type = 1 then 'موسس'
                                        when mem.membership_type = 2 then 'مسئول فنی'
                                        when mem.membership_type = 3 then 'دانشجو'
                                        when mem.membership_type = 4 then 'مدیر'
                                        else 'نامشخص'
                                        end as typeMember,
                                        mem.phone_number
                                        from  botshiftkari.membership as mem  where mem.membership_type={}'''.format(
                tye)
        mycursor.execute(sqlQuery)
        resualt = mycursor.fetchall()
        return resualt

    def get_all_shift_by_approver(self=None, creator='0', dateShift=''):
        mydb = self.connector()
        mycursor = mydb.cursor()
        sqlQuery = '''SELECT concat(mem.name,mem.last_name) as fullname,creator,
                        DateShift,startTime,endTime,wage,pharmacyAddress,progress,approver,shi.idshift,
                        shi.dateEndShift,shi.wfStudent
                        FROM botshiftkari.shift shi inner join botshiftkari.membership mem on
                         mem.chat_id = shi.Creator where  shi.approver = '{0}' and shi.DateShift> '{1}'
                          and (shi.progress=3 or shi.progress=4) and shi.del=0'''.format(creator, dateShift)
        mycursor.execute(sqlQuery)
        resualt = mycursor.fetchall()
        return resualt

    def get_all_property_shift_byId(self=None, idshift=0):
        mydb = self.connector()
        mydb.autocommit = True
        mycursor = mydb.cursor()
        sqlQuery = '''SELECT concat(mem.name,mem.last_name) as fullname,creator,
                        DateShift,startTime,endTime,wage,pharmacyAddress,progress,approver,shi.idshift,
                        shi.dateEndShift,shi.wfStudent
                        FROM botshiftkari.shift shi inner join botshiftkari.membership mem on
                         mem.chat_id = shi.Creator where  shi.idshift={0}'''.format(idshift)
        mycursor.execute(sqlQuery)
        resualt = mycursor.fetchone()
        return resualt

    def get_all_ts_chatid(self, creator=None):
        mydb = self.connector()
        mydb.autocommit = True
        mycursor = mydb.cursor()
        sqlQuery = None
        if creator is None:
            sqlQuery = '''SELECT mem.chat_id from botshiftkari.membership as mem where mem.del=0 and 
            mem.membership_type=2 '''
        else:
            sqlQuery = '''SELECT mem.chat_id from botshiftkari.membership as mem where mem.del=0 and 
                        mem.membership_type=2 and not mem.chat_id = \'{0}\''''.format(creator)
        mycursor.execute(sqlQuery)
        resualt = mycursor.fetchall()
        return resualt

    def get_property_domain(self, key):
        mydb = self.connector()
        mydb.autocommit = True
        myCursor = mydb.cursor()
        sqlQuery = '''SELECT value from `botshiftkari`.`domain` where `key` = \'{0}\''''.format(key)
        myCursor.execute(sqlQuery)
        resualt = myCursor.fetchone()
        return resualt[0]

    def domain_update_by_key(self, key, value):
        mydb = self.connector()
        mydb.autocommit = True
        myCursor = mydb.cursor()
        sqlQuery = 'UPDATE `botshiftkari`.`domain` SET `value` = \'{0}\'  where `key` = \'{1}\''.format(value, key)
        print(sqlQuery)
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
        resualt = myCursor.fetchone()
        if int(resualt[0]) > 0:
            return True
        sqlQuery = 'select count(*) from `botshiftkari`.`student` where `national_code` = \'{0}\''.format(
            nationCode)
        myCursor.execute(sqlQuery)
        resualt = myCursor.fetchone()
        if int(resualt[0]) > 0:
            return True
        return False

    def get_list_shift_for_student(self):
        # send تعیین می کند که آیا برای دانشجویان ارسال شده اس قبلا
        mydb = self.connector()
        mydb.autocommit = True
        myCursor = mydb.cursor()
        sqlQuery = 'select `value` from `botshiftkari`.`domain` where `key` = \'hrStudent\''
        myCursor.execute(sqlQuery)
        resualt = myCursor.fetchone()
        sqlQuery = '''SELECT concat(mem.name,' ',mem.last_name) as fullname,creator,
                        DateShift,startTime,endTime,wage,pharmacyAddress,progress,approver,shi.idshift,
                        shi.dateEndShift,shi.wfStudent
                        FROM botshiftkari.shift shi inner join botshiftkari.membership mem on
                         mem.chat_id = shi.Creator where `progress` > '0'  and    `progress` < '3'  and 
                         `send` = 0 and  date_add(shi.dateRegiter,interval {0} HOUR)<now()'''.format(
            resualt[0])
        myCursor.execute(sqlQuery)
        resualt = myCursor.fetchall()
        return resualt

    def get_all_student_chatid(self):
        mydb = self.connector()
        mycursor = mydb.cursor()
        sqlQuery = 'SELECT mem.chat_id from botshiftkari.membership as mem where mem.del=0 and mem.membership_type=3 '
        mycursor.execute(sqlQuery)
        resualt = mycursor.fetchall()
        return resualt

    def checkExsistDetail(self, mem: Membership, newType):
        mydb = self.connector()
        myCursor = mydb.cursor()
        sqlQuery = f'select id from botshiftkari.membership where chat_id = {mem.chatId}'
        myCursor.execute(sqlQuery)
        resualt = myCursor.fetchone()
        idMember = resualt[0]
        if newType == 1:
            sqlQuery = f'select count(*) from botshiftkari.founder where idMember = {idMember}'
        elif newType == 2:
            sqlQuery = f'select count(*) from botshiftkari.technicalmanager where idMember = {idMember}'
        elif newType == 3:
            sqlQuery = f'select count(*) from botshiftkari.student where idMember = {idMember}'
        else:
            return False
        myCursor.execute(sqlQuery)
        resualt = myCursor.fetchone()
        count = int(resualt[0])
        print(f'Count={count}')
        if count == 1:
            return True
        else:
            return False

    def registerDayShift(self, idShift, dateShift, requster, sendedForCreator, status=None):
        tmpIdDayShift = self.getIdRegisterDayOfShift(idShift, dateShift, requster)
        if tmpIdDayShift != 0:
            return tmpIdDayShift
        mydb = self.connector()
        myCursor = mydb.cursor()
        mydb.autocommit = True
        if status is None:
            sqlQuery = f'''INSERT INTO `botshiftkari`.`dayshift`
(`idShift`,
`dateShift`,
`requster`,
`approveCreator`,
`sendedForCreator`)
VALUES({idShift},\'{dateShift}\',\'{requster}\',0,{sendedForCreator});SELECT LAST_INSERT_ID();'''
        else:
            sqlQuery = f'''INSERT INTO `botshiftkari`.`dayshift`
            (`idShift`,
            `dateShift`,
            `requster`,
            `approveCreator`,
            `sendedForCreator`,status)
            VALUES({idShift},\'{dateShift}\',\'{requster}\',0,{sendedForCreator},{status});SELECT LAST_INSERT_ID();'''
        myCursor.execute(sqlQuery)
        res = myCursor.fetchone()
        return res

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
        mycursor = mydb.cursor()
        sqlQuery = f'SELECT {fieldName} from botshiftkari.dayshift  where  idDayShift={idDayShift}'
        mycursor.execute(sqlQuery)
        resualt = mycursor.fetchone()
        if resualt == None:
            return None
        else:
            return resualt[0]

    def getEmptyDayOfShift(self, idShift):
        mydb = self.connector()
        mycursor = mydb.cursor()
        sqlQuery = f'SELECT * from botshiftkari.dayshift  where  approveCreator=0 and idShift={idShift}'
        mycursor.execute(sqlQuery)
        resualt = mycursor.fetchall()
        return resualt

    def getIdRegisterDayOfShift(self, idShift, dateShift, requsterShift):
        mydb = self.connector()
        mycursor = mydb.cursor()
        sqlQuery = f'SELECT iddayShift from botshiftkari.dayshift  where  idShift={idShift} and dateShift=\'{dateShift}\'' + \
                   f' and requster=\'{requsterShift}\''
        mycursor.execute(sqlQuery)
        resualt = mycursor.fetchone()
        if resualt is not None:
            return resualt[0]
        else:
            return 0

    def isShiftDayFull(self, idShift, dateShift):
        mydb = self.connector()
        mycursor = mydb.cursor()
        sqlQuery = f'SELECT count(iddayShift) from botshiftkari.dayshift  where  idShift={idShift} and dateShift=\'{dateShift}\'' + \
                   f' and status = 2 '
        mycursor.execute(sqlQuery)
        resualt = mycursor.fetchone()
        return resualt[0]

    def getListDaySelection(self, idShift, requsterShift):
        mydb = self.connector()
        mycursor = mydb.cursor()
        sqlQuery = f'SELECT iddayShift,dateShift from botshiftkari.dayshift  where  idShift={idShift} and status= 0 ' + \
                   f' and requster=\'{requsterShift}\''
        mycursor.execute(sqlQuery)
        resualt = mycursor.fetchall()
        return resualt

    def getIdShiftFromDay(self, idDayShift):
        mydb = self.connector()
        mycursor = mydb.cursor()
        sqlQuery = f'SELECT idshift from botshiftkari.dayshift  where  iddayShift={idDayShift} '
        mycursor.execute(sqlQuery)
        resualt = mycursor.fetchone()
        if resualt is not None:
            return resualt[0]
        else:
            return None

    def removeFromSelection(self, idDayShift):
        mydb = self.connector()
        mycursor = mydb.cursor()
        mydb.autocommit = True
        sqlQuery = f'delete from botshiftkari.dayshift  where  iddayShift={idDayShift} and status = 0 '
        mycursor.execute(sqlQuery)

    def getListDayIsNotEmpty(self, idShift, status=2):
        mydb = self.connector()
        mycursor = mydb.cursor()
        sqlQuery = f'SELECT iddayShift,dateShift from botshiftkari.dayshift  where  idShift={idShift}'
        if status is not None:
            sqlQuery += f' and status= {status} '
        mycursor.execute(sqlQuery)
        result = mycursor.fetchall()
        return result

    def getListMember(self, sender, group=None):
        sqlQuery = ''
        if group is None:
            sqlQuery = f"SELECT chat_id FROM botshiftkari.membership where not chat_id = '{sender}'"
        else:
            sqlQuery = f"SELECT chat_id FROM botshiftkari.membership where not chat_id = '{sender}'  and membership_type = {group}"
        mydb = self.connector()
        mycursor = mydb.cursor()
        mycursor.execute(sqlQuery)
        result = mycursor.fetchall()
        return result
