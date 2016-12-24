import os
from supportmethods import support_supply as supply
from log import log_main

log = log_main.Log(100, "log/html_pages_log.txt")

def show_page_homepage(self, param_dict):

    supply.add_intro_html(self, 'Home page', 'Home page')
    supply.add_outro_html(self)

def show_page_ftp(self, param_dict):

    supply.add_intro_html(self,'File page','Welcome to this file upload page')

    self.wfile.write('<center>'
                     '<br>'
                     '<br>'
                     '<form method="post" enctype="multipart/form-data">'
                     '<input type="file" name="upload_file" multiple>'
                     '<br>'
                     '<br>'
                     '<p>'
                     'Input folder name'
                     '</p>'
                     '<input type="text" name="folder_name">'
                     '<br>'
                     '<br>'
                     '<input type="hidden" value="upload_file" name="task">'
                     '<input type="submit" value="upload files" name="submit">'
                     '</form>')

    self.wfile.write('<p>***</p>'
                     '<form method="post" enctype="multipart/form-data" id="remove">'
                     '<input type="hidden" value="remove_file" name="task">'
                     '<input type="submit" value="remove files" name="submit">'
                     '</center>'
                     '<br>')

    self.wfile.write('<center>'
                     '<table>'
                     '<th>'
                     'id'
                     '</th>'
                     '<th>'
                     'date'
                     '</th>'
                     '<th>'
                     'file name'
                     '</th>'
                     '<th>'
                     'file type'
                     '</th>'
                     '<th>'
                     'file path'
                     '</th>'
                     '<th>'
                     'Checkbox'
                     '</th>')


    counter = 0

    for param_dict_file in self.db.fetch_files():

        self.wfile.write('<tr>'
                         '<td>'
                         + str(param_dict_file["id"])+
                         '</td>'
                         '<td>'
                         + str(param_dict_file["date"])+
                         '</td>'
                         '<td>'
                         + str(param_dict_file["file_name"])+
                         '</td>'
                         '<td>'
                         + str(param_dict_file["file_type"])+
                         '</td>'
                         '<td>'
                         + str(param_dict_file["file_path"])+
                         '</td>'
                         '<td>'
                         '<input type="checkbox" name="id_'
                         + str(counter) +
                         '" value="'
                         + str(param_dict_file["id"]) +
                         '" form="remove">'
                         '</td>'
                         '</tr>')
        counter += 1

    self.wfile.write('</center>'
                     '</table>'
                     '<br>')

    supply.add_outro_html(self)

def show_page_note(self, param_dict):

    supply.add_intro_html(self, 'Note page', 'Welcome to this note display page')

    self.wfile.write('<center>'
                     '<br>'
                     '<br>'
                     '<form method="post" enctype="multipart/form-data">'
                     '<p>'
                     'Input note'
                     '</p>'
                     '<input type="text" name="note">'
                     '<br>'
                     '<br>'
                     '<input type="hidden" value="upload_note" name="task">'
                     '<input type="submit" value="add note" name="submit">'
                     '</form>')

    self.wfile.write('<p>***</p>'
                     '<form method="post" enctype="multipart/form-data" id="note">'
                     '<input type="hidden" value="remove_note" name="task">'
                     '<input type="submit" value="remove note" name="submit">'
                     '</center>'
                     '<br>')

    self.wfile.write('<center>'
                     '<table>'
                     '<th>'
                     'id'
                     '</th>'
                     '<th>'
                     'date'
                     '</th>'
                     '<th>'
                     'message'
                     '</th>'
                     '<th>'
                     'Checkbox'
                     '</th>')

    counter = 0

    try:

        notes = self.db.fetch_notes()

    except Exception as e:

        log.bug("html_pages",'Unable to fetch notes')
        supply.add_error_html(self, "Unable to fetch notes", e)
        return

    for param_dict_note in notes:

        self.wfile.write('<tr>'
                         '<td>'
                         + str(param_dict_note["id"]) +
                         '</td>'
                         '<td>'
                         + str(param_dict_note["date"]) +
                         '</td>'
                         '<td>'
                         + str(param_dict_note["message"]) +
                         '</td>'
                         '<td>'
                         '<input type="checkbox" name="id_'
                         + str(counter) +
                         '" value="'
                         + str(param_dict_note["id"]) +
                         '" form="note">'
                         '</td>'
                         '</tr>')
        counter += 1

    self.wfile.write('</center>'
                     '</table>'
                     '<br>')

    supply.add_outro_html(self)

def show_page_wiki(self, param_dict):

    supply.add_intro_html(self, 'Wiki page', 'Welcome to this wiki page')

    self.wfile.write('<a href="' + self.url + '?page=wiki&text=test1">test1</a><br>')
    if dict(param_dict).has_key("text") and param_dict["text"][0] == "test1":
        with open("wiki_text/text1.txt","r") as text:
            for line in text:
                self.wfile.write('&nbsp&nbsp&nbsp&nbsp' + line + '<br>')
    self.wfile.write('<a href="' + self.url + '/?page=wiki&text=test2">test2</a><br>')
    if dict(param_dict).has_key("text") and param_dict["text"][0] == "test2":
        with open("wiki_text/text2.txt","r") as text:
            for line in text:
                self.wfile.write('&nbsp&nbsp&nbsp&nbsp' + line + '<br>')

    with open('wiki_text/refs','r') as references:

        for ref in references:
            self.wfile.write('<a href="' + self.url + '/?page=wiki&text=' +  ref.split("/")[-1] +  '">' + ref.split("/")[-1] + '</a><br>')

            if dict(param_dict).has_key("text") and str(param_dict["text"][0]).strip() == str(ref.split("/")[-1]).strip():

                with open(ref.strip(), "r") as text:
                    print ref
                    for line in text:
                        self.wfile.write('&nbsp&nbsp&nbsp&nbsp' + line + '<br>')

    supply.add_outro_html(self)

def show_page_about(self, param_dict):

    supply.add_intro_html(self, 'About page', 'Welcome to this about page')
    supply.add_outro_html(self)

def show_page_debug(self, param_dict):

    supply.add_intro_html(self, 'Debug page', 'Welcome to this debug page')

    for files in os.listdir("log"):

        if ".txt" in files:

            self.wfile.write('<p>'
                             'Log file: '
                             + files +
                             '</p>')

            with open('log/' + files,"rb") as log_file:

                for line in log_file.readlines():

                    self.wfile.write(line + '<br>')

                self.wfile.write('<br>')


    supply.add_outro_html(self)
