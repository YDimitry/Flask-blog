from flask import Flask, redirect, url_for, request, render_template
from flask_login import current_user
from flask_sqlalchemy import SQLAlchemy
# from flask import render_template
from flask_migrate import Migrate
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_security import SQLAlchemyUserDatastore
from flask_security import Security


from config import app_config

db = SQLAlchemy()


def create_app(conf_name):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[conf_name])
    app.config.from_pyfile('config.py')

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404

    db.init_app(app)


    # @app.route('/')
    # def hello_world():
    #     conf_var = app.config
    #     return render_template('index.html',conf=conf_var)

    migrate = Migrate(app, db)
    from app import models

    #### Admin
    class AdminMixin:
        def is_accessible(self):
            # return current_user.has_role('admin')
            return True

        def inaccessible_callback(self, name, **kwargs):
            return redirect(url_for('security.login', next=request.url))

    class BaseModelView(ModelView):
        def on_model_change(self, form, model, is_created):
            model.generate_slug()
            return super(BaseModelView, self).on_model_change(form, model, is_created)

    class PostAdminView(AdminMixin,BaseModelView):
        # ограничение количества отображаемых аттрибутов
        form_columns = ['title', 'body', 'tags']

    class TagAdminView(AdminMixin,BaseModelView):
        form_columns = ['name']


    class HomeAdminView(AdminMixin, AdminIndexView):
        pass


    admin = Admin(app, 'FlaskApp', url='/',index_view=HomeAdminView(name='Home'))
    admin.add_view(PostAdminView(models.Post,db.session))
    admin.add_view(TagAdminView(models.Tag,db.session))

    ### Flask Security
    user_datastore = SQLAlchemyUserDatastore(db, models.User, models.Role)
    security = Security(app, user_datastore)

    from .home import home as home_blueprint
    app.register_blueprint(home_blueprint)

    from .posts import posts as posts_blueprint
    app.register_blueprint(posts_blueprint, url_prefix='/blog')

    return app
