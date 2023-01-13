from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_session import Session
from flask_login import LoginManager, login_user, login_required, current_user, logout_user
from dao import comments_dao, follows_dao, podcast_dao, series_dao, users_dao
from models import User
from datetime import date
from werkzeug.security import generate_password_hash, check_password_hash
import os, shutil

app = Flask(__name__)
app.secret_key = "secretkey" # change in production (not safe)
app.config["SESSION_TYPE"] = "filesystem"
app.config["SESSION_PERMANENT"] = False
Session(app)

login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.init_app(app)

@app.route("/")
def home():
    if current_user.is_authenticated:
        series_list = series_dao.get_series(current_user.id)
    else:
        series_list = series_dao.get_series(0)
    categories = series_dao.get_categories()
    return render_template("home.html", series_list=series_list, categories=categories, current_category="All", get_creator_name=users_dao.get_user_username_by_id, is_following=follows_dao.is_following)

@app.route("/<category>")
def home_category(category):
    series_list = series_dao.get_series_by_category(category)
    categories = series_dao.get_categories()
    return render_template("home.html", series_list=series_list, categories=categories, current_category=category, get_creator_name=users_dao.get_user_username_by_id, is_following=follows_dao.is_following)

@app.route('/series/<int:series_id>')
def series(series_id):
    series_selected = series_dao.get_one_series(series_id)
    if current_user.is_authenticated:
        podcasts = podcast_dao.get_podcasts(series_id, current_user.id)
    else:
        podcasts = podcast_dao.get_podcasts(series_id, 0)

    return render_template("series.html", series=series_selected, podcasts=podcasts, get_creator_name=users_dao.get_user_username_by_id, is_following=follows_dao.is_following, comments=comments_dao.get_comments)

@app.route("/series/new", methods=["GET", "POST"])
@login_required
def new_series():
    if request.method == "GET":
        if not current_user.is_creator:
            flash("Only creators can create a new series...", "danger")
            return redirect(url_for("home"))

        return render_template("new-series.html")

    elif request.method == "POST":
        if not current_user.is_creator:
            flash("Only creators can create a new series...", "danger")
            return redirect(url_for("home"))
        
        add_series = request.form.to_dict()
        image = request.files["image"]

        # handle errors (title too short)
        if len(add_series["title"]) < 3:
            flash("Title is too short...", "warning")
            return redirect(url_for("new_series"))
        
        # handle errors (cannot start with space)
        if add_series["title"][0] == " ":
            flash("Title cannot start with an empty space...", "warning")
            return redirect(url_for("new_series"))

        # handle errors (title too long)
        if len(add_series["title"]) > 30:
            flash("Title is too long...", "warning")
            return redirect(url_for("new_series"))
        
        # handle errors (category too short)
        if len(add_series["category"]) < 3:
            flash("Category is too short...", "warning")
            return redirect(url_for("new_series"))
        
        # handle errors (cannot start with space)
        if add_series["category"][0] == " ":
            flash("Category cannot start with an empty space...", "warning")
            return redirect(url_for("new_series"))

        # handle errors (category too long)
        if len(add_series["category"]) > 20:
            flash("Category is too long...", "warning")
            return redirect(url_for("new_series"))

        # handle errors (description too short)
        if len(add_series["text"]) < 100:
            flash("Description is too short...", "warning")
            return redirect(url_for("new_series"))
        
        # handle errors (cannot start with space)
        if add_series["text"][0] == " ":
            flash("Description cannot start with an empty space...", "warning")
            return redirect(url_for("new_series"))

        # handle errors (description too long)
        if len(add_series["text"]) > 400:
            flash("Description is too long...", "warning")
            return redirect(url_for("new_series"))

        # handle empty date
        if add_series["date"] == "":
            add_series["date"] = date.today()

        # handle image
        if image.filename == "":
            flash("File has no name...", "warning")
            return redirect(url_for("new_series"))

        if "." not in image.filename or (image.filename.split(".")[1] != "jpeg" and image.filename.split(".")[1] != "jpg"):
            flash("Wrong file extension...", "warning")
            return redirect(url_for("new_series"))
        
        image.save("static/images/" + add_series["title"].lower().replace(" ", "_") + ".jpeg")

        add_series["creator_id"] = current_user.id

        # add new series to the series list
        (success, id) = series_dao.add_series(add_series)

        if success:
            os.mkdir("static/audio/" + str(id))
            flash("Series successfully created!", "success")
        else:
            flash("Something went wrong!", "danger")
        
        return redirect(url_for("home"))

