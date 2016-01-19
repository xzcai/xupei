class Person(object):
    address = '江西'  # 类属性 相当于静态变量


    def __init__(self, name, gender, birth):
        self.name = name
        self.gender = gender
        self.birth = birth
        self.__wealth = '12000'  # 相当于私有变量

    # 实例方法
    def get_test(self):
        return self.name, self.gender, self.birth, self.__wealth

    # 静态方法
    @classmethod
    def how_many(cls):
        return cls.address

    def __pri(self):
        pass
