from api.v1 import con

class Program:
    
    def __init__(self,name,path):
        self.name = name
        self.path = path

    @staticmethod
    def getPrograms(mac):
        cur = con.cursor()
        query = "SELECT id FROM computers WHERE mac = %s"
        cur.execute(query,(mac,))
        computer = cur.fetchone()
        query = "select * from programs where computer_id = %s"
        cur.execute(query,(computer,))
        rows = cur.fetchall()
        return rows

    @staticmethod
    def setPrograms(program,mac):
        cur = con.cursor()
        query = "SELECT id FROM computers WHERE mac = %s"
        cur.execute(query,(mac,))
        computer = cur.fetchone()
        cur = con.cursor()
        try:
            query = "DELETE FROM programs where computer_id = %s"
            cur.execute(query,(computer,))
            con.commit()
        except:
            return -1
        try:
            query = "INSERT INTO programs (name,path,computer_id) VALUES (%s,%s,%s) ON CONFLICT DO NOTHING"
            cur.execute(query,(program.name,program.path,computer))
            con.commit()
            return 0
        except:
            con.rollback()
            return -1

