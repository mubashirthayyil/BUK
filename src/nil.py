<!--<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>View File</title>
    <link rel="stylesheet" href="static/style/view_file.css">
</head>
<body>
    <div class="file-view-container">
        <h1>Viewing File: {{ filename }}</h1>

        {% if file_ext == '.pdf' %}
            <embed src="{{ url_for('static', filename='digRes/' + filename + file_ext) }}" type="application/pdf" width="100%" height="600px">

        {% elif file_ext == '.txt' %}
            <pre>
                {% with open(file_path, 'r') as file %}
                    {{ file.read() }}
                {% endwith %}
            </pre>

        {% elif file_ext in ['.doc', '.docx'] %}
            <iframe src="https://docs.google.com/gview?url={{ url_for('static', filename='digRes/' + filename + file_ext) }}&embedded=true" width="100%" height="600px"></iframe>

        {% else %}
            <p>Unsupported file type.</p>
        {% endif %}

    </div>
</body>
</html>-->

--------------------------------------------------------------------------------------------------------------------------
< div


class ="table mt-3 px-2" >


{ % if data %}
< table
align = "center"


class ="table" >

< tbody >
{ %
for i in data %}
< tr


class ="clickable" onclick="window.location='/userProfile/{{ i[0] }}'" >

< td >
< div


class ="d-flex flex-row" >

< div


class ="pfpCircle-sm mt-1" style="background-image: url('/static/digRes/{{i[2]}}');" > < / div >

< div


class ="d-flex flex-column justify-content-start ml-2" >

< span


class ="d-block pname ms-1 mt-n1" > {{i[3]}} < / span >

< span


class ="d-block date text-black-50 loc ms-1" > {{i[1]}} < / span >

< / div >
< / div >
< / td >
< / tr >
{ % endfor %}
< / tbody >
< / table >
{ % else %}
< div
align = "center" >
< h3
align = "center" > {{p}} < / h3 >
< small > {{p1}} < / small >
< / div >
{ % endif %}
< / div >
------------------------------------------------------------------------------------------------------------------------------
    <script type="text/javascript">
    function valid()
    {
        if(document.getElementById("name").value=="")
        {
            alert("Enter Your Name!");
            document.getElementById("name").focus();
            return false;
        }
        if(/[^a-z\s]/gi.test(document.getElementById("name").value))
        {
            alert("Special characters are not allowed in name");
            document.getElementById("name").focus();
            return false;
        }

        if(document.getElementById("email").value=="")
        {
            alert("Enter your E-mail ID");
            document.getElementById("email").focus();
            return false;
        }
        var emailPat = /^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$/;
        var emailid = document.getElementById("email").value;
        var matchArray = emailid.match(emailPat);
        if (matchArray == null)
        {
            alert("Your Email ID seems incorrect. Enter Correct Email ID.");
            document.getElementById("email").focus();
            return false;
        }
        if(document.getElementById("phone").value=="")
        {
            alert("Enter Phone Number");
            document.getElementById("phone").focus();
            return false;
        }
        if(/[^0-9]/gi.test(document.getElementById("phone").value))
        {
            alert("Special characters not allowed in Phone Number");
            document.getElementById("phone").focus();
            return false;
        }
        if(document.getElementById("dob").value=="")
        {
            alert("Please select date of birth");
            document.getElementById("dob").focus();
            return false;
        }
        if(document.getElementById("country").value=="0")
        {
            alert("Please select Country");
            document.getElementById("country").focus();
            return false;
        }
        if(document.getElementById("utype").value=="0")
        {
            alert("Please select user type");
            document.getElementById("utype").focus();
            return false;
        }

        if(document.getElementById("username").value=="")
        {
            alert("Please Create an username");
            document.getElementById("dob").focus();
            return false;
        }
        if(document.getElementById("pass1").value=="")
        {
            alert("Enter Password!");
            document.getElementById("pass1").focus();
            return false;
        }
        if(document.getElementById("pass1").value.length<8)
        {
            alert("Password must contain atleast 8 characters");
            document.getElementById("pass1").focus();
            return false;
        }
        if(document.getElementById("pass2").value=="")
        {
            alert("Enter Confirm Password!");
            document.getElementById("pass2").focus();
            return false;
        }
        if((document.getElementById("pass2").value)!=(document.getElementById("pass1").value))
        {
            alert("Password doesn't match!");
            document.getElementById("pass2").focus();
            return false;
        }
}
    </script>

