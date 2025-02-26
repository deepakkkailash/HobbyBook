import sqlite3
import bcrypt
from flask_login import login_user, UserMixin


class Connect:
    def __init__(self):
        conn= sqlite3.connect('hobbybook.db')
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        self.__conn = conn
        self.__cursor = cursor

    def getcursor(self):
        return self.__cursor
    def commit(self):
        self.__conn.commit()
    def __del__(self):
        self.__conn.close()

class User(UserMixin):
    def __init__(self,props):
        self.props = props
    @staticmethod
    def loginuser(username,password):
        conn = Connect()
        cursor = conn.getcursor()
        cursor.execute('SELECT * FROM Users where users.username=?',(username,))
        out = dict(cursor.fetchone())

        if(len(out)==0):
            del conn
            return 500

        if (bcrypt.checkpw(password,  out['password'])):
            outputdict = {
                'username':  out['username'],
                'name':  out['name'],
                'noofhobbies': out['NOOFHOBBIES']
            }

            login_user(User(props=outputdict))

            del conn
            return 200
        else:

            del conn
            return 500

    @staticmethod
    def signupuser(username,password,name):
        conn = Connect()
        cursor = conn.getcursor()
        try:
            cursor.execute('INSERT INTO USERS(username,name,password,NOOFHOBBIES) values(?,?,?,?)',(username,name,bcrypt.hashpw(password,salt=bcrypt.gensalt()),0))
            conn.commit()
            login_user(User(props={'username':username,'name':name,'noofhobbies':0}))
            return 200
        except Exception:
                return 500
    def get_id(self):
        return self.props['username']

    @staticmethod
    def loaduserusingusername(username):
        conn = Connect()
        cursor = conn.getcursor()
        cursor.execute('SELECT * from Users where username=?',(username,))
        res= dict(cursor.fetchone())
        outputdict = {
            'username': res['username'],
            'name': res['name'],
            'noofhobbies':res['NOOFHOBBIES']
        }
        del conn
        return User(props=outputdict)

    def getHobbies(self):
        conn = Connect()
        cursor = conn.getcursor()
        cursor.execute('SELECT hobbies.hobbyname,hobbies.hobbytype,user_hobbies.progress,user_hobbies.isprogresscheckActive,user_hobbies.hobbycompleted from hobbies inner join user_hobbies on user_hobbies.hobbyname=hobbies.hobbyname where user_hobbies.username=?',(self.props['username'],))

        hobbies = [dict(i) for i in cursor.fetchall()]
        del conn
        return hobbies

    def addHobbies(self,hobbyname,milestones):
        conn = Connect()
        cursor = conn.getcursor()
        milestone1,milestone2,milestone3,milestone4,milestone5 = milestones

        cursor.execute('Insert into user_hobbies( username,hobbyname,progress,isprogresscheckActive,milestone1,milestone2,milestone3,milestone4,milestone5,HOBBYCOMPLETED) values(?,?,?,?,?,?,?,?,?,?)',(self.props['username'],hobbyname,0,0,milestone1,milestone2,milestone3,milestone4,milestone5,'No'))
        conn.commit()
        del conn
        return 200
    def addFriend(self,friendusername):
        conn = Connect()
        cursor = conn.getcursor()
        cursor.execute('INSERT INTO FRIENDSHIPS(USERNAME1,USERNAME2,STATUS) VALUES (?,?,?)',(self.props['username'],friendusername,'PENDING'))
        conn.commit()
        del conn
        return 200
    def acceptfriend(self,friendusername):
        conn = Connect()
        cursor = conn.getcursor()
        cursor.execute('''UPDATE FRIENDSHIPS SET STATUS='FRIENDS'
        WHERE (USERNAME1=? and USERNAME2=?) OR (USERNAME1=? AND USERNAME2=?)''',(self.props['username'],friendusername,friendusername,self.props['username']))
        conn.commit()
        del conn
        return 200
    def get_friends(self):
        conn = Connect()
        cursor = conn.getcursor()
        cursor.execute("""
             SELECT 
        CASE
           WHEN username1 = ? THEN username2
           WHEN username2 = ? THEN username1
        END from friendships WHERE   (USERNAME1=? OR USERNAME2=?) AND STATUS=?;
        """,(self.props['username'], self.props['username'],self.props['username'], self.props['username'],'FRIENDS'))
        res = cursor.fetchall()
        return res

    def setProgressCheckonHobby(self,hobby):
        conn = Connect()
        cursor = conn.getcursor()
        cursor.execute('''UPDATE USER_HOBBIES SET isprogresscheckActive=? WHERE username=? AND hobbyname=? ''',(1,str(self.props['username']),str(hobby)))
        conn.commit()
        del conn
        return 200

    def getMilestones(self,hobby):
        conn = Connect()
        cursor = conn.getcursor()

        cursor.execute('''
    SELECT 
        CASE 
            WHEN PROGRESS = 0 THEN milestone1 || ',' || milestone2 || ',' || milestone3 || ',' || milestone4 || ',' || milestone5
            WHEN PROGRESS = 20 THEN milestone2 || ',' || milestone3 || ',' || milestone4 || ',' || milestone5
            WHEN PROGRESS = 40 THEN milestone3 || ',' || milestone4 || ',' || milestone5
            WHEN PROGRESS = 60 THEN milestone4 || ',' || milestone5
            WHEN PROGRESS = 80 THEN milestone5
            
        END AS MILESTONES
    FROM user_hobbies 
    WHERE username = ? AND hobbyname = ?
''', (self.props['username'], hobby))
        res = cursor.fetchone()
        print(dict(res))

        del conn
        return dict(res)

    def updateMilestones(self,milestone_progress,target_hobby):
        try:
            conn = Connect()
            cursor = conn.getcursor()
            prog = int(milestone_progress)*20
            print(prog)
            cursor.execute('''
            UPDATE USER_HOBBIES SET HOBBYCOMPLETED=
             CASE 
                WHEN PROGRESS=80.0 THEN 'COMPLETED'
                ELSE 'ONGOING'
            END,
            PROGRESS=
            CASE
                WHEN PROGRESS<=80.0 THEN PROGRESS+?
                ELSE 100.0
            END
                WHERE USERNAME=? AND HOBBYNAME=?''',(prog,self.props['username'],target_hobby))
            conn.commit()
            return True
        except BaseException:
            return False
