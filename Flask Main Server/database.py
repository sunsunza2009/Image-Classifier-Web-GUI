from passlib.hash import pbkdf2_sha256
import pymysql

class Database:
	def __init__(self):
		host = "127.0.0.1"
		user = "root"
		password = ""
		db = "buumodelbuilder"
		self.con = pymysql.connect(host=host, user=user, password=password, db=db, cursorclass=pymysql.cursors.
								   DictCursor,autocommit=True)
		self.cur = self.con.cursor()

	def getUser(self,query):
		self.cur.execute("SELECT * FROM user WHERE (username=%s or email=%s)",(query,query))
		return self.cur.fetchone()

	def login(self,user,password):
		self.cur.execute("SELECT * FROM user WHERE username=%s or email=%s",(user,user))
		result = self.cur.fetchone()
		try:
			if result and pbkdf2_sha256.verify(password, result["password"]):
				return True, result["id"], result["api_key"]
			else:
				return False, -1, -1
		except:
			return False, -1, -1

	def register(self,user,email,password):
		self.cur.execute("SELECT * FROM user WHERE (username=%s or email=%s) or (username=%s or email=%s)",(user,user,email,email))
		result = self.cur.fetchone()
		if result:
			return False

		try:
			password = pbkdf2_sha256.using(rounds=8000, salt_size=10).hash(password)
			self.cur.execute("INSERT INTO `user` (`username`,`email`, `password`, `api_key`) VALUES (%s, %s, %s, uuid())", (user,email, password))
			return True
		except:
			return False

	def new_project(self,name,type,id):
		try:
			self.cur.execute("INSERT INTO `project` (`proj_name`,`proj_modelType`,`user_id`,`proj_class`) VALUES (%s, %s, %s, %s)",(name,type,id,"[]"))
			return True
		except:
			return False

	def del_project(self,proj_id,id):
		try:
			self.cur.execute("DELETE i FROM project p,image i WHERE p.proj_id = i.proj_id AND p.proj_id = %s AND p.user_id = %s",(proj_id,id))
			self.cur.execute("DELETE p FROM project p WHERE p.proj_id = %s AND p.user_id = %s",(proj_id,id))
			return True
		except:
			return False

	def list_project(self,id):
		self.cur.execute("SELECT *,COUNT(DISTINCT i.img_id) AS img_len FROM project p LEFT JOIN image i ON p.proj_id = i.proj_id WHERE p.user_id = %s GROUP BY p.proj_id ",id)
		result = self.cur.fetchall()
		return result

	def get_project(self,id,proj_id):
		self.cur.execute("SELECT * FROM `project` WHERE `user_id` = %s AND `proj_id` = %s",(id,proj_id))
		result = self.cur.fetchone()
		return result

	def new_image(self,id,proj_id,path):
		try:
			proj = int(proj_id) in [d['proj_id'] for d in self.list_project(id)]
			img = path not in [d['img_path'] for d in self.list_image(id,proj_id)]
			if(proj and img):
				self.cur.execute("INSERT INTO `image` (`img_path`,`proj_id`) VALUES (%s, %s)",(path,proj_id))
				return True
			return False
		except:
			return False

	def list_image(self,id,proj_id):
		proj = int(proj_id) in [d['proj_id'] for d in self.list_project(id)]
		if(proj):
			self.cur.execute("SELECT * FROM `image` WHERE `proj_id` = %s",proj_id)
			result = self.cur.fetchall()
			return result
		else:
			return False

	def updateDataset(self,path,id,proj_id):
		proj = int(proj_id) in [d['proj_id'] for d in self.list_project(id)]
		if(proj):
			self.cur.execute("UPDATE `project` SET `proj_datasetPath` = %s WHERE `project`.`proj_id` = %s",(path,proj_id))
			return True
		else:
			return False

if __name__ == '__main__':
	db = Database()
	'''print(db.getUser("admin"))
	print(db.register("admin","admin@.com","admin"))
	print(db.login("admin","admin"))'''
	print(db.list_image(1,11))