import math
import os
from io import BytesIO
from werkzeug.utils import secure_filename
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash, send_file, abort
import pymysql
from datetime import datetime, date

con = pymysql.connect(host="localhost", port=3306, user="root", passwd="root", db="buk")
cmd = con.cursor()

buk = Flask(__name__)
buk.secret_key = "nokkanda"

buk.config['UPLOAD_FOLDER'] = 'static/digRes/'  # Directory to save uploaded files
buk.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Limit file size to 16MB

# Allowed file extensions
ALLOWED_EXTENSIONS = {'pdf', 'txt', 'doc', 'docx'}


@buk.route('/')
def opening():
    return render_template('LoginPage.html')


@buk.route('/login', methods=['get', 'post'])
def login():
    usr = request.form['uname']
    pss = request.form['pass']


    cmd.execute("select * from login where username='" + usr + "' and password='" + pss + "' ")
    result = cmd.fetchone()
    print(result)

    if result is not None:
        cmd.execute("select * from login where lid='" + str(result[0]) + "'")
        lresult = cmd.fetchone()
        print(lresult)

        usertype = lresult[3]

        session['lid'] = result[0]
        session['usr'] = result[1]

        if usertype == 'fuser':
            return redirect(url_for('fUserHome'))
        elif usertype == 'puser':
            return redirect(url_for('pUserHome'))
        elif usertype == 'lib':
            return redirect(url_for('libHome'))
        elif usertype == 'admin':
            return redirect(url_for('adminHome'))

    else:
        return "<script>alert('Incorrect Password or Username');window.location='/'</script>"


# Library home age loading
@buk.route('/libHome', methods=['GET', 'POST'])
def libHome():
    lid = str(session.get('lid'))
    usr = session.get('usr')

    return render_template('libHome.html', lid=lid, usr=usr)


# pUserHome home age loading
@buk.route('/pUserHome', methods=['GET', 'POST'])
def pUserHome():
    lid = str(session.get('lid'))
    usr = session.get('usr')

    return render_template('pUserHome.html', lid=lid, usr=usr)


# fUserHome home age loading
@buk.route('/fUserHome', methods=['GET', 'POST'])
def fUserHome():
    lid = str(session.get('lid'))
    usr = session.get('usr')

    return render_template('fUserHome.html', lid=lid, usr=usr)


# Admin home age loading
@buk.route('/adminHome', methods=['GET', 'POST'])
def adminHome():
    lid = str(session.get('lid'))
    usr = session.get('usr')

    return render_template('adminHome.html', lid=lid, usr=usr)


@buk.route('/signuppage', methods=['GET', 'POST'])
def signuppage():
    return render_template('SignupPage.html')


