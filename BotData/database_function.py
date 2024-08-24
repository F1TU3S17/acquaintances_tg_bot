import sqlite3 as sq
db = sq.connect('BotData/database.db')
cur = db.cursor()
async def db_start():
    cur.execute('''CREATE TABLE IF NOT EXISTS users (
                tg_id INTEGER PRIMARY KEY,
                username TEXT,
                is_active INTEGER DEFAULT 0,
                name TEXT,
                age INTEGER,
                sex INTEGER,
                interest INTEGER,
                description TEXT,
                photo BLOB)
                ''')

    cur.execute('''CREATE TABLE IF NOT EXISTS location (
                tg_id INTEGER PRIMARY KEY,
                search_priority INTEGER DEFAULT 0,
                city TEXT,
                state TEXT,
                region TEXT,
                country TEXT)
                ''')

    cur.execute('''CREATE TABLE IF NOT EXISTS likes (
                    from_id INTEGER,
                    to_id INTEGER,
                    message TEXT)
                    ''')

    cur.execute('''CREATE TABLE IF NOT EXISTS reports (
                    tg_id INTEGER PRIMARY KEY,
                    message TEXT)
                    ''')
    cur.execute('''CREATE TABLE IF NOT EXISTS admins(
            tg_id INTEGER PRIMARY KEY)
                ''')
    db.commit()

async def users_list():
    users = cur.execute('SELECT tg_id FROM users').fetchall()
    user_list = [i[0] for i in users]
    return user_list
async def id_to_db(tg_id):
    cur.execute('SELECT COUNT(*) FROM users WHERE tg_id = ?', (tg_id,))
    exists = cur.fetchone()[0]
    if not exists:
        cur.execute('INSERT INTO users(tg_id) VALUES (?)',(tg_id,))
        db.commit()

async def check_id(tg_id):
    cur.execute('SELECT COUNT(*) FROM users WHERE tg_id = ?', (tg_id,))
    exists = cur.fetchone()[0]
    if exists:
        return True
    return False


async def photo_to_db(tg_id, photo):
    #cur.execute('SELECT * FROM users WHERE tg_id = ? and photo IS NULL', (tg_id,))
    #exists = cur.fetchone()[0]
    photo_bytes = photo.read()
    cur.execute('UPDATE users set photo = ? WHERE tg_id = ?', (photo_bytes, tg_id))
    db.commit()

async def all_info_to_db(tg_id, name, username, photo, age, sex, description, interest):
    if photo != None:
        photo_bytes = photo.read()
        cur.execute('UPDATE users set photo = ?, name = ?, username = ?, age = ?, sex = ?,'
                    'description = ?, interest = ? WHERE tg_id = ?',
                    (photo_bytes, name, username,age, sex, description, interest, tg_id))
    else:
        cur.execute('UPDATE users set name = ?, username = ?, age = ?, sex = ?,'
                    'description = ?, interest = ? WHERE tg_id = ?',
                    (name, username, age, sex, description, interest, tg_id))
    db.commit()


async def del_form(tg_id):
    cur.execute('DELETE FROM users WHERE tg_id = ?',(tg_id,))
    cur.execute('DELETE FROM location WHERE tg_id = ?',(tg_id, ))
    db.commit()


async def update_active(tg_id, active):
    cur.execute('UPDATE users set is_active = ? WHERE tg_id = ?',(active, tg_id))

def get_active(tg_id):
    active = cur.execute('SELECT is_active FROM users WHERE tg_id = ?',(tg_id,)).fetchone()
    return active[0]
#Фунция для записи локации пользователя в базу данных
async def location_to_db(tg_id, city, state, region, country):
    location = cur.execute('SELECT * FROM location WHERE tg_id = ?',(tg_id,)).fetchone()
    if location:
        cur.execute('UPDATE location set city = ?, state = ?, region = ?, country = ? WHERE tg_id = ?',
                    (city, state, region, country, tg_id))
    else:
        cur.execute('INSERT INTO location (tg_id, city, state, region, country) VALUES(?,?,?,?,?)',
                    (tg_id, city, state, region, country))
    db.commit()

#Функция для получения всей информации о пользователе
async def get_all_info(tg_id):
    query = '''
            SELECT 
                users.*, 
                location.city, location.state, location.region, location.country 
            FROM 
                users
            INNER JOIN 
                location ON users.tg_id = location.tg_id
            WHERE 
                users.tg_id = ?
            '''
    all_info = cur.execute(query, (tg_id,)).fetchone()
    if all_info:
        info_list = list(all_info)
        return info_list
    return None

#Функция для получения возраста пользователя
def get_age(tg_id):
    age = cur.execute('SELECT age FROM users WHERE tg_id == ?',(tg_id,)).fetchone()
    if age:
        return age[0]
    return None

#Функция для получения названия населенного пункта пользователя
def get_city(tg_id):
    city = cur.execute('SELECT city FROM location WHERE tg_id == ?', (tg_id,)).fetchone()
    if city:
        return city[0]
    return None

