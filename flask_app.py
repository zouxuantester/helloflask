__author__ = 'zouxuan'
__date__ = '2019/5/5 10:35 AM'


from flask import Flask, request, make_response, json, jsonify, redirect, url_for, session, abort, render_template, Markup
import click
import os
from urllib.parse import urlparse, urljoin
from jinja2.utils import generate_lorem_ipsum
from jinja2 import escape


app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'zouxuan')


@app.route('/')
def index():
    age = 29
    return render_template('index.html', age=age)


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


@app.route('/login')
def login():
    session['logged_in'] = True
    return redirect(url_for('say_hello'))


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


# app.add_template_global(bar)