@app.route("/series/<int:series_id>/edit", methods=["POST"])
@login_required
def edit_series(series_id):
    series_edit = series_dao.get_one_series(series_id)
    if not current_user.id == series_edit["creator_id"]:
        flash("Only creator can edit the series...", "danger")
        return redirect(url_for("home"))
    
    add_series = request.form.to_dict()
    image = request.files["image"]

    # no title
    if add_series["title"] == "":
        add_series["title"] = series_edit["title"]

    # handle errors (title too short)
    if len(add_series["title"]) < 3:
        flash("Title is too short...", "warning")
        return redirect(url_for("series", series_id=series_id))
    
    # handle errors (cannot start with space)
    if add_series["title"][0] == " ":
        flash("Title cannot start with an empty space...", "warning")
        return redirect(url_for("series", series_id=series_id))

    # handle errors (title too long)
    if len(add_series["title"]) > 30:
        flash("Title is too long...", "warning")
        return redirect(url_for("series", series_id=series_id))
    
    # no category
    if add_series["category"] == "":
        add_series["category"] = series_edit["category"]

    # handle errors (category too short)
    if len(add_series["category"]) < 3:
        flash("Category is too short...", "warning")
        return redirect(url_for("series", series_id=series_id))
    
    # handle errors (cannot start with space)
    if add_series["category"][0] == " ":
        flash("Category cannot start with an empty space...", "warning")
        return redirect(url_for("series", series_id=series_id))

    # handle errors (category too long)
    if len(add_series["category"]) > 20:
        flash("Category is too long...", "warning")
        return redirect(url_for("series", series_id=series_id))

    # no description
    if add_series["text"] == "":
        add_series["text"] = series_edit["text"]

    # handle errors (description too short)
    if len(add_series["text"]) < 100:
        flash("Description is too short...", "warning")
        return redirect(url_for("series", series_id=series_id))
    
    # handle errors (cannot start with space)
    if add_series["text"][0] == " ":
        flash("Description cannot start with an empty space...", "warning")
        return redirect(url_for("series", series_id=series_id))

    # handle errors (description too long)
    if len(add_series["text"]) > 400:
        flash("Description is too long...", "warning")
        return redirect(url_for("series", series_id=series_id))

    # handle empty date
    if add_series["date"] == "":
        add_series["date"] = series_edit["date"]

    # handle image
    if image.filename == "":
        os.rename("static/images/" + series_edit["title"].lower().replace(" ", "_") + ".jpeg", "static/images/" + add_series["title"].lower().replace(" ", "_") + ".jpeg")
    else:
        if "." not in image.filename or (image.filename.split(".")[1] != "jpeg" and image.filename.split(".")[1] != "jpg"):
            flash("Wrong file extension...", "warning")
            return redirect(url_for("series", series_id=series_id))
        image.save("static/images/" + add_series["title"].lower().replace(" ", "_") + ".jpeg")

    add_series["creator_id"] = current_user.id
    add_series["id"] = series_edit["id"]

    # update series
    success = series_dao.update_series(add_series)

    if success:
        flash("Series successfully created!", "success")
    else:
        flash("Something went wrong!", "danger")
    
    return redirect(url_for("series", series_id=series_id))

