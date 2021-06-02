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
    def exists(username):
        cur = con.cursor()
        query = "select count(1) from public.users where username = %s"
        cur.execute(query,(username,))
        rows = cur.fetchall()
        return rows[0]
    @staticmethod
    def get(username):
        cur = con.cursor()
        query = "select * from public.users where username = %s"
        cur.execute(query,(username,))
        rows = cur.fetchall()
        return rows[0]
    @staticmethod
    def delete(username):
        cur = con.cursor()
        query = "delete from public.users where username = %s"
        cur.execute(query,(username,))
        con.commit()
        rows = cur.rowcount
        return rows
    
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

    