----------------------------------------------------------------------------------------------------------------------------
@buk.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['dob']
        gen = request.form['gender']
        email = request.form['email']
        phone = request.form['phone']
        usr = request.form['username']
        password = request.form['password']
        addr = ''

        utype = 'fuser'
        libname = 'nil'

        if gen == 'lib':
            utype = 'lib'
            libname = 'lib'

        cmd.execute("SELECT * FROM `login` WHERE `username`='" + usr + "' ")
        result = cmd.fetchone()
        print(f" usr result = {result}")
        if result is None:
            cmd.execute("INSERT INTO `login` VALUES(NULL, '" + usr + "', '" + password + "', '" + utype + "',0,0)")
            lid = con.insert_id()
            cmd.execute("INSERT INTO `users` VALUES(NULL, '" + str(
                lid) + "','" + name + "', '" + age + "', '" + gen + "', '" + str(0) + "',\
             '" + email + "', '" + phone + "', 'nopfp.jpg','" + utype + "')")
            con.commit()
            return "<script>alert('Sign-up Successful');window.location='/'</script>"

        else:
            return "<script>alert('This Username is Already Taken, Please Create a New Username');window.location='/signup'</script>"
    else:
        cmd.execute("DELETE FROM `users` WHERE `lid` IS NULL")
        cmd.execute("DELETE FROM `login` WHERE `lid` IS NULL")
        con.commit()
        return render_template('SignupPage.html')
---------------------------------------------------------------------------------------------------------------------------------------
<!DOCTYPE html>
<html lang="en" xmlns="http://www.w3.org/1999/html">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
<!--    <link rel="stylesheet" href="\static\bootstrap.min.css">-->
<!--    <link rel="stylesheet" href="\static\font-awesome.min.css">-->


     <!-- Import bootstrap cdn -->

    <link rel="stylesheet" href="\static\SignupPage.css" />

    <link rel="stylesheet" href="\static\style.css">

     <!-- Import bootstrap cdn -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css"
          rel="stylesheet"
          integrity="sha384-GLhlTQ8iRABdZLl6O3oVMWSktQOp6b7In1Zl3/Jr59b6EGGoI1aFkw7cmDA6j6gD"
          crossorigin="anonymous"/>

    <link rel="stylesheet"
          href="https://stackpath.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css"
          crossorigin="anonymous"/>

    <link
      rel="stylesheet"
      href="https://unicons.iconscout.com/release/v4.0.0/css/line.css"/>


    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css"/>


    <script type="text/javascript">
    function valid()
    {
        if(document.getElementById("name").value=="")
        {
            alert("Enter Your Name!");
            document.getElementById("name").focus();
            return false;
        }
        if(/[^a-z\s]/gi.test(document.getElementById("name").value))
        {
            alert("Special characters are not allowed in name");
            document.getElementById("name").focus();
            return false;
        }

        if(document.getElementById("email").value=="")
        {
            alert("Enter your E-mail ID");
            document.getElementById("email").focus();
            return false;
        }
        var emailPat = /^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$/;
        var emailid = document.getElementById("email").value;
        var matchArray = emailid.match(emailPat);
        if (matchArray == null)
        {
            alert("Your Email ID seems incorrect. Enter Correct Email ID.");
            document.getElementById("email").focus();
            return false;
        }
        if(document.getElementById("phone").value=="")
        {
            alert("Enter Phone Number");
            document.getElementById("phone").focus();
            return false;
        }
        if(/[^0-9]/gi.test(document.getElementById("phone").value))
        {
            alert("Special characters not allowed in Phone Number");
            document.getElementById("phone").focus();
            return false;
        }
        if(document.getElementById("dob").value=="")
        {
            alert("Please select date of birth");
            document.getElementById("dob").focus();
            return false;
        }
        if(document.getElementById("country").value=="0")
        {
            alert("Please select Country");
            document.getElementById("country").focus();
            return false;
        }
        if(document.getElementById("utype").value=="0")
        {
            alert("Please select user type");
            document.getElementById("utype").focus();
            return false;
        }

        let checkRadio = document.querySelector(
                'input[name="gender"]:checked');

        if(checkRadio == null)
        {
            alert("Please select your gender");
            return false;
        }

        if(document.getElementById("username").value=="")
        {
            alert("Please Create an username");
            document.getElementById("username").focus();
            return false;
        }
        if(document.getElementById("pass1").value=="")
        {
            alert("Enter Password!");
            document.getElementById("pass1").focus();
            return false;
        }
        if(document.getElementById("pass1").value.length<8)
        {
            alert("Password must contain atleast 8 characters");
            document.getElementById("pass1").focus();
            return false;
        }
        if(document.getElementById("pass2").value=="")
        {
            alert("Enter Confirm Password!");
            document.getElementById("pass2").focus();
            return false;
        }
        if((document.getElementById("pass2").value)!=(document.getElementById("pass1").value))
        {
            alert("Password doesn't match!");
            document.getElementById("pass2").focus();
            return false;
        }
}
    </script>

    <title>Signup</title>
