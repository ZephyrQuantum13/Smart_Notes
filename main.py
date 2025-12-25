from PyQt5.QtCore import Qt, QFile, QTextStream 
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QListWidget, QLineEdit, QTextEdit, QInputDialog, QHBoxLayout, QVBoxLayout, QFormLayout, QMessageBox
import json
from PyQt5.QtGui import QFont, QPalette, QColor

app = QApplication([])

'''Заметки в json'''
try:
    with open("notes_data.json", "r", encoding="utf-8") as file:
        notes = json.load(file)
except FileNotFoundError:
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
        # Проверяем, существует ли уже заметка с таким именем
        if windowDialog in notes:
            QMessageBox.warning(notes_win, "Ошибка", "Заметка с таким именем уже существует!")
            return
            
        # Создаем новую заметку
        notes[windowDialog] = {"текст": "", "теги": []}
        list_notes.addItem(windowDialog)
        list_notes.setCurrentRow(list_notes.count() - 1)
        
        # Сохраняем в файл
        with open("notes_data.json", "w", encoding="utf-8") as file:
            json.dump(notes, file, ensure_ascii=False)

def del_note():
    '''Удаляет выбранную заметку из словаря notes,
    из файла и из виджетов'''
    if list_notes.selectedItems():
        # Получаем выбранную заметку
        selected_note = list_notes.selectedItems()[0]
        note_name = selected_note.text()
        
        # Удаляем из словаря
        if note_name in notes:
            del notes[note_name]
        
        # Удаляем из виджета
        list_notes.takeItem(list_notes.row(selected_note))
        
        # Очищаем поля
        field_text.clear()
        list_tags.clear()
        field_tag.clear()
        
        # Сохраняем изменения в файл
        with open("notes_data.json", "w", encoding="utf-8") as file:
            json.dump(notes, file, ensure_ascii=False)
    else:
        QMessageBox.warning(notes_win, "Ошибка", "Не выбрана заметка для удаления")

def save_note():
    '''Сохраняем текст в выбранную заметку
    из словаря notes и обновляет файл с данными'''
    if list_notes.selectedItems():
        name_note = list_notes.selectedItems()[0].text()
        text_note = field_text.toPlainText()
        
        # Сохраняем текст в структуре заметки
        if name_note in notes:
            notes[name_note]["текст"] = text_note
        
            with open("notes_data.json", "w", encoding="utf-8") as file:
                json.dump(notes, file, ensure_ascii=False)
    else:
        QMessageBox.warning(notes_win, "Ошибка", "Не выбрана заметка для сохранения")

def show_note():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        field_text.setText(notes[key]["текст"])
        list_tags.clear()
        list_tags.addItems(notes[key]["теги"])

def add_tag():
    if list_notes.selectedItems() and field_tag.text(): # Проверяем выбрана ли заметка и тег
        
        note_name = list_notes.selectedItems()[0].text() # Получаем имя заметки 
        tag = field_tag.text() # Получаем название тега
        
        if note_name in notes: # Проверяем есть ли имя заметки в списке заметок
            if tag not in notes[note_name]["теги"]: # Если тега нет в списке 
                notes[note_name]["теги"].append(tag) # то добавляем тег в список тегов у этой заметки
                list_tags.addItem(tag) # Добавляем тег в виджет списка
                field_tag.clear() # Очищаем поле ввода
                '''Сохраняем изменения'''
                with open("notes_data.json", "w", encoding="utf-8") as file:
                    json.dump(notes, file, ensure_ascii=False)

def del_tag():
    if list_notes.selectedItems() and list_tags.selectedItems(): # Проверка выбор заметки и тега
        note_name = list_notes.selectedItems()[0].text() # Получаем имя заметки
        tag_name = list_tags.selectedItems()[0].text() # Получаем название тега
        
        if note_name in notes and tag_name in notes[note_name]["теги"]:
            
            notes[note_name]["теги"].remove(tag_name) # Удаляем тег из списка
            list_tags.takeItem(list_tags.row(list_tags.selectedItems()[0])) # Удаляем тег из виджета списка
            '''Сохраняем изменения'''
            with open("notes_data.json", "w", encoding="utf-8") as file:
                json.dump(notes, file, ensure_ascii=False)

def search_tag():
    #Функция для поиска заметок по тегу 
    tag = field_tag.text() # Получаем текс тега
    if tag: #если строчка не пустая
        filtered_notes = {} # Создание словаря для отфильтрованных заметок
        for note_name, note_data in notes.items():
            # Если наш тег есть note_data["теги"]
            if tag in note_data["теги"]:

                filtered_notes[note_name] = note_data #Добавляем заметку в результат
                
        '''Обновляем интерфейс'''
        list_notes.clear() # Очищаем список тегов
        list_tags.clear() # Очищаем список тегов 
        field_text.clear() # Очищаем текс заметки
        list_notes.addItems(filtered_notes.keys()) # Добавляем список найденных заметок                                      
    else:
        # Если поле для ввода тегов пустое 
        list_notes.clear() # Очищаем  виджет ссписка
        list_notes.addItems(notes.keys()) # Добавляем все имена заметок

'''Запуск приложения'''
# подключение обработки событий
button_note_create.clicked.connect(CreateNotes)
list_notes.itemClicked.connect(show_note)
button_note_del.clicked.connect(del_note)
button_note_save.clicked.connect(save_note)
button_tag_add.clicked.connect(add_tag)
button_tag_del.clicked.connect(del_tag)
button_tag_search.clicked.connect(search_tag)

# загружаем заметки
list_notes.addItems(notes.keys())

notes_win.show()
app.exec_()