@buk.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form.get('name', '')
        age = request.form.get('dob', '')
        gen = request.form.get('gender', '')
        email = request.form.get('email', '')
        phone = request.form.get('phone', '')
        usrname = request.form.get('username', '')
        password = request.form.get('password', '')

        utype = 'fuser'
        libname = 'nil'

        # If the user is signing up as a library user
        if gen == 'lib':
            utype = 'lib'
            libname = 'lib'

        # Check if the username already exists
        cmd.execute("SELECT * FROM `login` WHERE `username`=%s", (usrname,))
        result = cmd.fetchone()
        print(f" usr result = {result}")

        if result is None:
            # Insert into `login` table with parameterized query
            cmd.execute("INSERT INTO `login` (username, password, usertype, report, plib) VALUES (%s, %s, %s, %s, %s)",
                        (usrname, password, utype, 0, 0))
            lid = con.insert_id()  # Get the inserted login ID

            # Insert into `users` table with parameterized query
            cmd.execute("""
                INSERT INTO `users` (lid, name, dob, gender, status, email, phone, photo, utype)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (lid, name, age, gen, 0, email, phone, 'nopfp.jpg', utype))

            con.commit()  # Commit the changes to the database

            return "<script>alert('Sign-up Successful');window.location='/'</script>"
        else:
            return "<script>alert('This Username is Already Taken, Please Create a New Username');window.location='/signup'</script>"

    else:
        # Clean up any rows with NULL values in 'lid' (just in case)
        cmd.execute("DELETE FROM `users` WHERE `lid` IS NULL")
        cmd.execute("DELETE FROM `login` WHERE `lid` IS NULL")
        con.commit()
        return render_template('SignupPage.html')


@buk.route('/addUserlib')
def addUserlib():
    lid = str(session.get('lid'))
    usr = session.get('usr')
    return render_template('addUser.html')


@buk.route('/addUser', methods=['GET', 'POST'])
def addUser():
    lid = str(session.get('lid'))  # Assuming 'lid' is the logged-in user's ID
    usr = session.get('usr')  # Assuming 'usr' is the logged-in username

    if request.method == 'POST':
        name = request.form.get('name', '')
        age = request.form.get('dob', '')
        gen = request.form.get('gender', '')
        email = request.form.get('email', '')
        phone = request.form.get('phone', '')
        username = request.form.get('username', '')
        password = request.form.get('password', '')

        utype = 'puser'

        # Check if the username already exists in the 'login' table
        cmd.execute("SELECT * FROM `login` WHERE `username`=%s", (username,))
        result = cmd.fetchone()
        print(f" usr result = {result}")

        if result is None:
            # Insert into 'login' table using parameterized query
            cmd.execute("""
                INSERT INTO `login` (username, password, usertype, report, plib)
                VALUES (%s, %s, %s, %s, %s)
            """, (username, password, utype, 0, lid))
            con.commit()  # Commit the changes to the 'login' table

            # Get the ID of the last inserted row
            cmd.execute("SELECT lid FROM `login` WHERE `username`=%s", (username,))
            uid = cmd.fetchone()

            # Insert into 'users' table using parameterized query
            cmd.execute("""
                INSERT INTO `users` (lid, name, dob, gender, status, email, phone, photo, utype)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (uid, name, age, gen, 0, email, phone, 'nopfp.jpg', utype))

            con.commit()  # Commit the changes to the 'users' table

            return "<script>alert('User added successfully!');window.location='/addUserlib'</script>"

        else:
            cmd.execute("DELETE FROM `users` WHERE `lid` IS NULL")
            cmd.execute("DELETE FROM `login` WHERE `username` IS NULL")
            con.commit()
            return "<script>alert('This Username is Already Taken, Please Create a New Username');window.location='/addUserlib'</script>"

    else:
        # Clean up any rows with NULL values in 'lid' (just in case)
        cmd.execute("DELETE FROM `users` WHERE `lid` IS NULL")
        cmd.execute("DELETE FROM `login` WHERE `username` IS NULL")
        con.commit()

        # Return the signup page template
        return render_template('SignupPage.html')


@buk.route('/addDigBook')
def pdfUpload():
    lid = str(session.get('lid'))
    usr = session.get('usr')
    return render_template('pdfUpload.html', lid=lid)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@buk.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':

        lid = str(session.get('lid'))
        usr = session.get('usr')

        # Check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)

        file = request.files['file']

        # If the user does not select a file, browser also
        # submits an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        # Check if the file is allowed
        if file and allowed_file(file.filename):

            # Handle form data (book details)
            bname = request.form.get('bname')
            btype = request.form.get('btype')
            bauthor = request.form.get('bauthor')
            blang = request.form.get('blang')
            disc = request.form.get('disc')

            # Secure the filename and save it to the UPLOAD_FOLDER
            filename = secure_filename(file.filename)
            file_path = os.path.join(buk.config['UPLOAD_FOLDER'], filename)

            cmd.execute("SELECT COUNT(*) FROM `digbooks` WHERE bname = '" + bname + "'")
            book = cmd.fetchone()[0]

            if book > 0:
                return "<script>alert('Book already exists');window.location='/addDigBook'</script>"
            file_data = file.read()
            ext = os.path.splitext(file.filename)[1].lower()
            print(ext)
            file.save('static/digRes/' + filename)

            cmd.execute(
                "INSERT INTO digbooks (bname, btype, bauthor, blang, bcap, lid, fname, path, ext, fdata) \
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)\
                ", (bname, btype, bauthor, blang, disc, lid, f"{bname}{lid}", file_path, ext, file_data)
            )
            con.commit()

            return "<script>alert('Upload Successful');window.location='/addDigBook'</script>"
        else:
            flash('Invalid file type')
            return redirect(request.url)

    return render_template('pdfUpload.html')


@buk.route('/inout')
def inout():
    return render_template('InOut.html')


