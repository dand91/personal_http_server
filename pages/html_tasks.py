from log import log_main
from supportmethods import support_supply as supply

import cgi

log = log_main.Log(100, "html_tasks_log.txt")

def show_task_upload_file(self, param_dict, file_dict):

    if len(file_dict) == 0:

        supply.add_error_html(self, "Select file(s)")


    else:

        supply.add_intro_html(self,'FTP result page', 'File upload complete')

        self.wfile.write('<br>'
                         '<br>'
                         '<center>'
                         '<p>')
        for files in file_dict:

            self.wfile.write('Saved file: ' + str(files) + '<br>')

        self.wfile.write('<center>'
                         '</p>')

        supply.add_outro_html(self)

def show_task_upload_note(self, param_dict, file_dict):

    supply.add_intro_html(self,'Note result page', 'Note upload complete')

    self.wfile.write('<br>'
                     '<br>'
                     '<center>'
                     '<p>')

    for param in param_dict:

        print(param)
        if param == "note":

            input = cgi.escape(str(param_dict[param])) # TODO kolla upp metodnamn

            try:
                self.db.insert_note(input)
            except Exception as e:
                log.bug("html_tasks", 'Unable to save notes',e)
                supply.add_error_html(self,"Unable to save note",e)
                return
            self.wfile.write('Saved note: ' + str(input) + '<br>')

    self.wfile.write('<center>'
                     '</p>')

    supply.add_outro_html(self)

def show_task_remove_file(self,param_dict,file_dict):

    for param in param_dict:

        if 'id' in param:

            self.db.remove_file(param_dict[param])

    supply.add_intro_html(self,'Remove result page', 'Removal complete')

    self.wfile.write('<br>'
                     '<br>'
                     '<center>'
                     '<p>')

    for param in param_dict:

        if 'id' in param:

            self.wfile.write('Removed file with id: ' + str(param_dict[param]) + '<br>')

    self.wfile.write('<center>'
                     '</p>')

    supply.add_outro_html(self)

def show_task_remove_note(self,param_dict,file_dict):

    for param in param_dict:

        if 'id' in param:

            self.db.remove_note(param_dict[param])

    supply.add_intro_html(self,'Remove result page', 'Removal complete')

    self.wfile.write('<br>'
                     '<br>'
                     '<center>'
                     '<p>')

    for param in param_dict:

        if 'id' in param:

            self.wfile.write('Removed note with id: ' + str(param_dict[param]) + '<br>')

    self.wfile.write('<center>'
                     '</p>')

    supply.add_outro_html(self)
