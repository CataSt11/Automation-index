import mysql.connector


class init_mysql:
    def __init__(self):
        # initialize mysql connector
        try:
            self.conn = mysql.connector.connect(
                host="0.0.0.0",
                user="root",
                passwd="",
                database="automationdb",
            )
        except Exception as e:
            print(e)

        self.mycursor = self.conn.cursor(dictionary=True)
