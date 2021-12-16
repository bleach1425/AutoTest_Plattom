# import json
# import xml.etree.ElementTree as etree

### Abstract Factory 抽象工廠: 解決複雜對象創建問題 ###

# class JSONConnector:
#     def __init__(self, filepath):
#         self.data = dict()
#         with open(filepath, mode='r', encoding='utf8') as f:
#             self.data = json.load(f)

#     def parsed_data(self):
#         print(self.data)


# class XMLConnector:
#     def __init__(self, filepath):
#         self.tree = etree.parse(filepath)

#     def parsed_data(self):
#         print(self.data)


# def connection_factory(filepath):
#     """ 工厂方法 """
#     if filepath.endswith('json'):
#         connector = JSONConnector
#     elif filepath.endswith('xml'):
#         connector = XMLConnector
#     else:
#         raise ValueError('Cannot connect to {}'.format(filepath))
#     return connector(filepath)

# connection_factory('./trash.json').parsed_data())


###  2.The Builder Pattern 建構模式: 控制複雜對象的構造 ###

# class Frog:
#     def __init__(self, name):
#         self.name = name

#     def __str__(self):
#         return self.name

#     def interact_with(self, obstacle):
#         """ 不同类型玩家遇到的障碍不同 """
#         print('{} the Frog encounters {} and {}!'.format(
#             self, obstacle, obstacle.action()))


# class Bug:
#     def __str__(self):
#         return 'a bug'

#     def action(self):
#         return 'eats it'


# class FrogWorld:
#     def __init__(self, name):
#         print(self)
#         self.player_name = name

#     def __str__(self):
#         return '\n\n\t----Frog World -----'

#     def make_character(self):
#         return Frog(self.player_name)

#     def make_obstacle(self):
#         return Bug()


# class Wizard:
#     def __init__(self, name):
#         self.name = name

#     def __str__(self):
#         return self.name

#     def interact_with(self, obstacle):
#         print('{} the Wizard battles against {} and {}!'.format(
#             self, obstacle, obstacle.action()))


# class Ork:
#     def __str__(self):
#         return 'an evil ork'

#     def action(self):
#         return 'kill it'


# class WizardWorld:
#     def __init__(self, name):
#         print(self)
#         self.player_name = name

#     def __str__(self):
#         return '\n\n\t------ Wizard World -------'

#     def make_character(self):
#         return Wizard(self.player_name)

#     def make_obstacle(self):
#         return Ork()


# class GameEnvironment:
#     """ 抽象工厂，根据不同的玩家类型创建不同的角色和障碍 (游戏环境)
#     这里可以根据年龄判断，成年人返回『巫师』游戏，小孩返回『青蛙过河』游戏"""
#     def __init__(self, factory):
#         self.hero = factory.make_character()
#         self.obstacle = factory.make_obstacle()

#     def play(self):
#         self.hero.interact_with(self.obstacle)


# # GameEnvironment先選一個遊戲(factory)以及設定一名玩家, class裡面的make_character()
# # 再從hero and obstacle class當初去取得使用者名稱及情境, make_obstacle()取得 GameEnvironment的hero、obstacle

# def main():
#     game = GameEnvironment(WizardWorld('Player1'))
#     game.play()

# main()


### 3.The Prototype Pattern(原型模式:解決對象拷貝問題) ###

# import copy
# from collections import OrderedDict

# class Book:
#     def __init__(self, name, authors, price, **rest):
#         '''Examples of rest: publisher, length, tags, publication
#         date'''
#         self.name = name
#         self.authors = authors
#         self.price = price      # in US dollars
#         self.__dict__.update(rest)

#     def __str__(self):
#         mylist = []
#         ordered = OrderedDict(sorted(self.__dict__.items()))
#         for i in ordered.keys():
#             mylist.append('{}: {}'.format(i, ordered[i]))
#             if i == 'price':
#                 mylist.append('$')
#             mylist.append('\n')
#         return ''.join(mylist)


# class Prototype:
#     def __init__(self):
#         self.objects = {}

#     def register(self, identifier, obj):
#         self.objects[identifier] = obj

#     def unregister(self, identifier):
#         del self.objects[identifier]

#     def clone(self, identifier, **attr):
#         """ 实现对象拷贝 """
#         found = self.objects.get(identifier)
#         if not found:
#             raise ValueError('Incorrect object identifier: {}'.format(identifier))
#         obj = copy.deepcopy(found)
#         obj.__dict__.update(attr)    # 实现拷贝时自定义更新
#         return obj


