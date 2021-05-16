from flask import Flask, render_template, redirect
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, URL
import csv


app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)


class CafeForm(FlaskForm):
    cafe_name = StringField('Cafe Name', validators=[DataRequired()])
    cafe_location = StringField('Cafe Location on Google Maps(url)', validators=[DataRequired(), URL()])
    opening_time = StringField('Opening Time e.g. 8AM', validators=[DataRequired()])
    closing_time = StringField('Closing Time e.g. 5:30PM', validators=[DataRequired()])
    coffee_rating = SelectField('Coffee Rating',
                                choices=['☕', '☕☕', '☕☕☕', '☕☕☕☕', '☕☕☕☕☕'])
    wifi_strength_rating = SelectField('Wifi Strength Rating',
                                       choices=['✘', '💪', '💪💪', '💪💪💪', '💪💪💪💪', '💪💪💪💪💪'])
    power_socket_availability = SelectField('Power Socket Availability',
                                            choices=['✘', '🔌', '🔌🔌', '🔌🔌🔌', '🔌🔌🔌🔌', '🔌🔌🔌🔌🔌'])
    submit = SubmitField('Submit')


@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods=["POST", "GET"])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        new_cafe_data = [form.cafe_name.data, form.cafe_location.data,
                         form.opening_time.data, form.closing_time.data,
                         form.coffee_rating.data, form.wifi_strength_rating.data, form.power_socket_availability.data]
        cafe_data_string = ""
        for data in new_cafe_data:
            cafe_data_string += data + ","
        with open('cafe-data.csv', 'a', encoding='utf-8', newline='') as csv_file:
            csv_file.write(f"\n{cafe_data_string[:-1]}")
            return redirect('/cafes')
    return render_template('add.html', form=form)


@app.route('/cafes')
def cafes():
    with open('cafe-data.csv', newline='', encoding='utf-8') as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
    return render_template('cafes.html', cafes=list_of_rows)


if __name__ == '__main__':
    app.run(debug=True)
