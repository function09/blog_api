import datetime
from sqlite3 import Error, IntegrityError

from flask import (Blueprint, flash, g, redirect, render_template, request, url_for, json, abort, session)

from blog.auth import login, login_required
from blog.db import get_db



bp = Blueprint('blog', __name__, url_prefix='/blog')

@bp.route('/create', methods=('GET','POST'))
@login_required
def create():
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
                cursor = db.execute('INSERT INTO blog_posts (user_id, created_at, blog_title, synopsis, published)' 'VALUES (?, ?, ?, ?, ?)', (user_id, today, title, blog_summary, 0))
                db.commit()
                db.execute('INSERT INTO blog_content (blog_post_id, blog_post)' 'VALUES(?,?)', (cursor.lastrowid, blog_content))
                db.commit()
                return json.jsonify({"status": 200, "message": "Blog post created successfully", "redirectUrl": url_for('blog.listBlogPosts')}), 200
            except Exception as e: 
                print("An unexpected error occured: ", e)

    return render_template('blog/blog_form.html')

@bp.route('/posts')
@login_required
def listBlogPosts():
    try:
        db = get_db()
        posts = db.execute('SELECT id, blog_title, synopsis, created_at, last_updated FROM blog_posts').fetchall()
    except Exception as e:
        print("An unexpected error occured: ", e)
        return "An error occured while fetching from database", 500
    return render_template('blog/blog_posts.html', posts=posts)

@bp.route('/posts/<int:post_id>')
def showBlogPost(post_id):
    db = get_db()
    try:
        post = db.execute(
            'SELECT bp.id, bp.blog_title,bp.created_at,bp.last_updated, bp.synopsis, bc.blog_post '
            'FROM blog_posts bp ' 
            'LEFT JOIN blog_content bc ON bp.id = bc.blog_post_id ' 
            'WHERE bp.id = ?', 
            (post_id,),
            ).fetchone()
    except Exception as e:
        print('An exception occured: ', e)
        return 'An error occured while fetching blog post', 500
    if post is None:
        print('No results for query were found')
    return render_template('blog/blog_post.html', post=post)

@bp.route('/posts/<int:post_id>/update', methods=('GET', 'PUT'))
def updatePost(post_id):

    db = get_db()

    if request.method == 'PUT':
        try:
            data = request.get_json()
            title = data['title']
            blog_summary = data['blogSummary']
            blog_content = data['blogContent']
            today = datetime.datetime.now().isoformat()

            db.execute(
            'UPDATE blog_posts '
            'SET blog_title = ?,  synopsis = ?, last_updated = ? '
            'WHERE id = ?',
            (title, blog_summary, today, post_id,)
        )
            db.commit()

            db.execute(
            'UPDATE blog_content '
            'SET blog_post = ? '
            'WHERE blog_post_id = ?',
            (blog_content, post_id,)
        )
            db.commit()
        except Exception as e:
            print('An unexpected error occured: ', e)
    
    try:
        post = db.execute(
            'SELECT bp.id, bp.blog_title, bp.synopsis, bc.blog_post '
            'FROM blog_posts bp INNER JOIN blog_content bc '
            'ON bp.id = bc.blog_post_id '
            'WHERE bp.id = ?', 
            (post_id,),
            ).fetchone()
    
    except Exception as e:
        print('An unexpected error occured: ', e)
        return 'An error occured while fetching blog post', 500
    if  post is None:
            print('No blog posts were found')

    return render_template('blog/blog_update.html', post=post)


