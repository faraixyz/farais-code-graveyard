from wtforms import Form, PasswordField

class LoginForm(Form):
    password = PasswordField("Password")
