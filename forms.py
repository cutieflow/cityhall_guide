from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Length


class FloorForm(FlaskForm):
    name = StringField(
        "フロア名",
        validators=[
            DataRequired(message="フロア名は必須です。"),
            Length(max=100, message="フロア名は100文字以内で入力してください。"),
        ],
    )

    description = TextAreaField(
        "説明",
        validators=[Length(max=500, message="説明は500文字以内で入力してください。")],
    )

    submit = SubmitField("登録")


class LoginForm(FlaskForm):
    username = StringField(
        "ユーザー名", validators=[DataRequired(message="ユーザー名は必須です。")]
    )

    password = PasswordField(
        "パスワード", validators=[DataRequired(message="パスワードは必須です。")]
    )

    submit = SubmitField("ログイン")