# Route to handle form submission
@buk.route('/check_value', methods=['POST'])
def check_value():
    libid = str(session.get('lid'))
    usr = session.get('usr')

    lid = request.form.get('lid')

    # Query to check if username exists
    cmd.execute("SELECT COUNT(*) FROM login WHERE lid = '" + lid + "'")
    i = cmd.fetchone()[0]

    # Determine message based on result
    if i > 0:
        cmd.execute("SELECT * FROM login WHERE lid = '" + lid + "'")
        lresult = cmd.fetchone()
        cmd.execute("SELECT * FROM users WHERE lid = '" + lid + "'")
        uresult = cmd.fetchone()[5]

        zero = 0
        one = 1

        entry = "0"
        out = "0"

        if uresult == 0:
            entry = datetime.now().time()
            cmd.execute("UPDATE users SET status = '" + "1" + "' WHERE lid = '" + lid + "'")
            con.commit()

        else:
            out = datetime.now().time()
            cmd.execute("UPDATE users SET status = '" + "0" + "' WHERE lid = '" + lid + "'")
            con.commit()

        cmd.execute("INSERT INTO `entry` VALUES(NULL, '" + str(lresult[0]) + "', '" + str(lresult[1]) + "',\
         '" + str(entry) + "', '" + str(out) + "', '" + str(date.today()) + "','" + libid + "')")
        con.commit()
        message = "Operation successfull!"

    else:
        message = "Operation failed!"

    return jsonify(message=message)


@buk.route('/addPhyBook')
def addPhyBook():
    return render_template('addPhyBook.html')


@buk.route('/phyBookUpload', methods=['GET', 'POST'])
def phyBookUpload():
    try:
        lid = str(session.get('lid'))
        usr = session.get('usr')

        # Retrieve form data
        # file = request.files.get('file')  # Single file uploaded under 'file' key
        bname = request.form.get('bname')  # Book name
        btype = request.form.get('btype')  # Book type (e.g., genre)
        bauthor = request.form.get('bauthor')  # Author of the book
        blang = request.form.get('blang')  # Language of the book
        disc = request.form.get('disc')  # Description of the book

        # if not file or file.filename == '':
        #    return "No file selected for uploading", 400

        cmd.execute("SELECT * FROM `phybooks` WHERE `bname`='" + bname + "' AND 'lid'='" + lid + "'")
        result = cmd.fetchone()

        if result is None:
            # Insert the main book record into the database
            cmd.execute("""
                        INSERT INTO phybooks (bname, btype, bauthor, blang, bcap, lid)
                        VALUES (%s, %s, %s, %s, %s, %s)
                    """, (bname, btype, bauthor, blang, disc, lid))

            # Get the book's unique ID after insertion
            book_id = str(con.insert_id())
            con.commit()

            # Redirect to user home after successful upload
            return redirect(url_for('addPhyBook'))
        else:
            return "<script>alert('This Username is Already Taken, Please Create a New Username');window.location='/addPhyBook'</script>"

    except Exception as e:
        # Handle any errors that occur
        print(f"Error occurred during file upload: {e}")
        return "An error occurred while uploading the book", 500


@buk.route('/searchUser', methods=['GET', 'POST'])
def searchUser():
    lid = str(session.get('lid'))
    usr = session.get('usr')

    uname = request.form.get('searchInput')
    cmd.execute("SELECT * FROM login WHERE username = '" + str(uname) + "' ")
    res = cmd.fetchone()
    print(res)

    if res[3] == "puser":
        usertype = "Library Member"
    elif res[3] == "fuser":
        usertype = "Free User"
    else:
        usertype = "library"

    return render_template('searchUser.html', uid=res[0], username=res[1], usertype=usertype)


@buk.route('/search')
def search():
    return render_template('searchUser.html')


@buk.route('/editProfUser/<uid>', methods=['GET', 'POST'])
def editProfUser(uid):
    lid = str(session.get('lid'))
    usr = session.get('usr')
    # uid = request.form['uid']
    # uid = request.args.get('uid')

    print(uid)
    cmd.execute("SELECT * FROM `login` WHERE `lid` = '" + uid + "' ")
    lresult = cmd.fetchone()
    cmd.execute("SELECT * FROM `users` WHERE `lid`='" + uid + "' ")
    uresult = cmd.fetchone()

    return render_template('editProfLibUser.html', uid=lresult[0], name=uresult[2], email=uresult[6],
                           phone=uresult[7], dob=uresult[3], gen=uresult[4], username=lresult[1],
                           passw=lresult[2])


