from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMessageBox, QApplication, QWidget, QPushButton, QListWidget, QLineEdit, QTextEdit, QLabel, QHBoxLayout, QVBoxLayout, QInputDialog


def show_note(): 
    '''Показывает текст и теги выбранной заметки в виджетах'''   
    name = list_notes.selectedItems()[0].text()
    note_txt.clear()
    list_tags.clear()
    for note in notes:
        if note[0] == name:
            if len(note) > 1:
                note_txt.setText(note[1])
            if len(note) > 2:
                list_tags.addItems(note[2])


def add_note():
    '''Запрашивает название новой заметки и добавляет новую пустую заметку с таким именем'''
    note_name, result = QInputDialog.getText(main_win, 'Добавить замету', 'Название заметки:')
    if note_name != '' and result:
        note = [note_name, '', []]
        notes.append(note)
        list_notes.addItem(note[0])
        note_txt.clear()
        list_tags.clear()
        filename = str(len(notes) - 1) + '.txt'
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(note[0] + '\n')
        #notes[note_name] = {'текст': '', 'теги': []}
        #list_notes.addItem(note_name)
        #list_tags.addItems(notes[note_name]['теги'])


def del_notes():
    '''Удаляет заметку из словарика'''
    if list_notes.selectedItems():
        delet = list_notes.selectedItems()[0].text()
        del notes[delet]
        with open('notes_data.json', 'w', encoding='utf-8') as file:
            json.dump(notes, file, sort_keys=True, ensure_ascii=False, indent=4)
        note_txt.clear()
        list_notes.clear()
        list_tags.clear()
        list_notes.addItems(notes)
    else:
        add_window = QMessageBox()
        add_window.setText('Вы не выбрали заметку!')
        add_window.exec_()


def save_notes():
    '''Сохраняет заметку в словарик'''
    if list_notes.selectedItems():
        save = list_notes.selectedItems()[0].text()
        text_save = note_txt.toPlainText()
        name_list = 0
        for note in notes:
            if note[0] == save:
                if len(note) > 1:
                    note[1] = text_save
                else:
                    note.append(text_save)
                with open(str(name_list) + '.txt', 'w', encoding='utf-8') as file:
                    file.write(note[0] + '\n')
                    file.write(note[1] + '\n')
                    if len(note) > 2:
                        for tag in note[2]:
                            file.write(tag + ' ')
                        file.write('\n')
            else:
                name_list += 1
    else:
        add_window = QMessageBox()
        add_window.setText('Вы не выбрали заметку!')
        add_window.exec_()


def add_tags():
    '''Добавляет тег в заметку'''
    if list_notes.selectedItems():
        add = list_notes.selectedItems()[0].text()
        tag = write_tag.text()
        if tag != '' and not tag in notes[add]['теги']:
            notes[add]['теги'].append(tag)
            list_tags.addItem(tag)
            write_tag.clear()
            with open('notes_data.json', 'w', encoding='utf-8') as file:
                json.dump(notes, file, sort_keys=True, ensure_ascii=False, indent=4)


def del_tags():
    '''Удаляет тег у выбранной заметки'''
    if list_notes.selectedItems():
        del_note = list_notes.selectedItems()[0].text()
        tag_name = list_tags.selectedItems()[0].text()
        notes[del_note]['теги'].remove(tag_name)
        list_tags.clear()
        list_tags.addItems(notes[del_note]['теги'])
        with open('notes_data.json', 'w', encoding='utf-8') as file:
            json.dump(notes, file, sort_keys=True, ensure_ascii=False, indent=4)


def search_tag():
    '''Ищет заметки у которых есть введённый тег'''
    if button_find.text() == 'Искать заметки по тегу':
        tag_ = write_tag.text()
        if tag_ != '':
            notes_filtered = {}
            for note in notes:
                if tag_ in notes[note]['теги']:
                    notes_filtered[note] = notes[note]
            button_find.setText('Сбросить поиск')
            list_notes.clear()
            list_tags.clear()
            list_notes.addItems(notes_filtered)
    elif button_find.text() == 'Сбросить поиск':
        list_notes.clear()
        list_tags.clear()
        write_tag.clear()
        list_notes.addItems(notes)
        button_find.setText('Искать заметки по тегу')


app = QApplication([])
main_win = QWidget()
main_win.setWindowTitle('Умные заметки')
main_win.resize(900, 600)

button_make = QPushButton('Создать заметку')
button_delet = QPushButton('Удалить заметку')
button_save = QPushButton('Сохранить заметку')
button_add = QPushButton('Добавить к заметке')
button_unpin = QPushButton('Открепить от заметки')
button_find = QPushButton('Искать заметки по тегу')
note_txt = QTextEdit()
write_tag = QLineEdit()
write_tag.setPlaceholderText('Введите тег...')
list_notes = QListWidget()
list_tags = QListWidget()
label_notes = QLabel('Список заметок')
label_tags = QLabel('Список тегов')

h1_main = QHBoxLayout()
v1_sec = QVBoxLayout()
v2_sec = QVBoxLayout()
h2 = QHBoxLayout()
h3 = QHBoxLayout()

v1_sec.addWidget(note_txt)
v2_sec.addWidget(label_notes)
v2_sec.addWidget(list_notes)
h2.addWidget(button_make)
h2.addWidget(button_delet)
v2_sec.addLayout(h2)
v2_sec.addWidget(button_save)
v2_sec.addWidget(label_tags)
v2_sec.addWidget(list_tags)
v2_sec.addWidget(write_tag)
h3.addWidget(button_add)
h3.addWidget(button_unpin)
v2_sec.addLayout(h3)
v2_sec.addWidget(button_find)
h1_main.addLayout(v1_sec, stretch = 2)
h1_main.addLayout(v2_sec, stretch = 1)
main_win.setLayout(h1_main)

note_name = 0
notes = []

while True:
    filename = str(note_name) + '.txt'
    note = []
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            for line in file:
                discard = line.replace('\n', '')
                note.append(discard)
            if len(note) > 2: 
                tags = note[2].split(' ')
                note[2] = tags
        notes.append(note)
        note_name += 1
    except IOError:
        break

print(notes)

for note in notes:
    list_notes.addItem(note[0])
list_notes.itemClicked.connect(show_note)
button_make.clicked.connect(add_note)
button_delet.clicked.connect(del_notes)
button_save.clicked.connect(save_notes)
button_add.clicked.connect(add_tags)
button_unpin.clicked.connect(del_tags)
button_find.clicked.connect(search_tag)

main_win.show()
app.exec_()