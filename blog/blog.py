import datetime
from sqlite3 import Error, IntegrityError

from flask import (Blueprint, flash, g, redirect, render_template, request, url_for, json, abort, session)

from blog.db import get_db



bp = Blueprint('blog', __name__, url_prefix='/blog')


@bp.route('/create', methods=('GET','POST'))
def createBlogPost():
    if request.method == 'POST':
            db = get_db()
            data = request.get_json()
            title = data['title']
            blog_summary = data['blogSummary']
            blog_content = data['blogContent']

            if not title:
                return json.jsonify({"status": 400, "message": "A title must be included"}), 400

            if not blog_summary:
                return json.jsonify({"status": 400, "message": "A blog summary must be included"}), 400

            if not blog_content:
                return json.jsonify({"status": 400, "message": "Blog content must be included"}), 400

            try:
                user_id = session.get('user_id')
                today = datetime.datetime.now().isoformat()
                cursor = db.execute('INSERT INTO blog_posts (user_id, created_at, blog_title, synopsis)' 'VALUES (?, ?, ?, ?)', (user_id, today, title, blog_summary))
                db.commit()
                print(cursor.lastrowid)
                print(blog_content)
                db.execute('INSERT INTO blog_content (blog_post_id, blog_post)' 'VALUES(?,?)', (cursor.lastrowid, blog_content))
                db.commit()
                return json.jsonify({"status": 200, "message": "Blog post created successfully"}), 200
            except Exception as e: 
                print("An unexpected error occured: ", e)

    return render_template('blog/blog_form.html')
