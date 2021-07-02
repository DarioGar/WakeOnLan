from api.v1 import con
from api.models.User import User

class Group:
    
    def __init__(self,userId,groupName,path,department):
        self.userID = userId
        self.name = groupName
        self.path = path
        self.department = department

    @staticmethod
    def getMembersOf(groupID):
        cur = con.cursor()
        query = "select username,role,email from users INNER JOIN group_member ON group_member.user_id = users.id where group_member.group_id = %s"
        cur.execute(query,(groupID,))
        users = cur.fetchall()
        return users

    @staticmethod
    def getWorkGroups(username):
        cur = con.cursor()
        query = "SELECT work_group.id,work_group.user_id,work_group.name,path,department FROM work_group INNER JOIN group_member ON group_member.group_id = work_group.id INNER JOIN users on users.id = group_member.user_id where users.username = %s"
        cur.execute(query,(username,))
        return cur.fetchall()

    def insertNewGroup(self):
        cur = con.cursor()
        query = "INSERT INTO public.work_group (user_id,name,path,department) VALUES (%s,%s,%s,%s) RETURNING id"
        cur.execute(query,(self.userID,self.name,self.path,self.department))
        con.commit()
        return cur.fetchone()[0] 

    