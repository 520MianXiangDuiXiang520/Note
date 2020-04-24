class DisplayTable:
    @staticmethod
    def get_table(order_dict: dict, foods: set):
        table = []
        foods = sorted(foods)
        head = ["Table"]
        for i in foods:
            head.append(i)
        table.append(head)
        tables = [int(i) for i in order_dict.keys()]
        tables.sort()
        for no in tables:
            food = order_dict.get(str(no))
            this_table = [str(no)]
            for i in foods:
                this_table.append(str(food.get(i, 0)))
            table.append(this_table)
        return table


    def displayTable(self, orders: list) -> list:
        order_dict = {}
        foods = set()
        for order in orders:
            table = order_dict.setdefault(order[1], {})
            food = table.get(order[2])
            foods.add(order[2])
            if food:
                table[order[2]] += 1
            else:
                table[order[2]] = 1
        print(order_dict)
        return self.get_table(order_dict, foods)


if __name__ == '__main__':
    order = [["Laura","2","Bean Burrito"],["Jhon","2","Beef Burrito"],["Jhon","2","Aeef Burrito"],["Melissa","2","Soda"]]
    print(DisplayTable().displayTable(order))
