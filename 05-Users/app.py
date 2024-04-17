from flask import Flask, render_template, redirect, url_for, flash, request, abort
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, SubmitField, FileField
from wtforms.fields.choices import SelectField
from wtforms.validators import DataRequired, Length
from flask_wtf.file import FileAllowed, FileRequired
from werkzeug.utils import secure_filename
from flask_bcrypt import Bcrypt
from flask_bs4 import Bootstrap
import os
from datetime import datetime

# konfiguracja aplikacji
app = Flask(__name__)
bootstrap = Bootstrap(app)
app.config['SECRET_KEY'] = 'lkjh6789&^&*(OKJHG&*(*&YHJ'
bcrypt = Bcrypt(app)
app.config['UPLOAD_PATH'] = 'upload'
app.config['UPLOAD_EXTENSIONS'] = ['.txt', '.png', '.jpg', '.jpeg']
app.config['MAX_CONTENT_LENGHT'] = 16 * 1024 * 1024  # 16MB

# konfiguracja bazy danych
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data/users.sqlite')
db = SQLAlchemy(app)

# tabela w bazie danych


class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(20))
    lastName = db.Column(db.String(30))
    userMail = db.Column(db.String(50), unique=True)
    userPass = db.Column(db.String(50))
    userRole = db.Column(db.String(20))

    def is_authenticated(self):
        return True


