from log import log_main

log = log_main.Log(100, "log/support_supply_log.txt")

def add_intro_html(self, title, headline):

    self.send_response(200)
    self.send_header("Content-type", "text/html")
    self.end_headers()
    add_css(self)

    self.wfile.write('<ul>'
                     '<li><a class="active" href="/' + self.url + '">Home</a></li>'
                     '<li><a href="/' + self.url + '?page=file">Files</a></li>'
                     '<li><a href="/' + self.url + '?page=note">Note</a></li>'
                     '<li><a href="/' + self.url + '?page=wiki">Wiki</a></li>'
                     '<li><a href="/' + self.url + '?page=about">About</a></li>'
                     '<li><a href="/' + self.url + '?page=debug">Debug</a></li>'
                     '</ul>')

    self.wfile.write("<html>"
                     "<head>"
                     "<title>"
                     + title +
                     "</title>"
                     "</head>"
                     "<body>"
                     "<center>"
                     '<h1>'
                     + headline +
                     '</h1>'
                     '</center>')


def add_outro_html(self):


    if self.headers.has_key('Referer') and not self.headers['Referer'] == None:

        referer = self.headers['Referer']

    else:

        referer = '/' + self.url

    self.wfile.write('<center>'
                    '<a href="'
                     + referer +
                     '">back</a>'
                     '</center>''</body>'
                     '</html>')

def add_error_html(self, message, e = "No internal message"):

    self.send_response(200)
    self.send_header("Content-type", "text/html")
    self.end_headers()
    add_css(self)

    if not self.headers.has_key('Referer') and self.headers['Referer'] == None:

        referer = self.headers['Referer']

    else:

        referer = '/' + self.url

    self.wfile.write('<html>'
                     '<head>'
                     '<title>'
                     'Error'
                     '</title>'
                     '</head>'
                     '<body>'
                     '<center>'
                     '<h1>'
                     'Failed to upload files'
                     '</h1>'
                     '<p>'
                     'Message: '
                     + str(e) +
                     '</p>'
                     '<a href="'
                     + referer +
                     '">back</a>'
                     '</center>'
                     '</body>'
                     '</html>')

def add_error_mid_html(self, message, e = "No internal message"):

    self.wfile.write('<center>'
                     '<h1>'
                     'Failed to upload files'
                     '</h1>'
                     '<p>'
                     'Message: '
                     + str(e) +
                     '</p>'
                     '</center>'
                     '<a href="/'
                     + self.url +
                     '">back</a>'
                     '</body>'
                     '</html>')


def add_css(self):

    with open('css/style.css', 'rb') as css_file:

        self.wfile.write(css_file.read())