# def main():
#     b1 = Book('The C Programming Language', ('Brian W. Kernighan', 'Dennis M.Ritchie'),
#             price=118, publisher='Prentice Hall', length=228, publication_date='1978-02-22',
#             tags=('C', 'programming', 'algorithms', 'data structures'))
#     prototype = Prototype()
#     cid = 'k&r-first'
#     prototype.register(cid, b1)
#     # print(prototype.objects['k&r-first'])
#     b2 = prototype.clone(cid, name='The C Programming Language (ANSI)', price=48.99, length=274,
#                         publication_date='1988-04-01', edition=2)
#     for i in (b1, b2):
#         print(i)
#         print("ID b1 : {} != ID b2 : {}".format(id(b1), id(b2)))

# main()



### 4. The Adapter Pattern(是配器模式:解決接口不兼容問題) ###
# class Computer:
#     def __init__(self, name):
#         self.name = name

#     def __str__(self):
#         return 'the {} computer'.format(self.name)

#     def execute(self):
#         """ call by client code """
#         return 'execute a program'


# class Synthesizer:
#     def __init__(self, name):
#         self.name = name

#     def __str__(self):
#         return 'the {} synthesizer'.format(self.name)

#     def play(self):
#         return 'is playing an electroinc song'


# class Human:
#     def __init__(self, name):
#         self.name = name

#     def __str__(self):
#         return 'the {} human'.format(self.name)

#     def speak(self):
#         return 'says hello'


# class Adapter:
#     def __init__(self, obj, adapted_methods):
#         """ 不使用继承，使用__dict__属性实现适配器模式 """
#         self.obj = obj
#         self.__dict__.update(adapted_methods)

#     def __str__(self):
#         return str(self.obj)


# # 适配器使用示例
# def main():
#     objs = [Computer('Asus')]
#     synth = Synthesizer('moog')
#     objs.append(Adapter(synth, dict(execute=synth.play)))
#     human = Human('Wnn')
#     objs.append(Adapter(human, dict(execute=human.speak)))

#     for o in objs:
#         # 用统一的execute适配不同对象的方法，这样在无需修改源对象的情况下就实现了不同对象方法的适配
#         print('{} {}'.format(str(o), o.execute()))


# if __name__ == "__main__":
#     main()


### 5. The Decorator Pattern 裝飾器 ###
# from functools import wraps

# def memoize(fn):
#     known = dict()

#     @wraps(fn)
#     def memoizer(*args):
#         if args not in known:
#             print('args: ', args)
#             print('fn(*args): ', fn(*args))
#             known[args] = fn(*args)
#         return known[args]
#     return memoizer


# @memoize
# def fibonacci(n):
#     assert(n >= 0), 'n must be >= 0'
#     return n if n in (0, 1) else fibonacci(n-1) + fibonacci(n-2)

# def main():
#     print(fibonacci(15))

# main()


#6. ### The Facade Pattern(外觀模式) ###

# import abc
# from abc import ABCMeta, abstractmethod, ABC
# from enum import Enum

# State = Enum('State', 'new running sleeping restart zombie')


# class Server(metaclass=ABCMeta):
#     """ 抽象基类 """
#     @abstractmethod
#     def __init__(self):
#         pass

#     def __str__(self):
#         return self.name

#     @abstractmethod
#     def boot(self):
#         pass

#     @abstractmethod
#     def kill(self, restart=True):
#         pass


# class FileServer(Server):
#     def __init__(self):
#         '''actions required for initializing the file server'''
#         self.name = 'FileServer'
#         self.state = State.new

#     def boot(self):
#         print('booting the {}'.format(self))
#         '''actions required for booting the file server'''
#         self.state = State.running

#     def kill(self, restart=True):
#         print('Killing {}'.format(self))
#         '''actions required for killing the file server'''
#         self.state = State.restart if restart else State.zombie

#     def create_file(self, user, name, permissions):
#         '''check validity of permissions, user rights, etc.'''
#         print("trying to create the file '{}' for user '{}' with permissions {}".format(name, user, permissions))

# class ProcessServer(Server):
#     def __init__(self):
#         '''actions required for initializing the process server'''
#         self.name = 'ProcessServer'
#         self.state = State.new

#     def boot(self):
#         print('booting the {}'.format(self))
#         '''actions required for booting the process server'''
#         self.state = State.running

#     def kill(self, restart=True):
#         print('Killing {}'.format(self))
#         '''actions required for killing the process server'''
#         self.state = State.restart if restart else State.zombie

