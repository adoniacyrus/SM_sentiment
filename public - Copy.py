from flask import Flask,Blueprint,render_template,redirect,url_for,request,flash,session
from database import*
public=Blueprint('public',__name__)

@public.route('/')
def home():
    return render_template('home.html')

@public.route('/login', methods=['post', 'get'])
def login():
    if 'sub' in request.form:
        uname = request.form['uname']
        pd = request.form['pass']
        s = "select * from login where username='%s' and password='%s'" % (uname, pd)
        res = select(s)
        
        if res:
            session['lid'] = res[0]['login_id']
            if res[0]['usertype'] == 'admin':
                return redirect(url_for('admin.admin_home'))
            
            elif res[0]['usertype'] == 'user':
                l = "select * from user where login_id='%s'" % (session['lid'])
                res = select(l)
                if res:
                    session['uid'] = res[0]['user_id']
                return redirect(url_for('user.user_home'))
        else:
            # Flash a message when the username or password is invalid
            flash("Invalid username or password!", "error")

    return render_template('login.html')


@public.route('/user_register', methods=['post', 'get'])
def user_register():
    if 'sub' in request.form:
        uname = request.form['uname']
        pd = request.form['pass']
        fname = request.form['fname']
        lname = request.form['lname']
        place = request.form['place']
        phone = request.form['phone']
        email = request.form['email']

        # Check if the username already exists in the login table
        check_username_query = "SELECT * FROM login WHERE username='%s'" % uname
        username_exists = select(check_username_query)

        # Check if the email already exists in the user table
        check_email_query = "SELECT * FROM user WHERE email='%s'" % email
        email_exists = select(check_email_query)

        # If username or email already exists, show an error message
        if username_exists:
            flash("Username already exists! Please choose another one.", "error")
            return redirect(url_for('public.user_register'))
        
        if email_exists:
            flash("Email already exists! Please use another email.", "error")
            return redirect(url_for('public.user_register'))

        # If both username and email are unique, insert the new user and login details
        insert_login_query = "INSERT INTO login VALUES (null, '%s', '%s', 'user')" % (uname, pd)
        res = insert(insert_login_query)  # Assume 'insert' function returns the inserted id

        insert_user_query = "INSERT INTO user VALUES (null, '%s', '%s', '%s', '%s', '%s', '%s')" % (res, fname, lname, place, phone, email)
        insert(insert_user_query)  # Insert the user details

        flash("Registered Successfully!", "success")
        return redirect(url_for('public.login'))

    return render_template('user_register.html')
    
# @public.route('/login',methods=['post','get'])
# def login():
# 	if 'sub' in request.form:
# 		uname=request.form['uname']
# 		pd=request.form['pass']
# 		s="select * from login where username='%s' and password='%s'"%(uname,pd)
# 		res=select(s)
# 		session['lid']=res[0]['login_id']
# 		if res:
# 			if res[0]['usertype']=='admin':
# 				return redirect(url_for('admin.admin_home'))

# 			elif res[0]['usertype']=='shop':
# 				l="select * from shop where login_id='%s'"%(session['lid'])
# 				res=select(l)
# 				if res:
# 					session['sid']=res[0]['shop_id']
# 				return redirect(url_for('shop.shop_home'))

# 			elif res[0]['usertype']=='user':
# 				l="select * from user where login_id='%s'"%(session['lid'])
# 				res=select(l)
# 				if res:
# 					session['uid']=res[0]['user_id']
# 				return redirect(url_for('user.user_home'))

# 	return render_template('login.html')

# @public.route('/shop_register',methods=['post','get'])
# def shop_register():
# 	if 'sub' in request.form:
# 		uname=request.form['uname']
# 		pd=request.form['pass']
# 		name=request.form['name']
# 		place=request.form['place']
# 		phone=request.form['phone']
# 		email=request.form['email']
# 		i="insert into login values(null,'%s','%s','shop')"%(uname,pd)
# 		res=insert(i)
# 		i="insert into shop values(null,'%s','%s','%s','%s','%s')"%(res,name,place,phone,email)
# 		insert(i)
# 		flash("Registered Successfully!")
# 		return redirect(url_for('public.login'))
# 	return render_template('shop_register.html')

# @public.route('/user_register',methods=['post','get'])
# def user_register():
# 	if 'sub' in request.form:
# 		uname=request.form['uname']
# 		pd=request.form['pass']
# 		fname=request.form['fname']
# 		lname=request.form['lname']
# 		place=request.form['place']
# 		phone=request.form['phone']
# 		email=request.form['email']
# 		i="insert into login values(null,'%s','%s','user')"%(uname,pd)
# 		res=insert(i)
# 		i="insert into user values(null,'%s','%s','%s','%s','%s','%s')"%(res,fname,lname,place,phone,email)
# 		insert(i)
# 		flash("Registered Successfully!")
# 		return redirect(url_for('public.login'))
# 	return render_template('user_register.html')


