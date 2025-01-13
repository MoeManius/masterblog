from flask import Flask, render_template
import json

app = Flask(__name__)


@app.route('/')
def index():
    # Fetch blog posts from the JSON file
    with open('posts.json', 'r') as file:
        blog_posts = json.load(file)

    # Render the blog posts
    return render_template('index.html', posts=blog_posts)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
