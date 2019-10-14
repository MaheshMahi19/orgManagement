from flask import *
from pymongo import *
from  flask_paginate import *

app = Flask(__name__)
app.config["SECRET_KEY"] = "nothingtoworry"
client = MongoClient()
admindb = client.test.admin
orgdb = client.test.orgs
userdb = client.test.usres


@app.route("/admin", methods=["GET", "POST"])
def admin():
    if request.method == "GET":
        if "Logged" in session and session["Logged"] == True:
            return redirect("/admindashboard")
        else:
            return render_template("/admin/adminlogin.html")
    else:
        username = request.form["username"]
        password = request.form["password"]
        res = {"username": username}
        adminresults = admindb.find_one(res)
        if adminresults is None:
            return "No Account found with that Name...!"
        else:
            if adminresults["password"] != password:
                return "Password didn't match!"
            else:
                session["Logged"] = True
                return redirect("/admindashboard")

def createPages(users,offset=0, per_page=10):
    return users[offset:offset+per_page]


@app.route("/admindashboard")
def admindashboard():
    # print(session["Logged"])
    if "Logged" in session and session["Logged"]==True:
        orgs = orgdb.find().count()
        users = userdb.find().count()
        return render_template("/admin/admindashboard.html", orgs=orgs, users=users)
    else:
        return redirect("/admin")


@app.route("/admindashboard/useraccounts")
def useraccounts():
    userres = userdb.find().limit(10)
    if userres is None:
        return "Sorry No Accounts.."
    else:
        count = userres.count()
        page,per_page,offset = get_page_args(page_parameter='page',per_page_parameter="per_page")
        page_users = createPages(userres, offset=offset, per_page=per_page)
        pagination = Pagination(page=page,per_page=per_page,total=count,css_framework='bootstrap4')

        return render_template("admin/users.html",usercount=count,users=page_users,page=page,
                               per_page=per_page,
                               pagination=pagination)
@app.route("/org/register",methods=["GET","POST"])
def orgRegister():
    if request.method == "GET":
        return "This is for `<kbd>org</kbd>` registaration..!"
    else:
        return "Posting...!"

if __name__ == "__main__":
    app.run(debug=True, port=80)
