from api.v1 import con
from api.reusable import check_password

class User:

    def __init__(self,name,password,fname,email):
        self.username = name
        self.pw = password
        self.email = email
        self.fullname = fname
        self.roles = []

    @staticmethod
    def getInvitations(username):
        cur = con.cursor()
        query = "select id from public.users where username = %s"
        cur.execute(query,(username,))
        user = cur.fetchone()
        query = "select * from public.invitations where receiver = %s"
        cur.execute(query,(user[0],))
        rows = cur.fetchall()
        return rows
        


    @staticmethod
    def sendInvite(sender,to,groupId):
        cur = con.cursor()
        query = "SELECT id FROM public.users WHERE username = %s"
        cur.execute(query,(sender,))
        sender = cur.fetchone()
        cur.execute(query,(to,))
        receiver = cur.fetchone()
        try:
            query = "INSERT INTO invitations (sender,receiver,work_group,status) VALUES (%s,%s,%s,%s) RETURNING id"
            cur.execute(query,(sender[0],receiver[0],groupId,"on hold"))
            con.commit()
            return cur.fetchone()
        except:
            con.rollback()
            return (-1,)

    @staticmethod
    def acceptInvitation(invitationID):
        cur = con.cursor()
        try:
            query = "UPDATE invitations SET status = 'accepted' WHERE id = %s"
            cur.execute(query,(invitationID,))
            con.commit()
        except Exception as e:
            return e
        return 0

    @staticmethod
    def addUserToGroup(userID,groupID):
        cur = con.cursor()
        try:
            query = "INSERT INTO group_member (user_id,group_id) VALUES (%s,%s)"
            cur.execute(query,(userID,groupID))
            con.commit()
        except Exception as e:
            return 0

    @staticmethod
    def denyInvitation(invitationID):
        cur = con.cursor()
        query = "UPDATE invitations SET status = 'refused' WHERE id = %s"
        cur.execute(query,(invitationID,))
        con.commit()
        return cur.fetchone()
        
    @staticmethod
    def exists(username):
        cur = con.cursor()
        query = "select count(1) from public.users where username = %s"
        cur.execute(query,(username,))
        rows = cur.fetchall()
        return rows[0]
    @staticmethod
    def fetchByUsername(username):
        cur = con.cursor()
        query = "select * from public.users where username = %s"
        cur.execute(query,(username,))
        rows = cur.fetchall()
        return rows[0]

    @staticmethod
    def delete(username):
        cur = con.cursor()
        query = "delete from users where username = %s"
        cur.execute(query,(username,))
        print("result")
        con.commit()
        rows = cur.rowcount
        return rows

    @staticmethod
    def updateUserDataAndPassword(username,pw,fullname,role,email):
        try:
            cur = con.cursor()
            query = "UPDATE users SET (password,full_name,role,email) = (%s,%s,%s,%s) WHERE username = %s"
            cur.execute(query,(pw,fullname,role,email,username))
            con.commit()
            return 0
        except:
            return -1

    @staticmethod
    def updateUserData(username,fullname,role,email):
        try:
            cur = con.cursor()
            query = "UPDATE users SET (full_name,role,email) = (%s,%s,%s) WHERE username = %s"
            cur.execute(query,(fullname,role,email,username))
            con.commit()
            return 0
        except:
            return -1
    
    @staticmethod
    def authenticate(username,password):
        cur = con.cursor()
        query = "select * from public.users where username = %s"
        cur.execute(query,(username,))
        rows = cur.fetchone()
        if(rows!=None):
            if check_password(password,rows[3]):
                return rows
            else:
                return None
        return None

    @staticmethod
    def fetchAll():
        cur = con.cursor()
        query = "select username,email,role,password,full_name from public.users"
        cur.execute(query)
        rows = cur.fetchall()
        if(rows!=None):
            return rows
        else:
            return None
    
    @staticmethod
    def fetch(id):
        cur = con.cursor()
        query = "select username from public.users where id = %s"
        cur.execute(query,(id,))
        rows = cur.fetchone()
        if(rows!=None):
            return rows[0]
        else:
            return None

    def register(self):
        cur = con.cursor()
        query = "INSERT INTO public.users (full_name,username,password,role,email) VALUES (%s,%s,%s,%s,%s) RETURNING id"
        cur.execute(query,(self.fullname,self.username,self.pw,self.roles.pop(),self.email))
        con.commit()
        return cur.fetchone()[0] 

    def setRoles(self,role):
        if(role == 'regular'):
            self.roles.append('regular')
        if(role == 'project_manager'):
            self.roles.append('project_manager')
            self.roles.append('regular')
        if(role == 'learning'):
            self.roles.append('learning')
        if(role == 'admin'):
            self.roles.append('admin')
            self.roles.append('project_manager')
            self.roles.append('learning')
            self.roles.append('regular')

    

