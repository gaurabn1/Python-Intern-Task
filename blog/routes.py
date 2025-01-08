from flask import json, request, jsonify, Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import Blog, User
from extensions import db
from schemas import BlogSchema


blog_blueprint = Blueprint("blog", __name__)

@blog_blueprint.route("/blogs", methods=['GET'])
def get_blogs():
    '''
    This endpoint returns all blogs in the system
    - Method: GET
    '''
    blogs = Blog.query.all()

    # Get all blogs
    if blogs:
        blog_schema = BlogSchema(many=True)
        blog_data = blog_schema.dump(blogs)
        return jsonify({"message": "All Blogs!", "blogs": blog_data}), 200
    return jsonify({"message": "No Blogs Found!"}), 200


@blog_blueprint.route("/<int:id>", methods=["GET"])
def get_blog(id):
    '''
    This endpoint returns a single blog based on the provided id
    -Method: GET
    '''
    blog = Blog.query.filter_by(id=id).first()

    # Get a blog
    if blog:
        blog_schema = BlogSchema()
        blog_data = blog_schema.dump(blog)
        return jsonify({"message": f"Blog with id {id}", "blog": blog_data}), 200
    return jsonify({"message": f"Blog with id {id} not found"}), 404

@blog_blueprint.route("/<int:id>", methods=["PUT", "DELETE"])
@jwt_required()
def update_delete_blog(id):
    '''
    This endpoint allows authenticated users to update or delete a blog with the provided id
    -Method: PUT, DELETE
    - Jwt Required
    '''
    current_user_id = get_jwt_identity()
    blog = Blog.query.filter_by(id=id, user_id=current_user_id).first()

    if not blog:
        return jsonify({"message": f"Blog with id {id} not found or user not authorized"}), 404

    # Delete a blog
    if request.method == "DELETE":
        db.session.delete(blog)
        db.session.commit()
        return jsonify({"message": f"Blog with id {id} deleted"}), 200

    # Update a blog
    if request.method == "PUT":
        data = request.get_json()
        title = data.get("title")
        content = data.get("content")

        if not any([title, content]):
            return jsonify({"message": "No data provided to update"}), 400
        
        if title:
            blog.title = title
        
        if content:    
            blog.content = content

        blog.updated_at = db.func.now()
        db.session.commit()

        updated_blog = Blog.query.filter_by(id=id).first()
        blog_schema = BlogSchema()
        blog_data = blog_schema.dump(updated_blog)

        return jsonify({"message": f"Blog with id {id} updated", "blog": blog_data}), 200

@blog_blueprint.route("/create", methods=["POST"])
@jwt_required()
def create_blog():
    '''
    This endpoint allows authenticated users to create a blog
    -Method: POST
    - Jwt Required
    '''
    data = request.get_json()
    if not data:
        return jsonify({"message": "No data provided"}), 400
    title = data.get("title")
    content = data.get("content")

    if not title or not content:
        return jsonify({"message": "Title and content are required"}), 400

    current_user_id = get_jwt_identity()
    author = User.query.filter_by(id=current_user_id).first()

    if not author:
        return jsonify({"message": "User not authenticated"}), 401

    new_blog = Blog(title=title, content=content, user_id=author.id)
    db.session.add(new_blog)
    db.session.commit()

    blog = Blog.query.filter_by(id=new_blog.id).first()
    blog_schema = BlogSchema()
    blog_data = blog_schema.dump(blog)
    return jsonify({"message": f"New Blog created with title {title}", "blog": blog_data}), 201




