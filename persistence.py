import sqlite3
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import shelve
import uuid
from datetime import date
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


class Savings:
    def __init__(self, username, month, target, actual):
        self.__username = username
        self.__month = month
        self.__target = target
        self.__actual = actual

    def get_username(self):
        return self.__username

    def get_month(self):
        return self.__month

    def get_target(self):
        return self.__target

    def get_actual(self):
        return self.__actual

    def get_id(self):
        return self.__username + self.__month

    def set_username(self, username):
        self.__username = username

    def set_month(self, month):
        self.__month = month

    def set_target(self, target):
        self.__target = target

    def set_actual(self, actual):
        self.__actual = actual

    def difference(self):
        return self.__actual <= self.__target


class Blog:
    def __init__(self, id):
        self.id = id
        self.username = ''
        self.title = ''
        self.body = ''
        self.created = ''


class Expenses:
    def __init__(self, name, amount, date, category):
        self.__name = name
        self.__amount = amount
        self.__date = date
        self.__category = category

    def get_name(self):
        return self.__name

    def get_amount(self):
        return self.__amount

    def get_date(self):
        return self.__date

    def get_category(self):
        return self.__category

    def set_name(self, name):
        self.__name = name

    def set_amount(self, amount):
        self.__amount = amount

    def set_date(self, date):
        self.__date = date

    def set_category(self, category):
        self.__category = category


conn = sqlite3.connect('user.db', check_same_thread=False)

c = conn.cursor()


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


def check_users(email, password):
    k = c.execute("SELECT * FROM user")
    conn.commit()
    for row in k:
        print(row)
        if row[3] == password and row[2] == email:
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
            server.login("raymondsinglaire2@gmail.com", "G0d1sg00d")
            text = msg.as_string()
            server.sendmail(fromaddr, toaddr, text)
            return False
        else:
            return None
    return None


def change(email, new_password):
    c.execute("SELECT * FROM user")
    [print(row) for row in c.fetchall()]
    c.execute("UPDATE user SET password = (?) WHERE email = (?)", (new_password, email))
    conn.commit()
    return False


con = sqlite3.connect('savings.db', check_same_thread=False)

t = con.cursor()
#t.execute("""CREATE TABLE save (
 #             id text NOT NULL,
  #            month text NOT NULL,
   ##          actual text NOT NULL
     #         )""")


def saving_table(username, month, target, actual):
    saving = Savings(username, month, target, actual)
    t.execute('INSERT INTO save VALUES (?,?,?,?)', (saving.get_id(), saving.get_month(), saving.get_target(), saving.get_actual()))
    con.commit()
    return False


def get_data(username):
    v = t.execute('SELECT * FROM save')
    lists = []
    for row in v:
        if row[0] == username + row[1]:
            saving = Savings(username, row[1], row[2], row[3])
            lists.append(saving)
#            lists.append(row[1])
#            lists.append(row[2])
 #           lists.append(row[3])
 #           dic = {username: lists}
    return lists


def clear_savings():
    t.execute("DELETE FROM save")
    con.commit()


blogs = shelve.open('blog')


def create_blog(username, title, body):
    id = str(uuid.uuid4())
    blog = Blog(id)
    blog.title = title
    blog.username = username
    blog.body = body
    blog.created = str(date.today())
    blogs[id] = blog


def update_blog(blog):
    blogs[blog.id] = blog


def delete_blog(id):
    if id in blogs:
        del blogs[id]


def get_blogs():
    klist = list(blogs.keys())
    x = []
    for i in klist:
        x.append(blogs[i])
    return x


def get_blog(id):
    if id in blogs:
        return blogs[id]


def clear_blog():
    klist = list(blogs.keys())
    for key in klist:
        del blogs[key]


def init_db():
    clear_user()
    clear_blog()
    for i in range(5):
        create_blog('user'+str(i), 'title'+str(i), 'body'+str(i))


cnct = sqlite3.connect('finance.db', check_same_thread=False)
print('db.opened')
cur = cnct.cursor()
# cur.execute('''CREATE TABLE spent(name TEXT, amount INTEGER, date TEXT, category TEXT)''')
print('Table Initialized')


def create_cell(name, amount, date, category):
    cell = Expenses(name, amount, date, category)
    cur.execute("INSERT INTO spent VALUES (?,?,?,?)",
                (cell.get_name(), cell.get_amount(), cell.get_date(), cell.get_category()))
    cnct.commit()
    return True


def retrieve_cell():
    x = cur.execute("SELECT * FROM spent")
    if x:
        expenses = cur.fetchall()
        return expenses


def remove_cell():
    cur.execute("DELETE FROM spent")
    cnct.commit()