@app.route("/series/<int:series_id>/delete")
@login_required
def delete_series(series_id):
    # check that series exist
    del_series = series_dao.get_one_series(series_id)
    
    if not del_series:
        flash("This series does not exist...", "danger")
        return redirect(url_for("home"))

    if not current_user.id == del_series["creator_id"]:
        flash("Only creator can delete the series...", "danger")
        return redirect(url_for("home"))
    
    os.remove("static/images/" + del_series["title"].lower().replace(" ", "_") + ".jpeg")
    success = series_dao.del_series(series_id)
    if not success:
        flash("Something went wrong...", "danger")
        return redirect(request.referrer)
    
    shutil.rmtree("static/audio/" + str(del_series["id"]))
    
    flash("Series deleted correctly!", "success")
    return redirect(url_for("home"))

@app.route("/series/<int:series_id>/add_podcast", methods=["POST"])
@login_required
def new_podcast(series_id):
    # check that series exist
    curr_series = series_dao.get_one_series(series_id)

    if not curr_series:
        flash("Cannot add podcast to non existent series...", "danger")
        return redirect(url_for("home"))

    # check user is creator of the series
    creator_id = curr_series["creator_id"]

    if not current_user.id == creator_id:
        flash("Only creator of the series can add new podcasts...", "danger")
        return redirect(url_for("home"))
    
    add_podcast = request.form.to_dict()
    audio = request.files["audio"]

    # handle errors (title too short)
    if len(add_podcast["title"]) < 3:
        flash("Title is too short...", "warning")
        return redirect(url_for("new_podcast"))
    
    # handle errors (cannot start with space)
    if add_podcast["title"][0] == " ":
        flash("Title cannot start with an empty space...", "warning")
        return redirect(url_for("new_podcast"))

    # handle errors (title too long)
    if len(add_podcast["title"]) > 30:
        flash("Title is too long...", "warning")
        return redirect(url_for("new_podcast"))

    # handle errors (description too short)
    if len(add_podcast["description"]) < 30:
        flash("Description is too short...", "warning")
        return redirect(url_for("new_podcast"))
    
    # handle errors (cannot start with space)
    if add_podcast["description"][0] == " ":
        flash("Description cannot start with an empty space...", "warning")
        return redirect(url_for("new_podcast"))

    # handle errors (description too long)
    if len(add_podcast["description"]) > 150:
        flash("Description is too long...", "warning")
        return redirect(url_for("new_podcast"))

    # handle empty date
    if add_podcast["date"] == "":
        add_podcast["date"] = date.today()

    # handle image
    if audio == "":
        flash("Audio is not present...", "warning")
        return redirect(url_for("new_podcast"))
    
    if audio.filename == "":
        flash("File has no name...", "warning")
        return redirect(url_for("new_podcast"))

    if "." not in audio.filename or audio.filename.split(".")[1] != "mp3":
        flash("Wrong file extension...", "warning")
        return redirect(url_for("new_podcast"))
    
    audio.save("static/audio/" + str(curr_series["id"]) + "/" + add_podcast["title"].lower().replace(" ", "_") + ".mp3")

    add_podcast["series_id"] = curr_series["id"]

    # add new series to the series list
    success = podcast_dao.add_podcast(add_podcast)

    if success:
        flash("Podcast successfully added!", "success")
    else:
        flash("Something went wrong!", "danger")
    
    return redirect(url_for("series", series_id=curr_series["id"]))

