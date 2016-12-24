import cgi
import os
from log import log_main
import urlparse
import magic

from urlparse import urlparse, parse_qs

log = log_main.Log(100, "log/support_parse_log.txt")

def parse_GET(self):

    param_dict = parse_qs(urlparse(self.path).query)

    return param_dict


def parse_POST(self):

    file_dict = dict()
    param_dict = dict()

    form = cgi.FieldStorage(
        fp=self.rfile,
        headers=self.headers,
        environ={'REQUEST_METHOD': 'POST',
                 'CONTENT_TYPE': self.headers['Content-Type'],
                 })

    try:

        for field in form.keys():
            field_item = form[field]

            if not isinstance(field_item, list):

                if field_item.filename:

                    file_dict[field_item.filename] = field_item.file.read()

                else:

                    param_dict[field] = form[field].value

            else:

                for field_item_sub in field_item:

                    if field_item_sub.filename:
                        file_dict[field_item_sub.filename] = field_item_sub.file.read()

        if param_dict.has_key('folder_name'):

            folder = param_dict["folder_name"]

            for file_name in file_dict:

                if not os.path.isdir(self.store_path):
                    os.makedirs(self.store_path)

                if not os.path.isdir(self.store_path + '/' + folder):
                    os.makedirs(self.store_path + '/' + folder)

                try:

                    with open(self.store_path + '/' + folder + '/' + file_name, 'wb') as store_file:

                        store_file.write(file_dict[file_name])

                except Exception as e:

                    log.bug("main", "Unable to write to file")
                    raise e

                file_path = self.store_path + '/' + folder

                mime = magic.Magic(mime=True)

                file_type = mime.from_file(self.store_path + '/' + folder + '/' + file_name)

                try:

                    self.db.insert_file(file_name, file_path, file_type)

                except Exception as e:

                    log.bug("Unable to save to database")
                    raise e

                # Begin HTML page

    except Exception as e:

        raise e

    return (param_dict, file_dict)