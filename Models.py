import sqlite3
import bcrypt
from flask_login import login_user, UserMixin


class Connect:
    def __init__(self):
        conn= sqlite3.connect('hobbybook.db')
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        self.conn = conn
        self.cursor = cursor

    def getcursor(self):
        return self.cursor
    def commit(self):
        self.conn.commit()
    def __del__(self):
        self.conn.close()

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
                'password':  out['password'],
                'name':  out['name'],
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
            cursor.execute('INSERT INTO USERS(username,name,password) values(?,?,?)',(username,name,bcrypt.hashpw(password,salt=bcrypt.gensalt())))
            conn.commit()
            login_user(User(props={'username':username,'name':name,'password':password}))
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
        del conn
        return User(props=res)

    def getHobbies(self):
        conn = Connect()
        cursor = conn.getcursor()
        cursor.execute('SELECT hobbies.hobbyname,hobbies.hobbytype,user_hobbies.progress,user_hobbies.isprogresscheckActive from hobbies inner join user_hobbies on user_hobbies.hobbyname=hobbies.hobbyname where user_hobbies.username=?',(self.props['username'],))

        hobbies = [dict(i) for i in cursor.fetchall()]
        del conn
        return hobbies

    def addHobbies(self,hobbyname,milestones):
        conn = Connect()
        cursor = conn.getcursor()
        milestone1,milestone2,milestone3,milestone4,milestone5 = milestones
        cursor.execute('Insert into user_hobbies(username,hobbyname,progress,isprogresscheckActive,milestone1,milestone2,milestone3,milestone4,milestone5) values(?,?,?,?,?,?,?,?,?)',(self.props['username'],hobbyname,0,0,milestone1,milestone2,milestone3,milestone4,milestone5))
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
        cursor.execute('''UPDATE FRIENDSHIPS SET STATUS='FRIENDS' WHERE USERNAME1=? and USERNAME2=?''',(self.props['username'],friendusername))
        conn.commit()
        del conn
        return 200
    def ShowAllFriends(self):
        conn = Connect()
        cursor = conn.getcursor()
        cursor.execute('SELECT CASE WHEN USERNAME1=? THEN USERNAME2 WHEN USERNAME2=? THEN USERNAME1 END FROM FRIENDSHIPS WHERE STATUS=?',(self.props['username'], self.props['username'],'FRIENDS'))
        res = cursor.fetchall()
        return res

    def setProgressCheckonHobby(self,hobby):
        conn = Connect()
        cursor = conn.getcursor()
        cursor.execute('''UPDATE USER_HOBBIES SET isprogresscheckActive=? WHERE username=? AND hobbyname=? ''',(1,str(self.props['username']),str(hobby)))
        conn.commit()
        del conn
        return 200

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
        hobbies = [i['hobbyname'] for i in temp]
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



conn = Connect()
cursor = conn.getcursor()
cursor.execute('PRAGMA table_info(USER_HOBBIES)');
print([dict(i) for i in cursor.fetchall()])
del conn