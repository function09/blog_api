from sqlite3 import IntegrityError

from flask import (Blueprint, flash, g, redirect, render_template, request, url_for)

from blog.db import get_db

bp = Blueprint('blog', __name__, url_prefix='/blog')

@bp.route('/create', methods=('GET','POST'))
def createBlogPost():
    return render_template('blog/blog_form.html')
