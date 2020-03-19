from app import db
from datetime import datetime
import re
from flask_security import UserMixin, RoleMixin

def slugify(title):
    return re.sub(r'[^\w+]', '-', title.lower())
# таблица для отношения many to many
post_tags =db.Table('post_tags',
                    db.Column('post_id',db.Integer,db.ForeignKey('post.id')),
                    db.Column('tag_id',db.Integer,db.ForeignKey('tag.id')))


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140))
    slug = db.Column(db.String(140), unique=True)
    body = db.Column(db.Text)
    created = db.Column(db.DateTime, default=datetime.now())
    tags = db.relationship('Tag', secondary=post_tags, backref=db.backref('posts'),lazy='dynamic')


    def __init__(self, *args, **kwargs):
        super(Post, self).__init__(*args, **kwargs)
        self.generate_slug()

    def generate_slug(self):
        self.slug = slugify(self.title)


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    slug = db.Column(db.String(100))

    def __init__(self, *args, **kwargs):
        super(Tag, self).__init__(*args, **kwargs)
        self.generate_slug()

    def generate_slug(self):
        self.slug = slugify(self.name)

    def __repr__(self):
        return f'<Tag id:{self.id}, name:{self.name}>'


# db.create_all()
# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# print('sqlite:////' + os.path.join(BASE_DIR, 'blog.sqlite3'))
def init_test_data():
    # p1 = Post(title="First post", body="First post body")
    # p2 = Post(title="Second post", body="Second post body")
    # p3 = Post(title="Third post", body="Third post body")
    t = Tag(name='python')
    db.session.add(t)
    # db.session.add_all([p1, p2, p3])
    db.session.commit()
    post = Post.query.first()

    post.tags.append(t)
    db.session.add(post)
    db.session.commit()
# posts = Post.query.all()
# p2 = Post.query.filter(Post.title.contains('second')).first()
# print(p2)

#### Flask Security

roles_users = db.Table('roles_users',
                       db.Column('user_id',db.Integer,db.ForeignKey('user.id')),
                       db.Column('role_id',db.Integer,db.ForeignKey('role.id'))
                       )


class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    roles = db.relationship('Role', secondary=roles_users,backref=db.backref('users',lazy='dynamic'))


class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(100),unique=True)
    description = db.Column(db.String(255))