import sqlite3


class BotDB:

    def __init__(self, UsatuBot_Database):
        self.conn = sqlite3.connect(UsatuBot_Database)
        self.cursor = self.conn.cursor()

    def user_exists(self, user_id):
        """Проверяем, есть ли юзер в базе"""
        result = self.cursor.execute("SELECT `id` FROM `users` WHERE `user_id` = ?", (user_id,))
        return bool(len(result.fetchall()))

    def get_user_id(self, user_id):
        """Достаем id юзера в базе по его user_id"""
        result = self.cursor.execute("SELECT `id` FROM `users` WHERE `user_id` = ?", (user_id,))
        return result.fetchone()[0]

    def add_user(self, user_id):
        """Добавляем юзера в базу"""
        self.cursor.execute("INSERT INTO `users` (`user_id`) VALUES (?)", (user_id,))
        return self.conn.commit()

    def add_record(self, user_id, value):
        """Создаем запись о экзамене"""
        self.cursor.execute("INSERT INTO `users_exams` (`user_id`, `user_exam`) VALUES (?, ?)", (user_id, value))
        return self.conn.commit()

    def user_exam_exists(self, user_id, value):
        """Проверяем, есть ли экзамен в базе"""
        result = self.cursor.execute("SELECT `user_exam` FROM `users_exams` WHERE `user_id` = ? AND `user_exam` = ?",
                                     (user_id, value))
        return len(result.fetchall())

    def user_exam_out(self, user_id):
        """Выводим экзамены пользователя"""
        result = []
        for row in self.cursor.execute("SELECT `user_exam` FROM `users_exams` WHERE `user_id` = ?",
                                       (user_id,)):
            result += row
        return result

    def del_record(self, user_id, value):
        """Удаляем запись о экзамене"""
        self.cursor.execute("DELETE FROM `users_exams` WHERE `user_id` = ? AND `user_exam` = ?",
                            (user_id, value))
        return self.conn.commit()

    def dir_out(self):
        """Выводим направления обучения"""
        result = []
        for row in self.cursor.execute("SELECT * FROM `directions`"):
            result += row
        return result

    def dir_exists(self, value):
        """Проверяем, есть ли направление в базе"""
        result = self.cursor.execute("SELECT `code` FROM `directions_water` WHERE `code` = ?", (value,))
        return len(result.fetchall())

    def dir_water_out(self, value):
        """Выводим информацию о направлении"""
        result = []
        for row in self.cursor.execute("SELECT `water` FROM `directions_water` WHERE `code` = ?", (value,)):
            result += row
        return result

    def dir_rec_exist(self, user_id):
        """Проверяем, есть ли направление под выбранные экзамены в базе"""
        result = self.cursor.execute("SELECT `name` FROM `directions` WHERE `exam_1` IN (SELECT `user_exam` FROM "
                                     "`users_exams` WHERE `user_id` = ?) AND `exam_2` IN (SELECT `user_exam` FROM "
                                     "`users_exams` WHERE `user_id` = ?) AND `exam_3` IN (SELECT `user_exam` FROM "
                                     "`users_exams` WHERE `user_id` = ?)", (user_id, user_id, user_id))
        return bool(len(result.fetchall()))

    def user_exam_check(self, user_id):
        """Проверяем, количество экзаменов в базе"""
        result = self.cursor.execute("SELECT `user_exam` FROM `users_exams` WHERE `user_id` = ?", (user_id,))
        return len(result.fetchall())

    def dir_rec_out(self, user_id):
        """Выводим направления обучения"""
        result = []
        for row in self.cursor.execute("SELECT * FROM `directions` WHERE `exam_1` IN (SELECT `user_exam` FROM "
                                       "`users_exams` WHERE `user_id` = ?) AND `exam_2` IN (SELECT `user_exam` FROM "
                                       "`users_exams` WHERE `user_id` = ?) AND `exam_3` IN (SELECT `user_exam` FROM "
                                       "`users_exams` WHERE `user_id` = ?)", (user_id, user_id, user_id)):
            result += row
        return result

    def about_fac_out(self):
        """Выводим информацию о факультетах"""
        result = []
        for row in self.cursor.execute("SELECT `water` FROM `about_water` WHERE `flag` = 1"):
            result += row
        return result

    def about_arm_out(self):
        """Выводим информацию о военной кафедре"""
        result = []
        for row in self.cursor.execute("SELECT `water` FROM `about_water` WHERE `flag` = 2"):
            result += row
        return result

    def about_admission(self, value):
        """Выводим необходимую информацию для раздела поступление"""
        result = []
        for row in self.cursor.execute("SELECT `water` FROM `about_water` WHERE `flag` = ?", (value,)):
            result += row
        return result

    def user_dir_flag_out(self, user_id):
        """Выводим флаг направления пользователя"""
        result = []
        for row in self.cursor.execute("SELECT `direction_flag` FROM `users` WHERE `user_id` = ?",
                                       (user_id,)):
            result += row
        return result

    def user_dir_add(self, user_id, value):
        """Изменяем флаг направления пользователя"""
        self.cursor.execute("UPDATE `users` SET `direction_flag` = ? WHERE `user_id` = ?", (value, user_id))
        return self.conn.commit()

    def user_dir_out(self, user_id):
        """Выводим направления обучения по интересам"""
        result = []
        for row in self.cursor.execute("SELECT * FROM `directions` WHERE `code` IN (SELECT `code` FROM `directions_flags` WHERE `flag` IN (SELECT `direction_flag` FROM `users` WHERE `user_id` = ?))", (user_id,)):
            result += row
        return result

    def close(self):
        """Закрываем соединение с БД"""
        self.conn.close()
