import email
import json
import uuid
import secrets
import pyotp
import qrcode
import os
from flask_login import UserMixin
from datetime import datetime

from App import bcrypt
from App.Emails import send_welcome_email, send_resetPassword_email, sendVerificationEmail, sendChangedEmailAdressEmail, sendMFAViaEmail

class User(UserMixin):
    name = None
    email = None
    password = None
    uuid = None
    isEmailVerified = None
    isOTPEnabled = None
    OTPToken = None
    provider = None
    isAdmin = None

    def getUserById(self, id):
        with open('./App/data/users.json', 'r', encoding='utf-8') as f:
            fread = f.read();
            userlist = json.loads(fread)
            for item in userlist:
                if item['uuid'] == id:
                    self.name = item['name']
                    self.email = item['email']
                    self.password = item['password']
                    self.uuid = item['uuid']
                    self.isEmailVerified = item['isEmailVerified']
                    self.isOTPEnabled = item['isOTPEnabled']
                    self.OTPToken = item['OTPToken']
                    self.provider = item['provider']
                    self.isAdmin = item['isAdmin']
                    return True;

        return False

    def getUserByName(self, name):
        with open('./App/data/users.json', 'r', encoding='utf-8') as f:
            fread = f.read();
            userlist = json.loads(fread)
            for item in userlist:
                if item['name'] == name:
                    self.name = item['name']
                    self.email = item['email']
                    self.password = item['password']
                    self.uuid = item['uuid']
                    self.isEmailVerified = item['isEmailVerified']
                    self.isOTPEnabled = item['isOTPEnabled']
                    self.OTPToken = item['OTPToken']
                    self.provider = item['provider']
                    self.isAdmin = item['isAdmin']
                    return True;

        return False;

    def getUserByEmail(self, email):
        with open('./App/data/users.json', 'r', encoding='utf-8') as f:
            fread = f.read();
            userlist = json.loads(fread)
            for item in userlist:
                if item['email'] == email:
                    self.name = item['name']
                    self.email = item['email']
                    self.password = item['password']
                    self.uuid = item['uuid']
                    self.isEmailVerified = item['isEmailVerified']
                    self.isOTPEnabled = item['isOTPEnabled']
                    self.OTPToken = item['OTPToken']
                    self.provider = item['provider']
                    self.isAdmin = item['isAdmin']
                    return True;

        return False;

    def getUserByPasswordResetToken(self, token):
        with open('./App/data/forgot_password.json', 'r') as f:
            fread = f.read()
            fread = json.loads(fread)

        for item in fread:
            if item['token'] == token:
                dt = datetime.now()
                ts = datetime.timestamp(dt)
                if ts - item['time'] < 60*5:
                    self.getUserById(item['uuid'])
                    break

    def getUserByVerifyEmailToken(self, token):
        with open('./App/data/verification_email.json', 'r') as f:
            fread = f.read()
            fread = json.loads(fread)

        for item in fread:
            if item['token'] == token:
                dt = datetime.now()
                ts = datetime.timestamp(dt)
                if ts - item['time'] < 60*5:
                    self.getUserById(item['uuid'])
                    break

    def getUserByMFAVerifyToken(self, token):
        with open('./App/data/mfa_verify.json', 'r') as f:
            fread = f.read()
            fread = json.loads(fread)

        for item in fread:
            if item['token'] == token:
                dt = datetime.now()
                ts = datetime.timestamp(dt)
                if ts - item['time'] < 60*5:
                    self.getUserById(item['uuid'])
                    break

    def isUser(self):
        if self.uuid and self.name and self.email:
            return True;
        else:
            return False;

    def createUser(self, name, email, password, provider="password", isEmailVerified=False, isOTPEnabled=False, OTPToken=None, isAdmin=False):

        with open('./App/data/users.json', 'r', encoding='utf-8') as f:
            fread = f.read();
            userlist = json.loads(fread)

        while True:
            id = str(uuid.uuid4())
            t = User()
            t.getUserById(id)

            if t.isUser() == False: break

        if password:
            password = password+id
            password = bcrypt.generate_password_hash(password).decode('utf-8')

        if not isAdmin:
            isAdmin = makeAdmin(email)

        user = {
            "name": name,
            "email": email,
            "password": password,
            "uuid": id,
            "isEmailVerified": isEmailVerified,
            "isOTPEnabled": isOTPEnabled,
            "OTPToken": OTPToken,
            "provider": provider,
            "isAdmin": isAdmin
        };

        self.name = name
        self.email = email
        self.password = password
        self.uuid = id
        self.isEmailVerified = isEmailVerified
        self.isOTPEnabled = isOTPEnabled
        self.OTPToken = OTPToken
        self.provider = provider
        self.isAdmin = isAdmin

        userlist.append(user)
        fwrite = json.dumps(userlist);

        with open('./App/data/users.json', 'w', encoding='utf-8') as f:
            f.write(fwrite)

        send_welcome_email(self.email, self.name)
        return self

    def send_verification_email(self):
        token = secrets.token_hex(32)
        with open('./App/data/verification_email.json', 'r') as f:
            fread = f.read()
            fread = json.loads(fread)

        dt = datetime.now()
        ts = datetime.timestamp(dt)

        sve = {"token": token,
              "uuid": self.uuid,
              "time": ts}

        fread.append(sve)

        with open('./App/data/verification_email.json', 'w') as f:
            fwrite = json.dumps(fread);
            f.write(fwrite)

        link = f'https://{os.environ["DOMAIN"]}/verifyEmail?token=' + token
        sendVerificationEmail(self.email, self.name, link)

    def verify_email(self):
        self.isEmailVerified = True
        with open('./App/data/users.json', 'r', encoding='utf-8') as f:
            fread = f.read();
            userlist = json.loads(fread)
            i = 0
            for item in userlist:
                if item['uuid'] == self.uuid: break
                i += 1

        userlist[i]['isEmailVerified'] = True
        fwrite = json.dumps(userlist);

        with open('./App/data/users.json', 'w', encoding='utf-8') as f:
            f.write(fwrite)

        with open('./App/data/verification_email.json', 'r') as f:
            fread = f.read()
            fread = json.loads(fread)

        i = 0
        to_pop = []
        for item in fread:
            print(item)
            if item['uuid'] == self.uuid:
                to_pop.append(i)
            i += 1

        itemps_poped = 0
        for i in to_pop:
            fread.pop(i - itemps_poped)
            itemps_poped += 1

        with open('./App/data/verification_email.json', 'w') as f:
            fwrite = json.dumps(fread);
            f.write(fwrite)

    def forgot_password(self):
        token = secrets.token_hex(32)
        with open('./App/data/forgot_password.json', 'r') as f:
            fread = f.read()
            fread = json.loads(fread)

        dt = datetime.now()
        ts = datetime.timestamp(dt)

        fp = {"token": token,
            "uuid": self.uuid,
            "time": ts}

        fread.append(fp)

        with open('./App/data/forgot_password.json', 'w') as f:
            fwrite = json.dumps(fread);
            f.write(fwrite)

        link = f'https://{os.environ["DOMAIN"]}/resetPassword?token=' + token
        send_resetPassword_email(self.email, self.name, link)

    def change_password(self, new_password):
        new_password = new_password + self.uuid
        new_password = bcrypt.generate_password_hash(new_password).decode('utf-8')
        self.password = new_password
        with open('./App/data/users.json', 'r', encoding='utf-8') as f:
            fread = f.read();
            userlist = json.loads(fread)
            i = 0
            for item in userlist:
                if item['uuid'] == self.uuid: break
                i += 1

        userlist[i]['password'] = new_password
        fwrite = json.dumps(userlist);

        with open('./App/data/users.json', 'w', encoding='utf-8') as f:
            f.write(fwrite)

        with open('./App/data/forgot_password.json', 'r') as f:
            fread = f.read()
            fread = json.loads(fread)


        i = 0
        to_pop = []
        for item in fread:
            print(item)
            if item['uuid'] == self.uuid:
                to_pop.append(i)
            i += 1

        itemps_poped = 0
        for i in to_pop:
            fread.pop(i-itemps_poped)
            itemps_poped += 1

        with open('./App/data/forgot_password.json', 'w') as f:
            fwrite = json.dumps(fread);
            f.write(fwrite)

    def change_name(self, new_name):
        with open('./App/data/users.json', 'r', encoding='utf-8') as f:
            fread = f.read();
            userlist = json.loads(fread)
            i = 0
            for item in userlist:
                if item['uuid'] == self.uuid: break
                i += 1

        userlist[i]['name'] = new_name
        self.name = new_name

        fwrite = json.dumps(userlist);

        with open('./App/data/users.json', 'w', encoding='utf-8') as f:
            f.write(fwrite)

    def change_email(self, new_email):
        with open('./App/data/users.json', 'r', encoding='utf-8') as f:
            fread = f.read();
            userlist = json.loads(fread)
            i = 0
            for item in userlist:
                if item['uuid'] == self.uuid: break
                i += 1

        old_email = self.email
        userlist[i]['email'] = new_email
        userlist[i]['isEmailVerified'] = False
        userlist[i]['isOTPEnabled'] = False
        self.email = new_email
        self.isEmailVerified = False
        self.isOTPEnabled = False

        fwrite = json.dumps(userlist);

        with open('./App/data/users.json', 'w', encoding='utf-8') as f:
            f.write(fwrite)

        sendChangedEmailAdressEmail(new_email, old_email, self.name)

    def is_correct_login(self, email, password):
        password = password + self.uuid
        print(password)
        if self.email == email and bcrypt.check_password_hash(self.password, password):
            return True
        else:
            return False

    def delete_account(self):
        with open('./App/data/users.json', 'r', encoding='utf-8') as f:
            fread = f.read();
            userlist = json.loads(fread)
            i = 0
            for item in userlist:
                if item['uuid'] == self.uuid: break
                i += 1

        userlist.pop(i)

        with open('./App/data/users.json', 'w') as f:
            fwrite = json.dumps(userlist);
            f.write(fwrite)

    def create_MFA(self):
        with open('./App/data/users.json', 'r', encoding='utf-8') as f:
            fread = f.read();
            userlist = json.loads(fread)
            i = 0
            for item in userlist:
                if item['uuid'] == self.uuid: break
                i += 1

        token = pyotp.random_base32()
        userlist[i]['OTPToken'] = token
        self.OTPToken = token

        fwrite = json.dumps(userlist);

        with open('./App/data/users.json', 'w', encoding='utf-8') as f:
            f.write(fwrite)

        img = qrcode.make(pyotp.totp.TOTP(token).provisioning_uri(name=self.email, issuer_name='Y210 App'))
        img.save(os.path.abspath(f"App/static/img/qr/{token}.png").replace('\\','/'), "PNG")
        return token

    def enable_mfa(self):
        with open('./App/data/users.json', 'r', encoding='utf-8') as f:
            fread = f.read();
            userlist = json.loads(fread)
            i = 0
            for item in userlist:
                if item['uuid'] == self.uuid: break
                i += 1

        userlist[i]['isOTPEnabled'] = True
        self.isOTPEnabled = True

        fwrite = json.dumps(userlist);

        with open('./App/data/users.json', 'w', encoding='utf-8') as f:
            f.write(fwrite)

    def disable_mfa(self):
        with open('./App/data/users.json', 'r', encoding='utf-8') as f:
            fread = f.read();
            userlist = json.loads(fread)
            i = 0
            for item in userlist:
                if item['uuid'] == self.uuid: break
                i += 1

        userlist[i]['isOTPEnabled'] = False
        self.isOTPEnabled = False
        userlist[i]['OTPToken'] = None
        self.OTPToken = None

        fwrite = json.dumps(userlist);

        with open('./App/data/users.json', 'w', encoding='utf-8') as f:
            f.write(fwrite)

    def send_mfa(self):
        totp = pyotp.TOTP(self.OTPToken)
        code = totp.now()

        with open('./App/data/mfa_via_email.json', 'r') as f:
            fread = f.read()
            fread = json.loads(fread)

        dt = datetime.now()
        ts = datetime.timestamp(dt)

        smfa = {"code": code,
            "uuid": self.uuid,
            "time": ts}

        fread.append(smfa)

        with open('./App/data/mfa_via_email.json', 'w') as f:
            fwrite = json.dumps(fread);
            f.write(fwrite)

        sendMFAViaEmail(self.email, self.name, code)

    def verify_mfa_via_email(self, code):
        with open('./App/data/mfa_via_email.json', 'r') as f:
            fread = f.read()
            fread = json.loads(fread)

        correct_code = False

        i = 0
        to_pop = []
        for item in fread:
            if item['uuid'] == self.uuid:
                to_pop.append(i)
                if not correct_code:
                    dt = datetime.now()
                    ts = datetime.timestamp(dt)
                    if ts - item['time'] < 60*5:
                        correct_code = (item['code'] == code )
            i += 1

        if correct_code:
            itemps_poped = 0
            for i in to_pop:
                fread.pop(i - itemps_poped)
                itemps_poped += 1

            with open('./App/data/mfa_via_email.json', 'w') as f:
                fwrite = json.dumps(fread)
                f.write(fwrite)

            return True
        else:
            return False

    def verify_mfa(self, mfa):
        totp = pyotp.TOTP(self.OTPToken)
        return mfa == totp.now()

    def create_mfa_verify_token(self):
        token = secrets.token_hex(32)
        with open('./App/data/mfa_verify.json', 'r') as f:
            fread = f.read()
            fread = json.loads(fread)

        dt = datetime.now()
        ts = datetime.timestamp(dt)

        mv = {"token": token,
              "uuid": self.uuid,
              "time": ts}

        fread.append(mv)

        with open('./App/data/mfa_verify.json', 'w') as f:
            fwrite = json.dumps(fread);
            f.write(fwrite)

        return token

    def get_id(self):
        return self.uuid

def makeAdmin(email):
    return ("@upatras.gr" in email) or email == "ssveronis@gmail.com"