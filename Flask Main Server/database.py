from passlib.hash import pbkdf2_sha256
import pymysql

class Database:
	def __init__(self):
		host = "127.0.0.1"
		user = "root"
		password = ""
		db = "ai_tool"
		self.con = pymysql.connect(host=host, user=user, password=password, db=db, cursorclass=pymysql.cursors.
								   DictCursor,autocommit=True)
		self.cur = self.con.cursor()

	def login(self,user,password):
		self.cur.execute("SELECT * FROM user WHERE username=%s or email=%s",(user,user))
		result = self.cur.fetchone()
		try:
			if result and pbkdf2_sha256.verify(password, result["password"]):
				return True, result["id"]
			else:
				return False, -1
		except:
			return False, -1

	def register(self,user,email,password):  
		self.cur.execute("SELECT * FROM user WHERE (username=%s or email=%s) or (username=%s or email=%s)",(user,user,email,email))
		result = self.cur.fetchone()
		if result:
			return False

		try:
			password = pbkdf2_sha256.using(rounds=8000, salt_size=10).hash(password)
			self.cur.execute("INSERT INTO `user` (`username`,`email`, `password`) VALUES (%s, %s, %s)", (user,email, password))
			return True
		except:
			return False

	def list_project(self,id):
		self.cur.execute("SELECT * FROM project WHERE user_id=%s",id)
		result = self.cur.fetchall()
		return result

if __name__ == '__main__':
	db = Database()
	print(db.register("admin","admin@.com","test"))
	print(db.login("admin","admin"))