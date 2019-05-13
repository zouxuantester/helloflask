__author__ = 'zouxuan'
__date__ = '2019/5/9 1:34 PM'


from flask_wtf import FlaskForm
from wtforms.validators import ValidationError, DataRequired
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from flask_wtf.file import FileField, FileAllowed, FileRequired
from flask_ckeditor import CKEditorField


def validate_field(form, field):
    if field.data == "":
        raise ValidationError('不能为空')


class MyBaseForm(FlaskForm):
    class Meta:
        locales = ['zh']


class LoginForm(MyBaseForm):
    username = StringField('Username',
                           render_kw={'placeholder': 'Please enter username'})
    password = PasswordField('Password',
                             render_kw={'placeholder': 'Please enter password'})
    remember = BooleanField('Remember me')
    submit = SubmitField('Log in')

    def validate_username(self, username):
        if username.data == "":
            raise ValidationError('用户名不能为空')


class UploadForm(FlaskForm):
    photo = FileField('上传图片', validators=[FileRequired(), FileAllowed(['jpeg', 'jpg', 'png', 'gif'])])
    submit = SubmitField('上传')


class RichTextForm(FlaskForm):
    title = StringField('Title')
    body = CKEditorField('body')
    submit = SubmitField()
    pass


class NoteForm(FlaskForm):
    body = CKEditorField('Body', validators=[DataRequired()])
    submit = SubmitField('Save')


class EditNoteForm(NoteForm):
    submit = SubmitField('Update')


class DeleteForm(FlaskForm):
    submit = SubmitField('删除日记')





