# Y210-flask-app

### Τίτλος εργασίας: Flask Να χρησιμοποιήσετε το framework για να αναπτύξετε μια φόρμα που επιτρέπει εγγραφές νέων χρηστών σε ιστοσελίδα. Οι χρήστες να αποθηκεύονται σε αρχείο.

Η εργασία αυτή δημιουργήθηκε στο πλαίσιο του μαθήματος Εισαγωγή στην Επιστήμη του Ηλεκτρολόγου Μηχανικού (ECE_Y210) του τμήματος Ηλεκτρολόγων Μηχανικών και Τεχνολογίας Υπολογιστών του Πανεπιστημίου Πατρών.

## Προβλήματα
<ul>
  <li>Το μεγαλύτερο πρόβλημα της εφαρμογής είναι ότι τα html templates σχεδιάστηκαν για υπολογιστή με τον browser σε πλήρη οθόνη (1920x1080) και δεν είναι ευανάγνωστα σε άλλες συνθήκες. (π.χ. κινητό)</li>
  <li>Μερικές φορές όταν ο χρήστης συνδέεται μέσω του λογαριασμού του στο Google επιστρέφεται ένα σφάλμα σύμφωνα με το οποίο το token που επέστρεψε η Google χρησιμοποιήθηκε πολύ νωρίς. Για τον λόγω αυτόν υπάρχει προγραμματιστεί μια μικρή καθυστέρηση των 6 δευτερολέπτων</li>
</ul>

## Live Demo

