from PyQt5.QtCore import Qt, QFile, QTextStream 
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QListWidget, QLineEdit, QTextEdit, QInputDialog, QHBoxLayout, QVBoxLayout, QFormLayout
import json
from PyQt5.QtGui import QFont, QPalette, QColor

app = QApplication([])


'''Заметки в json'''
notes = {
    "Добро пожаловать!": {
        "текст": "Это самое лучшее приложение для заметок в мире!",
        "теги": ["добро", "инструкция"]
    }
}

with open("notes_data.json", "w", encoding="utf-8") as file:
    json.dump(notes, file, ensure_ascii=False)

'''Интерфейс приложения'''
# параметры окна приложения
notes_win = QWidget()
notes_win.setWindowTitle('Умные заметки')
notes_win.resize(900, 600)
font = QFont("Segoe UI", 10)
app.setFont(font)
# виджеты окна приложения
list_notes = QListWidget()
list_notes_label = QLabel('Список заметок')
button_note_create = QPushButton('Создать заметку')
button_note_del = QPushButton('Удалить заметку')
button_note_save = QPushButton('Сохранить заметку')
field_tag = QLineEdit('')
field_tag.setPlaceholderText('Введите тег...')
field_text = QTextEdit()
button_tag_add = QPushButton('Добавить к заметке')
button_tag_del = QPushButton('Открепить от заметки')
button_tag_search = QPushButton('Искать заметки по тегу')
list_tags = QListWidget()
list_tags_label = QLabel('Список тегов')

# Подключаем стили из файла style.qss
file = QFile("styles/main_style.qss")  # Используем QFile из QtCore
if file.open(QFile.ReadOnly | QFile.Text):
    stream = QTextStream(file)
    stream.setCodec("UTF-8")  # Устанавливаем кодировку для русского текста
    app.setStyleSheet(stream.readAll())
    file.close()

# расположение виджетов по лэйаутам
layout_notes = QHBoxLayout()
col_1 = QVBoxLayout()
col_1.addWidget(field_text)

col_2 = QVBoxLayout()
col_2.addWidget(list_notes_label)
col_2.addWidget(list_notes)

row_1 = QHBoxLayout()
row_1.addWidget(button_note_create)
row_1.addWidget(button_note_del)

row_2 = QHBoxLayout()
row_2.addWidget(button_note_save)

col_2.addLayout(row_1)
col_2.addLayout(row_2)
col_2.addWidget(list_tags_label)
col_2.addWidget(list_tags)
col_2.addWidget(field_tag)

row_3 = QHBoxLayout()
row_3.addWidget(button_tag_add)
row_3.addWidget(button_tag_del)

row_4 = QHBoxLayout()
row_4.addWidget(button_tag_search)

col_2.addLayout(row_3)
col_2.addLayout(row_4)

layout_notes.addLayout(col_1, stretch=2)
layout_notes.addLayout(col_2, stretch=1)
notes_win.setLayout(layout_notes)

'''Функционал приложения'''
def CreateNotes():
    windowDialog, ok = QInputDialog.getText(notes_win, "Создание заметки", "Введите имя заметки:")
    if ok and windowDialog:
        # Создаем новую заметку
        notes[windowDialog] = {"текст": "", "теги": []}
        list_notes.addItem(windowDialog)
def del_note():
    '''Удаляет выбранную заметку из словаря notes,
    из файла и из виджетов'''

    
    
def show_note():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        field_text.setText(notes[key]["текст"])
        list_tags.clear()
        list_tags.addItems(notes[key]["теги"])

'''Запуск приложения'''
# подключение обработки событий
button_note_create.clicked.connect(CreateNotes)
list_notes.itemClicked.connect(show_note)

# загружаем заметки
try:
    with open("notes_data.json", "r", encoding="utf-8") as file:
        notes = json.load(file)
        list_notes.addItems(notes.keys())
except FileNotFoundError:
    pass

notes_win.show()
app.exec_()