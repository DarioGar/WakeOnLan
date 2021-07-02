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
        # Get both role and id from the user
        query = "select role,id from public.users where username = %s"
        cur.execute(query,(username,))
        user = cur.fetchone()

        
        # CASE 1 User is an admin, return everything
        if user[0] == 'admin':
            query = "SELECT ip,mac,cpu,ram,ssd,os,gpu,computers.id FROM computers"
            cur.execute(query,)
            computersInRoom = cur.fetchall()
            computers.append(computersInRoom)
            return list(set(computers[0]))
        # CASE 2a User belongs to some group, add computers assigned to the group
        query = "select group_id from group_member where user_id = %s"
        cur.execute(query,(user[1],))
        work_groups = cur.fetchall()
        if len(work_groups) != 0:
            for group_id in work_groups:
                    # Necesita cambio URGENTE
                    query = "SELECT DISTINCT rooms.id FROM rooms where group_id = %s"
                    cur.execute(query,(group_id[0],))
                    rooms = cur.fetchall()
                    # We look for all the computers in every room and append them to the computers array
                    for room in rooms:
                        query = "SELECT ip,mac,cpu,ram,ssd,os,gpu,computers.id FROM computers INNER JOIN rooms ON computers.room_id = rooms.id where rooms.id = %s"
                        cur.execute(query,(room[0],))
                        computersInRoom = cur.fetchall()
                        computers.append(computersInRoom)
        # CASE 3 Check if the user has been given permissions to a specific computer
        query = "SELECT ip,mac,cpu,ram,ssd,os,gpu,computers.id FROM permissions INNER JOIN computers on computers.id = permissions.computer_id where permissions.user_id = %s"
        cur.execute(query,(user[1],))
        rows = cur.fetchall()
        computers.append(rows)
        return list(set(computers[0]))
        

    @staticmethod
    def powerOn(MAC):
        formattedMAC = MAC.replace('-',':')
        if(checkMAC(formattedMAC)):
             send_magic_packet(formattedMAC)
        return schedule.CancelJob

    @staticmethod
    def fetch(id):
        cur = con.cursor()
        query = "select * from public.computers where id = %s"
        cur.execute(query,(id,))
        computer = cur.fetchone()
        return computer
        