! [image](https://user-images.githubusercontent.com/62189294/173043044-8cf46749-573f-441a-b2fd-e04698dfcb4a.png)

<ul>
  <li>https://flaskapp.sveronis.net/</li> ή
  <li>https://y210-flask-app.azurewebsites.net/</li>
</ul>

## Εγκατάσταση
Αφού κατεβάσετε τον κώδικα και ενδεχομένως φτιάξετε και ενεργοποιήσετε ένα εικονικό περιβάλλον πρέπει να εγκαταστήσετε τις ακόλουθες βιβλιοθήκες:

<table>
  <tr>
    <th>Library Name</th>
    <th>Version</th>
  </tr>
  <tr>
    <td>bcrypt</td>
    <td>3.2.2</td>
  </tr>
  <tr>
    <td>cachetools</td>
    <td>5.2.0</td>
  </tr>
  <tr>
    <td>certifi</td>
    <td>2022.5.18.1</td>
  </tr>
  <tr>
    <td>cffi</td>
    <td>1.15.0</td>
  </tr>
  <tr>
    <td>charset-normalizer</td>
    <td>2.0.12</td>
  </tr>
  <tr>
    <td>click</td>
    <td>8.1.3</td>
  </tr>
  <tr>
    <td>colorama</td>
    <td>0.4.4</td>
  </tr>
  <tr>
    <td>dnspython</td>
    <td>2.2.1</td>
  </tr>
  <tr>
    <td>email-validator</td>
    <td>1.2.1</td>
  </tr>
  <tr>
    <td>Flask</td>
    <td>2.1.2</td>
  </tr>
  <tr>
    <td>Flask-Bcrypt</td>
    <td>1.0.1</td>
  </tr>
  <tr>
    <td>Flask-Login</td>
    <td>0.6.1</td>
  </tr>
  <tr>
    <td>Flask-WTF</td>
    <td>1.0.1</td>
  </tr>
  <tr>
    <td>google-auth</td>
    <td>2.7.0</td>
  </tr>
  <tr>
    <td>google-auth-oauthlib</td>
    <td>0.5.1</td>
  </tr>
  <tr>
    <td>gunicorn</td>
    <td>20.1.0</td>
  </tr>
  <tr>
    <td>idna</td>
    <td>3.3</td>
  </tr>
  <tr>
    <td>itsdangerous</td>
    <td>2.1.2</td>
  </tr>
  <tr>
    <td>Jinja2</td>
    <td>3.1.2</td>
  </tr>
  <tr>
    <td>MarkupSafe</td>
    <td>2.1.1</td>
  </tr>
  <tr>
    <td>oauthlib</td>
    <td>3.2.0</td>
  </tr>
  <tr>
    <td>pathlib</td>
    <td>1.0.1</td>
  </tr>
  <tr>
    <td>Pillow</td>
    <td>9.1.1</td>
  </tr>
  <tr>
    <td>pyasn1</td>
    <td>0.4.8</td>
  </tr>
  <tr>
    <td>pyasn1-modules</td>
    <td>0.2.8</td>
  </tr>
  <tr>
    <td>pycparser</td>
    <td>2.21</td>
  </tr>
  <tr>
    <td>pyotp</td>
    <td>2.6.0</td>
  </tr>
  <tr>
    <td>python-dotenv</td>
    <td>0.20.0</td>
  </tr>
  <tr>
    <td>qrcode</td>
    <td>7.3.1</td>
  </tr>
  <tr>
    <td>requests</td>
    <td>2.27.1</td>
  </tr>
  <tr>
    <td>requests-oauthlib</td>
    <td>1.3.1</td>
  </tr>
  <tr>
    <td>rsa</td>
    <td>4.8</td>
  </tr>
  <tr>
    <td>six</td>
    <td>1.16.0</td>
  </tr>
  <tr>
    <td>urllib3</td>
    <td>1.26.9</td>
  </tr>
  <tr>
    <td>Werkzeug</td>
    <td>2.1.2</td>
  </tr>
  <tr>
    <td>WTForms</td>
    <td>3.0.1</td>
  </tr>
</table>

το οποίο μπορείτε να κάνετε με την εντολή:
```
pip install -r requirements.txt
```

Στην συνέχεια πρέπει να δώσουμε τιμές στις μεταβλητές που βρίσκονται στο αρχείο `.env`. Δείτε [Μεταβλητές Συστήματος](#)

Είμαστε έτοιμοι!:tada: Τρέχουμε το πρόγραμμά μας `app.py`:
```
python app.py
```

## Μεταβλητές Συστήματος
Στο αρχείο `.env` υπάρχουν οι ακόλουθες μεταβλητές:

<table>
  <tr>
    <th>Όνομα μεταβλητής</th>
    <th>Επεξήγηση</th>
    <th>Αποδεκτές Τιμές</th>
  </tr>
  <tr>
    <td>DEBUG</td>
    <td>TRUE για να τρέξει το Flask σε debug mode. Διαφορετικά False</td>
    <td>TRUE | FALSE</td>
  </tr>
  <tr>
    <td>PORT</td>
    <td>Η πόρτα στην οποιά θα τρέξει η εφαρμογή. Απαιτήται Port Forwarding.</td>
    <td>1 - 65535</td>
  </tr>
  <tr>
    <td>DOMAIN</td>
    <td>Ένα domain ή διεύθυνση IP που να δείχνει στον υπολογιστεί που φιλοξενεί την εφαρμογή. Χρησιμοποιείται κατα την αποστολή των email.</td>
    <td>Ένα domain ή διεύθυνση IP που να δείχνει στον υπολογιστεί που φιλοξενεί την εφαρμογή</td>
  </tr>
  <tr>
    <td>SECRET_KEY</td>
    <td>[Flask Docs](https://flask.palletsprojects.com/en/2.1.x/config/#SECRET_KEY)</td>
    <td>Ένα οποιοδήποτε string</td>
  </tr>
  <tr>
    <td>WTF_CSRF_SECRET_KEY</td>
    <td>[Flask-WTF Docs](https://flask-wtf.readthedocs.io/en/1.0.x/config/)</td>
    <td>Ένα οποιοδήποτε string</td>
  </tr>
  <tr>
    <td>OAUTHLIB_INSECURE_TRANSPORT</td>
    <td>1 για να λειτουργήσει η δυνατότητα σύνδεσης μέσω Google σε περιπτώσεις που δεν υποστηρίζεται https. Διαφορετικά 0</td>
    <td>0 | 1</td>
  </tr>
  <tr>
    <td>EMAIL_FROM_HEADER</td>
    <td>From email header</td>
    <td>Name &lt;soneone@example.com&gt;</td>
  </tr>
  <tr>
    <td>EMAIL_SMTP_SERVER_IP</td>
    <td>Ένα domain η διεύθυνση IP που να δείχνει στον SMTP Server</td>
    <td>Ένα domain η διεύθυνση IP που να δείχνει στον SMTP Server</td>
  </tr>
  <tr>
    <td>EMAIL_SMTP_SERVER_PORT</td>
    <td>Η πόρτα του SMTP Server</td>
    <td>25 | 465 | 587 | 2525</td>
  </tr>
  <tr>
    <td>EMAIL_SMTP_SERVER_LOGIN</td>
    <td>Το usename με τον οποιο πρέπει να γίνει η σύνδεση στον SMTP Server</td>
    <td>Το usename με τον οποιο πρέπει να γίνει η σύνδεση στον SMTP Server</td>
  </tr>
  <tr>
    <td>EMAIL_SMTP_SERVER_PASSWORD</td>
    <td>Ο κωδικός με τον οποιο πρέπει να γίνει η σύνδεση στον SMTP Server</td>
    <td>Ο κωδικός με τον οποιο πρέπει να γίνει η σύνδεση στον SMTP Server</td>
  </tr>
  <tr>
    <td>GOOGLE_CLIENT_ID</td>
    <td>Το string που πείρατε από το Google Cloud Platform</td>
    <td>Το string που πείρατε από το Google Cloud Platform</td>
  </tr>
  <tr>
    <td>GOOGLE_SECRET_FILE</td>
    <td>Η θέση που είναι αποθηκευμένο το αρχείο που κατεβάσατε από το Google Cloud Platform</td>
    <td>Η θέση που είναι αποθηκευμένο το αρχείο που κατεβάσατε από το Google Cloud Platform</td>
  </tr>
  <tr>
    <td>GOOGLE_REDIRECT_URL</td>
    <td>Η διευθυνση στην οποία θα επιστρέφει ο χρήστης αφού συνδεθεί μέσω Google.</td>
    <td>/signInWithGoogle/auth</td>
  </tr>
</table>

## Σύνδεση με Google
Για να λειτουργίσει η δυνατότητα σύνδεσης μέσω Google πρέπει να δηλωθούν στο αρχείο `.env` οι μεταβλητές `GOOGLE_CLIENT_ID` και `GOOGLE_SECRET_FILE`. Για να βρούμε αυτές τις τιμές:

1. Μεταβαίνουμε στο [Google Cloud Platform](https://console.cloud.google.com/)
2. Επιλέγουμε το project που θέλουμε να χρησιμοποιήσουμε ή δημιουργούμε ένα νέο
3. Επιλέγουμε `Navigation menu`>`APIs & Services`>`Credentials`
4. Επιλέγουμε `Create Credentials`>`OAuth client ID`![image](https://user-images.githubusercontent.com/62189294/173060712-6de4e576-9717-4118-85d1-be1d74055528.png)

5. Ίσως σας ζητηθεί να δημιουργίσετε μία `OAuth consent screen`
6. Επιλέγουμε `Application type`:`Web application` και ένα όνομα. ![image](https://user-images.githubusercontent.com/62189294/173060944-b0325ed8-02e9-4d07-97ae-eec1daaf81c7.png)

7. Ως `Authorized redirect URIs` εισάγουμε `https://example.com/signInWithGoogle/auth` ή `http://example.com/signInWithGoogle/auth` αν ή εφαρμογή είναι ακόμα σε testing mode ![image](https://user-images.githubusercontent.com/62189294/173061912-460b8e69-5d91-4451-8b58-318b40ffb278.png)

8. Επιλέγουμε `Create`
9. Στο παράθυρο που εμφανίζεται υπάρχει το `GOOGLE_CLIENT_ID` και μπορούμε να αποθηκεύσουμε το CLIENT SECRET

## Διαχειριστές
Η εφαρμογή γίνεται εύκολα κατανοητη. Αξίζει όμως να αναφέρουμε ότι υπάρχει η σελίδα `/admin` στην οποία έχουν πρόσβαση μόνο οι 'διαχειριστές'. Για να γίνει ένας χρήστης διαχειριστής πρέπει το κλειδί `isAdmin` που αντισοιχεί στον λογαριασμό του, και μπορεί να βρεθεί στο αρχείο `/App/data/users.json`, να είναι ορισμένο σε `true`
