from flask import render_template
from flask import request
from flask import redirect
from flask import url_for

# from app import models
from . import posts
from ..models import Post, Tag
from .forms import PostForm
from app import db
from flask_security import login_required
import app


@posts.route('/create', methods=['POST', 'GET'])
@login_required
def create_post():
    if request.method == 'POST':
        title = request.form.get('title')
        body = request.form.get('body')
        try:
            post = Post(title=title, body=body)
            db.session.add(post)
            db.session.commit()
        except:
            print('')
        return redirect(url_for('posts.blogpage'))
    form = PostForm()
    return render_template('create_post.html', form=form)


@posts.route('/')
def blogpage():
    q = request.args.get('q')
    page = request.args.get('page')
    if page and page.isdigit():
        page = int(page)
    else:
        page = 1
    if q:
        p = Post.query.filter(Post.title.contains(q) | Post.body.contains(q))  # .all()
    else:
        p = Post.query.order_by(Post.created.desc())
    pages = p.paginate(page=page, per_page=3)
    # models.init_test_data()
    return render_template('posts.html', pages=pages)

@posts.route('/<slug>/edit', methods=['POST','GET'])
@login_required
def edit_post(slug):
    post = Post.query.filter(Post.slug == slug).first_or_404()
    if request.method == 'POST':
        form = PostForm(formdata=request.form, obj=post)
        form.populate_obj(post)  # заполнение аттрибутов объекта post
        db.session.commit()
        return redirect(url_for('posts.post_detail',slug=post.slug))
    form = PostForm(obj=post)
    return render_template('edit_post.html', post=post, form=form)


@posts.route('/<slug>')
def post_detail(slug):
    post = Post.query.filter(Post.slug == slug).first_or_404()
    return render_template('post_detail.html', post=post)


@posts.route('/tag/<slug>')
def tag_detail(slug):
    tag = Tag.query.filter(Tag.slug == slug).first_or_404()
    p = tag.posts  # .all()
    return render_template('tag_detail.html', posts=p, tag=tag)