@buk.route('/editSelfLayout', methods=['GET', 'POST'])
def editSelfLayout():
    lid = str(session.get('lid'))
    usr = session.get('usr')
    # uid = request.form['uid']
    # uid = request.args.get('uid')

    print(lid)
    cmd.execute("SELECT * FROM `login` WHERE `lid` = '" + lid + "' ")
    lresult = cmd.fetchone()
    cmd.execute("SELECT * FROM `users` WHERE `lid`='" + lid + "' ")
    uresult = cmd.fetchone()

    return render_template('editSelfProf.html', uid=lresult[0], name=uresult[2], email=uresult[6],
                           phone=uresult[7], dob=uresult[3], gen=uresult[4], username=lresult[1],
                           passw=lresult[2])


@buk.route('/editSelfPforFun', methods=['GET', 'POST'])
def editSelfPforFun():
    if request.method == 'POST':
        lid = str(session.get('lid'))

        name = request.form['name']
        age = request.form['dob']
        gen = request.form.get('gender')
        email = request.form['email']
        phone = request.form['phone']
        usrname = request.form['username']
        password = request.form['password']

        cmd.execute("SELECT lid, username FROM `login`")
        result = cmd.fetchall()
        print(result)
        res = 0
        for i in result:
            if i[1] == usrname and i[0] != lid:
                res = 1
            else:
                res = 0

        if res == 0:
            cmd.execute(
                "UPDATE login SET username = '" + usrname + "',password = '" + password + "' WHERE lid = '" + lid + "' ")
            cmd.execute("UPDATE users SET name = '" + name + "', dob = '" + age + "', gender = '" + str(
                gen) + "', email = '" + email + "', phone = '" + phone + "' WHERE lid = '" + lid + "' ")
            con.commit()
            return "<script>alert('Update Successful');window.location='/reHome'</script>"

        else:
            return "<script>alert('This Username is Already Taken, Please Create a New Username');window.location='/reHome'</script>"
    else:
        cmd.execute("DELETE FROM `users` WHERE `lid` IS NULL")
        cmd.execute("DELETE FROM `login` WHERE `username` IS NULL")
        con.commit()
        return redirect(url_for('reHome'))


@buk.route('/editProfFunc/<uid>', methods=['GET', 'POST'])
def editProfFunc(uid):
    if request.method == 'POST':
        lid = str(session.get('lid'))
        print(uid, " Update")

        name = request.form['name']
        age = request.form['dob']
        gen = request.form.get('gender')
        email = request.form['email']
        phone = request.form['phone']
        usrname = request.form['username']
        password = request.form['password']

        cmd.execute("SELECT username FROM `login` WHERE lid <> '" + uid + "'")
        result = cmd.fetchall()
        print(result)
        res = 0
        for i in result:
            if i == usrname:
                res = 1
                break
            else:
                res = 0

        if res == 0:
            cmd.execute(
                "UPDATE login SET username = '" + usrname + "',password = '" + password + "' WHERE lid = '" + uid + "' ")
            cmd.execute("UPDATE users SET name = '" + name + "', dob = '" + age + "', gender = '" + str(
                gen) + "', email = '" + email + "', phone = '" + phone + "' WHERE lid = '" + uid + "' ")
            con.commit()
            return "<script>alert('Update Successful');window.location='/reHome'</script>"

        else:
            return "<script>alert('This Username is Already Taken, Please Create a New Username');window.location='/reHome/{{ lid }}'</script>"
    else:
        cmd.execute("DELETE FROM `users` WHERE `lid` IS NULL")
        cmd.execute("DELETE FROM `login` WHERE `username` IS NULL")
        con.commit()
        return redirect(url_for('search'))


@buk.route('/delUser/<uid>', methods=['GET', 'POST'])
def delUser(uid):
    cmd.execute("DELETE FROM `login` WHERE `lid`='" + uid + "' ")
    cmd.execute("DELETE FROM `users` WHERE `lid`='" + uid + "' ")
    con.commit()

    return "<script>alert('User Deleted');window.location='/search'</script>"


