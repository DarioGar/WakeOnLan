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
    def fetchAll():
        cur = con.cursor()
        query = "select * from computers"
        cur.execute(query,)
        computers = cur.fetchall()
        return computers

    @staticmethod
    def fetchComputersUnassigned():
        cur = con.cursor()
        query = "select ip,mac,cpu,ram,ssd,os,gpu,computers.id from computers where room_id IS NULL"
        cur.execute(query,)
        computers = cur.fetchall()
        return computers
    
    @staticmethod
    def insert(mac,ip,ram,cpu,gpu,os,ssd,owner):
        cur = con.cursor()
        try:
            query = "select id from public.users where username = %s"
            cur.execute(query,(owner,))
            user = cur.fetchone()
        except:
            return -1
        try:
            query = "INSERT INTO computers (mac,ip,ram,cpu,gpu,ssd,os,owner) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
            cur.execute(query,(mac,ip,ram,cpu,gpu,ssd,os,user[0]))
            con.commit()
            return 0
        except Exception as e:
            con.rollback()
            return -1

    @staticmethod
    def update(mac,ip,ram,cpu,gpu,os,ssd):
        cur = con.cursor()    
        try:
            query = "UPDATE computers SET (ip,ram,cpu,gpu,ssd,os) = (%s,%s,%s,%s,%s,%s) WHERE mac = %s"
            cur.execute(query,(ip,ram,cpu,gpu,ssd,os,mac))
            con.commit()
            return 0
        except Exception as e:
            con.rollback()
            return -1
    
    @staticmethod
    def delete(mac):
        cur = con.cursor()
        try:
            query = "DELETE FROM computers WHERE mac = %s"
            cur.execute(query,(mac,))
            con.commit()
            return 0
        except Exception as e:
            con.rollback()
            return -1

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
    def powerOn(MAC,user):
        formattedMAC = MAC.replace('-',':')
        if(checkMAC(formattedMAC)):
            Computer.registerLog(user,MAC)
            send_magic_packet(formattedMAC)
        return schedule.CancelJob

    @staticmethod
    def registerLog(user,mac):
        cur = con.cursor()
        query = "select id from public.computers where mac = %s"
        cur.execute(query,(mac,))
        id = cur.fetchone()
        try:
            query = "INSERT INTO bootup_log (username,computer_ip) VALUES (%s,%s)"
            cur.execute(query,(user,id))
            con.commit()
        except Exception as e:
            return 0

    @staticmethod
    def fetch(id):
        cur = con.cursor()
        query = "select * from public.computers where id = %s"
        cur.execute(query,(id,))
        computer = cur.fetchone()
        return computer

    @staticmethod
    def computersOf(username):
        cur = con.cursor()
        query = "select id from public.users where username = %s"
        cur.execute(query,(username,))
        user = cur.fetchone()

        query = "SELECT ip,mac,cpu,ram,ssd,os,gpu,id from public.computers where owner = %s"
        cur.execute(query,(user[0],))
        computer = cur.fetchall()
        return computer

    @staticmethod
    def logsFor(mac):
        cur = con.cursor()
        query = "select id from public.computers where mac = %s"
        cur.execute(query,(mac,))
        user = cur.fetchone()

        query = "select * from public.bootup_log where computer_ip = %s"
        cur.execute(query,(user[0],))
        computer = cur.fetchall()
        return computer

    @staticmethod
    def usersAllowedOn(mac):
        cur = con.cursor()
        query = "select id from public.computers where mac = %s"
        cur.execute(query,(mac,))
        user = cur.fetchone()

        query = "select user_id from public.permissions where computer_id = %s"
        cur.execute(query,(user[0],))
        computer = cur.fetchall()
        return computer
        
    @staticmethod
    def changeAllowed(username,allowed,mac):
        cur = con.cursor()
        query = "select id from public.users where username = %s"
        cur.execute(query,(username,))
        user = cur.fetchone()
        query = "select id from public.computers where mac = %s"
        cur.execute(query,(mac,))
        computer = cur.fetchone()
        if(allowed):
            try:
                query = "insert into permissions values (%s,%s)"
                cur.execute(query,(user,computer,))
                con.commit()
                result = "allowed"
            except:
                con.rollback()
                result = "allowed"
        else:
            query = "delete from permissions where user_id=%s AND computer_id=%s"
            cur.execute(query,(user[0],computer[0]))
            con.commit()
            result = "disallowed"
        return result
