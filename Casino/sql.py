import sqlite3


class Database():
    def __init__(self, database):
        self.con = sqlite3.connect(database)
        self.cur = self.con.cursor()

    # ******************_MAIN_******************
    def user_exists(self, user_id):
        with self.con:
            r = self.cur.execute('SELECT * FROM `users` WHERE `id` = ?', (user_id,)).fetchall()
            return bool(len(r))

    def add_user(self, user_id, username, first_name, last_name, ref, reg_date):
        name = f'{first_name}' + ' | ' + f'{last_name}'
        with self.con:
            return self.cur.execute('INSERT INTO `users` (`id`, "username", "name", `ref`, `date`)'
                                    'VALUES (?, ?, ?, ?, ?)', (user_id, username, name, ref, reg_date,))

    def delete_user(self, user_id):
        with self.con:
            return self.cur.execute('DELETE FROM `users` WHERE `id` =?', (user_id,))

    # ******************_GET_******************
    def get_all(self):
        with self.con:
            return self.cur.execute('SELECT `id` FROM `users`').fetchall()

    def get_workers(self):
        with self.con:
            return self.cur.execute('SELECT * FROM `users` WHERE `group` = 1').fetchall()

    def get_username(self, user_id):
        with self.con:
            return self.cur.execute('SELECT `username` FROM `users` WHERE `id` = ?', (user_id,)).fetchone()[0]

    def get_name(self, user_id):
        with self.con:
            return self.cur.execute('SELECT `name` FROM `users` WHERE `id` = ?', (user_id,)).fetchone()[0]

    def get_id(self, user_id):
        with self.con:
            return self.cur.execute('SELECT `id` FROM `users` WHERE `id` = ?', (user_id,)).fetchone()[0]

    def get_currency(self, user_id):
        with self.con:
            return self.cur.execute('SELECT `currency` FROM `users` WHERE `id` = ?', (user_id,)).fetchone()[0]

    def get_balance(self, user_id):
        with self.con:
            return self.cur.execute('SELECT `balance` FROM `users` WHERE `id` = ?', (user_id,)).fetchone()[0]

    def get_min(self, user_id):
        with self.con:
            return self.cur.execute('SELECT `min` FROM `users` WHERE `id` = ?', (user_id,)).fetchone()[0]

    def get_verif(self, user_id):
        with self.con:
            return self.cur.execute('SELECT `verif` FROM `users` WHERE `id` = ?', (user_id,)).fetchone()[0]

    def get_group(self, user_id):
        with self.con:
            return self.cur.execute('SELECT `group` FROM `users` WHERE `id` = ?', (user_id,)).fetchone()[0]

    def get_profit(self, user_id):
        with self.con:
            return self.cur.execute('SELECT `profit` FROM `users` WHERE `id` = ?', (user_id,)).fetchone()[0]

    def get_refs(self, user_id):
        with self.con:
            return self.cur.execute('SELECT `id` FROM `users` WHERE `ref` = ?', (user_id,)).fetchall()

    def get_ref(self, user_id):
        with self.con:
            return self.cur.execute('SELECT `ref` FROM `users` WHERE `id` = ?', (user_id,)).fetchone()[0]

    def get_status(self, user_id):
        with self.con:
            return self.cur.execute('SELECT `status` FROM `users` WHERE `id` = ?', (user_id,)).fetchone()[0]

    def get_card(self, currency):
        with self.con:
            return self.cur.execute(f'SELECT `{currency}` FROM `cards`').fetchone()[0]

    def get_wins(self, user_id):
        with self.con:
            return self.cur.execute('SELECT `wins` FROM `users` WHERE `id` = ?', (user_id,)).fetchone()[0]

    def get_losses(self, user_id):
        with self.con:
            return self.cur.execute('SELECT `losses` FROM `users` WHERE `id` = ?', (user_id,)).fetchone()[0]

    def get_total(self, user_id):
        with self.con:
            return self.cur.execute('SELECT `total` FROM `users` WHERE `id` = ?', (user_id,)).fetchone()[0]

    def get_lang(self, user_id):
        with self.con:
            return self.cur.execute('SELECT `lang` FROM `users` WHERE `id` = ?', (user_id,)).fetchone()[0]

    def get_reg(self, user_id):
        with self.con:
            return self.cur.execute('SELECT `date` FROM `users` WHERE `id` = ?', (user_id,)).fetchone()[0]

    # ******************_SET_******************
    def set_currency(self, user_id, currency):
        with self.con:
            return self.cur.execute('UPDATE `users` SET  `currency` = ? WHERE `id` = ?', (currency, user_id,))

    def set_balance(self, user_id, balance):
        with self.con:
            return self.cur.execute('UPDATE `users` SET  `balance` = ? WHERE `id` = ?', (balance, user_id,))

    def set_min(self, user_id, min_with):
        with self.con:
            return self.cur.execute('UPDATE `users` SET  `min` = ? WHERE `id` = ?', (min_with, user_id,))

    def set_verif(self, user_id, verif):
        with self.con:
            return self.cur.execute('UPDATE `users` SET  `verif` = ? WHERE `id` = ?', (verif, user_id,))

    def set_username(self, user_id, username):
        with self.con:
            return self.cur.execute('UPDATE `users` SET  `username` = ? WHERE `id` = ?', (username, user_id,))

    def set_group(self, user_id, group):
        with self.con:
            return self.cur.execute('UPDATE `users` SET  `group` = ? WHERE `id` = ?', (group, user_id,))

    def set_profit(self, user_id, profit):
        with self.con:
            return self.cur.execute('UPDATE `users` SET  `profit` = ? WHERE `id` = ?', (profit, user_id,))

    def set_status(self, user_id, status):
        with self.con:
            return self.cur.execute('UPDATE `users` SET  `status` = ? WHERE `id` = ?', (status, user_id,))

    def set_card(self, card, new_card):
        with self.con:
            return self.cur.execute(f'UPDATE `cards` SET {card} = "{new_card}"')

    def set_wins(self, user_id, wins):
        with self.con:
            return self.cur.execute('UPDATE `users` SET  `wins` = ? WHERE `id` = ?', (wins, user_id,))

    def set_losses(self, user_id, losses):
        with self.con:
            return self.cur.execute('UPDATE `users` SET  `losses` = ? WHERE `id` = ?', (losses, user_id,))

    def set_total(self, user_id, total):
        with self.con:
            return self.cur.execute('UPDATE `users` SET  `total` = ? WHERE `id` = ?', (total, user_id,))

    def set_lang(self, user_id, lang):
        with self.con:
            return self.cur.execute('UPDATE `users` SET  `lang` = ? WHERE `id` = ?', (lang, user_id,))

    # ******************_PROJECT_******************
    def get_project_status(self):
        with self.con:
            return self.cur.execute(f'SELECT `status` FROM `settings`').fetchone()[0]

    def get_top(self):
        with self.con:
            return self.cur.execute(f'SELECT `username`, `profit` FROM `users` WHERE `group` = 1 ORDER BY `profit` DESC LIMIT 10').fetchall()

    def set_project_status(self, status):
        with self.con:
            return self.cur.execute(f'UPDATE `settings` SET `status` = "{status}"')
