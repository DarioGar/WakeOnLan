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
        query = "select ip,mac,cpu,ram,ssd,os,gpu,computers.id,name from computers where room_id IS NULL"
        cur.execute(query,)
        computers = cur.fetchall()
        return computers
    
    @staticmethod
    def poweredEachDay():
        cur = con.cursor()
        query = "select extract(dow from booted_at) as days, count(*) from bootup_log group by days"
        cur.execute(query,)
        days = cur.fetchall()
        return days

    @staticmethod
    def activeUsers():
        cur = con.cursor()
        query = "select username,count(*) from bootup_log group by username"
        cur.execute(query,)
        users = cur.fetchall()
        return users

    @staticmethod
    def insert(mac,ip,ram,cpu,gpu,os,ssd,owner,name):
        cur = con.cursor()
        try:
            query = "select id from public.users where username = %s"
            cur.execute(query,(owner,))
            user = cur.fetchone()
        except:
            return -1
        try:
            query = "INSERT INTO computers (mac,ip,ram,cpu,gpu,ssd,os,owner,name) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            cur.execute(query,(mac,ip,ram,cpu,gpu,ssd,os,user[0],name))
            con.commit()
            return 0
        except Exception as e:
            con.rollback()
            return -1

    @staticmethod
    def update(mac,ip,ram,cpu,gpu,os,ssd,name):
        cur = con.cursor()    
        try:
            query = "UPDATE computers SET (ip,ram,cpu,gpu,ssd,os,name) = (%s,%s,%s,%s,%s,%s,%s) WHERE mac = %s"
            cur.execute(query,(ip,ram,cpu,gpu,ssd,os,name,mac))
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
            query = "SELECT ip,mac,cpu,ram,ssd,os,gpu,computers.id,name FROM computers"
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
                        query = "SELECT ip,mac,cpu,ram,ssd,os,gpu,computers.id,name FROM computers INNER JOIN rooms ON computers.room_id = rooms.id where rooms.id = %s"
                        cur.execute(query,(room[0],))
                        computersInRoom = cur.fetchall()
                        computers.append(computersInRoom)
        # CASE 3 Check if the user has been given permissions to a specific computer
        query = "SELECT ip,mac,cpu,ram,ssd,os,gpu,computers.id,name FROM permissions INNER JOIN computers on computers.id = permissions.computer_id where permissions.user_id = %s"
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
            query = "INSERT INTO bootup_log (username,computer_id) VALUES (%s,%s)"
            cur.execute(query,(user,id))
            con.commit()
        except Exception as e:
            con.rollback()
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

        query = "SELECT ip,mac,cpu,ram,ssd,os,gpu,id,name from public.computers where owner = %s"
        cur.execute(query,(user[0],))
        computer = cur.fetchall()
        return computer

    @staticmethod
    def logsFor(mac):
        cur = con.cursor()
        query = "select id from public.computers where mac = %s"
        cur.execute(query,(mac,))
        id = cur.fetchone()

        query = "select * from public.bootup_log where computer_id = '%s'"
        cur.execute(query,(id[0],))
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
