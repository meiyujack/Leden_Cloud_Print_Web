import socket, time
import uuid, random
import sqlite3
import os

from template import Template


class App: 
    # def select_db(table, get='*', prep=None, **condition):
    #     sql = f"SELECT {get} FROM {table}"
    #     try:
    #         if condition:
    #             where = f" WHERE {','.join(condition.keys())}={','.join(['?'])}"
    #             if len(condition) == 1:
    #                 sql += where
    #             else:
    #                 where = f' {prep} '.join([
    #                     f"{''.join(m.keys())}={''.join(['?'])}" for m in [{i: j} for i, j in condition.items()]
    #                 ])
    #                 sql += ' WHERE ' + where
    #         cur=conn.cursor()
    #         cur.execute(sql,tuple(condition.values()))
    #         rows= cur.fetchall()
    #         return rows
    #     except sqlite3.Error as e:
    #         conn.rollback()
    #         return f"Error: {e}"

    def insert(data:dict=None):
        if data:
            keys = ','.join(data.keys())
            values = ','.join(['?'] * len(data))
            try:
                sql = f"INSERT INTO log({keys}) VALUES({values});"
                with sqlite3.connect('db.sqlite3') as conn:
                    cur=conn.cursor()
                    cur.execute(sql, tuple(data.values()))
                    conn.commit()
            except sqlite3.Error as e:
                conn.rollback()
                return f"Error:{e}"
            
    def generate_unique(type: str, num: int):
        answer = ''
        uid = str(uuid.uuid4())
        while len(answer) != num:
            r = random.choice(uid)
            match type:
                case 0:
                    if r.isalnum():
                        answer += r
            match type:
                case 1:
                    if r.isdigit():
                        answer += r
            match type:
                case 2:
                    if r.isalpha():
                        answer += r
        return answer

    def send_print_job(cmd, printer_ip="40.90.232.31", port=6000):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.connect((printer_ip, port))
                s.sendall(App.interpret(cmd))
                print(
                    f"{time.strftime('%Y-%m-%d %H:%M:%S')}打印任务已发送"
                )
            except Exception as e:
                print(f"发送打印任务失败：{e}")
    
    def generate_cmd(title: str, content: list, rfid_type_num: tuple,
                     qr: str):
        my = Template()
        title_cmd = my.get_content(X=200, Y=10, WD=40, LG=40, text=title)
        text, text2, text3, text4 = content
        rfid = App.generate_unique(rfid_type_num[0], rfid_type_num[1])
        qr_cmd = my.get_qr(qr=qr, x=480, y=220)

        App.insert({"title":title,"content1":text,"content2":text2,"content3":text3,"content4":text4,"rfid":rfid,"qrcode":qr})
        return f"{my.header}{title_cmd}{my.get_content(Y=60,text=text)}{my.get_content(Y=110,text=text2)}{my.get_content(Y=150,text=text3)}{my.get_content(Y=200,text=text4)}{my.get_rfid(rfid)}{qr_cmd}{my.footer}"

    @staticmethod
    def interpret(cmd:str)->bytes:
        return cmd.encode('ansi') if os.name =='nt' else cmd.encode('gbk')