</head>
<body>

<section class="vh-100" style="background-color: #626cd6;overflow: hidden;">
  <div class="container mt-5">
    <div class="row justify-content-center align-items-center" >
        <div class="card shadow-2-strong card-registration" style="border-radius: 15px; background-color: #ADD2C2;
    width: 100%;
    background: #fff;
    border-radius: 6px;
    padding: 41px 30px;
    box-shadow: 0 10px 20px rgba(0, 0, 0, 0.15);">
          <div class="card-body p-4 p-md-3">
            <div class="d-flex justify-content-center">
              <h3 class="mb-4 pb-2 pb-md-0 mb-md-3">Add new user</h3>
            </div>

            <form action="/addUser" method="post" enctype="multipart/form-data" onsubmit="return valid()">
              <div class="row">
                <div class="col-md-12 mb-3 pb-2">
                      <div class="form-outline">
                        <input type="text" id="name" name="name" class="form-control" placeholder="Name" aria-label="Username" aria-describedby="dr">
                      </div>
                </div>
              </div>

              <div class="row">
                <div class="col-md-12 mb-3 pb-2">
                  <div class="form-outline">
                    <input type="text" id="email" name="email" class="form-control form-control-md" placeholder="Email"/>
                  </div>
                </div>
                <div class="col-md-12 mb-3 pb-2">
                  <div class="form-outline">
                    <input type="tel" id="phone" name="phone" class="form-control form-control-md" placeholder="Phone Number"/>
                  </div>
                </div>
              </div>

              <div class="row">
                <div class="col-md-3 mb-3 d-flex align-items-center">
                  <div class="form-outline datepicker w-100">
                      <h6 class="mb-2 pb-1">Date Of Birth :</h6>
                  </div>
                </div>
                 <div class="col-md-9 mb-3">
                  <div class="form-outline datepicker w-100">
                    <input type="date" class="form-control form-control-md" id="dob" name="dob" />
                  </div>
                </div>

              <div class="row">
                 <div class="col-md-4  mb-4">
                  <h6 class="pb-1">Gender: </h6>
                 </div>
                  <div class="form-check form-check-inline">
                    <input class="form-check-input" type="radio" name="gen" value="female" >
                    <label class="form-check-label" for="female">Female</label>
                </div>
                <div class="form-check form-check-inline">
                    <input class="form-check-input" type="radio" name="gen" value="male">
                    <label class="form-check-label" for="male">Male</label>
                </div>
                <div class="form-check form-check-inline">
                    <input class="form-check-input" type="radio" name="gen" value="other">
                    <label class="form-check-label" for="other">Other</label>
                </div>
              </div>

              <div class="d-flex justify-content-center">
                  <h4 class="mb-md-4">Create Username and Password</h4>
              </div>

              <div class="d-flex justify-content-center">
                  <div class="col-md-7 mb-3 ">
                      <input type="text" class="form-control" name="username" id="username" placeholder="Create an username">
                  </div>
              </div>
              <div class="d-flex justify-content-center">
                  <div class="col-md-7 mb-3">
                      <input type="text" class="form-control" name="password" id="pass1" placeholder="Enter password" aria-describedby="pswdhelp">
                        <!--<small id="pswdhelp" class="form-text text-muted">
                          Your password must be minimum 8 characters long.
                        </small>-->
                  </div>
              </div>
              <div class="d-flex justify-content-center">
                  <div class="col-md-7 mb-3">
                       <input type="text" class="form-control" name="psswd1" id="pass2" placeholder="Confirm password">
                  </div>
              </div>

              <div class="row">
                  <div>
                     <div class="d-flex justify-content-center">
                        <button type="submit">Signup</button>
                     </div>
                      <center>
                      <a style="" href="/" class="button small text-muted">Go back to login...</a>
                          </center>
                  </div>
              </div>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
</section>
</body>
</html>


---------------------------------------------------------------------------------------------------------------
from datetime import datetime, date