class Folders(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    folderName = db.Column(db.String(50), unique=True)
    type = db.Column(db.String(20))
    icon = db.Column(db.String(20))

    time = db.Column(db.String(20))


class Files(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fileName = db.Column(db.String(50), unique=True)
    type = db.Column(db.String(20))
    icon = db.Column(db.String(20))
    time = db.Column(db.String(20))

    size = db.Column(db.String(20))

# konfiguracja Flask-Login


loginManager = LoginManager()
loginManager.init_app(app)

loginManager.login_view = 'login'
loginManager.login_message = 'Nie jesteś zalogowany'
loginManager.login_message_category = 'warning'


@loginManager.user_loader
def loadUser(id):
    return Users.query.filter_by(id=id).first()

# formularze


class Login(FlaskForm):
    """formularz logowania"""
    userMail = EmailField('Mail', validators=[DataRequired()], render_kw={"placeholder": "Mail"})
    userPass = PasswordField('Hasło', validators=[DataRequired()], render_kw={"placeholder": "Hasło"})
    submit = SubmitField('Zaloguj')


class Register(FlaskForm):

    """formularz rejestracji"""
    firstName = StringField('Imię', validators=[DataRequired()], render_kw={"placeholder": "Imię"})
    lastName = StringField('Nazwisko', validators=[DataRequired()], render_kw={"placeholder": "Nazwisko"})
    userMail = EmailField('Mail', validators=[DataRequired()], render_kw={"placeholder": "Mail"})
    userPass = PasswordField('Hasło', validators=[DataRequired()], render_kw={"placeholder": "Hasło"})
    submit = SubmitField('Rejestruj')


class Add(FlaskForm):
    """formularz dodawania użytkowników"""
    firstName = StringField('Imię', validators=[DataRequired()], render_kw={"placeholder": "Imię"})
    lastName = StringField('Nazwisko', validators=[DataRequired()], render_kw={"placeholder": "Nazwisko"})
    userMail = EmailField('Mail', validators=[DataRequired()], render_kw={"placeholder": "Mail"})
    userPass = PasswordField('Hasło', validators=[DataRequired()], render_kw={"placeholder": "Hasło"})
    userRole = SelectField('Uprawnienia', validators=[DataRequired()],
                           choices=[('user', 'Użytkownik'), ('admin', 'Administrator')])
    submit = SubmitField('Dodaj')


class Edit(FlaskForm):
    """formularz edycji danych użytkowników"""
    firstName = StringField('Imię', validators=[DataRequired()], render_kw={"placeholder": "Imię"})
    lastName = StringField('Nazwisko', validators=[DataRequired()], render_kw={"placeholder": "Nazwisko"})
    userMail = EmailField('Mail', validators=[DataRequired()], render_kw={"placeholder": "Mail"})
    userRole = SelectField('Uprawnienia', validators=[DataRequired()],
                           choices=[('user', 'Użytkownik'), ('admin', 'Administrator')])
    submit = SubmitField('Zapisz')


class Password(FlaskForm):
    """formularz zmiany hasła przez użytkowników"""
    userMail = EmailField('Mail', validators=[DataRequired()], render_kw={"placeholder": "Mail"})
    userPass = PasswordField('Hasło', validators=[DataRequired()], render_kw={"placeholder": "Hasło"})
    newUserPass = PasswordField('Nowe hasło', validators=[DataRequired()], render_kw={"placeholder": "Nowe hasło"})
    submit = SubmitField('Zapisz')


class ChangePass(FlaskForm):
    """formularz do zmiany hasła uzytkownika z panelu admina"""
    userPass = PasswordField('Nowe hasło:', validators=[DataRequired(), Length(min=3, max=50)],
                             render_kw={"placeholder": "Nowe hasło"})
    submit = SubmitField('Zapisz')


class Search(FlaskForm):
    """formularz wyszukiwania plików / folderów"""
    searchKey = StringField('Szukaj', validators=[DataRequired()])
    submit = SubmitField('Szukaj')


class CreateFolders(FlaskForm):
    """formularz tworzenia nowego folderu"""
    folderName = StringField('Nazwa folderu', validators=[DataRequired()], render_kw={'placeholder': 'Nazwa folderu'})
    submit = SubmitField('Utwórz')


class UploadFiles(FlaskForm):
    """formularz przesyłania plików"""
    fileName = FileField('Plik', validators=[FileAllowed([app.config['UPLOAD_EXTENSIONS']])],
                         render_kw={'placeholder': '.txt, .png, .jpg, .jpeg'})
    submit = SubmitField('Prześlij')


class renameFolders(FlaskForm):
    """formularz przesyłania plików"""
    folderName = StringField('Nazwa folderu', validators=[DataRequired()], render_kw={'placeholder': 'Nazwa folderu'})
    submit = SubmitField('Zapisz')


class delFolders(FlaskForm):
    """formularz przesyłania plików"""
    submit = SubmitField('Usuń')

# główna aplikacja


@app.route('/')
def index():
    return render_template('index.html', title='Home', headline='Zarządzanie użytkownikami')


@app.route('/login', methods=['GET', 'POST'])
def login():
    user = Users.query.all()
    if not user:
        return redirect(url_for('register'))
    else:
        loginForm = Login()
        if loginForm.validate_on_submit():
            user = Users.query.filter_by(userMail=loginForm.userMail.data).first()
            if user:
                if bcrypt.check_password_hash(user.userPass, loginForm.userPass.data):
                    login_user(user)
                    return redirect(url_for('dashboard'))
    return render_template('login.html', title='Logowanie', headline='Logowanie', loginForm=loginForm)


@app.route('/register', methods=['GET', 'POST'])
def register():
    registerForm = Register()
    user = Users.query.all()
    if registerForm.validate_on_submit() and not user:
        try:
            hashPass = bcrypt.generate_password_hash(registerForm.userPass.data)
            newUser = Users(userMail=registerForm.userMail.data, userPass=hashPass,
                            firstName=registerForm.firstName.data,
                            lastName=registerForm.lastName.data, userRole='admin')
            db.session.add(newUser)
            db.session.commit()
            flash('Konto utworzone poprawnie', 'success')
            return redirect(url_for('login'))
        except Exception:
            flash('Taki adres mail już istnieje, wpisz inny', 'danger')
            # return redirect(url_for('register'))
    elif registerForm.validate_on_submit():
        try:
            hashPass = bcrypt.generate_password_hash(registerForm.userPass.data)
            newUser = Users(userMail=registerForm.userMail.data, userPass=hashPass,
                            firstName=registerForm.firstName.data,
                            lastName=registerForm.lastName.data, userRole='user')
            db.session.add(newUser)
            db.session.commit()
            flash('Konto utworzone poprawnie', 'success')
            return redirect(url_for('login'))
        except Exception:
            flash('Taki adres mail już istnieje, wpisz inny', 'danger')
            # return redirect(url_for('register'))
    return render_template('register.html', title='Rejestracja', headline='Rejestracja', registerForm=registerForm)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/dashboard')
@login_required
def dashboard():
    users = Users.query.all()
    addUser = Add()
    editUser = Edit()
    editUserPass = ChangePass()
    search = Search()
    createFolder = CreateFolders()
    renameFolder = renameFolders()
    delFolder = delFolders()
    uploadFile = UploadFiles()
    folders = Folders.query.all()
    files = Files.query.all()
    editPass = Password()
    return render_template('dashboard.html', editPass=editPass,
                           delFolder=delFolder, renameFolder=renameFolder,
                           title='Dashboard', users=users, addUser=addUser, editUser=editUser,
                           editUserPass=editUserPass, search=search, createFolder=createFolder,
                           uploadFile=uploadFile, files=files, folders=folders)


@app.route('/add-user', methods=['GET', 'POST'])
@login_required
def addUser():
    addUser = Add()
    if addUser.validate_on_submit():
        try:
            hashPass = bcrypt.generate_password_hash(addUser.userPass.data)
            newUser = Users(userMail=addUser.userMail.data, userPass=hashPass, firstName=addUser.firstName.data,
                            lastName=addUser.lastName.data, userRole=addUser.userRole.data)
            db.session.add(newUser)
            db.session.commit()
            flash('Użytkownik dodany poprawnie', 'success')
            return redirect(url_for('dashboard'))
        except Exception:
            flash('Taki adres mail już istnieje, wpisz inny', 'danger')
            return redirect(url_for('dashboard'))


@app.route('/edit-user<int:id>', methods=['GET', 'POST'])
@login_required
def editUser(id):
    editUser = Edit()
    user = Users.query.get_or_404(id)
    if editUser.validate_on_submit():
        user.firstName = editUser.firstName.data
        user.lastName = editUser.lastName.data
        user.userMail = editUser.userMail.data
        user.userRole = editUser.userRole.data
        db.session.commit()
        flash('Dane zapisane poprawnie', 'success')
        return redirect(url_for('dashboard'))


@app.route('/delete-user', methods=['GET', 'POST'])
@login_required
def deleteUser():
    if request.method == 'GET':
        id = request.args.get('id')
        user = Users.query.filter_by(id=id).one()
        db.session.delete(user)
        db.session.commit()
        flash('Użytkownik usunięty poprawnie', 'success')
        return redirect(url_for('dashboard'))


@app.route('/edit-user-pass<int:id>', methods=['GET', 'POST'])
@login_required
def editUserPass(id):
    editUserPass = ChangePass()
    user = Users.query.filter_by(id=id).first()
    if editUserPass.validate_on_submit() and user:
        user.userPass = bcrypt.generate_password_hash(editUserPass.userPass.data)
        db.session.commit()
        flash('Hasło zmienione poprawnie', 'success')
        return redirect(url_for('dashboard'))


@app.route('/change-pass', methods=['GET', 'POST'])
@login_required
def changePass():
    changePassForm = Password()
    user = Users.query.filter_by(userMail=changePassForm.userMail.data).first()
    if changePassForm.validate_on_submit() and user:
        if bcrypt.check_password_hash(user.userPass, changePassForm.userPass.data):
            user.userPass = bcrypt.generate_password_hash(changePassForm.newUserPass.data)
            flash('Hasło zostało zmienione pomyślnie', 'success')
            db.session.commit()
            return redirect(url_for('dashboard'))
        else:
            flash('Błąd przy zapisie hasła', 'danger')
    else:
        flash('Błąd przy zapisie hasła', 'danger')
    return redirect(url_for('dashboard'))


@app.route('/upload-file', methods=['GET', 'POST'])
@login_required
def uploadFile():
    uploadedFile = request.files['fileName']
    fileName = secure_filename(uploadedFile.filename)
    if fileName != '':
        fileExtension = os.path.splitext(fileName)[1]
        if fileExtension not in app.config['UPLOAD_EXTENSIONS']:
            abort(400)
        type = ''
        icon = ''
        if fileExtension == '.png':
            type = 'png'
            icon = 'bi bi-filetype-png'
        elif fileExtension == '.jpg':
            type = 'jpg'
            icon = 'bi bi-filetype-jpg'
        elif fileExtension == '.jpeg':
            type = 'jpg'
            icon = 'bi bi-filetype-jpg'
        elif fileExtension == '.txt':
            type = 'txt'
            icon = 'bi bi-filetype-txt'
        uploadedFile.save(os.path.join(app.config['UPLOAD_PATH'], fileName))
        size = round(os.stat(os.path.join(app.config['UPLOAD_PATH'], fileName)).st_size / (1024 * 1024), 2)
        time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        newFile = Files(fileName=fileName, size=size, type=type, icon=icon, time=time)
        db.session.add(newFile)
        db.session.commit()
        flash('Plik przesłany poprawnie', 'success')
        return redirect(url_for('dashboard'))


@app.route('/rename-file<int:id>', methods=['GET', 'POST'])
@login_required
def renameFile(id):
    newFileName = request.form['folderName']
    print(id)
    print(newFileName)
    if newFileName != "":
        fileToRename = Files.query.filter_by(id=id).first()
        arr = newFileName.split(".")
        print(arr)
        if len(arr) == 2:
            if not arr[1] == fileToRename.type:
                newFileName = arr[0] + f".{fileToRename.type}"
                flash(f'Pomyślnie zmieniono nazwę pliku {fileToRename.fileName} na {newFileName}', 'success')
        else:
            newFileName += arr[0] + f".{fileToRename.type}"
            flash(f'Zmieniono nazwę pliku {fileToRename.fileName} na {newFileName}', 'success')
        print(newFileName)
        # if not newFileName.split(".")[1]
        os.rename(os.path.join(app.config['UPLOAD_PATH'], fileToRename.fileName),
                  os.path.join(app.config['UPLOAD_PATH'], newFileName))
        fileToRename.fileName = newFileName
        db.session.commit()

    return redirect(url_for('dashboard'))


@app.route('/delete-file<int:id>', methods=['GET', 'POST'])
@login_required
def deleteFile(id):
    fileToDelete = Files.query.filter_by(id=id).first()
    os.remove(os.path.join(app.config['UPLOAD_PATH'], fileToDelete.fileName))
    Files.query.filter_by(id=id).delete()
    db.session.commit()
    flash(f'Pomyślnie usunięto plik {fileToDelete.fileName}', 'success')
    return redirect(url_for('dashboard'))


@app.route('/create-folder', methods=['GET', 'POST'])
@login_required
def createFolder():
    folderName = request.form['folderName']
    if folderName != '':
        time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        os.mkdir(os.path.join(app.config['UPLOAD_PATH'], folderName))
        newFolder = Folders(folderName=folderName, type='folder', icon='bi bi-folder', time=time)
        db.session.add(newFolder)
        db.session.commit()
        flash('Folder utworzony poprawnie', 'success')
        return redirect(url_for('dashboard'))


@app.route('/rename-folder<int:id>', methods=['GET', 'POST'])
@login_required
def renameFolder(id):
    newFolderName = request.form['folderName']
    if newFolderName != '':
        print(id)
        print(newFolderName)
        folder = Folders.query.filter_by(id=id).first()
        if folder:
            os.rename(os.path.join(app.config['UPLOAD_PATH'], folder.folderName),
                      os.path.join(app.config['UPLOAD_PATH'], newFolderName))
            folder.folderName = newFolderName
        db.session.commit()
        flash(f'Pomyślnie zmieniono nazwę foldery {id} na {newFolderName}', 'success')
        print(folder)

    # if newFolderName != '':
    #
    #     db.session.add(newFolder)
    #     db.session.commit()
    #     flash('Folder utworzony poprawnie', 'success')
    #     return redirect(url_for('dashboard'))
    #
    # db.session.commit()
    return redirect(url_for('dashboard'))


@app.route('/delete-folder<int:id>', methods=['GET', 'POST'])
@login_required
def deleteFolder(id):
    folderToDelete = Folders.query.filter_by(id=id).first()
    os.rmdir(os.path.join(app.config['UPLOAD_PATH'], folderToDelete.folderName))
    Folders.query.filter_by(id=id).delete()
    db.session.commit()
    flash(f'Pomyślnie usunięto folder {folderToDelete.folderName}', 'success')
    return redirect(url_for('dashboard'))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
