import cgi, json, MySQLdb, passwords, random, webapp2

class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        self.response.write("Hello!")
        conn = MySQLdb.connect(
			unix_socket = passwords.SQL_HOST,
			user = passwords.SQL_USER,
			passwd = passwords.SQL_PASSWD,
			db = user)

		cursor_1 = conn.cursor()

		cursor_1.execute('SELECT * FROM details')
		res = cursor_1.fetchall()

		json = json.dumps([{'ID': p[0], 'Name': p[1]} for p in res], indent = 2)

		cursor_1.close()

		cookie = self.request.cookies.get('cookie1')

		if cookie is None:
			id = '%032x' % random.getrandbits(128)
			self.response.set_cookie('cookie1', id, maxage = 1800)
			self.response.write(cookie)

			cursor_2 = conn.cursor()
            cursor_2.execute("INSERT INTO session (ID, USERNAME) VALUES(%s,%s);", (id, ""))

			self.response.write("""
			<html>
			<head>
			<title>Form</title>
			</head>
            <body>
                <form action="https://gaelab-259221.appspot.com/" method="get">
	                <input type="text" name=USERNAME value=""><br>
                    <input type=submit><br/>
                </form>
       		</body>
            </html>
            """)

			cursor_3 = conn.cursor()
			USERNAME = self.request.get('USERNAME')
			cursor3.execute("UPDATE session SET USERNAME=% WHERE ID=%;", (USERNAME,id))
            self.response.write(USERNAME)
			cursor_3.close()
			conn.commit()
			conn.close()
		else:
			self.response.write(cookie)

		self.response.write("""
		<html>
		<head>
		<title>Increment Link Page</title>
		</head>
		<body>
			<a href='https://gaelab-259221.appspot.com'>Increment Page</a>
		</body>
		</html>
		""")
app = webapp2.WSGIApplication([("/", MainPage),], debug=True)
