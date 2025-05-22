from flask_admin import Admin, AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView
from flask_admin.form import BaseForm
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired
from wtforms import StringField, IntegerField
from .models import db, Teacher, Course, Student, Request
from .auth import auth
import sqlalchemy.exc

class SecureAdminIndexView(AdminIndexView):
    @expose('/')
    def index(self):
        return super().index()

    def is_accessible(self):
        return auth.username() == 'admin'

    def inaccessible_callback(self, name, **kwargs):
        return auth.auth_error_callback(401)

class AdminModelView(ModelView):
    def is_accessible(self):
        return auth.username() == 'admin'
    def inaccessible_callback(self, name, **kwargs):
        return auth.auth_error_callback(401)

class TeacherAdmin(AdminModelView):
    form_columns = [
        'full_name',
        'experience',
        'specialty',
        'department'
    ]   

def get_teachers():
    return Teacher.query.all()

class CourseForm(BaseForm):
    title = StringField('Title')
    teacher = QuerySelectField(
        query_factory=get_teachers,
        validators=[DataRequired()]
    )
    student_limit = IntegerField('Student Limit')

class CourseAdmin(AdminModelView):
    form = CourseForm
    form_columns = ['title', 'teacher', 'student_limit']
    
class StudentAdmin(AdminModelView):
    form_columns = ['full_name', 'email']
    
    def scaffold_form(self):
        form_class = super(StudentAdmin, self).scaffold_form()
        if 'requests' in form_class.__dict__.keys():
            delattr(form_class, 'requests')
        return form_class
    
class RequestAdmin(AdminModelView):
    form_ajax_refs = {
        'student': {
            'fields': ('full_name', 'email'),
            'page_size': 10
        },
        'course': {
            'fields': ('title',),
            'page_size': 10
        }
    }

    def handle_exception(self, exc):
        if isinstance(exc, sqlalchemy.exc.IntegrityError):
            from flask import flash
            flash('Ошибка: превышен лимит студентов курса', 'error')
            return True
        return super().handle_exception(exc)

    def on_model_change(self, form, model, is_created):
        try:
            super().on_model_change(form, model, is_created)
        except sqlalchemy.exc.IntegrityError as e:
            if 'course student limit exceeded' in str(e).lower():
                from flask import flash
                flash('Нельзя утвердить заявку: курс заполнен', 'error')
                raise

admin = Admin(
    name='Exam Admin',
    template_mode='bootstrap3',
    index_view=SecureAdminIndexView()
)

def init_admin(app):
    admin.init_app(app)
    admin.add_view(TeacherAdmin(Teacher, db.session))
    admin.add_view(CourseAdmin(Course, db.session))
    admin.add_view(StudentAdmin(Student, db.session))
    admin.add_view(RequestAdmin(Request, db.session))
