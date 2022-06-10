import os
import pathlib
import requests
import time
import json
from App import app, bcrypt
from flask import render_template, redirect, url_for, session, flash, request, abort
from flask_login import login_user, current_user, logout_user

from google_auth_oauthlib.flow import Flow
from pip._vendor import cachecontrol
from google.oauth2 import id_token
import google.auth.transport.requests

from App.forms import SignUpWithEmailAndPassword, SignInWithEmailAndPassword, ForgotPassword, ResetPassword, ChangePassword, DeleteAccount, DashboardName, DashboardEmail, MFACode, AdminEdit, AdminChange
from App.User import User

GOOGLE_CLIENT_ID = os.environ['GOOGLE_CLIENT_ID']
client_secrets_file = os.environ['GOOGLE_SECRET_FILE']

flow = Flow.from_client_secrets_file(  #Flow is OAuth 2.0 a class that stores all the information on how we want to authorize our users
    client_secrets_file=client_secrets_file,
    scopes=["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email", "openid"],  #here we are specifing what do we get after the authorization
    redirect_uri=f"https://{os.environ['DOMAIN']}{os.environ['GOOGLE_REDIRECT_URL']}"  #and the redirect URI is the point where the user will end up after the authorization
)


@app.route("/")
def root():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return render_template("index.html")

@app.route("/dashboard")
def dashboard():
    if not current_user.is_authenticated:
        flash('To see this page you must login first', 'warning')
        return redirect(url_for('root'))
    footer_type = 'static'
    if not current_user.isEmailVerified:
        flash(f'Your email address {current_user.email} is not verified! Go to the <a href="/dashboard" class="alert-link">dashboard</a> to fix this.', 'warning')

    formName = DashboardName()
    formEmail = DashboardEmail()

    formName.name.data = current_user.name
    formEmail.email.data = current_user.email
    return render_template("dashboard.html", formName=formName, formEmail=formEmail, footer_type=footer_type)

@app.route("/signin")
def signin():
    if current_user.is_authenticated:
        flash('You have already signed in', 'warning')
        return redirect(url_for('dashboard'))
    try:
        form = SignInWithEmailAndPassword()
        hasform = session['form']
        print(hasform)
        if hasform:
            form.email.data = session['form-email-data']
            form.email.errors = session['form-email-err']
            form.password.errors = session['form-password-err']

            keys = ['form', 'form-email-data', 'form-email-err', 'form-password-err']
            for key in keys: session.pop(key)

            flash('Some of your entries seem to be invalid', 'warning')
    except:
        form = SignInWithEmailAndPassword()

    return render_template("signin.html", form=form)

@app.route("/signup")
def signup():
    if current_user.is_authenticated:
        flash('You have already signed in', 'warning')
        return redirect(url_for('dashboard'))
    try:
        form = SignUpWithEmailAndPassword()
        hasform = session['form']
        if hasform:
            form.name.errors = session['form-name-err']
            form.name.data = session['form-name-data']
            form.email.errors = session['form-email-err']
            form.email.data = session['form-email-data']
            form.password.errors = session['form-password-err']
            form.password2.errors = session['form-password2-err']

            keys = ['form', 'form-name-err', 'form-name-data', 'form-email-data', 'form-email-err', 'form-password-err', 'form-password2-err']
            for key in keys: session.pop(key)

            flash('Some of your entries seem to be invalid', 'warning')
    except:
        form = SignUpWithEmailAndPassword()

    return render_template("signup.html", form=form)

@app.route('/logout')
def logout():
    if not current_user.is_authenticated:
        flash('To see this page you must login first', 'warning')
        return redirect(url_for('signin'))
    logout_user()
    flash('You have successfully logged out', 'success')
    return render_template('logout.html')

@app.route("/resetPasswordViaEmail", methods=["GET", "POST"])
def resetPasswordViaEmail():
    if current_user.is_authenticated:
        flash('You have already signed in', 'warning')
        return redirect(url_for('dashboard'))

    form = ForgotPassword()

    if request.method == "POST" and form.validate_on_submit():
        dbUser = User()
        dbUser.getUserByEmail(form.email.data)
        if dbUser.isUser():
            dbUser.forgot_password()
            flash("Great! We will send an email to you to reset your password.", "info")
            return redirect(url_for('signin'))
        else:
            flash("Something went wrong", "warning")
            return render_template('resetPasswordViaEmail.html', form=form)
    else:
        if request.method == "POST":
            flash('Some of your entries seem to be invalid', 'warning')
        return render_template('resetPasswordViaEmail.html', form=form)