class Hobby:
    def __init__(self):
        None
    @staticmethod
    def addhobby(name,type):
        conn = Connect()
        cursor = conn.getcursor()
        cursor.execute('Insert into hobbies (hobbyname,hobbytype) values(?,?)',(name,type))
        conn.commit()
        del conn
        return 200

    @staticmethod
    def getall():
        conn = Connect()
        cursor = conn.getcursor()
        cursor.execute('SELECT * from Hobbies')
        res = cursor.fetchall()
        temp = [dict(i) for i in res]
        hobbies = [i['hobbyname']  for i in temp if i['hobbyname']!='' and i['hobbyname'][0].isalpha()]
        del conn
        return hobbies[1:]

    @staticmethod
    def searchhobby(hobby):
        conn = Connect()
        cursor = conn.getcursor()
        cursor.execute('SELECT user_hobbies.username, hobbies.hobbyname, hobbies.hobbytype from hobbies left join user_hobbies on hobbies.hobbyname = user_hobbies.hobbyname where hobbies.hobbyname=?',(hobby,))
        res = cursor.fetchall()
        details = {'numberOfUsers':0,'hobbyname':'NotFound','hobbytype':'NotFound'}
        if (len(res) == 0):
            return details
        for i in res:
            print(dict(i))
        if((len(res)==1) and ((dict(res[0]).get('username'))==None)):
            details = {'numberOfUsers': 0, 'hobbyname': dict(res[0])['hobbyname'], 'hobbytype': dict(res[0])['hobbytype']}
            return details


        details['numberOfUsers'] = len(res)
        details['hobbyname'] = dict(res[0])['hobbyname']
        details['hobbytype'] = dict(res[0])['hobbytype']
        del conn
        return details


