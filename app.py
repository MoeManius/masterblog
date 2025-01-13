from flask import Flask, render_template, request, redirect, url_for
import json

app = Flask(__name__)

# Helper function to load blog posts from the JSON file
def load_posts():
    with open('blog_posts.json', 'r') as file:
        return json.load(file)

# Helper function to save blog posts to the JSON file
def save_posts(posts):
    with open('blog_posts.json', 'w') as file:
        json.dump(posts, file, indent=4)

@app.route('/')
def index():
    """
    Index route to display all blog posts.
    """
    blog_posts = load_posts()
    return render_template('index.html', posts=blog_posts)

@app.route('/add', methods=['GET', 'POST'])
def add():
    """
    Add route to create a new blog post.
    """
    if request.method == 'POST':
        # Retrieve data from the form
        author = request.form.get('author')
        title = request.form.get('title')
        content = request.form.get('content')

        # Load existing blog posts
        blog_posts = load_posts()

        # Generate a unique ID for the new post
        new_id = max(post['id'] for post in blog_posts) + 1 if blog_posts else 1

        # Create a new blog post dictionary
        new_post = {
            "id": new_id,
            "author": author,
            "title": title,
            "content": content,
            "likes": 0  # Initialize likes to 0
        }

        # Append the new post and save to the JSON file
        blog_posts.append(new_post)
        save_posts(blog_posts)

        # Redirect to the index page
        return redirect(url_for('index'))

    # If GET request, render the add post form
    return render_template('add.html')

@app.route('/delete/<int:post_id>', methods=['POST'])
def delete(post_id):
    """
    Delete route to remove a blog post by its ID.
    """
    blog_posts = load_posts()

    # Filter out the post to be deleted
    blog_posts = [post for post in blog_posts if post['id'] != post_id]

    # Save the updated posts back to the JSON file
    save_posts(blog_posts)

    # Redirect to the index page
    return redirect(url_for('index'))

@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    """
    Update route to edit an existing blog post.
    """
    blog_posts = load_posts()

    # Find the post to be updated
    post = next((p for p in blog_posts if p['id'] == post_id), None)
    if post is None:
        return "Post not found", 404

    if request.method == 'POST':
        # Update post details from the form data
        post['author'] = request.form.get('author')
        post['title'] = request.form.get('title')
        post['content'] = request.form.get('content')

        # Save the updated posts to the JSON file
        save_posts(blog_posts)

        # Redirect to the index page
        return redirect(url_for('index'))

    # If GET request, render the update form with the current post details
    return render_template('update.html', post=post)

@app.route('/like/<int:post_id>', methods=['POST'])
def like(post_id):
    """
    Like route to increment the 'likes' count of a blog post.
    """
    blog_posts = load_posts()

    # Find the post to be liked
    for post in blog_posts:
        if post['id'] == post_id:
            post['likes'] += 1
            break

    # Save the updated posts back to the JSON file
    save_posts(blog_posts)

    # Redirect to the index page
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
