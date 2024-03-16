import sqlite3



class Database:
    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file, check_same_thread=False)
        self.cursor = self.connection.cursor()

    #ДОБАВЛЕНИЕ ЮЗЕРА В БД
    def add_user(self, user_id):
        with self.connection:
            self.cursor.execute("INSERT INTO users (id, level) VALUES (?, 0)", (user_id,))
            self.connection.commit()

    def user_exists(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchall()
            return bool(len(result))

    #ИЗМЕНИТЬ НИКНЕЙМ
    def set_nickname(self, user_id, nickname):
        with self.connection:
            return self.cursor.execute("UPDATE 'users' SET 'nickname' = ? WHERE 'user_id' = ?", (nickname, user_id,))

    def get_signup(self, user_id):
        with self.connection:
            return self.cursor.execute("SELECT 'signup'")

    def get_lc(self, user_id):
        #Получения последние команды пользования
        with self.connection:
            result = self.cursor.execute("SELECT l_c FROM users WHERE id = ?", (user_id,)).fetchall()
            return str(result[0][0])


    def set_lc(self, user_id, l_c):
        with self.connection:
            self.cursor.execute("UPDATE users SET l_c = ? WHERE id = ?", (l_c, user_id,))
            self.connection.commit()

    #ФУНКЦИЯ ОБНОВЛЯЕТ ДАННЫЕ ЮЗЕРА
    def update_user(self, user_id, field, value):
        with self.connection:
            self.cursor.execute(f'UPDATE users SET {field} = ? WHERE id = ?', (value, user_id,))
            self.connection.commit()

    #ФУНКЦИЯ ВЫЗЫВАЕТ РАЗДЕЛЫ ИЗ БД
    def get_chapters(self):
        with self.connection:
            result = self.cursor.execute('SELECT id, name FROM chapter').fetchall()
            return result


    def add_chapters(self, name, sticker):
        with self.connection:
            self.cursor.execute('INSERT INTO chapter (name, sticker) VALUES (?, ?)', (name, sticker,))
            self.connection.commit()

    #ФУКЦИЯ ОТПРАВЛЯЕТ СТИКЕР ИЗ БД В РАЗДЕЛ СОФТА
    def get_chapter_sticker(self, chapter):
        with self.connection:
            result = self.cursor.execute('SELECT sticker FROM chapter WHERE id = ?', (chapter,)).fetchall()[0][0]
            return result

    #ФУНКЦИЯ ПОЛУЧАЕТ СОФТ ИЗ РАЗДЕЛА
    def get_soft(self, chapter):
        with self.connection:
            result = self.cursor.execute('SELECT message FROM soft WHERE chapter = ?', (chapter,)).fetchall()
            return result

    def get_level(self, _id):
        # -1 это бан
        # 0 юзер
        # 1 модератор
        # 2 админ
        with self.connection:
            result = self.cursor.execute('SELECT level FROM users WHERE id = ?', (_id,)).fetchall()[0][0]
            return int(result)

    #ФУНКЦИЯ МЕНЯЕТ ЮЗЕРА ЧЕРЕЗ БОТА
    def set_level(self, _id, level):
        # изменение уровня доступа
        with self.connection:
            self.cursor.execute('UPDATE users SET level = ? WHERE id = ? ', (level, _id,))
            self.connection.commit()

   #ФУНКЦИЯ ВНОСИТ СОФТ В РАЗДЕЛ
    def add_soft(self, chapter, soft, author):
        with self.connection:
            self.cursor.execute('INSERT INTO soft (chapter, author, message)  VALUES (?, ?, ?)', (chapter, author, soft,))
            self.connection.commit()










