import random

from resource.reflections import reflect
from resource.questions import quest

from tkinter import *
from tkinter.ttk import *


class Elizabeth(object):
    def __init__(self):
        self.passed = -1
        keys_func = lambda x: re.compile(x[0], re.IGNORECASE)

        self.keys = list(map(keys_func, quest))
        self.values = list(map(lambda x: x[1], quest))

    def reset(self):
        self.passed = -1

    def translate(self, string, dictionary):
        words = string.lower().split()
        keys = dictionary.keys()

        for i in range(len(words)):
            if words[i] in keys:
                words[i] = dictionary[words[i]]

        return " ".join(words)

    def respond(self, string):
        self.passed = self.passed + 1

        for i in range(len(self.keys)):
            match = self.keys[i].match(string)

            if match:
                resp = random.choice(self.values[i])

                pos = resp.find("%")
                while pos > -1:
                    numb = int(resp[pos + 1:pos + 2])
                    resp = resp[:pos] + \
                           self.translate(match.group(numb), reflect) + \
                           resp[pos + 2:]
                    pos = resp.find("%")

                if resp[-2:] == "?.": resp = resp[:-2] + "."
                if resp[-2:] == "??": resp = resp[:-2] + "?"

                return resp


def tkinter_app():
    Eliza = Elizabeth()

    root = Tk()

    root.title("Чат")
    root.geometry("500x400")
    root.resizable(False, False)

    frame = Frame(root)

    entry_str_var = StringVar()

    group_chat = PanedWindow(frame)
    group_chat.pack(side=TOP, fill=BOTH, expand=True, padx=5, pady=5)

    scrollbar = Scrollbar(group_chat)
    text = Text(group_chat, width=40, height=15, wrap=WORD, yscrollcommand=scrollbar.set)

    btn_send = Button(frame, text=u"Отправить")
    btn_send.pack(side=RIGHT, fill=X, padx=5, pady=5)

    ent = Entry(frame, textvariable=entry_str_var)
    ent.pack(side=RIGHT, expand=True, fill=X, padx=5, pady=5)
    ent.focus()

    def onSubmit():
        value = entry_str_var.get()

        if len(value) == 0:
            return

        respond = Eliza.respond(value)

        text.config(state=NORMAL)

        line = u"{}: {}\n\t{}\n".format(Eliza.passed, value, respond)

        text.insert(END, line)

        text.config(state=DISABLED)

        text.see(END)

        entry_str_var.set("")

    def onClick(event):
        onSubmit()

    btn_send.bind("<Button-1>", onClick)

    text["state"] = DISABLED
    text.pack(side=LEFT, fill=BOTH, expand=True, padx=5, pady=5)

    scrollbar.pack(side=RIGHT, fill=Y)
    scrollbar.config(command=text.yview)

    def reset():
        text.config(state=NORMAL)

        text.delete(1.0, END)

        text.config(state=DISABLED)

        Eliza.reset()

    frame.pack(fill=BOTH, expand=True)

    def onReturn(event):
        onSubmit()

    root.bind("<Return>", onReturn)

    reset()

    root.mainloop()


if __name__ == "__main__":
    tkinter_app()