def get_photo(tg_id):
    cur.execute('SELECT photo FROM users WHERE tg_id = ?', (tg_id,))
    photo = cur.fetchone()
    if photo is None:
        return None
    return photo[0]


def get_username(tg_id):
    cur.execute('SELECT username FROM users WHERE tg_id = ?', (tg_id,))
    username = cur.fetchone()
    if username is None:
        return None
    return username[0]

def get_description(tg_id):
    cur.execute('SELECT description FROM users WHERE tg_id = ?', (tg_id,))
    description = cur.fetchone()
    if description is None:
        return None
    return description[0]

def get_sex(tg_id):
    sex = cur.execute('SELECT sex FROM users WHERE tg_id = ?',(tg_id,)).fetchone()
    if sex:
        return sex[0]
    return None

async def update_name(tg_id, name):
    cur.execute('UPDATE users set name = ? WHERE tg_id = ?',(name, tg_id))
    db.commit()

async def update_age(tg_id, age):
    cur.execute('UPDATE users set age = ? WHERE tg_id = ?',(age, tg_id))
    db.commit()

async def update_sex(tg_id, sex):
    cur.execute('UPDATE users set sex = ? WHERE tg_id = ?',(sex, tg_id))
    db.commit()

async def update_description(tg_id, description):
    cur.execute('UPDATE users set description = ? WHERE tg_id = ?',(description, tg_id))
    db.commit()

async def update_interest(tg_id, interest):
    cur.execute('UPDATE users set interest = ? WHERE tg_id = ?', (interest, tg_id))
    db.commit()

async def update_search_priority(tg_id, search_priority):
    cur.execute('UPDATE location set search_priority = ? WHERE tg_id = ?', (search_priority, tg_id))
    db.commit()

async def get_search_priority(tg_id):
    search_priority = cur.execute('SELECT search_priority FROM location WHERE tg_id = ?',
                                 (tg_id, )).fetchone()
    if search_priority:
        return search_priority[0]
    return None


async def get_partner(tg_id, limit=20, offset=0):
    index_sex = get_sex(tg_id)
    index_search_priority = await get_search_priority(tg_id)
    location_list = ['city', 'state', 'region', 'country']
    age = get_age(tg_id)
    age_min = age - 4
    age_max = age + 4
    partners = cur.execute(f'''
                SELECT users.tg_id
                FROM users
                JOIN location 
                ON users.tg_id = location.tg_id
                WHERE ((users.interest == ? OR users.interest == 2) 
                    AND (location.{location_list[index_search_priority]} == (SELECT {location_list[index_search_priority]} FROM location WHERE tg_id = ?))
                    AND (location.search_priority == ?) AND (users.is_active == 1) AND (users.age >= {age_min} AND users.age <= {age_max}))
                ORDER BY users.tg_id DESC
                LIMIT ? OFFSET ?
                ''', (index_sex, tg_id, index_search_priority, limit, offset)).fetchall()

    partners_list = [i[0] for i in partners if i[0] != tg_id]

    return partners_list


async def like_to_db(from_id, to_id, message=None):
    cur.execute('INSERT INTO likes values(?,?,?)',(from_id, to_id, message))
    if message != None:
        cur.execute('UPDATE likes SET message = ? WHERE from_id = ? AND to_id = ? ',(message, from_id, to_id))
    db.commit()

async def like_counts(to_id):
    count_like = cur.execute('SELECT count(from_id) FROM likes WHERE to_id = ?',(to_id,)).fetchone()
    if count_like:
        return count_like[0]
    return None

async def like_list(user_id, limit=20, offset=0):
    likes = cur.execute('SELECT from_id FROM likes WHERE to_id = ? LIMIT ? OFFSET ?',
                        (user_id, limit, offset)).fetchall()
    likes_list = [i[0] for i in likes]
    return likes_list

async def message_to_user(from_id, to_id):
    message = cur.execute('SELECT message FROM likes WHERE from_id = ? and to_id = ?', (from_id, to_id)).fetchone()
    if message:
        return message[0]
    return None


async def del_like(from_id, to_id):
    cur.execute('DELETE FROM likes WHERE from_id = ? AND to_id = ?',(from_id, to_id))
    db.commit()


async def check_admin(tg_id):
    admin = cur.execute('SELECT tg_id FROM admins WHERE tg_id = ?',(tg_id,)).fetchone()
    if admin:
        return True
    return False

async def send_report(tg_id, message):
    cur.execute('INSERT INTO reports VALUES(?,?)',(tg_id, message))
    db.commit()

async def f_report():
    first_report = cur.execute('SELECT * FROM reports').fetchone()
    if first_report:
        return list(first_report)
    else:
        return []

async def del_report(tg_id, message, del_form=False):
    if not(del_form):
        cur.execute('DELETE FROM reports WHERE tg_id = ? AND message = ?',(tg_id, message))
    else:
        cur.execute('DELETE FROM reports WHERE tg_id = ?',(tg_id,))
    db.commit()