@app.route("/series/<int:podcast_id>/edit_podcast", methods=["POST"])
@login_required
def edit_podcast(podcast_id):
    # check that podcast exsists
    podcast_edit = podcast_dao.get_podcast(podcast_id)
    series_pod = series_dao.get_one_series(podcast_edit["series_id"])

    # check user is creator of the series
    creator_id = series_pod["creator_id"]
    if not current_user.id == creator_id:
        flash("Only creator of the series can edit podcasts...", "danger")
        return redirect(url_for("series", series_id=series_pod["id"]))
    
    add_podcast = request.form.to_dict()
    audio = request.files["audio"]

    # no title
    if add_podcast["title"] == "":
        add_podcast["title"] = podcast_edit["title"]

    # handle errors (title too short)
    if len(add_podcast["title"]) < 3:
        flash("Title is too short...", "warning")
        return redirect(url_for("new_podcast"))
    
    # handle errors (cannot start with space)
    if add_podcast["title"][0] == " ":
        flash("Title cannot start with an empty space...", "warning")
        return redirect(url_for("new_podcast"))

    # handle errors (title too long)
    if len(add_podcast["title"]) > 30:
        flash("Title is too long...", "warning")
        return redirect(url_for("new_podcast"))

    # no description
    if add_podcast["description"] == "":
        add_podcast["description"] = podcast_edit["description"]

    # handle errors (description too short)
    if len(add_podcast["description"]) < 30:
        flash("Description is too short...", "warning")
        return redirect(url_for("new_podcast"))
    
    # handle errors (cannot start with space)
    if add_podcast["description"][0] == " ":
        flash("Description cannot start with an empty space...", "warning")
        return redirect(url_for("new_podcast"))

    # handle errors (description too long)
    if len(add_podcast["description"]) > 150:
        flash("Description is too long...", "warning")
        return redirect(url_for("new_podcast"))

    # handle empty date
    if add_podcast["date"] == "":
        add_podcast["date"] = podcast_edit["date"]

    # handle audio
    if audio.filename == "":
        os.rename("static/audio/" + series_pod["id"] + "/" + podcast_edit["title"].lower().replace(" ", "_") + ".mp3", "static/audio/" + add_podcast["title"].lower().replace(" ", "_") + ".mp3")
    else:
        if "." not in audio.filename or audio.filename.split(".")[1] != "mp3":
            flash("Wrong file extension...", "warning")
            return redirect(url_for("new_podcast"))
        
        audio.save("static/audio/" + add_podcast["title"].lower().replace(" ", "_") + ".mp3")

    add_podcast["series_id"] = podcast_edit["series_id"]
    add_podcast["id"] = podcast_edit["id"]

    success = podcast_dao.update_podcast(add_podcast)

    if success:
        flash("Podcast successfully added!", "success")
    else:
        flash("Something went wrong!", "danger")
    
    return redirect(url_for("series", series_id=series_pod["id"]))

@app.route("/series/<int:podcast_id>/delete_podcast")
@login_required
def delete_podcast(podcast_id):
    # check that podcast exist
    del_podcast = podcast_dao.get_podcast(podcast_id)
    
    if not del_podcast:
        flash("This podcast does not exist...", "danger")
        return redirect(url_for("home"))

    # check if user is creator of the series
    podcast_series = series_dao.get_one_series(del_podcast["series_id"])

    if not current_user.id == podcast_series["creator_id"]:
        flash("Only creator of the series can delete podcasts...", "danger")
        return redirect(url_for("series", series_id=podcast_series["id"]))
    
    success = podcast_dao.del_podcast(podcast_id)
    if not success:
        flash("Something went wrong...", "danger")
        return redirect(request.referrer)
    
    os.remove("static/audio/" + str(podcast_series["id"]) + "/" + del_podcast["title"].lower().replace(" ", "_") + ".mp3")
    
    flash("Podcast deleted correctly!", "success")
    return redirect(url_for("series", series_id=podcast_series["id"]))

@app.route("/profile")
@login_required
def profile():
    follows = follows_dao.get_follows(current_user.id)

    return render_template("profile.html", follows=follows, get_one_series=series_dao.get_one_series, get_creator=users_dao.get_user_username_by_id)

@app.route("/follow/<int:series_id>")
@login_required
def follow(series_id):
    # check if user already follows
    already_follows = follows_dao.is_following(current_user.id, series_id)

    if already_follows:
        flash("You already follow this series...", "warning")
        return redirect(request.referrer)
    
    new_follow = {"user_id": current_user.id, "series_id": series_id}
    success = follows_dao.add_follow(new_follow)
    if not success:
        flash("Something went wrong...", "danger")
    
    return redirect(request.referrer)

