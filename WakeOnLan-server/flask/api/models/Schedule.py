from api.v1 import con

class Schedule:

    def __init__(self,user_id,computer_id,time,days):
        self.user_id = user_id
        self.computer_id = computer_id
        self.time = time
        self.days = days

    def insert(self):
        cur = con.cursor()
        query = "INSERT INTO schedule_bootup (user_id,computer_id,time,days) values (%s,%s,%s,%s) RETURNING id"
        cur.execute(query,(self.user_id,self.computer_id,self.time,self.days))
        con.commit()
        return cur.fetchone()[0]