@buk.route('/editSelfProf', methods=['GET', 'POST'])
def editSelfProf():
    lid = str(session.get('lid'))
    if not lid:
        return redirect('/login')  # Redirect if session does not contain a user ID

    try:
        # Use parameterized queries to avoid SQL injection
        cmd.execute("SELECT * FROM `login` WHERE `lid` = '" + lid + "' ")
        lresult = cmd.fetchone()
        cmd.execute("SELECT * FROM `users` WHERE `lid`='" + lid + "' ")
        uresult = cmd.fetchone()

        return render_template('editSelfProf.html', lid=lid, uid=lresult[0], name=uresult[2], email=uresult[6],
                               phone=uresult[7], dob=uresult[3], gen=uresult[4], username=lresult[1],
                               passw=lresult[2])
    except Exception as e:
        print("An error occurred:", e)
        return "<script>alert('Error occured!');window.location='/reHome'</script>"


@buk.route('/reHome', methods=['get', 'post'])
def reHome():
    lid = str(session.get('lid'))

    cmd.execute("select * from login where lid='" + lid + "'")
    result = cmd.fetchone()

    if result is not None:
        cmd.execute("select * from users where lid='" + str(result[0]) + "'")
        lresult = cmd.fetchone()

        usertype = lresult[9]

        if usertype == 'fuser':
            return redirect(url_for('fUserHome'))
        elif usertype == 'puser':
            return redirect(url_for('pUserHome'))
        elif usertype == 'lib':
            return redirect(url_for('libHome'))
        elif usertype == 'admin':
            return redirect(url_for('adminHome'))
        else:
            return "<script>alert('Error occured while loading!');window.location='/'</script>"


@buk.route('/searchPhyBook', methods=['get', 'post'])
def searchPhyBook():
    return render_template('searchPhyBook.html')


@buk.route('/view_file/<bid>')
def view_file(file_id):

    # Retrieve the file information
    query = "SELECT path, fname, ext FROM digbooks WHERE id = %s"
    cmd.execute(query, (file_id,))
    result = cmd.fetchone()

    if result:
        path, filename, file_ext = result
        file_path = os.path.join('static', path)

        # Check if file exists
        if os.path.exists(file_path):
            return render_template('view_file.html', file_path=file_path, file_ext=file_ext)
        else:
            return "File not found", 404
    else:
        return "File not found", 404

@buk.route('/searchPhyBookFunc', methods=['GET', 'POST'])
def searchPhyBookFunc():
    lid = str(session.get('lid'))
    usr = session.get('usr')

    bname = request.form.get('searchInput')
    cmd.execute("SELECT * FROM `phybooks` WHERE bname = '" + str(bname) + "' ")
    res = cmd.fetchall()
    upBy = ()

    if res is not None:
        for i in res:
            cmd.execute("SELECT name FROM `users` WHERE lid = '" + str(i[6]) + "' ")
            upBy = upBy + cmd.fetchone()

        return render_template('searchPhyBook.html', res=res, upBy=upBy, view="0", lid=lid)

    else:
        flash('File not found!')
        return "<script>alert('Book not found!');window.location='/searchPhyBook'</script>"


@buk.route('/inoutList')
def inoutList():
    return render_template('listOfVisits.html')


@buk.route('/inoutListFunc', methods=['GET', 'POST'])
def inoutListFunc():
    lid = str(session.get('lid'))
    usr = session.get('usr')

    uid = request.form.get('searchInput')
    cmd.execute("SELECT * FROM `users` WHERE lid = '" + str(uid) + "' ")
    uuser = cmd.fetchone()
    cmd.execute("SELECT * FROM `login` WHERE lid = '" + str(uid) + "' ")
    luser = cmd.fetchone()
    cmd.execute("SELECT * FROM `entry` WHERE lid = '" + str(uid) + "' ")
    res = cmd.fetchall()

    if res is not None:
        return render_template('listOfVisits.html', res=list(res), uuser=uuser, luser=luser, view="1")
    else:
        flash('File not found!')
        return "<script>alert('Book not found!');window.location='/inoutList'</script>"


@buk.route('/viewNoti', methods=['GET', 'POST'])
def viewNoti():
    lid = str(session.get('lid'))
    usr = session.get('usr')

    #user = ()

    notify = ()
    cmd.execute("SELECT * FROM `notification`")
    notif = cmd.fetchall()
    for i in notif:
        tday = date.today()
        eday = i[6]
        d1 = datetime.strptime(str(tday), "%Y-%m-%d")
        d2 = datetime.strptime(str(eday), "%Y-%m-%d")

        if d1 < d2:
            notify = notify + (i,)

    ls = ()

    for i in notify:
        cmd.execute("SELECT usertype FROM `login` WHERE lid = '" + str(i[4]) + "'")
        ut = cmd.fetchone()

        if i[4] == lid or ut == "admin":
            ls = ls + (1,)
        else:
            ls = ls + (0,)

    return render_template('listOfNotif.html', notif=notify, lid=lid, ls=ls)

