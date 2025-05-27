from flask import Flask,Blueprint,render_template,request,flash,redirect,url_for
from database import*
from flask import*
import uuid


user=Blueprint('user',__name__)

@user.route('/user_home',methods=['get','post'])
def user_home():
    data = {}

    if 'lid' not in session:
        return redirect(url_for('login'))

    s = "SELECT *, CONCAT(fname, ' ', lname) AS fullname FROM `user` WHERE login_id = '%s'" % (session['lid'])
    data['res'] = select(s)

    if not data['res']:
        return redirect(url_for('login'))

    return render_template('user_home.html', data=data)

from textblob import TextBlob  # Ensure you install TextBlob: pip install textblob

def analyze_sentiment(text):
    """
    Analyzes the sentiment of a given text.
    Returns 'positive', 'negative', or 'neutral' based on polarity.
    """
    polarity = TextBlob(text).sentiment.polarity
    if polarity > 0:
        return 'positive'
    elif polarity < 0:
        return 'negative'
    else:
        return 'neutral'

@user.route('/user_managepost', methods=['get', 'post'])
def user_managepost():
    data = {}
    s = "select * from post where user_id='%s'" % (session['uid'])
    data['res'] = select(s)

    if 'sub' in request.form:
        pos = request.form['pos']
        image = request.files['pat']
        path = "static/images/" + str(uuid.uuid4()) + image.filename
        image.save(path)

        # Use the separate function to determine sentiment
        sentiment_label = analyze_sentiment(pos)

        i = "insert into post values(null, '%s', '%s', '%s', now(), 'pending', '%s')" % (
            session['uid'], pos, path, sentiment_label
        )
        insert(i)
        flash("Post added successfully!")
        return redirect(url_for('user.user_managepost'))

    if 'action' in request.args:
        action = request.args['action']
        pid = request.args['pid']
    else:
        action = None

    if action == 'update':
        s1 = "select * from post where post_id='%s'" % (pid)
        data['s2'] = select(s1)

    if 'ups' in request.form:
        pos = request.form['pos']
        image = request.files['pat']
        if image.filename:  # Check if a new image is uploaded
            path = "static/images/" + str(uuid.uuid4()) + image.filename
            image.save(path)
        else:
            # Retain the current image path
            path = data['s2'][0]['path']

        # Use the separate function to determine sentiment
        sentiment_label = analyze_sentiment(pos)

        u = "update post set post='%s', path='%s', sentiment='%s' where post_id='%s'" % (
            pos, path, sentiment_label, pid
        )
        update(u)
        flash("Post updated successfully!")
        return redirect(url_for('user.user_managepost'))

    if action == 'delete':
        d = "delete from post where post_id='%s'" % (pid)
        delete(d)
        flash("Post deleted successfully!")
        return redirect(url_for('user.user_managepost'))

    return render_template('user_managepost.html', data=data)


@user.route('/user_viewprofile', methods=['POST', 'GET'])
def user_viewprofile():
    data = {}

    # Fetch all staff
    staff_query = "SELECT * FROM user where user_id='%s'"%(session['uid'])
    data['res'] = select(staff_query)

    # Check for actions (update/delete)
    action = request.args.get('action')
    sid = request.args.get('sid')

    if action == 'update' and sid:
        # Fetch specific staff details
        fetch_staff_query = (
            "SELECT * FROM user WHERE user_id='%s'" % sid
        )
        data['s2'] = select(fetch_staff_query)

    if 'ups' in request.form:
        # Update staff details
        fname = request.form['fname']
        lname = request.form['lname']
        place = request.form['place']
        phone = request.form['phone']
        email = request.form['email']

        update_staff_query = (
            "UPDATE user SET fname='%s',lname='%s',place='%s',phone='%s', email='%s' WHERE user_id='%s'"
            % (fname, lname,place,phone, email, sid)
        )
        update(update_staff_query)

        flash("Updated successfully!", "success")
        return redirect(url_for('user.user_viewprofile'))

    return render_template('user_viewprofile.html', data=data)