@app.route('/resetPassword', methods=["GET", "POST"])
def resetPassword():
    if current_user.is_authenticated:
        flash('You have already signed in', 'warning')
        return redirect(url_for('dashboard'))

    try:
        token = request.args['token']
        dbUser = User()
        dbUser.getUserByPasswordResetToken(token)
        if dbUser.isUser():
            form = ResetPassword()

            if request.method == "POST" and form.validate_on_submit():
                dbUser.getUserByEmail(form.email.data)
                dbUser.change_password(form.password.data)

                flash('Password changed successfully. Please login using your new password', 'success')
                return redirect(url_for('signin'))
            else:
                if request.method == "POST":
                    flash('Some of your entries seem to be invalid', 'warning')
                form.email.data = dbUser.email
                return render_template('resetPassword.html', form=form)
        else:
            flash("The link you clicked doesn't seem to be correct or it has expired", "warning")
            return redirect(url_for('root'))
    except:
        return redirect(url_for('root'))

@app.route('/changePassword', methods=["GET", "POST"])
def changePassword():
    if not current_user.is_authenticated:
        flash('To see this page you must login first', 'warning')
        return redirect(url_for('root'))

    if not current_user.isEmailVerified:
        flash(f'Your email address {current_user.email} is not verified! Go to the <a href="/dashboard" class="alert-link">dashboard</a> to fix this.', 'warning')

    form = ChangePassword()
    dbUser = current_user

    if request.method == "POST" and form.validate_on_submit():
        if dbUser.is_correct_login(current_user.email, form.current_password.data):
            dbUser.change_password(form.password.data)

            flash('Password changed successfully.', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Incorrect current password', 'danger')
            return redirect(url_for('changePassword'))

    else:
        if request.method == "POST":
            flash('Some of your entries seem to be invalid', 'warning')
        return render_template('changePassword.html', form=form)

    return render_template('changePassword.html', form=form)

@app.route('/deleteAccount', methods=["GET", "POST"])
def deleteAccount():
    if not current_user.is_authenticated:
        flash('To see this page you must login first', 'warning')
        return redirect(url_for('root'))

    if not current_user.isEmailVerified:
        flash(f'Your email address {current_user.email} is not verified! Go to the <a href="/dashboard" class="alert-link">dashboard</a> to fix this.', 'warning')

    form = DeleteAccount()
    dbUser = current_user

    if dbUser.provider == "password":
        if request.method == "POST" and form.validate_on_submit():
            if dbUser.is_correct_login(current_user.email, form.current_password.data):
                dbUser.delete_account()

                flash('Your account has been deleted successfully.', 'success')
                logout_user()
                return redirect(url_for('root'))
            else:
                flash('Incorrect current password', 'danger')
                return redirect(url_for('deleteAccount'))
        else:
            if request.method == "POST":
                flash('Some of your entries seem to be invalid', 'warning')
            return render_template('deleteAccount.html', form=form)
    elif request.method == "POST":
        dbUser.delete_account()

        flash('Your account has been deleted successfully.', 'success')
        logout_user()
        return redirect(url_for('root'))

    return render_template('deleteAccount.html', form=form)

@app.route('/sendVerificationEmail')
def sendVerificationEmail():
    if not current_user.is_authenticated:
        flash('To see this page you must login first', 'warning')
        return redirect(url_for('root'))

    if not current_user.isEmailVerified:
        flash(f'Your email address {current_user.email} is not verified! Go to the <a href="/dashboard" class="alert-link">dashboard</a> to fix this.', 'warning')
    else:
        flash(f'Your email address {current_user.email} is already verified!','info')
        return redirect(url_for('root'))


    current_user.send_verification_email()
    flash(f'A verification email has been sent to {current_user.email}.', 'success')
    return render_template('sendVerificationEmail.html')

@app.route('/verifyEmail')
def verifyEmail():
    try:
        token = request.args['token']
        dbUser = User()
        dbUser.getUserByVerifyEmailToken(token)
        if dbUser.isUser():
            dbUser.verify_email()

            flash(f"Your email {dbUser.email} has been verified", 'success')
            return redirect(url_for('root'))
        else:
            flash("The link you clicked doesn't seem to be correct or it has expired", "warning")
            return redirect(url_for('root'))
    except:
        return redirect(url_for('root'))

    return render_template('base.html')

@app.route('/enableMFA', methods=["GET", "POST"])
def enableMFA():
    if not current_user.is_authenticated:
        flash('To see this page you must login first', 'warning')
        return redirect(url_for('root'))

    if not current_user.isEmailVerified:
        flash(f'Your email address {current_user.email} is not verified! Go to the <a href="/dashboard" class="alert-link">dashboard</a> to fix this.', 'warning')
        flash(f'You can\'t enable Multi-factor authentication without a verified email address', 'warning')
        return redirect(url_for('root'))

    if current_user.OTPToken:
        token = current_user.OTPToken
    else:
        token = current_user.create_MFA()

    img = url_for('static', filename=f'/img/qr/{token}.png')

    form = MFACode()

    if request.method == "POST" and form.validate_on_submit():
        if current_user.verify_mfa(form.MFACode.data):
            current_user.enable_mfa()

            flash("Multi-factor authentication has been enabled successfully", "success")
            return redirect(url_for('dashboard'))
        else:
            flash("MFA code is invalid", "danger")
            return render_template('enableMFA.html', token=token, img=img, form=form)
    else:
        return render_template('enableMFA.html', token=token, img=img, form=form)

@app.route('/disableMFA')
def disableMFA():
    if not current_user.is_authenticated:
        flash('To see this page you must login first', 'warning')
        return redirect(url_for('root'))

    current_user.disable_mfa()
    return redirect(url_for('dashboard'))

@app.route('/editMFA')
def editMFA():
    if not current_user.is_authenticated:
        flash('To see this page you must login first', 'warning')
        return redirect(url_for('root'))

    current_user.disable_mfa()
    return redirect(url_for('enableMFA'))

@app.route('/verifyMFA', methods=["GET", "POST"])
def verifyMFA():
    if current_user.is_authenticated:
        flash('You have already signed in', 'warning')
        return redirect(url_for('dashboard'))

    token = request.args['token']

    form = MFACode()
    dbUser = User()
    dbUser.getUserByMFAVerifyToken(token)

    if request.method == "POST" and form.validate_on_submit():
        if dbUser.verify_mfa(form.MFACode.data):
            login_user(dbUser)

            flash(f"Hello {dbUser.name}! Welcome back.", 'success')
            return redirect(url_for('dashboard'))
        else:
            flash("MFA code is invalid", "danger")
            return render_template('verifyMFA.html', form=form, token=token)
    else:
        return render_template('verifyMFA.html', form=form, token=token)

    return render_template('verifyMFA.html', form=form, token=token)

@app.route('/verifyMFAViaEmail', methods=["GET", "POST"])
def verifyMFAViaEmail():
    if current_user.is_authenticated:
        flash('You have already signed in', 'warning')
        return redirect(url_for('dashboard'))

    token = request.args['token']

    form = MFACode()
    dbUser = User()
    dbUser.getUserByMFAVerifyToken(token)

    if request.method == "POST" and form.validate_on_submit():
        if dbUser.verify_mfa_via_email(form.MFACode.data):
            login_user(dbUser)
            dbUser.disable_mfa()

            flash(f"Hello {dbUser.name}! Welcome back.", 'success')
            flash(f"Multi-factor authentication has been disabled", 'warning')
            return redirect(url_for('dashboard'))
        else:
            flash("MFA code is invalid", "danger")
            return render_template('verifyMFAViaEmail.html', form=form, token=token)
    elif request.method == "POST":
        return render_template('verifyMFAViaEmail.html', form=form, token=token)

    dbUser.send_mfa()
    flash('The email has been sent', 'info')

    return render_template('verifyMFAViaEmail.html', form=form, token=token)

@app.route("/signUpWithEmailAndPassword", methods=["POST"])
def signUpWithEmailAndPassword():
    form = SignUpWithEmailAndPassword()

    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        password = form.password.data
        password2 = form.password2.data

        new_user = User().createUser(name, email, password)

        flash(f"Hello {new_user.name}! Your account has been created!", 'success')
        login_user(new_user)

        return redirect(url_for('sendVerificationEmail'))
    else:
        session['form'] = True
        session['form-name-err'] = form.name.errors
        session['form-name-data'] = form.name.data
        session['form-email-err'] = form.email.errors
        session['form-email-data'] = form.email.data
        session['form-password-err'] = form.password.errors
        session['form-password2-err'] = form.password2.errors
        return redirect(url_for('signup'))

@app.route('/signinWithEmailAndPassword', methods=["POST"])
def signinWithEmailAndPassword():
    form = SignInWithEmailAndPassword()

    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        dbUser = User()
        dbUser.getUserByEmail(email)

        if dbUser.isUser() and dbUser.is_correct_login(email, password):
            if dbUser.isOTPEnabled:
                return redirect(url_for('verifyMFA',token=dbUser.create_mfa_verify_token()))
            else:
                flash(f"Hello {dbUser.name}! Welcome back.", 'success')
                login_user(dbUser)
                return redirect(url_for('root'))
        else:
            flash("Incorrect password", 'danger')
            return redirect(url_for('signin'))

    else:
        session['form'] = True
        session['form-email-err'] = form.email.errors
        session['form-email-data'] = form.email.data
        session['form-password-err'] = form.password.errors
        return redirect(url_for('signin'))

@app.route('/signInWithGoogle')
def signInWithGoogle():
    authorization_url, state = flow.authorization_url()  # asking the flow class for the authorization (login) url
    session["state"] = state
    return redirect(authorization_url)

@app.route('/signInWithGoogle/auth')
def signInWithGoogleAuth():
    flow.fetch_token(authorization_response=request.url)

    if not session["state"] == request.args["state"]:
        abort(500)  # state does not match!

    credentials = flow.credentials
    request_session = requests.session()
    cached_session = cachecontrol.CacheControl(request_session)
    token_request = google.auth.transport.requests.Request(session=cached_session)

    time.sleep(6)

    id_info = id_token.verify_oauth2_token(
        id_token=credentials._id_token,
        request=token_request,
        audience=GOOGLE_CLIENT_ID
    )

    print(id_info)
    dbUser = User()
    if dbUser.getUserByEmail(id_info["email"]):
        if dbUser.isOTPEnabled:
            return redirect(url_for('verifyMFA', token=dbUser.create_mfa_verify_token()))
        else:
            flash(f"Hello {dbUser.name}! Welcome back.", 'success')
            login_user(dbUser)
            return redirect(url_for('root'))
    else:
        dbUser.createUser(id_info["name"], id_info["email"], None, provider="Google", isEmailVerified=id_info["email_verified"], isOTPEnabled=False, OTPToken=None)
        flash(f"Hello {dbUser.name}! Welcome back.", 'success')
        login_user(dbUser)

        return redirect(url_for('root'))

@app.route('/changeName', methods=["POST"])
def changeName():
    formName = DashboardName()
    if formName.validate_on_submit():
        current_user.change_name(formName.name.data)
        flash(f'Your name has been changed to {formName.name.data} successfully.', 'success')
    else:
        flash('Some of your entries seem to be invalid', 'warning')
    return redirect(url_for('dashboard'))

@app.route('/changeEmail', methods=["POST"])
def changeEmail():
    formEmail = DashboardEmail()
    if formEmail.validate_on_submit():
        current_user.change_email(formEmail.email.data)
        flash(f'Your email has been changed to {formEmail.email.data} successfully.', 'success')
    else:
        flash('Some of your entries seem to be invalid', 'warning')
    return redirect(url_for('dashboard'))

@app.route('/admin')
def admin():
    if not current_user.is_authenticated or not current_user.isAdmin:
        flash('You are not allowed to access this page', 'warning')
        return redirect(url_for('root'))

    with open('./App/data/users.json', 'r') as f:
        users = f.read()
        users = json.loads(users)
    return render_template('admin.html', users=users)

@app.route('/admin/edit', methods=["GET", "POST"])
def adminEdit():
    if not current_user.is_authenticated or not current_user.isAdmin:
        flash('You are not allowed to access this page', 'warning')
        return redirect(url_for('root'))

    uuid = request.args['user']
    item = request.args['item']

    form = AdminEdit()

    if request.method == "POST" and form.validate_on_submit():
        uuid = form.user.data
        item = form.item.data
        value = form.value.data

        dbUser = User()
        if item == "Name":
            dbUser.getUserById(uuid)
            dbUser.change_name(value)
            flash('The name has been changed successfully', 'success')
        elif item == "Email":
            dbUser.getUserById(uuid)
            dbUser.change_email(value)
            flash('The email address has been changed successfully', 'success')
        else:
            flash('Operation failed', 'danger')

        return redirect(url_for('admin'))

    form.user.data = uuid
    form.item.data = item

    return render_template('adminEdit.html', item=item, uuid=uuid, form=form)

@app.route('/admin/change', methods=["GET", "POST"])
def adminChange():
    if not current_user.is_authenticated or not current_user.isAdmin:
        flash('You are not allowed to access this page', 'warning')
        return redirect(url_for('root'))

    uuid = request.args['user']
    item = request.args['item']

    form = AdminChange()

    if request.method == "POST" and form.validate_on_submit():
        uuid = form.user.data
        item = form.item.data

        dbUser = User()
        if item == "Disable MFA":
            dbUser.getUserById(uuid)
            dbUser.disable_mfa()
            flash('Multi-factor authentication has successfully been disabled', 'success')
        elif item == "Delete Account":
            dbUser.getUserById(uuid)
            dbUser.delete_account()
            flash('Account deleted successfully', 'success')
        else:
            flash('Operation failed', 'danger')

        return redirect(url_for('admin'))

    form.user.data = uuid
    form.item.data = item

    return render_template('adminChange.html', item=item, uuid=uuid, form=form)