from flask import Flask,Blueprint,render_template,request,flash,redirect,url_for
from database import*

admin=Blueprint('admin',__name__)

@admin.route('/admin_home')
def admin_home():
	return render_template('admin_home.html')

@admin.route('/admin_viewuser',methods=['post','get'])
def admin_viewuser():
    data={}
    s="select *,concat(fname,' ',lname) as fullname from user inner join login using(login_id)"
    data['res']=select(s)

    if 'action' in request.args:
        action = request.args['action']
        lid = request.args['lid']
    else:
        action = None

    if action == 'block':
        u = "update login set usertype='Blocked' where login_id='%s'" %(lid)
        update(u)
        flash("Blocked user successfully!")
        return redirect(url_for('admin.admin_viewuser'))

    if action == 'unblock':
        un = "update login set usertype='user' where login_id='%s'" %(lid)
        update(un)
        flash("UnBlocked user successfully!")
        return redirect(url_for('admin.admin_viewuser'))

    return render_template('admin_viewuser.html',data=data)

@admin.route('/admin_viewpost',methods=['post','get'])
def admin_viewpost():
    data={}
    s="select *,concat(fname,' ',lname) as fullname from user inner join post using(user_id)"
    data['res']=select(s)

    if 'action' in request.args:
        action = request.args['action']
        pid = request.args['pid']
    else:
        action = None

    if action == 'delete':
        d = "delete from post where post_id='%s'" % (pid)
        delete(d)
        flash("Post deleted successfully!")
        return redirect(url_for('admin.admin_viewpost'))


    return render_template('admin_viewpost.html',data=data)

@admin.route('/admin_viewcomments',methods=['post','get'])
def admin_viewcomments():
    data={}
    pid=request.args['pid']
    s="select *,concat(fname,' ',lname) as fullname from user inner join comment using(user_id) where post_id='%s'"%(pid)
    data['res']=select(s)

    return render_template('admin_viewcomments.html',data=data)


@admin.route('/admin_viewcomplaints', methods=['POST', 'GET'])
def admin_viewcomplaints():
    data = {}
    # Query to fetch complaints with user details
    z = """
        SELECT 
            complaint.complaint_id, complaint.complaint, complaint.reply, 
            complaint.date, CONCAT(user.fname, ' ', user.lname) AS fullname 
        FROM 
            user 
        INNER JOIN 
            complaint USING(user_id)
    """
    data['x'] = select(z)

    # Handle reply submission
    if 'sub' in request.form:
        # Retrieve the complaint ID from the form
        complaint_id = request.form.get('complaint_id')
        reply_key = f'reply_{complaint_id}'  # Construct the dynamic key
        reply = request.form.get(reply_key, '').strip()

        if reply and complaint_id:
            # Update the specific complaint reply
            u = "UPDATE complaint SET reply = '%s' WHERE complaint_id = '%s'"%(reply, complaint_id)
            update(u)
            flash('Replied successfully', 'success')
        else:
            flash('Failed to send reply. Please try again.', 'error')

        return redirect(url_for('admin.admin_viewcomplaints'))

    return render_template('admin_viewcomplaints.html', data=data)



# @admin.route('/admin_viewcomplaints', methods=['POST', 'GET'])
# def admin_viewcomplaints():
#     data = {}
#     z = "SELECT *, CONCAT(fname, ' ', lname) AS fullname FROM user INNER JOIN complaint USING(user_id)"
#     data['x'] = select(z)
    
#     if 'sub' in request.form:
#         reply = request.form['rep']
#         complaint_id = request.form['complaint_id']  # Retrieve the unique ID of the complaint
#         u = "UPDATE complaint SET reply = '%s' WHERE complaint_id = %s" % (reply, complaint_id)
#         update(u)
#         flash('Replied successfully')
#         return redirect(url_for('admin.admin_viewcomplaints'))

#     return render_template('admin_viewcomplaints.html', data=data)


        