@buk.route('/createNoti', methods=['GET', 'POST'])
def createNoti():
    return render_template('createNoti.html')


@buk.route('/createNotiFunc', methods=['GET', 'POST'])
def createNotiFunc():
    lid = str(session.get('lid'))
    usr = session.get('usr')

    if request.method == 'POST':
        head = request.form['head']
        disc = request.form['disc']
        contact = request.form['contact']
        ldate = request.form['ldate']

        cmd.execute("INSERT INTO `notification`VALUES(NULL, %s, %s, %s, %s, %s, %s)",
                    (head, disc, contact, lid, str(date.today()), ldate))
        con.commit()
        return "<script>alert('Notification uploaded successfully!');window.location='/noti'</script>"
    else:
        return "<script>alert('Error occured!');window.location='/reHome'</script>"

@buk.route('/editNotiList', methods=['GET', 'POST'])
def editNotiList():
    lid = str(session.get('lid'))
    usr = session.get('usr')

    cmd.execute("SELECT usertype FROM `login` WHERE lid = '" + str(lid) + "'")
    user = cmd.fetchone()

    cmd.execute("SELECT * FROM `notification` WHERE upid = '" + str(lid) + "'")
    notif = cmd.fetchall()

    print(notif)

    dformat = "%Y-%m-%d"
    notify = ()
    for i in notif:
        tday = date.today()
        eday = i[6]
        d1 = datetime.strptime(str(tday), "%Y-%m-%d")
        d2 = datetime.strptime(str(eday), "%Y-%m-%d")

        if d1 < d2:
            notify = notify + (i,)

    print(notify)

    return render_template('editNotificationList.html', notif=notify, user=user, lid=lid)

@buk.route('/editNotif/<nid>', methods=['GET', 'POST'])
def editNotif(nid):

    cmd.execute("SELECT * FROM `notification` WHERE `nid` ='" + nid + "' ")
    uresult = cmd.fetchone()

    return render_template('editNoti.html', uresult=uresult)

@buk.route('/updateNoti/<nid>', methods=['GET', 'POST'])
def updateNoti(nid):
    if request.method == 'POST':
        head = request.form['head']
        disc = request.form['disc']
        contact = request.form['contact']
        ldate = request.form['ldate']

        cmd.execute("UPDATE `notification` SET (head, disc, contact, ldate) VALUES( %s, %s, %s, %s",
                    (head, disc, contact, ldate))
        con.commit()
        return "<script>alert('Notification updated successfully!');window.location='/noti'</script>"
    else:
        return "<script>alert('Error occured!');window.location='/reHome'</script>"

@buk.route('/searchDigBook', methods=['GET', 'POST'])
def searchDigBook():
    return render_template('searchDigBook.html')

@buk.route('/searchDigBookFunc', methods=['GET', 'POST'])
def searchDigBookFunc():
    lid = str(session.get('lid'))
    usr = session.get('usr')

    bname = request.form.get('searchInput')
    cmd.execute("SELECT * FROM `digbooks` WHERE bname = '" + str(bname) + "' ")
    res = cmd.fetchall()
    upBy = ()
    li = []
    c = int(len(res))
    print("res: ", res)

    if res is not None:
        for i in res:
            cmd.execute("SELECT name FROM `users` WHERE lid = '" + str(i[6]) + "' ")
            upBy = upBy + (cmd.fetchone(),)

        return render_template('searchPhyBook.html', res=res, upBy=upBy, view="0")


    else:
        flash('File not found!')
        return "<script>alert('Book not found!');window.location='/searchPhyBook'</script>"

@buk.route('/editDigBook/<bid>', methods=['GET', 'POST'])
def editDigBook(bid):

    print(bid)

    cmd.execute("SELECT * FROM `digbooks` WHERE `bid` ='" + str(bid) + "' ")
    uresult = cmd.fetchone()

    return render_template('editDigBook.html', uresult=uresult)


