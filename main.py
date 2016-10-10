import webapp2
import re
			

# html boilerplate header and footer
header = """ 
<!DOCTYPE html>
<html>
<head>
		<style type="text/css">
			.error{
				color:red;
			}
		</style>
</head> 
"""
form = """
	<body>
	<h1>Sign Up</h1>
		<form method="post">
			<table>
				<tr>
					<td class="label">Username</td>
					<td>
						<input name="username" type="text" value="">
						<span class="error">{erroru}</span>
					</td>
				</tr>
				<tr>
					<td class="label">Password</td>
					<td>
						<input name="password" type="password" required/>
						<span class="error">{errorp}</span>
					</td>
				</tr>
				<tr>
					<td class="label">Verify Password</td>
					<td>
						<input name="verify" type="password" required/>
						<span class="error">{errorv}</span>
					</td>
					</tr>
				 <tr>
          			<td class="label">Email</td>
					<td>
						<input name="email" type="email">
						<span class="error">{errore}</span>
					</td>
				</tr>
			</table>
			<input type= "submit">
		</form>
</body>
</html>"""
				
						
								
class MainHandler(webapp2.RequestHandler):

	def validate_username(self, username):
		USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
		if USER_RE.match(username):
			return username
		else:
			return ""
		
	def validate_password(self, password):
		PWD_RE = re.compile(r"^.{3,20}$")
		if PWD_RE.match(password):
			return password
		else:
			return ""

	def validate_verify(self, password, verify):
		# will not continue if password is not verified
		if password == verify:
			return verify

	def validate_email(self, email):
		# allow blank email field
		if not email:
			return ""
		EMAIL_RE = re.compile(r"^[\S]+@[\S]+.[\S]+$")
		if EMAIL_RE.match(email):
			return ""

	def get(self):
		# create dictionary from errors
		errors = {'erroru':'', 'errorp':'', 'errorv':'', 'errore':''}
		self.response.write(header + form.format(**errors))

	def post(self):
		submitted_username = self.request.get("username")
		submitted_password = self.request.get("password")
		submitted_verify = self.request.get("verify")
		submitted_email = self.request.get("email")


		username = self.validate_username(submitted_username)
		password = self.validate_password(submitted_password)
		verify = self.validate_verify(submitted_password, submitted_verify)
		email = self.validate_email(submitted_email)

		if (username and password and verify and (email is not None) ):
			self.redirect('/welcome?username=%s' % username)
		

		errors = {'erroru':'', 'errorp':'', 'errorv':'', 'errore':''}
		if not username:
			errors['erroru'] = "Not a valid username"
			erroru = True
		if not password:
			errors['errorp'] = "Not a valid password"
			errorp = True
		if not verify:
			errors['errorv'] = "Passwords do not match"
			errorv = True
	
		
		self.response.write(header + form.format(**errors))
		#self.render('signup.html', username=username, email=email, errors=errors)

#class Welcome(Handler):
	#def get(self):
		#username = self.request.get("username")
		#self.render('welcome.html', username=username)
		
app = webapp2.WSGIApplication([
	('/', MainHandler)], debug = True)