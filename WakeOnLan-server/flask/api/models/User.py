from api.v1 import con
from api.reusable import check_password

class User:

    def __init__(self,name,password,fname,rtype):
        self.username = name
        self.pw = password
        self.fullname = fname
        self.role = rtype

    @staticmethod
    def get(username):
        cur = con.cursor()
        query = "select count(1) from public.users where username = %s"
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
        query = "select id,password from public.users where username = %s"
        cur.execute(query,(username,))
        rows = cur.fetchone()
        if check_password(password,rows[1]):
            return rows[0]
        else:
            return None

    def register(self):
        cur = con.cursor()
        # Hash and salt the password before storing it
        query = "INSERT INTO public.users (full_name,username,password,role) VALUES (%s,%s,%s,%s) RETURNING id"
        cur.execute(query,(self.fullname,self.username,self.pw,self.role))
        con.commit()
        return cur.fetchone()[0]

    

