from flask import Flask
from flask import render_template
from flask_wtf import FlaskForm, RecaptchaField
from flask_wtf.file import FileField, FileAllowed, FileRequired
from flask_bootstrap import Bootstrap
from wtforms import SubmitField, FloatField
from wtforms.validators import NumberRange
from werkzeug.utils import secure_filename
import utils

print("Hello world")

SECRET_KEY = 'secret'

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
app.config['RECAPTCHA_USE_SSL'] = False
app.config['RECAPTCHA_PUBLIC_KEY'] = '6LfJlHIkAAAAAIsnXzvxbngHOR9wTvd2C96t0W8F'
app.config['RECAPTCHA_PRIVATE_KEY'] = '6LfJlHIkAAAAAIqxAa6o2TKo_JrPLHrQ2x1vFylN'
app.config['RECAPTCHA_OPTIONS'] = {'theme': 'white'}
bootstrap = Bootstrap(app)

#Создаём класс формы с полями для ввода исходных файлов, полем для ввода коэфф. смешивания, капчей и кнопкой отправки формы
class NetForm(FlaskForm):
    upload_first = FileField('Load first image', validators=[FileRequired(),
                                                             FileAllowed(['jpg', 'jpeg'], 'jpg, jpeg only!')])
    upload_second = FileField('Load second image', validators=[FileRequired(),
                                                               FileAllowed(['jpg', 'jpeg'], 'jpg, jpeg only!')])
    mix_ratio = FloatField('Mixing ratio (from 0 to 1)', validators=[NumberRange(min=0, max=1,
                                                                                 message="Wrong value")])
    recaptcha = RecaptchaField()
    submit = SubmitField('send')


@app.route("/", methods=['GET', 'POST'])
def main():
    form = NetForm()
    #Начальные значения
    filename_first, filename_second, filename_result = None, None, None
    gist_first, gist_second, gist_result = None, None, None
    mixing_ratio = 0.5
    if form.validate_on_submit():
        #Сохранение загруженный пользователей изображений в папку static
        filename_first = './static/' + secure_filename(form.upload_first.data.filename)
        filename_second = './static/' + secure_filename(form.upload_second.data.filename)
        form.upload_first.data.save(filename_first)
        form.upload_second.data.save(filename_second)
        #Считывание коэфф. смешивания
        mixing_ratio = form.mix_ratio.data
        #Смешивание двух изображений
        filename_result = utils.mix_photos([filename_first, filename_second], mixing_ratio)
        #Построение столбчатых диаграмм
        gist_first = utils.gist_colors(filename_first)
        gist_second = utils.gist_colors(filename_second)
        gist_result = utils.gist_colors(filename_result)
    return render_template('index.html', form=form, image_first=filename_first, image_second=filename_second,
                           image_result=filename_result, gist_first=gist_first,
                           gist_second=gist_second, gist_result=gist_result)


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000)
