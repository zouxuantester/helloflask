__author__ = 'zouxuan'
__date__ = '2019/5/5 10:35 AM'


from flask import Flask , request , make_response , json , jsonify , redirect , url_for , session , abort , \
    render_template , Markup , flash , send_from_directory
import click
import os
from urllib.parse import urlparse, urljoin
from jinja2.utils import generate_lorem_ipsum
from jinja2 import escape
from forms import LoginForm, UploadForm, RichTextForm, NoteForm, EditNoteForm, DeleteForm
from util import random_file
from flask_ckeditor import CKEditor
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'zouxuan')
app.config['WTF_I18N_ENABLED'] = False
app.config['MAX_CONTENT_LENGTH'] = 3 * 1024 * 1024
app.config['UPLOAD_PATH'] = os.path.join(app.root_path, 'uploads')
ckeditor = CKEditor(app)
app.config['CKEDITOR_SERVE_LOCAL'] = True
db = SQLAlchemy(app)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
import model
from model import Note, Article, Author, Writer, Book


@app.route('/')
def index():
    form = DeleteForm()
    notes = Note.query.all()

    return render_template('index.html', notes=notes, form=form)


@app.route('/hello')
@app.route('/hi')
def say_hello():
    print(request.referrer)
    name = request.args.get('name')
    if not name:
        name = request.cookies.get('name', 'Human')
    res = "<h1>Hello %s</h1>" % escape(name)
    if session.get('logged_in', None):
        res += '[Authenticated]'
    else:
        res += '[not Authenticated]'
    return res


@app.route('/greet', defaults={'name': 'test'})
@app.route('/greet/<name>')
def greet(name):
    return "Hello %s" % name


@app.route('/color/<any(blue, white, black):color>')
def color(color):
    return '<p>test color</p>'


@app.cli.command('say-hello')
def hello():
    click.echo('Hello command')


@app.route('/plain')
def plain():
    res = make_response('<h1>Hello plain, the MIME type is text/plain</h1>')
    res.mimetype = 'text/plain'
    return res
    pass


@app.route('/text_html')
def text_html():
    res = make_response('<h1>Hello html, The MIME type is text/html</h1>')
    res.mimetype = 'text/html'
    return res


@app.route('/app_json')
def app_json():
    # res = make_response(json.dumps({"a": "b", "name": "Perter"}))
    # res.mimetype = 'application/json'
    # return res
    return jsonify(name='zouxuan', sex='male', age=29), 302
    pass


@app.route('/set/<name>')
def set_name(name):
    res = make_response(redirect(url_for('say_hello')))
    res.set_cookie('name', name, max_age=600)
    return res
    pass


@app.route('/sec')
def get_sec():
    return app.secret_key


@app.route('/login', methods=['GET', 'POST'])
def login():
    # session['logged_in'] = True
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        flash('Welcome home %s!' % username)
        return redirect(url_for('index'))
        pass
    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    if 'logged_in' in session:
        session.pop('logged_in')
    return redirect(url_for('say_hello'))


@app.route('/admin')
def admin():
    if not session.get('logged_in'):
        abort(403)
    return 'Welcome to admin page!!!'
    pass


@app.route('/foo')
def foo():
    for k, v in request.args:
        print(k, v)
    return '<p>test<a href="%s">to login</a></p>' % url_for('do_something', next=request.full_path)


@app.route('/do_something')
def do_something():
    return redirect_back()


def redirect_back():
    for target in request.args.get('next'), request.referrer:
        if not target:
            continue
        if is_safe_url(target):
            return redirect(target)
    return redirect(url_for('say_hello'))
    pass


def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc
    pass


@app.route('/post')
def load_post():
    post_body = generate_lorem_ipsum(n=3)
    return """
    <h1>a very long post</h1>
    <div class="body">%s</div>
    <button id="load">More</button>
    <script src="https://code.jquery.com/jquery-3.3.1.min.js"></script>
    <script type="text/javascript">
    $('#load').click(function(){
        $.ajax({
            url: '/more',
            type: 'get',
            success: function(data){
                $(".body").append(data);
            }
        })
    })
    </script>
    """ % post_body


