@buk.route('/upload')
def upload_book():
    lid = str(session['lid'])
    usr = session['usr']

    pfiles = request.files('file')

    bname = request.form['bname']
    btype = request.form['btype']
    bauthor = request.form['bauthor']
    blang = request.form['blang']
    disc = request.form['disc']

    c = 1
    con.commit()

    for file in pfiles:
        # photo file save to folder
        split = str.split(file.filename, '.')
        ext = '.' + split[len(split) - 1]
        fname = usr + uid
        photo = fname + "-" + str(c) + ext
        file.save('static/book/' + photo)
        cmd.execute("INSERT INTO `books` VALUES(NULL,'" + bname + "','" + btype + "','" + bauthor + "','" + blang + "','" + disc + "','" + lid + "')")
        uid = str(con.insert_id())
        cmd.execute("INSERT INTO `upload_files` VALUES(NULL, '" + uid + "', '" + photo + "')")
        cmd.execute(
            "UPDATE `uploads` SET `fname`='" + fname + "', `ext`='" + ext + "' WHERE `upload_id`='" + uid + "' ")
        con.commit()
        c += 1

    return redirect(url_for('userHome'))

###########################################################################################################################################
