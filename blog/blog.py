from sqlite3 import Error, IntegrityError

from flask import (Blueprint, flash, g, redirect, render_template, request, url_for, json)

from blog.db import get_db

bp = Blueprint('blog', __name__, url_prefix='/blog')



@bp.route('/create', methods=('GET','POST'))
def createBlogPost():
    if request.method == 'POST':
        try:
            data = request.get_json()
            title = data['title']
            blog_summary = data['blogSummary']
            blog_content = data['blogContent']

            if not title:
                return json.jsonify({"status": 400, "message": "A title must be included"})
            if not blog_summary:
                return json.jsonify({"status": 400, "message": "A blog summary must be included"})
            if not blog_content:
                return json.jsonify({"status": 400, "message": "Blog content must be included"})
            return json.jsonify({"status": 200, "message": "Blog post created successfully"})
        except Exception as e: 
            print("An unexpected error occured: ", e)

    return render_template('blog/blog_form.html')