@buk.route('/editPhyBookSearch', methods=['GET', 'POST'])
def editPhyBookSearch():
    return render_template('editPhyBookSearch.html')

@buk.route('/editPhyBookSearchFunc', methods=['GET', 'POST'])
def editPhyBookSearchFunc():
    lid = str(session.get('lid'))
    usr = session.get('usr')

    bname = request.form.get('searchInput')
    cmd.execute("SELECT * FROM `phybooks` WHERE bname = '" + str(bname) + "' AND lid = '" + str(lid) + "' ")
    res = cmd.fetchall()
    upBy = ()

    if res is not None:
        for i in res:
            cmd.execute("SELECT name FROM `users` WHERE lid = '" + str(i[6]) + "' ")
            upBy = upBy + cmd.fetchone()

        return render_template('editPhyBookSearch.html', res=res, upBy=upBy, view="0", lid=lid)

    else:
        flash('File not found!')
        return "<script>alert('Book not found!');window.location='/searchPhyBook'</script>"

@buk.route('/editPhyBook', methods=['GET', 'POST'])
def editPhyBook():
    if request.method == 'POST':
        lid = str(session.get('lid'))

        bid = request.form.get('bid')
        print(bid)

        cmd.execute("SELECT * FROM `phybooks` WHERE bid = '" + str(bid) + "' AND lid = '" + str(lid) + "'")
        result = cmd.fetchone()
        print(result)
        res = 0

        return render_template('editPhyBookLayout.html', res=result, lid=lid, bid=result[0])

@buk.route('/phyBookUpdate', methods=['GET', 'POST'])
def phyBookUpdate():
    try:
        lid = str(session.get('lid'))
        usr = session.get('usr')

        # Retrieve form data
        # file = request.files.get('file')  # Single file uploaded under 'file' key
        bname = request.form.get('bname')  # Book name
        btype = request.form.get('btype')  # Book type (e.g., genre)
        bauthor = request.form.get('bauthor')  # Author of the book
        blang = request.form.get('blang')  # Language of the book
        disc = request.form.get('disc')  # Description of the book

        # if not file or file.filename == '':
        #    return "No file selected for uploading", 400

        cmd.execute("SELECT * FROM `phybooks` WHERE `bname`='" + bname + "' AND 'lid'='" + lid + "'")
        result = cmd.fetchone()

        if result is not None:
            # Insert the main book record into the database
            cmd.execute("UPDATE phybooks SET bname = '" + bname + "', btype = '" + btype + "', bauthor = '" + bauthor + "', blang = '" + blang + "', bcap = '" + disc + "'" )

            return "<script>alert('Update Successful');window.location='/reHome'</script>"
        else:
            return "<script>alert('Error');window.location='/reHome'</script>"
    except Exception as e:
        # Handle any errors that occur
        print(f"Error occurred during file upload: {e}")
        return "<script>alert('Error');window.location='/reHome'</script>"

@buk.route('/delPhyBook/<bid>', methods=['GET', 'POST'])
def delPhyBook(bid):
    lid = str(session.get('lid'))

    cmd.execute("DELETE FROM `phyBooks` WHERE `bid`='" + bid + "' ")
    con.commit()

    return "<script>alert('Book deleted!');window.location='/reHome'</script>"

@buk.route('/catelog', methods=['GET', 'POST'])
def catelog():
    return render_template('catelogHome.html')

@buk.route('/catelogBookList/<uid>', methods=['GET', 'POST'])
def catelogBookList(uid):
    return render_template('catelogAddBook.html', uid=uid)

@buk.route('/select_books', methods=['GET'])
def select_books():
    lid = str(session.get('lid'))

    # Fetch book titles and IDs from the database
    cmd.execute("SELECT * FROM phybooks WHERE lid = '" + lid + "'")
    books = cmd.fetchall()  # Returns a list of tuples [(id, title), ...]
    return render_template('book_selection_form.html', books=books)

"""@buk.route('/add_books', methods=['POST'])
def add_books():
    selected_books = request.form.getlist('book_ids')
    for i in selected_books:
        
    return redirect(url_for('select_books'))"""


@buk.route('/logout')
def logout():
    con.close()
    session.clear()
    return "<script>alert('Loged out!');window.location='/'</script>"


if __name__ == "__main__":
    buk.run(debug=True, port=5001)