now = date.today()
print(now)


#-----------------------------------------------------------------------------------------------------------
@buk.route('/addUser', methods=['GET', 'POST'])
def addUser():
    lid = str(session.get('lid'))
    usr = session.get('usr')

    if request.method == 'POST':
        name = request.form['name']
        age = request.form['dob']
        gen = request.form['gender']
        email = request.form['email']
        phone = request.form['phone']
        usr = request.form['username']
        password = request.form['password']

        utype = 'puser'

        cmd.execute("SELECT * FROM `login` WHERE `username`='" + usr + "' ")
        result = cmd.fetchone()
        print(f" usr result = {result}")
        if result is None:
            cmd.execute("INSERT INTO `login` VALUES(NULL, '" + usr + "', '" + password + "', '" + utype + "',0,'" + lid + "')")
            log = con.insert_id()
            cmd.execute("INSERT INTO `users` VALUES(NULL, '" + str(lid) + "','" + name + "', '" + age + "', '" + gen + "', '" + str(0) + "',\
                         '" + email + "', '" + phone + "', 'nopfp.jpg','" + utype + "')")
            con.commit()
            return "<script>alert('Member added Successfully');window.location='/addUserlib'</script>"

        else:
            return "<script>alert('This Username is Already Taken, Please Create a New Username');window.location='/signup'</script>"
    else:
        cmd.execute("DELETE FROM `users` WHERE `lid` IS NULL")
        con.commit()
        return render_template('addUser.html')


#--------------------------------------------------------------------------------------------------------------------------------------------------------
<!DOCTYPE html>
<html lang="en" xmlns="http://www.w3.org/1999/html">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
<!--    <link rel="stylesheet" href="\static\bootstrap.min.css">-->
<!--    <link rel="stylesheet" href="\static\font-awesome.min.css">-->


     <!-- Import bootstrap cdn -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css"
          rel="stylesheet"
          integrity="sha384-GLhlTQ8iRABdZLl6O3oVMWSktQOp6b7In1Zl3/Jr59b6EGGoI1aFkw7cmDA6j6gD"
          crossorigin="anonymous"/>

    <link rel="stylesheet" href="\static\SignupPage.css" />

    <link rel="stylesheet"
          href="https://stackpath.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css"
          crossorigin="anonymous"/>

    <link
      rel="stylesheet"
      href="https://unicons.iconscout.com/release/v4.0.0/css/line.css"/>


    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css"/>


    <script type="text/javascript">
    function valid()
    {
        if(document.getElementById("name").value=="")
        {
            alert("Enter Your Name!");
            document.getElementById("name").focus();
            return false;
        }
        if(/[^a-z\s]/gi.test(document.getElementById("name").value))
        {
            alert("Special characters are not allowed in name");
            document.getElementById("name").focus();
            return false;
        }
        if(document.getElementById("email").value=="")
        {
            alert("Enter your E-mail ID");
            document.getElementById("email").focus();
            return false;
        }
        var emailPat = /^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$/;
        var emailid = document.getElementById("email").value;
        var matchArray = emailid.match(emailPat);
        if (matchArray == null)
        {
            alert("Your Email ID seems incorrect. Enter Correct Email ID.");
            document.getElementById("email").focus();
            return false;
        }
        if(document.getElementById("phone").value=="")
        {
            alert("Enter Phone Number");
            document.getElementById("phone").focus();
            return false;
        }
        if(/[^0-9]/gi.test(document.getElementById("phone").value))
        {
            alert("Special characters not allowed in Phone Number");
            document.getElementById("phone").focus();
            return false;
        }
        if(document.getElementById("dob").value=="")
        {
            alert("Please select date of birth");
            document.getElementById("dob").focus();
            return false;
        }
        if(document.getElementById("country").value=="0")
        {
            alert("Please select Country");
            document.getElementById("country").focus();
            return false;
        }
        if(document.getElementById("utype").value=="0")
        {
            alert("Please select user type");
            document.getElementById("utype").focus();
            return false;
        }

        let checkRadio = document.querySelector(
                'input[name="gender"]:checked');

        if(checkRadio == null)
        {
            alert("Please select your gender");
            return false;
        }

        if(document.getElementById("username").value=="")
        {
            alert("Please Create an username");
            document.getElementById("username").focus();
            return false;
        }
        if(document.getElementById("pass1").value=="")
        {
            alert("Enter Password!");
            document.getElementById("pass1").focus();
            return false;
        }
        if(document.getElementById("pass1").value.length<8)
        {
            alert("Password must contain atleast 8 characters");
            document.getElementById("pass1").focus();
            return false;
        }
        if(document.getElementById("pass2").value=="")
        {
            alert("Enter Confirm Password!");
            document.getElementById("pass2").focus();
            return false;
        }
        if((document.getElementById("pass2").value)!=(document.getElementById("pass1").value))
        {
            alert("Password doesn't match!");
            document.getElementById("pass2").focus();
            return false;
        }
}
    </script>

    <title>Signup</title>