@user.route('/user_sendcomments', methods=['get', 'post'])
def user_sendcomments():
    data = {}
    pid = request.args['pid']
    
    # Fetch existing comments for the post
    s = "select * from comment where post_id='%s'" % (pid)
    data['res'] = select(s)
    
    if 'sub' in request.form:
        cmt = request.form['cmt']
        
        # Analyze the sentiment of the comment
        sentiment_label = analyze_sentiment(cmt)
        
        # Insert the comment into the database
        i = "insert into comment values(null, '%s', '%s', '%s', '%s')" % (pid, session['uid'], cmt, sentiment_label)
        insert(i)
        flash("Commented Successfully!")
        return redirect(url_for("user.user_home"))
    
    return render_template('user_sendcomments.html', data=data)

from textblob import TextBlob  # Ensure you install TextBlob: pip install textblob

# Define a function to analyze sentiment
def analyze_sentiment(text):
    """
    Analyzes the sentiment of a given text.
    Returns 'positive', 'negative', or 'neutral' based on polarity.
    """
    polarity = TextBlob(text).sentiment.polarity
    if polarity > 0:
        return 'positive'
    elif polarity < 0:
        return 'negative'
    else:
        return 'neutral'

@user.route('/user_chatwithotherusers',methods=['get','post'])
def user_chatwithotherusers():
    data={}
    reciver_id=request.args['rid']

    if 'submit' in request.form:
        message=request.form['msg']
        i="insert into chat values(null,'%s','%s','%s',now())"%(session['lid'],reciver_id,message)
        insert(i)
        
    s1="select * from chat where sender_id='%s' and receiver_id='%s' or sender_id='%s' and receiver_id='%s'"%(reciver_id,session['lid'],session['lid'],reciver_id)
    data['msg']=select(s1)
    return render_template('user_chatwithotherusers.html',data=data)




	# if 'action' in request.args:
	# 	action=request.args['action']
	# 	pid=request.args['pid']
	# else:
	# 	action=None

	# if action=='update':
	# 	s1="select * from post where post_id='%s'"%(pid)
	# 	data['s2']=select(s1)

	# if 'ups' in request.form:
	# 	image=request.files['pos']
	# 	path="static/images/"+str(uuid.uuid4())+image.filename
	# 	image.save(path)
	# 	pat=request.form['pat']
	# 	u="update post set post='%s',path='%s' where post_id='%s'"%(path,pat,pid)
	# 	update(u)
	# 	flash("updated Successfully!")
	# 	return redirect(url_for('user.user_managepost'))

	# if action=='delete':
	# 	d="delete from post where post_id='%s'"%(pid)
	# 	delete(d)
	# 	flash("deleted Successfully!")
	# 	return redirect(url_for('user.user_managepost'))


@user.route('/send_complaints',methods=['post','get'])
def complaints():
    data={}
    if 'sub' in request.form:
        complaints=request.form['com']
        i="insert into complaint values(null,'%s','%s','pending',now())"%(session['uid'],complaints)
        r=insert(i);
        
    z="select * from complaint where user_id='%s'"%(session['uid'])
    data['x']=select(z)

        
    return render_template('user_sendcomplaints.html',data=data)


@user.route('/user_viewotherpost', methods=['GET', 'POST'])
def user_viewotherpost():
    data = {}
    sentiment_filter = request.args.get('sentiment')  # Get from query params like ?sentiment=positive

    if sentiment_filter:
        # Filter based on sentiment
        q = """
        SELECT *, CONCAT(fname, ' ', lname) AS fullname 
        FROM user 
        INNER JOIN post USING(user_id) 
        WHERE user_id != '%s' AND sentiment = '%s'
        """ % (session['uid'], sentiment_filter)
    else:
        # Show all posts from other users
        q = """
        SELECT *, CONCAT(fname, ' ', lname) AS fullname 
        FROM user 
        INNER JOIN post USING(user_id) 
        WHERE user_id != '%s'
        """ % (session['uid'])

    data['res'] = select(q)
    return render_template('user_viewotherpost.html', data=data)


# @user.route('/user_viewotherpost',methods=['post','get'])
# def user_viewotherpost():
#     data={}
#     s="select *,concat(fname,' ',lname) as fullname from user inner join post using(user_id) where user_id!='%s'"%(session['uid'])
#     data['res']=select(s)

#     return render_template('user_viewotherpost.html',data=data)





