from datetime import date
from api.v1 import con
from api.reusable import checkMAC
from wakeonlan import send_magic_packet
import schedule

class Computer:

    def __init__(self,mac,os,cpu,ssd,ram,gpu):
        self.mac = mac
        self.cpu = cpu
        self.os = os
        self.ram = ram
        self.gpu = gpu
        self.ssd = ssd

    @staticmethod
    def fetchComputerFor(username):
        cur = con.cursor()
        computers = []
        query = "select role,id from public.users where username = %s"
        cur.execute(query,(username,))
        user = cur.fetchone()
        # If the role is project_manager we return all the computers assigned to the room
        
        if user[0] == 'project_manager':
            query = "SELECT DISTINCT  rooms.id FROM rooms INNER JOIN work_group ON work_group.id = rooms.group_id where work_group.user_id = %s"
            cur.execute(query,(user[1],))
            rows = cur.fetchall()
            # We look for all the computers in every room and append them to the computers array
            for row in rows:
                query = "SELECT ip,mac,cpu,ram,ssd,os,gpu,computers.id FROM computers INNER JOIN rooms ON computers.room_id = rooms.id where rooms.id = %s"
                cur.execute(query,(row[0],))
                computersInRoom = cur.fetchall()
                computers.append(computersInRoom)
        if user[0] == 'admin':
            query = "SELECT ip,mac,cpu,ram,ssd,os,gpu,computers.id FROM computers"
            cur.execute(query,)
            computersInRoom = cur.fetchall()
            computers.append(computersInRoom)
        if user[0] != 'admin':
            query = "SELECT ip,mac,cpu,ram,ssd,os,gpu,computers.id FROM permissions INNER JOIN computers on computers.id = permissions.computer_id where permissions.user_id = %s"
            cur.execute(query,(user[1],))
            rows = cur.fetchall()
            computers.append(rows)
        return list(set(computers[0]))

    @staticmethod
    def powerOn(MAC):
        formattedMAC = MAC.replace('-',':')
        if(checkMAC(formattedMAC)):
            responseData = send_magic_packet(formattedMAC)
        print(responseData)
        print(date.today())
        return schedule.CancelJob

    @staticmethod
    def fetch(id):
        cur = con.cursor()
        query = "select * from public.computers where id = %s"
        cur.execute(query,(id,))
        computer = cur.fetchone()
        return computer
        