#     def create_process(self, user, name):
#         '''check user rights, generate PID, etc.'''
#         print("trying to create the process '{}' for user '{}'".format(name, user))


# class OperatingSystem:
#     ''' 实现外观模式，外部使用的代码不必知道 FileServer 和 ProcessServer的
#     内部机制，只需要通过 OperatingSystem类调用'''
#     def __init__(self):
#         self.fs = FileServer()
#         self.ps = ProcessServer()

#     def start(self):
#         """ 被客户端代码使用 """
#         [i.boot() for i in (self.fs, self.ps)]

#     def create_file(self, user, name, permissions):
#         return self.fs.create_file(user, name, permissions)

#     def create_process(self, user, name):
#         return self.ps.create_process(user, name)

# def main():
#     os = OperatingSystem()
#     os.start()
#     os.create_file('foo', 'hello', '-rw-r-r')
#     os.create_process('bar', 'ls /tmp')

# main()



# 7. The Flyweight Pattern(享元模式: 線对象复用从而改善资源使用)
# import random
# from enum import Enum
# TreeType = Enum('TreeType', 'apple_tree cherry_tree peach_tree')


# class Tree:
#     pool = dict()

#     def __new__(cls, tree_type):
#         obj = cls.pool.get(tree_type, None)
#         if obj is None:
#             obj = object.__new__(cls)
#             cls.pool[tree_type] = obj
#             obj.tree_type = tree_type
#         return obj

#     def render(self, age, x, y):
#         print('render a tree of type {} and age {} at ({}, {})'.format(self.tree_type, age, x, y))


# def main():
#     rnd = random.Random()
#     age_min, age_max = 1, 30    # in years
#     min_point, max_point = 0, 100
#     tree_counter = 0

#     for _ in range(10):
#         t1 = Tree(TreeType.apple_tree)
#         t1.render(rnd.randint(age_min, age_max),
#                 rnd.randint(min_point, max_point),
#                 rnd.randint(min_point, max_point))
#         tree_counter += 1

#     for _ in range(3):
#         t2 = Tree(TreeType.cherry_tree)
#         t2.render(rnd.randint(age_min, age_max),
#                 rnd.randint(min_point, max_point),
#                 rnd.randint(min_point, max_point))
#         tree_counter += 1

#     for _ in range(5):
#         t3 = Tree(TreeType.peach_tree)
#         t3.render(rnd.randint(age_min, age_max),
#                 rnd.randint(min_point, max_point),
#                 rnd.randint(min_point, max_point))
#         tree_counter += 1

#     print('trees rendered: {}'.format(tree_counter))
#     print('trees actually created: {}'.format(len(Tree.pool)))
#     t4 = Tree(TreeType.cherry_tree)
#     t5 = Tree(TreeType.cherry_tree)
#     t6 = Tree(TreeType.apple_tree)
#     print('{} == {}? {}'.format(id(t4), id(t5), id(t4) == id(t5)))
#     print('{} == {}? {}'.format(id(t5), id(t6), id(t5) == id(t6)))


# if __name__ == '__main__':
#     main()


# 8. The Model-View-Controller Pattern
# quotes = ('A man is not complete until he is married. Then he is finished.',
#         'As I said before, I never repeat myself.',
#         'Behind a successful man is an exhausted woman.',
#         'Black holes really suck...', 'Facts are stubborn things.')


# class QuoteModel:
#     def get_quote(self, n):
#         try:
#             return quotes[n]
#         except IndexError:
#             return 'Not found'


# class QuoteTerminalView:

#     def show(self, quote):
#         print('And the quote is: "{}"'.format(quote))

#     def error(self, msg):
#         print('Error: {}'.format(msg))

#     def select_quote(self):
#         return input('Which quote number would you like to see? ')



# class QuoteTerminalController:
#     def __init__(self):
#         self.model = QuoteModel()
#         self.view = QuoteTerminalView()

#     def run(self):
#         valid_input = False
#         while not valid_input:
#             n = self.view.select_quote()
#             try:
#                 n = int(n)
#             except ValueError:
#                 self.view.error("Incorrect index '{}'".format(n))
#             else:
#                 valid_input = True
#                 quote = self.model.get_quote(n)
#                 self.view.show(quote)


# def main():
#     controller = QuoteTerminalController()
#     while True:
#         controller.run()

# main()


### 9: The Proxy Pattern(代理模式：通過一層間接保護層實現更安全的接口訪問） ###

