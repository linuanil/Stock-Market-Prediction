from flask import*
from src.dbconnection import*
app=Flask(__name__)
app.secret_key="1234"



@app.route('/',methods=['post','get'])
def login():
    return render_template('Login.html')
                    #login url create



@app.route("/login_post",methods=['post','get'])
def login_post():
    username=request.form['textfield']
    password=request.form['textfield2']
    qry="SELECT * FROM `login` WHERE `username`=%s AND `password`=%s"
    val=(username,password)
    res=selectone(qry,val)
    if res is None :
        return'''<script> alert("invalid");window.location="/"</script>'''
    elif res['type']=='admin':
        return redirect ('/admin_home')
    elif res['type'] == 'expert':
        session['lid']=res['login_id']
        return redirect('/exprt_home')
    else:
        return'''<script> alert("invalid");window.location="/"</script>'''
                    #login form(check user name and password)then go to admim/expert/user



@app.route('/admin_home',methods=['post','get'])
def admin_home():
    return render_template('Admin home.html')
                    #admin url create



@app.route('/add_manage_expert',methods=['post','get'])
def add_manage_exert():
    qry="SELECT * FROM`expert`"
    res=selectall(qry)
    return render_template('Add & manage exprt.html',val=res)
                    #admin home -> add and manage expert page (show all expert)



@app.route('/edit_expert',methods=['get','post'])
def edit_expert():
    id=request.args.get('id')
    session['expert_id']=id
    qry="select * from expert where login_id=%s"
    val=(id)
    res=selectone(qry,val)
    return render_template('Edit Expert.html',val=res)
                    #admin home -> add and manage expert -> edit[link] (edit expert)



@app.route('/delete_expert',methods=['get','post'])
def delete_expert():
    id=request.args.get('id')
    qry="delete from expert where login_id = %s"
    val=(id)
    iud(qry,val)
    qry2="delete from login where login_id = %s"
    iud(qry2,val)
    return'''<script>alert("delete successfull");window.location="add_manage_expert"</script>'''
                    #admin home -> add and manage expert -> delete[link] (delete expert)



@app.route('/reg_exprt',methods=['post','get'])
def reg_exprt():
    return render_template('Expert Registration.html')
                    #admin home -> add and manage expert -> add[button] (forward to expert registration)



@app.route('/add_expert',methods=['get','post'])
def add_expert():
    fname=request.form['textfield1']
    lname = request.form['textfield2']
    gender = request.form['radiobutton']
    place = request.form['textfield3']
    post = request.form['textfield4']
    pin = request.form['textfield5']
    email = request.form['textfield6']
    phone = request.form['textfield7']
    username = request.form['textfield8']
    password = request.form['textfield9']
    qry="insert into login values(null,%s,%s,'expert')"
    val=(username,password)
    id=iud(qry,val)
    qry2="insert into expert values(null,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    val2=(id,fname,lname,gender,place,pin,post,email,phone)
    iud(qry2,val2)
    return'''<script>alert("add success");window.location="add_manage_expert"</script>'''
                    #admin home -> add and manage expert -> add[button](forward to expert registration) -> register[button](add new expert to database)



@app.route('/view_user',methods=['post','get'])
def view_user():
    qry = "SELECT * FROM`user`"
    res = selectall(qry)
    print(res)
    return render_template('Viewuser.html',val=res)
                    #admin home -> view user(forward to view user)







@app.route('/view_complaint',methods=['post','get'])
def view_complaint():
    qry="SELECT `user`.*,`complaint`.* FROM`user` JOIN `complaint` ON`user`.`login_id`=`complaint`.`login_id` where complaint.reply='pending'"
    res = selectall(qry)
    return render_template('view complaint and send replay.html',val=res)
                    #admin home -> view complaint and send reply(show all complaints)



@app.route('/send_reply',methods=['post','get'])
def send_replay():
    replay=request.form['textarea']
    qry="update complaint set reply=%s where id=%s"
    val=(replay,session['comp_id'])
    iud(qry,val)
    return '''<script>alert("successfull");window.location="view_complaint"</script>'''
                    #admin home -> view complaint and send reply(show all complaints) -> reply(forward to complaint reply form) -> send[button](add replay to database)



@app.route('/insert_notification',methods=['post','get'])
def insert_notification():
    notification=request.form['textarea']
    qry="insert into notification values(null,%s,curdate())"
    val=(notification)
    iud(qry,val)
    return '''<script>alert("successfull");window.location="admin_home"</script>'''
                    #admin home -> send notification(forward to send notification form) -> send[button](add notification to database)






