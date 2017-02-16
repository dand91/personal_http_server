#!/usr/bin/python

import BaseHTTPServer
from sql import sql_main
from log import log_main

from pages import html_pages
from pages import html_tasks
from supportmethods import support_parse as parse
from supportmethods import  support_supply as supply

log = log_main.Log(100, "log/main_log.txt")

class HTTP_Handler(BaseHTTPServer.BaseHTTPRequestHandler):

    # def do_HEAD(s):
    #     """
    #     Overridden method for receiving and answering HTTP HEAD
    #     """
    #
    #     s.send_response(200)
    #     s.send_header("Content-type", "text/html")
    #     s.end_headers()

    def do_POST(self):
        """
        Overridden method for receiving and answering HTTP POST
        """

        try:

            result = parse.parse_POST(self)

        except Exception as e:

            log.bug("main","Unable to do POST parsing")
            supply.add_error_html(self, "Unable to do POST parsing",e)
            return

        param_dict = result[0]
        file_dict = result[1]

        print(str(param_dict))

        if param_dict.has_key("task") and param_dict["task"] == "upload_file":

            html_tasks.show_task_upload_file(self, param_dict, file_dict)

        elif param_dict.has_key("task") and param_dict["task"] == "upload_note":

            html_tasks.show_task_upload_note(self, param_dict, file_dict)

        elif param_dict.has_key("task") and param_dict["task"] == "remove_file":

            html_tasks.show_task_remove_file(self, param_dict, file_dict)

        elif param_dict.has_key("task") and param_dict["task"] == "remove_note":

            html_tasks.show_task_remove_note(self, param_dict, file_dict)

    def do_GET(self):

        """
        Overridden method for receiving and answering HTTP GET
        """

        try:

            param_dict = parse.parse_GET(self)

        except Exception as e:

            log.bug("main","Unable to do GET parsing")
            supply.add_error_html(self, "Unable to do GET parsing", e)
            return

        print(str(param_dict))

        if param_dict.has_key("page") and param_dict["page"][0] == "wiki":

            html_pages.show_page_wiki(self, param_dict)

        elif param_dict.has_key("page") and param_dict["page"][0] == "about":

            html_pages.show_page_about(self, param_dict)

        elif param_dict.has_key("page") and param_dict["page"][0] == "file":

            html_pages.show_page_ftp(self, param_dict)

        elif param_dict.has_key("page") and param_dict["page"][0] == "note":

            html_pages.show_page_note(self, param_dict)

        elif param_dict.has_key("page") and param_dict["page"][0] == "debug":

            html_pages.show_page_debug(self, param_dict)

        else:

            html_pages.show_page_homepage(self, param_dict)



if __name__ == '__main__':


    Handler = HTTP_Handler

    try:

        Handler.db = sql_main.Database()
        
    except Exception as e:
        
        log.err("main","Unable to start database")

    port_nbr = 1443

    Handler.store_path = "store_dir"
    Handler.url = "pi"

    httpd = BaseHTTPServer.HTTPServer(("", port_nbr), Handler)

    log.bug("main","Starting HTTP server at port: ", port_nbr)

    httpd.serve_forever()
