import mysql.connector
import  db.env as helper
from pprint import pprint
from model.membership import Founder,Membership,Student,TechnicalManager
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
        return mysql.connector.connect(host=self._ipDb,user=self._userDb,password=self._passDb,port=self._portDb,database=helper.dbName)
    def insert_Founder(self, member: Founder):
            sqlQuery= 'select * from `botshiftkari`.`membership` where username = \'{}\''.format(member.userName)
            mydb = self.connector()
            mydb.autocommit = True;
            mycursor =mydb.cursor()
            mycursor.execute(sqlQuery)
            resualt = mycursor.fetchall()
            mycursor.reset()
            if len(resualt) == 0 :
                sql = '''insert into membership (name,last_name,phone_number,membership_type,membership_fee_paid,
                registration_progress,username,chat_id,last_message_sent) VALUEs (%s,%s,%s,%s,%s,%s,%s,%s,%s)'''
                val = (member.name,member.last_name,member.phone_number,member.membership_type,member.membership_fee_paid,
                       member.register_progress,member.userName,member.chatId,member.lastMessage)
                resualt = mycursor.execute(sql,val)
                mycursor.reset()
            else :
                sql = 'UPDATE `botshiftkari`.`membership` SET'
                updateExp = ''
                if member.name != None : updateExp = '`name` = \'{}\''.format(member.name)
                if member.last_name != None :
                    if updateExp != None :
                        updateExp = '`last_name` = \'{}\''.format(member.last_name)
                    else :
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
                        updateExp = '`chat_id` = \'{}\''.format(member.chatId)
                    else:
                        updateExp = ', `chat_id` = \'{}\''.format(member.chatId)
                if member.lastMessage != None:
                    if updateExp != None:
                        updateExp = '`last_message_sent` = \'{}\''.format(member.lastMessage)
                    else:
                        updateExp = ', `last_message_sent` = \'{}\''.format(member.lastMessage)
                print(updateExp)
                if len(updateExp) > 0 :
                    updateExp += ' WHERE `username` = \'{0}\';'.format(member.userName)
                    sql += updateExp
                    pprint(sql)
                    resualt = mycursor.execute(sql)
            pprint(resualt)
            mycursor.reset()
            mydb.close();

    def getAdmins(self):
        sqlQuery = 'select chat_id from `botshiftkari`.`membership` where membership_type = 4 and verifyAdmin =1'
        mydb = self.connector()
        mycursor = mydb.cursor()
        mycursor.execute(sqlQuery)
        resualt = mycursor.fetchall()
        mycursor.reset()
        return  resualt

    def load_member(self,uname):
        sqlQuery = 'select * from `botshiftkari`.`membership` where username = \'{}\''.format(uname)
        mydb = self.connector()
        mycursor = mydb.cursor()
        mycursor.execute(sqlQuery)
        resualt = mycursor.fetchone()
        mycursor.reset()
        tempMember=Membership()
        if resualt != None :
            tempMember.name=resualt[1]
            tempMember.last_name=resualt[2]
            tempMember.phone_number=resualt[3]
            tempMember.membership_type=resualt[4]
            tempMember.membership_fee_paid=resualt[5]
            tempMember.register_progress=resualt[6]
            tempMember.userName = resualt[7]
            tempMember.chatId = resualt[8]
            tempMember.lastMessage = resualt[9]
        else:
            tempMember = None
        return  tempMember
    def member_update(self,fieldName,fieldValue,uname):
        sqlQuery = 'UPDATE `botshiftkari`.`membership` SET `{0}` = \'{1}\'  where username = \'{2}\''.format(fieldName,fieldValue,uname)
        mydb = self.connector()
        mydb.autocommit=True
        mycursor = mydb.cursor()
        resualt= mycursor.execute(sqlQuery)
        mycursor.reset()
        return  resualt
    def member_update_chatid(self,fieldName,fieldValue,chatid):
        sqlQuery = 'UPDATE `botshiftkari`.`membership` SET `{0}` = \'{1}\'  where chat_id = \'{2}\''.format(fieldName,fieldValue,chatid)
        mydb = self.connector()
        mydb.autocommit=True
        mycursor = mydb.cursor()
        resualt= mycursor.execute(sqlQuery)
        mycursor.reset()
        return  resualt
    def set_member_last_update_id(self,chatid,last_uid):
        sqlQuery = 'UPDATE `botshiftkari`.`membership` SET last_message_sent = {1}  where chat_id = \'{0}\''.format(chatid,last_uid)
        mydb = self.connector()
        mydb.autocommit=True
        mycursor = mydb.cursor()
        resualt= mycursor.execute(sqlQuery)
        mycursor.reset()
        return  resualt
    def del_member_chatid(self,chatid):
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
            sqlQuery = '''DELETE FROM `botshiftkari`.`membership` WHERE id={0};
                          DELETE FROM `botshiftkari`.`founder`WHERE idMember={0};
                          DELETE FROM `botshiftkari`.`student` WHERE idMember ={0};
                          DELETE FROM `botshiftkari`.`technicalmanager` WHERE idMember={0};'''.format(resualt[0])
            mycursor.execute(sqlQuery)
            return resualt[0]
    def get_member_property_Adminchatid(self,fieldName,chatid):
        sqlQuery = 'select `{1}` from `botshiftkari`.`membership` where  adminChatId = \'{0}\''.format(chatid,fieldName)
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
    def get_member_property_chatid(self,fieldName,chatid):
        sqlQuery = 'select `{1}` from `botshiftkari`.`membership` where  chat_id = \'{0}\''.format(chatid,fieldName)
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
    def create_member(self,member:Membership):
        sqlQuery = 'select * from `botshiftkari`.`membership` where username = \'{}\''.format(member.userName)
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
            member.register_progress, member.userName, member.chatid, member.lastMessage)
            resualt = mycursor.execute(sql, val)
            mycursor.reset()
        return member;
    def get_funder_property(self,fieldName,chatid):
        sqlQuery = 'select id from `botshiftkari`.`membership` where  chat_id = \'{0}\''.format(chatid)
        mydb = self.connector()
        mydb.autocommit = True
        mycursor = mydb.cursor()
        mycursor.execute(sqlQuery)
        resualt = mycursor.fetchone();
        idMember = resualt[0]
        sqlQuery = 'select {0} from `botshiftkari`.`founder` where idMember={1}'.format(fieldName,idMember)
        mycursor.execute(sqlQuery)
        resualt = mycursor.fetchone()
        if resualt is None:
            return None
        else:
            return resualt[0]
    def founder_update(self,fieldName,fieldValue,chatid):
        sqlQuery = 'select id from `botshiftkari`.`membership` where  chat_id = \'{0}\''.format(chatid)
        mydb = self.connector()
        mydb.autocommit=True
        mycursor = mydb.cursor()
        mycursor.execute(sqlQuery)
        resualt = mycursor.fetchone();
        idMember = resualt[0]
        sqlQuery = 'select id from `botshiftkari`.`founder` where idMember={}'.format(idMember)
        mycursor.execute(sqlQuery)
        resualt = mycursor.fetchone()
        if resualt is None:
            sqlQuery= 'insert into `botshiftkari`.`founder` (idMember,{0}) values ({1},\'{2}\')'.format(fieldName,idMember,fieldValue)
        else:
            sqlQuery = 'UPDATE `botshiftkari`.`founder` SET `{0}` = \'{1}\'  where idMember = \'{2}\''.format(fieldName,fieldValue,idMember)
        pprint(sqlQuery)
        mycursor.execute(sqlQuery)
        mycursor.reset()
        return  resualt
    def get_student_property(self,fieldName,chatid):
        sqlQuery = 'select id from `botshiftkari`.`membership` where  chatid = \'{0}\''.format(chat_id)
        mydb = self.connector()
        mydb.autocommit = True
        mycursor = mydb.cursor()
        mycursor.execute(sqlQuery)
        resualt = mycursor.fetchone();
        idMember = resualt[0]
        sqlQuery = 'select {0} from `botshiftkari`.`student` where idMember={1}'.format(fieldName,idMember)
        mycursor.execute(sqlQuery)
        resualt = mycursor.fetchone()
        if resualt is None:
            return None
        else:
            return resualt[0]
    def student_update(self,fieldName,fieldValue,chatid):
        sqlQuery = 'select id from `botshiftkari`.`membership` where  chat_id = \'{0}\''.format(chatid)
        mydb = self.connector()
        mydb.autocommit=True
        mycursor = mydb.cursor()
        mycursor.execute(sqlQuery)
        resualt = mycursor.fetchone();
        idMember = resualt[0]
        sqlQuery = 'select id from `botshiftkari`.`student` where idMember={}'.format(idMember)
        mycursor.execute(sqlQuery)
        resualt = mycursor.fetchone()
        if resualt is None:
            sqlQuery= 'insert into `botshiftkari`.`student` (idMember,{0}) values ({1},\'{2}\')'.format(fieldName,idMember,fieldValue)
        else:
            sqlQuery = 'UPDATE `botshiftkari`.`student` SET `{0}` = \'{1}\'  where idMember = \'{2}\''.format(fieldName,fieldValue,idMember)
        pprint(sqlQuery)
        mycursor.execute(sqlQuery)
        mycursor.reset()
        return  resualt
    def get_technical_property(self,fieldName,chatid):
        sqlQuery = 'select id from `botshiftkari`.`membership` where  chat_id = \'{0}\''.format(chatid)
        mydb = self.connector()
        mydb.autocommit = True
        mycursor = mydb.cursor()
        mycursor.execute(sqlQuery)
        resualt = mycursor.fetchone();
        idMember = resualt[0]
        sqlQuery = 'select {0} from `botshiftkari`.`technicalmanager` where idMember={1}'.format(fieldName,idMember)
        mycursor.execute(sqlQuery)
        resualt = mycursor.fetchone()
        if resualt is None:
            return None
        else:
            return resualt[0]
    def technicalManager_update(self,fieldName,fieldValue,chatid):
        sqlQuery = 'select id from `botshiftkari`.`membership` where  chat_id = \'{0}\''.format(chatid)
        mydb = self.connector()
        mydb.autocommit=True
        mycursor = mydb.cursor()
        mycursor.execute(sqlQuery)
        resualt = mycursor.fetchone();
        idMember = resualt[0]
        sqlQuery = 'select id from `botshiftkari`.`technicalmanager` where idMember={}'.format(idMember)
        mycursor.execute(sqlQuery)
        resualt = mycursor.fetchone()
        if resualt is None:
            sqlQuery= 'insert into `botshiftkari`.`technicalmanager` (idMember,{0}) values ({1},\'{2}\')'.format(fieldName,idMember,fieldValue)
        else:
            sqlQuery = 'UPDATE `botshiftkari`.`technicalmanager` SET `{0}` = \'{1}\'  where idMember = \'{2}\''.format(fieldName,fieldValue,idMember)
        pprint(sqlQuery)
        mycursor.execute(sqlQuery)
        mycursor.reset()
        return  resualt
