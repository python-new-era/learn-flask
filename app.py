from flask import Flask , render_template,request,make_response,session,redirect,url_for,flash,abort
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.secret_key = "jksdbsj87hiubdehbwhevuvudffgff"



@app.errorhandler(401)
def adakesalahan(e):
    return render_template('404.html'),401

@app.route('/')
# def index():
#     return render_template('index.html')

# metode get
def index():
    id = request.args.get('id')
    vieo = request.args.get('video')

    return render_template('index.html',id=id)

ALLOWED_EXTENSION = set(['png','jpg','jpeg'])
app.config['UPLOAD_FOLDER'] = 'uploads'

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSION

@app.route('/upload',methods=['GET','POST'])
def uploadfile():

    if request.method == 'POST':

        file = request.files['file']

        if 'file' not in request.files:
            return redirect(request.url)

        if file.filename == '':
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return 'File Berhasil Disimpan di ' + filename

    return  render_template('/upload.html')



@app.route('/setting')
def setting():
    return 'Halo kamu ada di halaman settting'

@app.route('/profile/<name>')
def profile(name):
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('profile.html',username=name)

@app.route('/blog/<int:idnya>')
def blogId(idnya):
    return 'id nya adalah %d' % idnya

@app.route('/login',methods=['GET','POST'])
def login():

    if request.method == 'POST':
        if request.form['password'] == '':
            abort(401)

        session['username'] = request.form['email']
        flash('Kamu berhasil login>', 'success')
        return redirect(url_for('profile', name=session['username']))

    if 'username' in session:
        username = session['username']
        return redirect(url_for('profile',name=username))

    return render_template('login.html')


@app.route('/cookie')
def getCookie():
    email = request.cookies.get('email')
    return 'email dalam cokies adalah ' + email


@app.route('/logout')
def keluar():
    session.pop('username',None)
    return redirect(url_for("login"))


