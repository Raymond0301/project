import sqlite3
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
# class and stuff


class User:
    def __init__(self, id, username, email, password):
        self.__id = id
        self.__username = username
        self.__email = email
        self.__password = password

    def get_id(self):
        return self.__id

    def get_username(self):
        return self.__username

    def get_email(self):
        return self.__email

    def get_password(self):
        return self.__password

    def set_username(self, username):
        self.__username = username

    def set_email(self, email):
        self.__email = email

    def set_password(self, password):
        self.__password = password

class Savings(User):
    def __init__(self,username,month,target,actual):
        super.__init__(username)
        self.__month = month
        self.__target = target
        self.__actual = actual

    def get_month(self):
        return self.__month

    def get_target(self):
        return self.__target

    def get_actual(self):
        return self.__actual

    def set_month(self,month):
        self.__month = month

    def set_target(self,target):
        self.__target = target

    def set_actual(self,actual):
        self.__actual = actual

conn = sqlite3.connect('user.db', check_same_thread=False)

c = conn.cursor()

#c.execute("""CREATE TABLE user (
 #              id text,
   #           username text,
  #              email text,
    #           password text
    #           )""")


def create_user(id, username, email, password):
    emp_1 = User(id, username, email, password)
    c.execute("INSERT INTO user VALUES(?, ?, ?, ?)", (emp_1.get_id(), emp_1.get_username(), emp_1.get_email(), emp_1.get_password()))
    conn.commit()


def get_user(username, password):
    g = c.execute("SELECT * FROM user WHERE username=? AND password=?", (username, password))
    conn.commit()
    if g is None:
        return None
    else:
        for row in g:
            print(row)
            if username in row[1] and password in row[3]:
                return username
        return None


def check_user(username, email):
    k = c.execute("SELECT * FROM user")
    conn.commit()
    for row in k:
        print(row)
        if row[1] == username or row[2] == email:
            return False


# after forget password send email and user got password, add a back button for user to go back


def clear_user():
    c.execute("DELETE FROM user")
    conn.commit()


def forget_passwords(email):
    d = c.execute("SELECT * FROM user")
    conn.commit()
    for row in d:
        print(row)
        if email == row[2]:
            password = row[3]
            username = row[1]
            fromaddr = "raymondsinglaire@gmail.com"
            toaddr = email
            msg = MIMEMultipart()
            msg['From'] = fromaddr
            msg['To'] = toaddr
            msg['Subject'] = "Forget password"
            body = "Dear " + username + "," + "\n" + "          Your password is " + password + "." + "\n" + "\n" + "Regards ," + "\n" + "Bot"
            msg.attach(MIMEText(body, 'plain'))
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login("raymondsinglaire@gmail.com", "g0d1sg00d")
            text = msg.as_string()
            server.sendmail(fromaddr, toaddr, text)
            return False
    return None


con = sqlite3.connect('savings.db', check_same_thread=False)

t = con.cursor()
#t.execute('''CREATE TABLE savings(
          #username text NOT NULL,
          #month text NOT NULL,
          #traget_saving INTEGER,
          #actual_amount_saved INTEGER
                      #)''')


def saving_table(username, month, target, actual):
    saving = Savings(username, month, target, actual)
    t.execute('INSERT INTO savings VALUES (?,?,?,?)', (saving.get_username(), saving.get_month(), saving.get_target(), saving.get_actual()))
    con.commit()

