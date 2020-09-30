import random
import re

# Импорт фраз для ответов
from resource.reflections import reflect
# Импорт замен местоимений
from resource.questions import quest

# Импорт библиотеки для пользовательского интерфейса
from tkinter import *
from tkinter.ttk import *


class Elizabeth(object):
    """
    Класс для реализации логики работы "Элизы"
    """

    def __init__(self):
        """
        Конструктор класса
        """
        # Переменная для сохранения количества пройденых вопросов.
        self.passed = -1
        keys_func = lambda x: re.compile(x[0], re.IGNORECASE)

        # Переменая для хранения ключевых фраз
        self.keys = list(map(keys_func, quest))
        # Переменная для хранения вариантов ответов
        self.values = list(map(lambda x: x[1], quest))

    def reset(self):
        self.passed = -1

    def translate(self, string, dictionary):
        """
        Функция для модификации текста по словарю.
        Аргументы:
            string: Строка текста, в которой нужно произвести замены.
            dictionary: Словарь, по которому происходят замены
        """

        # Разбивка текста на слова
        words = string.lower().split()
        # Получение списка ключей
        keys = dictionary.keys()

        # Для каждого слова проверить, входит ли оно в список словарей
        # Если входит, осуществить замену
        for i in range(len(words)):
            if words[i] in keys:
                words[i] = dictionary[words[i]]

        # Собрать строку из слов, разделяя их пробелами, и вернуть
        return " ".join(words)

    def respond(self, string):
        """
        Функция для подбора ответа по вводу пользователя
        """
        # Увеличить количество пройденых вопросов на 1
        self.passed = self.passed + 1

        # Для каждого ключа из списка ключей
        for i in range(len(self.keys)):
            # Проверить, соответствует ли входной текст ключу
            match = self.keys[i].match(string)

            if match:
                # Вибрать случайный ответ из списка ответов, который соответствует ключу
                resp = random.choice(self.values[i])

                # Если в тексте ответа содержится замена, произвести замену
                pos = resp.find("%")
                while pos > -1:
                    numb = int(resp[pos + 1:pos + 2])
                    resp = resp[:pos] + \
                           self.translate(match.group(numb), reflect) + \
                           resp[pos + 2:]
                    pos = resp.find("%")

                # Удаление лишних символов
                if resp[-2:] == "?.": resp = resp[:-2] + "."
                if resp[-2:] == "??": resp = resp[:-2] + "?"
                # Возвращение ответа
                return resp


def console_inout():
    print("Приветствуем в системе \"Элизабет\"")
    print("Пожалуйста, соблюдайте правила русского языка")

    # Создание обьекта класса "Elizabeth"
    Eliza = Elizabeth()

    # Переменная для хранения пользовательского ввода
    s = ""

    # Продолжать пока не будет введено одна из комманд для вихода
    while not s in ["Выход", "Exit", "exit", "выход"]:
        # Запросить у пользователя строку текста
        s = input("> ")

        # Если ничего не введено, то пропустить 1 итерацию цикла
        if s == "": continue

        # Удалить определенные знаки из конца строки
        while s[-1] in "!.":
            s = s[:-1]

        # Вывести реакцию на введенный пользователем текст
        print(Eliza.respond(s))

    # В зависимости от количества пройденых вопросов вывести сообщение с количеством пройденых вопросов
    if Eliza.passed < 10:
        print(f"Пережито вопросов: {Eliza.passed}. Не очень.")
    else:
        print(f"Пережито вопросов: {Eliza.passed}. Успех.")


def tkinter_app():
    Eliza = Elizabeth()

    root = Tk()

    root.title("Элизабет")

    frame = Frame(root)

    Label(frame, text="Приветствуем в системе \"Элизабет\"\nПожалуйста, соблюдайте правила русского языка", justify=CENTER).pack()

    entry_str_var = StringVar()

    group_chat = LabelFrame(frame, text=u"Сообщения")
    group_chat.pack(side=TOP, fill=BOTH, expand=True, padx=5, pady=5)

    scrollbar = Scrollbar(group_chat)
    text = Text(group_chat, width=40, height=15, wrap=WORD, yscrollcommand=scrollbar.set)

    btn_send = Button(frame, text=u"Отправить")

    ent = Entry(frame, textvariable=entry_str_var)
    ent.pack(side=TOP, fill=X, padx=5, pady=5)
    ent.focus()

    def onSubmit():
        value = entry_str_var.get()

        if len(value) == 0:
            return

        respond = Eliza.respond(value)

        text.config(state=NORMAL)

        line = u"#{}\n> {}\n< {}\n".format(Eliza.passed, value, respond)

        text.insert(END, line)

        text.config(state=DISABLED)

        text.see(END)

        entry_str_var.set("")

    def onClick(event):
        onSubmit()

    btn_send.bind("<Button-1>", onClick)
    btn_send.pack(side=TOP, fill=X, padx=5, pady=5)

    text["state"] = DISABLED
    text.pack(side=LEFT, fill=BOTH, expand=True, padx=5, pady=5)

    scrollbar.pack(side=RIGHT, fill=Y)
    scrollbar.config(command=text.yview)

    btn_reset = Button(frame, text=u"Заново")

    def reset():
        text.config(state=NORMAL)

        text.delete(1.0, END)

        text.config(state=DISABLED)

        Eliza.reset()

    def onBtnResetClick(event):
        reset()

    btn_reset.bind("<Button-1>", onBtnResetClick)
    btn_reset.pack(side=TOP, fill=BOTH, padx=5, pady=5)

    frame.pack(fill=BOTH, expand=True)

    def onReturn(event):
        onSubmit()

    root.bind("<Return>", onReturn)

    reset()

    root.mainloop()


if __name__ == "__main__":
    tkinter_app()
