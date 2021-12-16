class Work:
    def __init__(self, cursor, sorted_by, sorted_, min_, max_):
        self.cursor = cursor
        if sorted_by and sorted_:
            self.sorted_by = sorted_by
            self.sorted = sorted_
        if min_ and max_:
            self.min = min_
            self.max = max_
    def judge_columns(self):
        if self.sorted_by == 'price':
            if self.sorted == 'up':
                self.cursor.execute('SELECT * FROM `commodity` ORDER BY `price`')
                data = self.cursor.fetchall()
                return data       
            else:
                self.cursor.execute('SELECT * FROM `commodity` ORDER BY `price` DESC')
                data = self.cursor.fetchall()
                return data
        elif self.sorted_by == 'popular':
            pass

    def min_max_search(self):
        self.cursor.execute(f'SELECT * FROM `commodity` WHERE `price` BETWEEN {self.min} AND {self.max}')
        data = self.cursor.fetchall()
        return data

    def min_max_after_judge(self):
        if self.sorted == 'up':
            self.cursor.execute(f'SELECT * FROM `commodity` WHERE `price` BETWEEN {self.min} AND {self.max} ORDER BY `price`')
            data = self.cursor.fetchall()
            return data
        else:
            self.cursor.execute(f'SELECT * FROM `commodity` WHERE `price` BETWEEN {self.min} AND {self.max} ORDER BY `price` DESC')
            data = self.cursor.fetchall()
            return data