</head>
<body>

<section class="vh-100" style="background-color: #626cd6;overflow: hidden;">
  <div class="container mt-5">
    <div class="row justify-content-center align-items-center" >
        <div class="card shadow-2-strong card-registration" style="border-radius: 15px; background-color: #ADD2C2;
    width: 100%;
    background: #fff;
    border-radius: 6px;
    padding: 41px 30px;
    box-shadow: 0 10px 20px rgba(0, 0, 0, 0.15);">
          <div class="card-body p-4 p-md-3">
            <div class="d-flex justify-content-center">
              <h3 class="mb-4 pb-2 pb-md-0 mb-md-3">Add a member</h3>
            </div>

            <form action="/addUser" method="post" enctype="multipart/form-data" onsubmit="return valid()">
              <div class="row">
                <div class="col-md-12 mb-3 pb-2">
                      <div class="form-outline">
                        <input type="text" id="name" name="name" class="form-control" placeholder="Name" aria-label="Username" aria-describedby="dr">
                      </div>
                </div>

              </div>

              <div class="row">
                <div class="col-md-12 mb-3 pb-2">
                  <div class="form-outline">
                    <input type="text" id="email" name="email" class="form-control form-control-md" placeholder="Email"/>
                  </div>
                </div>
                <div class="col-md-12 mb-3 pb-2">
                  <div class="form-outline">
                    <input type="tel" id="phone" name="phone" class="form-control form-control-md" placeholder="Phone Number"/>
                  </div>
                </div>
              </div>

              <div class="row">
                <div class="col-md-3 mb-3 d-flex align-items-center">
                  <div class="form-outline datepicker w-100">
                      <h6 class="mb-2 pb-1">Date Of Birth:</h6>
                  </div>
                </div>
                 <div class="col-md-9 mb-3">
                  <div class="form-outline datepicker w-100">
                    <input type="date" class="form-control form-control-md" id="dob" name="dob" />
                  </div>
                </div>

              </div>

              <div class="row">
                 <div class="col-md-3  mb-4">
                  <h6 class="pb-1">Gender: </h6>
                 </div>
                  <div class="col-md-6">
                      <div class="form-check form-check-inline">
                        <input class="form-check-input" type="radio" name="gender" id="female" value="female" />
                        <label class="form-check-label" for="female">Female</label>
                      </div>

                      <div class="form-check form-check-inline">
                        <input class="form-check-input" type="radio" name="gender" id="male" value="male" />
                        <label class="form-check-label" for="male">Male</label>
                      </div>

                      <div class="form-check form-check-inline">
                        <input class="form-check-input" type="radio" name="gender" id="other" value="other" />
                        <label class="form-check-label" for="other">Other</label>
                      </div>
                </div>
              </div>

              <div class="d-flex justify-content-center">
                  <h4 class="mb-md-4">Create Username and Password</h4>
              </div>

              <div class="d-flex justify-content-center">
                  <div class="col-md-7 mb-3 ">
                      <input type="text" class="form-control" name="username" id="username" placeholder="Create an username">
                  </div>
              </div>
              <div class="d-flex justify-content-center">
                  <div class="col-md-7 mb-3">
                      <input type="text" class="form-control" name="password" id="pass1" placeholder="Enter password" aria-describedby="pswdhelp">
                        <!--<small id="pswdhelp" class="form-text text-muted">
                          Your password must be minimum 8 characters long.
                        </small>-->
                  </div>
              </div>
              <div class="d-flex justify-content-center">
                  <div class="col-md-7 mb-3">
                       <input type="text" class="form-control" name="psswd1" id="pass2" placeholder="Confirm password">
                  </div>
              </div>

              <div class="row">
                  <div>
                     <div class="d-flex justify-content-center">
                        <button type="submit">Signup</button>
                     </div>
                      <center>
                      <a style="" href="libHome.html" class="button small text-muted">Go back to home...</a>
                          </center>
                  </div>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
</section>
</body>
</html>
