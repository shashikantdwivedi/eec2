from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_mail import Mail, Message
import database_functions as db_fun

app = Flask(__name__)
# TODO - Replace the SECRET-KEY with your application secret key
app.secret_key = "SECRET-KEY"
ALLOWED_EXTENSIONS = set(['doc', 'docx'])


mail_settings = {
    "MAIL_SERVER": 'smtp.gmail.com',
    "MAIL_PORT": 465,
    "MAIL_USE_TLS": False,
    "MAIL_USE_SSL": True,
    "MAIL_USERNAME": db_fun.mail_username(),
    "MAIL_PASSWORD": db_fun.mail_password()
}

app.config.update(mail_settings)
mail = Mail(app)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/validate_login', methods=["POST"])
def validate_login():
    email = (request.form['email']).strip()
    password = (request.form['password']).strip()
    result = db_fun.validate_login(email, password)
    session["email"] = email
    if result:
        if result["account_validity"]:
            session["status"] = 1
            if db_fun.registration_status(email):
                return redirect(url_for('already_registered'))
            else:
                return redirect(url_for('fill_form'))
        else:
            flash("Account not verified")
            otp = db_fun.get_otp(email)
            try:
                msg = Message(subject="Emerging Entrepreneur Competition 2019 Account Verification",
                              sender=app.config.get("MAIL_USERNAME"),
                              recipients=[email],  # replace with your email for testing
                              html=render_template('otp_template.html', otp=str(otp)))
                mail.send(msg)
                flash("Otp is send to your email")
                return redirect(url_for('verify_otp'))
            except RuntimeError:
                return render_template('error_occurred.html')
    else:
        pass
        flash("Wrong Username or Password")
        return redirect(url_for('login'))


@app.route('/already_registered')
def already_registered():
    if 'status' in session:
        if session['status']:
            return render_template('already_registered.html')
        else:
            return redirect(url_for('login'))
    else:
        return redirect(url_for('login'))


@app.route('/download_form')
def download_form():
    if 'status' in session:
        if session['status']:
            return render_template('download_form.html')
        else:
            return redirect(url_for('login'))
    else:
        return redirect(url_for('login'))


@app.route('/upload_form', methods=["POST"])
def upload_form():
    if 'status' in session:
        if session['status']:
            if not db_fun.form_status(session['email']):
                if db_fun.verify_participants(session['email']):
                    file = request.files['file']
                    # if user does not select file, browser also
                    # submit an empty part without filename
                    if file.filename == '':
                        flash('No selected file')
                        return redirect(url_for('download_form'))
                    if file and allowed_file(file.filename):
                        try:
                            msg = Message(subject="New form submitted",
                                          sender=app.config.get("MAIL_USERNAME"),
                                          recipients=[app.config.get("MAIL_USERNAME")],
                                          # replace with your email for testing
                                          html="<b>Email<b>: " + session['email'])
                            msg.attach(
                                file.filename,
                                'application/octect-stream',
                                file.read())
                            mail.send(msg)
                            db_fun.form_uploaded(session['email'])
                            return redirect(url_for('submit_registration'))
                        except RuntimeError:
                            return render_template('error_occurred.html')
                    else:
                        flash('Please upload correct file')
                        return redirect(url_for('download_form'))
                else:
                    flash('No participants added')
                    return redirect(url_for('fill_form'))
            else:
                flash('form already submitted')
                return render_template('fill_form.html')
        else:
            return redirect(url_for('login'))
    else:
        return redirect(url_for('login'))


@app.route('/fill_form')
def fill_form():
    if 'status' in session:
        if session['status']:
            return render_template('fill_form.html')
        else:
            return redirect(url_for('login'))
    else:
        return redirect(url_for('login'))


@app.route('/register_participant/<int:user_number>', methods=['POST'])
def register_participant(user_number):
    if 'status' in session:
        if session['status']:
            full_name = (request.form['full_name']).strip()
            age = (request.form['age']).strip()
            phone_number = (request.form['phone_number']).strip()
            email = (request.form['email']).strip()
            qualification = (request.form['qualification']).strip()
            school = (request.form['school']).strip()
            address = (request.form['address']).strip()
            city = (request.form['city']).strip()
            pin_code = (request.form['pin_code']).strip()
            user_data = {"full_name": full_name, 'age': age, 'phone_number': phone_number, 'email': email,
                         'qualification': qualification, 'school': school, 'address': address, 'city': city,
                         'pin_code': pin_code}
            result = db_fun.register_participant(session['email'], user_number, user_data)
            if result:
                flash('Participant added successfully')
            else:
                flash('Participant already added')
            return render_template('fill_form.html')
        else:
            return redirect(url_for('login'))
    else:
        return redirect(url_for('login'))


@app.route('/register')
def register():
    return render_template('register.html')


@app.route('/new_user', methods=["POST"])
def new_user():
    email = (request.form["email"]).strip()
    password = (request.form["password"]).strip()
    session["email"] = email
    user_data = {"_id": email, "password": password}
    result = db_fun.add_new_user(user_data)
    if result:
        flash("You have registered successfully")
        return redirect(url_for('login'))
    else:
        flash("Email is already registered")
        return redirect(url_for('register'))


@app.route('/verify_otp')
def verify_otp():
    if 'email' in session:
        if session['email']:
            return render_template('verify_otp.html')
        else:
            return redirect(url_for('register'))
    else:
        return redirect(url_for('register'))


@app.route('/validating_registration', methods=["POST"])
def validating_registration():
    otp = int((request.form["otp"]).strip())
    result = db_fun.verify_otp(session["email"], otp)
    if result:
        flash("Account successfully created")
        return redirect(url_for('login'))
    else:
        flash("Wrong OTP")
        return redirect(url_for('verify_otp'))


@app.route('/finish_registration')
def finish_registration():
    if 'email' in session:
        if session['email']:
            return render_template('finish.html')
        else:
            return redirect(url_for('login'))
    else:
        return redirect(url_for('login'))


@app.route('/submit_registration')
def submit_registration():
    if 'email' in session:
        if session['email']:
            if db_fun.verify_submission(session['email']):
                print('Completed')
                flash('Registration Already Completed')
                return redirect(url_for('finish_registration'))
            if not db_fun.verify_upload(session['email']):
                flash('Form not Uploaded')
                return redirect(url_for('download_form'))
            if not db_fun.verify_participants(session['email']):
                flash('No participants added')
                return redirect(url_for('fill_form'))
            try:
                msg = Message(subject="New Completed Registration",
                              sender=app.config.get("MAIL_USERNAME"),
                              recipients=[app.config.get("MAIL_USERNAME")],  # replace with your email for testing
                              html=render_template('user_info.html', user_info=db_fun.export_json(session['email'])))
                msg1 = Message(subject="Registration completed successfully",
                               sender=app.config.get("MAIL_USERNAME"),
                               recipients=[session['email']],  # replace with your email for testing
                               html=render_template('congo.html'))
                mail.send(msg)
                mail.send(msg1)
                db_fun.form_upload_done(session['email'])
                return render_template('registration_complete.html')
            except RuntimeError:
                return render_template('error_occurred.html')
        else:
            return redirect(url_for('login'))
    else:
        return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