@app.route('/exprt_home',methods=['post','get'])
def exprt_home():
    return render_template('Expert home.html')
                    #expert url create



@app.route('/view_expert',methods=['post','get'])
def view_expert():
    qry = "SELECT * FROM`expert`"
    res = selectall(qry)
    print(res)
    return render_template('Viewexpert.html',val=res)
                    #expert home -> view profile(forward to view expert)



@app.route('/view_doubt',methods=['post','get'])
def view_doubt():
    qry = "select user.*,doubt.* from doubt join user on user.`login_id`= doubt.login_id where doubt.reply='pending'"
    res = selectall(qry)
    return render_template('View doubts & send reply.html',val=res)
             #expert home -> view doubts and send reply(forward to view doubts and send reply form)



@app.route('/doubt_replay',methods=['post','get'])
def doubt_reply():
    id=request.args.get('id')
    session['id']=id
    return render_template('doubt_reply.html')
            #exper -> view doubts and send reply -> replay(forward to doubt_replay form)


@app.route('/doubt_replys',methods=['post','get'])
def doubt_replys():
    reply=request.form['textarea']
    qry="update doubt set reply=%s where login_id =%s"
    val=(reply,session['id'])
    iud(qry,val)
    return'''<script>alert("success");window.location="/view_doubt"</script>'''
            # exper -> view doubts and send reply -> replay(forward to doubt_replay form) -> submit



@app.route('/view_notification',methods=['post','get'])
def view_notification():
    qry="SELECT * FROM stock.notification"
    res=selectall(qry)
    print(res)
    return render_template('View Notification.html',val=res)
                    #expert home -> view notificatio(forward to view notification form)



@app.route('/view_tip',methods=['post','get'])
def view_tip():
    qry="select * from tip where login_id=%s"
    res=selectall2(qry,session['lid'])
    return render_template('view tips.html',val=res)
 #expert home -> add tip(forward to view tip form_)


@app.route('/add_tip', methods=['post', 'get'])
def add_tip():
    return render_template('add tip.html')
#expert home -> add tip(forward to view tip form_) -> add(button)



@app.route('/tips',methods=['post','get'])
def tips():
    tip=request.form['textarea']
    qry = "insert into tip values(null,%s,%s,curdate())"
    val=(session['lid'],tip)
    iud(qry,val)
    return '''<script>alert("successfull");window.location="view_tip"</script>'''
#expert home -> add tip(forward to view tip form_) -> view tips(add button) -> add(insert values)


@app.route('/delete_tip', methods=['post', 'get'])
def delete_tip():
    id=request.args.get('id')
    qry = "delete from tip where id = %s"
    iud(qry,str(id))
    return  '''<script>alert("successfull");window.location="view_tip"</script>'''
#expert home -> add tip(forward to view tip form_) -> view tips(add button) -> delete(delete values)



@app.route('/update_expert',methods=['get','post'])
def update_expert():
    fname = request.form['textfield1']
    lname = request.form['textfield2']
    gender = request.form['radiobutton']
    place = request.form['textfield3']
    post = request.form['textfield4']
    pin = request.form['textfield5']
    email = request.form['textfield6']
    phone = request.form['textfield7']
    qry="update expert set fname=%s, lname = %s, gender=%s, place=%s, post=%s, pin=%s, email=%s, phone=%s where login_id=%s"
    val = ( fname,lname,gender,place,post,pin,email,phone,session['expert_id'])
    iud(qry,val)
    return  '''<script>alert("Edited successfully");window.location="add_manage_expert"</script>'''
    #admin home -> add and manage expert -> edit(forward to edit expert) -> register[button](update existing expert to database)




@app.route('/user_home',methods=['post','get'])
def user_home():
    return render_template('User Home.html')



@app.route('/user_reg',methods=['post','get'])
def user_reg():
    return render_template('User registration.html')



@app.route('/send_notification',methods=['post','get'])
def send_notification():
    return render_template('Send Notification.html')



@app.route('/snd_comp_rply',methods=['post','get'])
def snd_comp_rply():
    return render_template('Send Complaint & View Replay.html')



@app.route('/reply',methods=['post','get'])
def reply():
    id=request.args.get('id')
    session['comp_id']=id
    return render_template('Reply.html')
    #admin home -> view complaint and send reply(show all complaints) ->










@app.route('/view_edit',methods=['post','get'])
def view_edit():
    return render_template('View & edit Profile.html')
app.run(debug=True)