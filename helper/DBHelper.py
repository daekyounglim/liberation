from helper.config import Config
import psycopg2


class DBHelper:

    def __init__(self):
        self.host = Config.DATABASE_CONFIG['host']
        self.user = Config.DATABASE_CONFIG['user']
        self.password = Config.DATABASE_CONFIG['password']
        self.database = Config.DATABASE_CONFIG['database']
        self.port = Config.DATABASE_CONFIG['port']

    def __connect__(self):
        self.con = psycopg2.connect(host=self.host, user=self.user, password=self.password, database=self.database,
                                    port=self.port)
        self.cur = self.con.cursor()

    def __disconnect__(self):
        self.con.close()

    def fetch(self, sql):
        '''excute Sql Query(READ) and return List[Dictionary]'''

        self.__connect__()
        self.cur.execute(sql)
        result = self.cur.fetchall()
        self.__disconnect__()
        return result

    def execute(self, sql):
        '''excute Sql Query(CUD)'''

        self.__connect__()
        self.cur.execute(sql)
        self.con.commit()
        self.__disconnect__()

    def batch_insert(self, dict_list, table_name):
        '''excute Batch Sql Query(CUD) using List[Dictionary]'''

        self.__connect__()

        for dict in dict_list:
            cols = dict.keys()
            cols_str = ','.join(cols)
            vals = ["'" + dict[k] + "'" for k in cols]
            vals_str = ','.join(vals)

            sql = "INSERT INTO " + table_name + " ({}) VALUES ({})".format(cols_str, vals_str)
            print(sql)
            self.cur.execute(sql)

        self.con.commit()
        self.__disconnect__()

