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
    ss = {'name': ' 杨楠',
          'id': ' 1807004102',
          'idcode': '142329200004092327',
          'sex': '女',
          'place': '山西省吕梁市岚县',
          'highschool': '太原北辰双语学校',
          'gkid': ' 8140107151667',
          'mingzu': '汉族'
          }
    s = SaveDataBase()
    s.save(ss)