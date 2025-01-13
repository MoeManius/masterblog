from flask import Flask, render_template, request, redirect, url_for
import json

app = Flask(__name__)


@app.route('/')
def index():
    # Fetch blog posts from the JSON file
    with open('posts.json', 'r') as file:
        blog_posts = json.load(file)

    # Render the blog posts
    return render_template('index.html', posts=blog_posts)


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        # Get form data from the request
        title = request.form.get('title')
        author = request.form.get('author')
        content = request.form.get('content')

        # Read the existing posts from the JSON file
        with open('posts.json', 'r') as file:
            blog_posts = json.load(file)

        # Generate a new ID based on the existing posts
        new_id = max(post['id'] for post in blog_posts) + 1 if blog_posts else 1

        # Create a new blog post
        new_post = {
            'id': new_id,
            'author': author,
            'title': title,
            'content': content
        }

        # Add the new post to the list of blog posts
        blog_posts.append(new_post)

        # Write the updated list back to the JSON file
        with open('posts.json', 'w') as file:
            json.dump(blog_posts, file, indent=4)

        # Redirect to the home page after adding the post
        return redirect(url_for('index'))

    return render_template('add.html')


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
