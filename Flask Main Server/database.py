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
			self.cur.execute("INSERT INTO `project` (`proj_name`,`proj_modelType`,`user_id`) VALUES (%s, %s, %s)",(name,type,id))
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
		return self.cur.fetchall()

	def get_project(self,id,proj_id):
		self.cur.execute("SELECT * FROM `project` WHERE `user_id` = %s AND `proj_id` = %s",(id,proj_id))
		return self.cur.fetchone()

	def new_image(self,id,proj_id,path):
		try:
			proj = int(proj_id) in [d['proj_id'] for d in self.list_project(id)]
			lst_img = self.list_image(id,proj_id)
			imgid = [d['img_id'] for d in lst_img]
			imgpath = [d['img_path'] for d in lst_img]
			img = path not in imgpath
			if(proj and img):
				self.cur.execute("INSERT INTO `image` (`img_path`,`proj_id`) VALUES (%s, %s)",(path,proj_id))
				return self.cur.lastrowid
			idx = imgpath.index(path)
			return imgid[idx]
		except:
			return False

	def list_image(self,id,proj_id):
		proj = int(proj_id) in [d['proj_id'] for d in self.list_project(id)]
		if(proj):
			self.cur.execute("SELECT * FROM `image` WHERE `proj_id` = %s",proj_id)
			return self.cur.fetchall()
		else:
			return False

	def del_image(self,img,id,proj_id):
		proj = int(proj_id) in [d['proj_id'] for d in self.list_project(id)]
		if(proj):
			self.cur.execute("DELETE FROM `image` WHERE `img_id` = %s AND `proj_id` = %s",(img,proj_id))
			return True
		else:
			return False

	def get_image(self,img,id,proj_id):
		proj = int(proj_id) in [d['proj_id'] for d in self.list_project(id)]
		if(proj):
			self.cur.execute("SELECT * FROM `image` WHERE `img_id` = %s AND `proj_id` = %s",(img,proj_id))
			return self.cur.fetchone()
		else:
			return False

	def update_Class(self,oldclass,newclass,id,proj_id):
		proj = int(proj_id) in [d['proj_id'] for d in self.list_project(id)]
		if(proj):
			self.cur.execute("UPDATE image SET `img_path` = REPLACE(`img_path` , %s, %s) WHERE `img_path` LIKE (%s) AND `proj_id` = %s",(oldclass,newclass,"%"+oldclass+"%",proj_id))
			return True
		else:
			return False

	def updateDataset(self,path,id,proj_id):
		proj = int(proj_id) in [d['proj_id'] for d in self.list_project(id)]
		if(proj):
			img = self.list_image(id,proj_id)
			self.cur.execute("UPDATE `project` SET `proj_datasetDate` = CURDATE(),`proj_datasetImage` = %s, `proj_datasetPath` = %s WHERE `project`.`proj_id` = %s",(len(img),path,proj_id))
			return True
		else:
			return False

	def updateModel(self,path,id,proj_id):
		proj = int(proj_id) in [d['proj_id'] for d in self.list_project(id)]
		if(proj):
			self.cur.execute("UPDATE `project` SET `proj_modelDate` = CURDATE(), `proj_modelPath` = %s WHERE `project`.`proj_id` = %s",(path,proj_id))
			return True
		else:
			return False

	def get_proj_api(self,key,proj_id):
		self.cur.execute("SELECT * FROM project p LEFT JOIN user u ON p.user_id = u.id WHERE u.api_key = %s AND p.proj_id = %s",(key,proj_id))
		return self.cur.fetchone()

if __name__ == '__main__':
	db = Database()
	print(db.getUser("admin"))
	print(db.register("admin","admin@.com","admin"))
	print(db.login("admin","admin"))
	print(db.list_image(1,11))