@app.route('/more')
def more():
    return generate_lorem_ipsum(n=1)
    pass


user = {
    "username": "zouxuan",
    "bio": "喜欢唱歌，喜欢电影，一个简单的人。。"
}

movies = [
    {'name': 'My Neighbor Totoro', 'year': '1988'},
    {'name': 'Three Colours trilogy', 'year': '1993'},
    {'name': 'Forrest Gump', 'year': '1994'},
    {'name': 'Perfect Blue', 'year': '1997'},
    {'name': 'The Matrix', 'year': '1999'},
    {'name': 'Memento', 'year': '2000'},
    {'name': 'The Bucket list', 'year': '2007'},
    {'name': 'Black Swan', 'year': '2010'},
    {'name': 'Gone Girl', 'year': '2014'},
    {'name': 'CoCo', 'year': '2017'},
]


@app.route('/watch_list')
def watch_list():
    text = "<h1>这是安全的</h1>"
    age = '2312'
    return render_template('watchlist.html', user=user, movies=movies, text=text, age=age)


@app.route('/flash')
def just_flash():
    flash('This is flash message')
    return redirect(url_for('index'))


@app.errorhandler(404)
def page_not_found(e):
    return render_template('error/404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('error/500.html'), 500


# 自定义全局变量
@app.context_processor
def indicate_foo():
    foo = 'I am foo'
    return dict(foo=foo)


# 自定义全局函数
@app.template_global()
def bar():
    return 'I am bar'


# 自定义过滤器
@app.template_filter()
def turn_to_int(num):
    return 'str ' + str(num)


# 自定义测试器
@app.template_test()
def is_same(self, other):
    if id(self) == id(other):
        return True
    return False


# 定义python shell上下文
@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'note': Note, 'author': Author, 'article': Article, 'writer': Writer, 'book': Book}


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    form = UploadForm()
    if form.validate_on_submit():
        f = form.photo.data
        filename = random_file(f.filename)
        f.save(os.path.join(app.config['UPLOAD_PATH'], filename))
        flash('Upload success!!')
        session['filenames'] = [filename]
        return redirect(url_for('show_image'))
    return render_template('upload.html', form=form)


@app.route('/uploads/<path:filename>')
def get_file(filename):
    return send_from_directory(app.config['UPLOAD_PATH'], filename)


@app.route('/show_image')
def show_image():
    return render_template('uploaded.html')


@app.route('/cke_view')
def cke_view():
    form = RichTextForm()
    return render_template('ckeditor.html', form=form)


@app.cli.command('init_db')
def init_db():
    db.create_all()
    click.echo('Initialized database!!')


@app.route('/new_note', methods=['GET', 'POST'])
def new_note():
    form = NoteForm()
    if form.validate_on_submit():
        note_body = form.body.data
        note = Note(body=note_body)
        db.session.add(note)
        db.session.commit()
        flash('Create Note success!!')
        return redirect(url_for('index'))
        pass
    return render_template('new_note.html', form=form)
    pass


@app.route('/edit_note/<int:id>', methods=['POST', 'GET'])
def edit_note(id):
    form = EditNoteForm()
    note = Note.query.get(id)
    if form.validate_on_submit():
        note.body = form.body.data
        db.session.commit()
        return redirect(url_for('index'))
    form.body.data = note.body
    return render_template('update_note.html', form=form)


@app.route('/delete/<int:id>', methods=['POST', 'GET'])
def delete_note(id):
    form = DeleteForm()
    if form.validate_on_submit():
        note = Note.query.get(id)
        db.session.delete(note)
        db.session.commit()
        flash('Delete note success!!')
    else:
        abort(400)
    return redirect(url_for('index'))
    pass


# app.add_template_global(bar)

