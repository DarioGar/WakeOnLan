from api.v1 import con
import json

class Room:

    def __init__(self,id,location,capacity,use,computers):
        self.id = id
        self.location = location
        self.capacity = capacity
        self.use = use
        self.computers = computers

    @staticmethod
    def fetchAll():
        cur = con.cursor()
        query = "select * from rooms"
        cur.execute(query,)
        rooms = cur.fetchall()
        return rooms
    
    @staticmethod
    def insert(location,capacity,use):
        cur = con.cursor()
        query = "INSERT INTO rooms (location,capacity,expected_use) VALUES (%s,%s,%s)"
        try:
            cur.execute(query,(location,capacity,use))
            con.commit()
            return 0
        except:
            con.rollback()
            return -1

    @staticmethod
    def delete(roomID):
        cur = con.cursor()
        query = "DELETE FROM rooms WHERE id = %s"
        try:
            cur.execute(query,(roomID,))
            con.commit()
            return 0
        except:
            con.rollback()
            return -1


    @staticmethod
    def fetchComputersInRoom(room):
        cur = con.cursor()
        query = "select ip,mac,cpu,ram,ssd,os,gpu,computers.id,name from computers where room_id = %s"
        cur.execute(query,(room,))
        rooms = cur.fetchall()
        return rooms

    @staticmethod
    def setRoomIDFor(computers,roomID):
        cur = con.cursor()
        try:
            query = "UPDATE computers AS c1 SET room_id = NULL FROM computers AS c2 WHERE c1.room_id=%s"
            cur.execute(query,(roomID,))
            con.commit()
        except:
            return -1
        try:
            for computer in computers:
                query = "UPDATE computers SET room_id = %s WHERE mac = %s"
                cur.execute(query,(roomID,computer['mac']))
                con.commit()
            return 0
        except:
            return -1