@app.route("/unfollow/<int:series_id>")
@login_required
def unfollow(series_id):
    # check if user is following
    del_follow = follows_dao.is_following(current_user.id, series_id)

    if del_follow:
        success = follows_dao.delete_follow(del_follow["id"])
        if not success:
            flash("Something went wrong...", "danger")
    return redirect(request.referrer)

@app.route("/podcast/<int:podcast_id>/new_comment", methods=["POST"])
@login_required
def new_comment(podcast_id):
    comment = request.form.to_dict()

    if len(comment["comment"]) < 3:
        flash("Comment is too short...", "warning")
        return redirect(url_for("home"))
    
    if comment["comment"][0] == " ":
        flash("Comment cannot start with an empty space...", "warning")
        return redirect(url_for(request.referrer))

    if len(comment["comment"]) > 30:
        flash("Comment is too long...", "warning")
        return redirect(url_for("home"))

    # handle date
    comment["date"] = date.today()

    comment["user_id"] = current_user.id
    comment["podcast_id"] = podcast_id

    success = comments_dao.post_comment(comment)

    if not success:
        flash("Something went wrong!", "danger")
    
    return redirect(request.referrer)

@app.route("/podcast/<int:comment_id>/del_comment")
@login_required
def delete_comment(comment_id):
    # check that comment exist
    comment = comments_dao.get_comment(comment_id)
    
    if not comment:
        flash("This comment does not exist...", "danger")
        return redirect(url_for("home"))

    # check if user posted the comment
    if not current_user.id == comment["user_id"]:
        flash("Only user who posted the comment can delete it...", "danger")
        return redirect(url_for("home"))
    
    success = comments_dao.del_comment(comment_id)
    if not success:
        flash("Something went wrong...", "danger")
        return redirect(request.referrer)

    return redirect(request.referrer)

@login_manager.user_loader
def load_user(id):
    user = users_dao.get_user_by_id(id)
    
    if user is not None:
        user_obj = User(user["id"], user["username"], user["email"], user["password"], user["is_creator"])
    else:
        user_obj = None

    return user_obj

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    elif request.method == "POST":
        user = request.form.to_dict()

        user_db = users_dao.get_user_by_email(user["email"])

        if not user_db or not check_password_hash(user_db["password"], user["password"]):
            flash("Email or password are wrong, try again...", "warning")
            return redirect(request.referrer)
        else:
            user_obj = User(user_db["id"], user_db["username"], user_db["email"], user_db["password"], user_db["is_creator"])
            app.logger.debug(user_obj)
            success = login_user(user_obj, True)

            if success:
                return redirect(url_for("home"))
            else:
                flash("Something went wrong...", "danger")
                return redirect(request.referrer)
            

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "GET":
        return render_template("signup.html")
    elif request.method == "POST":
        new_user = request.form.to_dict()

        # check that new user is not already signed up (check by email)
        user_db = users_dao.get_user_by_email(new_user["email"])
        
        if user_db:
            flash("This email has already been used...", "warning")
            return redirect(request.referrer)
        
        else:
            # check all fields are correct
            if new_user["username"] == "":
                flash("Username is required...", "warning")
                return redirect(request.referrer)
            
            if len(new_user["username"]) > 20:
                flash("Username is too long...", "warning")
                return redirect(request.referrer)
            
            if new_user["email"] == "":
                flash("Email is required...", "warning")
                return redirect(request.referrer)

            if len(new_user["password"]) < 8:
                flash("Password is too short...", "warning")
                return redirect(request.referrer)

            if len(new_user["password"]) > 30:
                flash("Password is too long...", "warning")
                return redirect(request.referrer)

            new_user["password"] = generate_password_hash(new_user["password"], method="sha256")
            app.logger.debug(new_user)
            if new_user.get("is_creator"):
                new_user["is_creator"] = 1
            else:
                new_user["is_creator"] = 0

            success = users_dao.add_user(new_user)
            
            if success:
                flash("User successfully created!", "success")
                return redirect(url_for("login"))
            else:
                flash("Something went wrong...", "danger")
                return redirect(request.referrer)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run("localhost", 3000, True)