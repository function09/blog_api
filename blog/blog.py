from sqlite3 import Error, IntegrityError

from flask import (Blueprint, flash, g, redirect, render_template, request, url_for, json, abort)

from blog.db import get_db


bp = Blueprint('blog', __name__, url_prefix='/blog')



@bp.route('/create', methods=('GET','POST'))
def createBlogPost():
    if request.method == 'POST': 
        data = request.get_json()
        title = data['title']
        blog_summary = data['blogSummary']
        blog_content = data['blogContent']
        error = None

        """
        If there are input errors, log them 
        in order to render them
        """
        if not title:
            error = 'A title must be included.'
        elif not blog_summary:
            error = 'A blog summary must be included.'
        elif not blog_content:
            error = 'Blog content must be included.'

        if error is None:
            print("success!")
        else:
            return json.jsonify({"error": error}), 400
    return render_template('blog/blog_form.html')
