from api.v1 import con

class Group:
    
    def __init__(self,userId,groupName,path,department):
        self.userID = userId
        self.groupName = groupName
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

    def insertNewGroup(self,username):
        cur = con.cursor()
        try:
            query = "INSERT INTO public.work_group (user_id,name,path,department) VALUES (%s,%s,%s,%s) RETURNING id"
            cur.execute(query,(self.userID,self.groupName,self.path,self.department))
            con.commit()
            id = cur.fetchone()[0] 
        except:
            return -1
        try:
            query = "INSERT INTO group_member (user_id,group_id) VALUES (%s,%s)"
            cur.execute(query,(self.userID,id))
            con.commit()
        except:
            return -1
        return 0
    @staticmethod
    def delete(groupID):
        cur = con.cursor()
        try:
            query = "DELETE FROM work_group where id = %s"
            cur.execute(query,(groupID,))
            con.commit()
            return 0
        except:
            con.rollback()
            return -1

    @staticmethod
    def assign(roomID,groupID):
        cur = con.cursor()
        try:
            query = "UPDATE rooms SET group_id = %s where id = %s"
            cur.execute(query,(groupID,roomID))
            con.commit()
            return 0
        except:
            con.rollback()
            return -1

    def getRoomForGroup(groupID):
        cur = con.cursor()
        try:
            query = "SELECT FROM rooms WHERE group_id = %s"
            cur.execute(query,(groupID,))
            result = cur.fetchone()
            return result
        except:
            return -1

