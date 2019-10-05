import pymysql

class SaveDataBase:

    @staticmethod
    def save(data):
        with pymysql.connect("localhost", "root", "1234567", "nuc_stu") as pdb:
            pdb.execute(f'INSERT INTO student'
                        f'(stu_name,stu_id, id_cade, sex, place, high_school, gk_id, mingzu )'
                        f' VALUES ('
                           f'{repr(data["name"])},'
                           f'{repr(data["id"])},'
                           f'{repr(data["idcode"])},'
                           f'{repr(data["sex"])},'
                           f'{repr(data["place"])},'
                           f'{repr(data["highschool"])},'
                           f'{repr(data["gkid"])},'
                           f'{repr(data["mingzu"])})'
                        )



if __name__ == '__main__':
    ss = {'name': ' **',
          'id': ' ******102',
          'idcode': '14232***********',
          'sex': '女',
          'place': '山西********',
          'highschool': '太原*******',
          'gkid': ' 8*********7',
          'mingzu': '**'
          }
    s = SaveDataBase()
    s.save(ss)