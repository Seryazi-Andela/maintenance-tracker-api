import psycopg2


class DBHandler():
    def __init__(self):
        try:
            self.conn = psycopg2.connect(
                "dbname=maintenance_tracker_db user=postgres password=seryazi")
            self.conn.autocommit = True
            self.cur = self.conn.cursor()
        except psycopg2.DatabaseError as e:
            print(e)

    def create_user_table(self):
        try:
            statement = """\
                CREATE TABLE IF NOT EXISTS users(
                userId SERIAL,
                email varchar NOT NULL UNIQUE,
                username varchar NOT NULL UNIQUE,
                user_password varchar NOT NULL,
                isadmin BOOL NOT NULL DEFAULT FALSE,
                PRIMARY KEY (userId)
                );"""
            self.cur.execute(statement)
        except psycopg2.DatabaseError as e:
            if self.conn:
                self.conn.rollback()
            raise e
        finally:
            if self.conn:
                self.conn.close

    def create_requests_table(self):
        try:
            statement = """\
                CREATE TABLE IF NOT EXISTS requests(
                requestId SERIAL,
                username varchar NOT NULL,
                header varchar NOT NULL,
                details varchar NOT NULL,
                approved BOOL NOT NULL DEFAULT FALSE,
                resolved BOOL NOT NULL DEFAULT FALSE,
                PRIMARY KEY (requestId),
                FOREIGN KEY (username) REFERENCES Users(username)
                );"""
            self.cur.execute(statement)
        except psycopg2.DatabaseError as e:
            if self.conn:
                self.conn.rollback()
            raise e
        finally:
            if self.conn:
                self.conn.close

    def create_user(self, user):
        try:
            self.cur.execute(
                "SELECT * FROM users WHERE email=%s OR username=%s", (user.email, user.username))
            existing_users = self.cur.fetchall()
            if len(existing_users) > 0:
                return False
            else:
                self.cur.execute("INSERT INTO users(email,username,user_password,isadmin) VALUES(%s,%s,%s,%s)",
                                 (user.email, user.username, user.password, user.isAdmin))
                return True
        except psycopg2.DatabaseError:
            if self.conn:
                self.conn.rollback()
        finally:
            if self.conn:
                self.conn.close

    def auth_user(self, email, password):
        try:
            self.cur.execute(
                "SELECT username, isadmin, user_password FROM users WHERE email=%s", [email])
            user = self.cur.fetchone()
            if user is None:
                return None

            userDict = {"username": user[0],
                        "isadmin": user[1], "password": user[2]}
            return userDict
        except psycopg2.DatabaseError:
            if self.conn:
                self.conn.close
        finally:
            if self.conn:
                self.conn.close

    def create_request(self, request):
        try:
            self.cur.execute("INSERT INTO requests(username,header,details,approved,resolved) VALUES(%s,%s,%s,%s,%s)",
                             (request.username, request.header, request.details, request.approved, request.resolved))
        except psycopg2.DatabaseError:
            if self.conn:
                self.conn.close
        finally:
            if self.conn:
                self.conn.close

    def get_user_requests(self, username):
        try:
            statement = "SELECT header,details,approved,resolved FROM requests WHERE username='"+username+"';"
            self.cur.execute(statement)
            rows = self.cur.fetchall()
            requestList = []
            requestDict = {}
            for row in rows:
                requestDict['header'] = row[0]
                requestDict['details'] = row[1]
                requestDict['approved'] = row[2]
                requestDict['resolved'] = row[3]
                requestList.append(requestDict)
                requestDict = {}

            return requestList
        except psycopg2.DatabaseError:
            if self.conn:
                self.conn.close
        finally:
            if self.conn:
                self.conn.close

    def get_user_request(self, username, requestid):
        try:
            self.cur.execute(
                "SELECT header,details,approved,resolved FROM requests WHERE username=%s AND requestid=%s", (username, requestid))
            req = self.cur.fetchone()
            if req is None:
                return None

            requestDict = {"header": req[0], "details": req[1],
                           "approved": req[2], "resolved": req[3]}
            return requestDict
        except psycopg2.DatabaseError:
            if self.conn:
                self.conn.close
        finally:
            if self.conn:
                self.conn.close

    def modify_user_request(self, header, details, username, requestid):
        try:
            self.cur.execute(
                "UPDATE requests SET header=%s, details=%s WHERE username=%s AND requestid=%s", (header, details, username, requestid))
            self.cur.execute(
                "SELECT header,details,approved,resolved FROM requests WHERE username=%s AND requestid=%s", (username, requestid))
            req = self.cur.fetchone()
            if req is None:
                return None
            requestDict = {"header": req[0], "details": req[1],
                           "approved": req[2], "resolved": req[3]}
            return requestDict
        except psycopg2.DatabaseError:
            if self.conn:
                self.conn
        finally:
            if self.conn:
                self.conn.close

    def get_all_user_requests(self):
        try:
            statement = "SELECT username,header,details,approved,resolved FROM requests;"
            self.cur.execute(statement)
            rows = self.cur.fetchall()
            requestList = []
            requestDict = {}
            for row in rows:
                requestDict['username'] = row[0]
                requestDict['header'] = row[1]
                requestDict['details'] = row[2]
                requestDict['approved'] = row[3]
                requestDict['resolved'] = row[4]
                requestList.append(requestDict)
                requestDict = {}

            return requestList
        except psycopg2.DatabaseError:
            if self.conn:
                self.conn.close
        finally:
            if self.conn:
                self.conn.close

    def approve_user_request(self, requestid):
        try:
            self.cur.execute(
                "UPDATE requests SET approved=%s WHERE requestid=%s", (True, requestid))
            self.cur.execute(
                "SELECT username,header,details,approved,resolved FROM requests WHERE requestid=%s", [requestid])
            req = self.cur.fetchone()
            if req is None:
                return None
            requestDict = {"username": req[0], "header": req[1], "details": req[2],
                           "approved": req[3], "resolved": req[4]}
            return requestDict
        except psycopg2.DatabaseError:
            if self.conn:
                self.conn
        finally:
            if self.conn:
                self.conn.close

    def disapprove_user_request(self, requestid):
        try:
            self.cur.execute(
                "UPDATE requests SET approved=%s WHERE requestid=%s", (False, requestid))
            self.cur.execute(
                "SELECT username,header,details,approved,resolved FROM requests WHERE requestid=%s", [requestid])
            req = self.cur.fetchone()
            if req is None:
                return None
            requestDict = {"username": req[0], "header": req[1], "details": req[2],
                           "approved": req[3], "resolved": req[4]}
            return requestDict
        except psycopg2.DatabaseError:
            if self.conn:
                self.conn.rollback()
        finally:
            if self.conn:
                self.conn.close

    def check_approval(self, requestid):
        try:
            self.cur.execute(
                "SELECT approved FROM requests WHERE requestid=%s", [requestid])
            row = self.cur.fetchone()
            return row[0]
        except psycopg2.DatabaseError:
            if self.conn:
                self.conn.rollback()
        finally:
            if self.conn:
                self.conn.close

    def resolve_user_request(self, requestid):
        try:
            self.cur.execute(
                "UPDATE requests SET resolved=%s WHERE requestid=%s", (True, requestid))
            self.cur.execute(
                "SELECT username,header,details,approved,resolved FROM requests WHERE requestid=%s", [requestid])
            req = self.cur.fetchone()
            if req is None:
                return None
            requestDict = {"username": req[0], "header": req[1], "details": req[2],
                           "approved": req[3], "resolved": req[4]}
            return requestDict
        except psycopg2.DatabaseError:
            if self.conn:
                self.conn.rollback()
        finally:
            if self.conn:
                self.conn.close()

    def delete_user(self, username):
        try:
            self.cur.execute("DELETE FROM users WHERE username=%s", [username])
        except psycopg2.DatabaseError:
            if self.conn:
                self.conn.rollback()
        finally:
            if self.conn:
                self.conn.close()