# class LazyProperty:
#     """ 用描述符实现延迟加载的属性 """
#     def __init__(self, method):
#         self.method = method
#         self.method_name = method.__name__

#     def __get__(self, obj, cls):
#         if not obj:
#             return None
#         value = self.method(obj)
#         print('value {}'.format(value))
#         setattr(obj, self.method_name, value)
#         return value


# class Test:
#     def __init__(self):
#         self.x = 'foo'
#         self.y = 'bar'
#         self._resource = None

#     @LazyProperty
#     def resource(self):    # 构造函数里没有初始化，第一次访问才会被调用
#         print('initializing self._resource which is: {}'.format(self._resource))
#         self._resource = tuple(range(5))    # 模拟一个耗时计算
#         return self._resource


# def main():
#     t = Test()
#     print(t.x)
#     print(t.y)
#     # 访问LazyProperty, resource里的print语句只执行一次，实现了延迟加载和一次执行
#     print('1', t.resource)
#     print('2', t.resource)


# main()

###  延遲及一次執行範例 ###
# class Circle(object):
#     def __init__(self, radius):
#         self.radius = radius

#     @property 
#     def area(self):
#         return 3.14 * self.radius ** 2

# c = Circle(4)
# print(c.radius)
# print(c.area)


# class lazy(object):
#     def __init__(self, func):
#         self.func = func

#     def __get__(self, instance, cls):
#         val = self.func(instance)
#         print(instance, self.func.__name__, val)
#         setattr(instance, self.func.__name__, val)
#         return val

# class Circle(object):
#     def __init__(self, radius):
#         self.radius = radius

#     @lazy # area = lazy(area)
#     def area(self):
#         print('-')
#         return 3.14 * self.radius ** 2

# c = Circle(4)
# print(c.radius)
# print('*'*10)
# print(c.__dict__)
# print(c.area)
# print(c.__dict__)
# print('*'*10)
# print(c.area)
# print(c.area)


# class SensitiveInfo:
#     def __init__(self):
#         self.users = ['nick', 'tom', 'ben', 'mike']

#     def read(self):
#         print('There are {} users: {}'.format(len(self.users), ' '.join(self.users)))

#     def add(self, user):
#         self.users.append(user)
#         print('Added user {}'.format(user))


# class Info:
#     '''protection proxy to SensitiveInfo'''
#     def __init__(self):
#         self.protected = SensitiveInfo()
#         # 为了方便示例这里直接写死在代码里，为了安全不应该这么做
#         self.secret = '0xdeadbeef'

#     def read(self):
#         self.protected.read()

#     def add(self, user):
#         """ 给add操作加上密钥验证，保护add操作"""
#         sec = input('what is the secret? ')
#         self.protected.add(user) if sec == self.secret else print("That's wrong!")


# def main():
#     info = Info()
#     while True:
#         print('1. read list |==| 2. add user |==| 3. quit')
#         key = input('choose option: ')
#         if key == '1':
#             info.read()
#         elif key == '2':
#             name = input('choose username: ')
#             info.add(name)
#         elif key == '3':
#             exit()
#         else:
#             print('unknown option: {}'.format(key))
# main()

### 10: The Chain of Responsibility Pattern(責任鍊模式: 創建鍊式對象用來接收廣播消息) ###

class Event:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name


class Widget:
    """Docstring for Widget. """

    def __init__(self, parent=None):
        self.parent = parent

    def handle(self, event):
        handler = 'handle_{}'.format(event)
        if hasattr(self, handler):
            method = getattr(self, handler)
            method(event)
        elif self.parent:
            self.parent.handle(event)
        elif hasattr(self, 'handle_default'):
            self.handle_default(event)


class MainWindow(Widget):
    def handle_close(self, event):
        print('MainWindow: {}'.format(event))

    def handle_default(self, event):
        print('MainWindow: Default {}'.format(event))


class SendDialog(Widget):
    def handle_paint(self, event):
        print('SendDialog: {}'.format(event))


class MsgText(Widget):
    def handle_down(self, event):
        print('MsgText: {}'.format(event))


def main():
    mw = MainWindow()
    sd = SendDialog(mw)    # parent是mw
    msg = MsgText(sd)

    for e in ('down', 'paint', 'unhandled', 'close'):
        evt = Event(e)
        print('\nSending event -{}- to MainWindow'.format(evt))
        mw.handle(evt)
        print('Sending event -{}- to SendDialog'.format(evt))
        sd.handle(evt)
        print('Sending event -{}- to MsgText'.format(evt))
        msg.handle(evt)

if __name__ == "__main__":
    main()