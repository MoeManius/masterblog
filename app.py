from flask import Flask, render_template, request, redirect, url_for
import json

app = Flask(__name__)


def fetch_post_by_id(post_id):
    # Fetch blog posts from the JSON file
    with open('posts.json', 'r') as file:
        blog_posts = json.load(file)

    # Find the post with the matching ID
    for post in blog_posts:
        if post['id'] == post_id:
            return post
    return None


@app.route('/')
def index():
    with open('posts.json', 'r') as file:
        blog_posts = json.load(file)
    return render_template('index.html', posts=blog_posts)


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        title = request.form.get('title')
        author = request.form.get('author')
        content = request.form.get('content')

        with open('posts.json', 'r') as file:
            blog_posts = json.load(file)

        new_id = max(post['id'] for post in blog_posts) + 1 if blog_posts else 1
        new_post = {'id': new_id, 'author': author, 'title': title, 'content': content}
        blog_posts.append(new_post)

        with open('posts.json', 'w') as file:
            json.dump(blog_posts, file, indent=4)

        return redirect(url_for('index'))

    return render_template('add.html')


@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    with open('posts.json', 'r') as file:
        blog_posts = json.load(file)

    # Find the post by ID
    post = next((post for post in blog_posts if post['id'] == post_id), None)

    if not post:
        return "Post not found", 404

    if request.method == 'POST':
        # Update post details
        post['title'] = request.form.get('title')
        post['author'] = request.form.get('author')
        post['content'] = request.form.get('content')

        # Save the updated posts list back to the file
        with open('posts.json', 'w') as file:
            json.dump(blog_posts, file, indent=4)

        return redirect(url_for('index'))

    return render_template('update.html', post=post)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
