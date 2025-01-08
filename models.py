from extensions import db

class User(db.Model):
    id = db.Column("id", db.Integer, primary_key=True)
    first_name = db.Column("first_name", db.String(100))
    last_name = db.Column("last_name", db.String(100))
    email = db.Column("email", db.String(100), nullable=False)
    password = db.Column("password", db.String(100), nullable=False)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Blog(db.Model):
    id = db.Column("id", db.Integer, primary_key=True)
    title = db.Column("title", db.String(200), nullable=False)
    content = db.Column("content", db.Text, nullable=False)
    created_at = db.Column("create_at", db.DateTime, nullable=False, default=db.func.now())
    updated_at = db.Column("updated_at", db.DateTime, nullable=False, default=db.func.now())

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    author = db.relationship("User", backref=db.backref("blogs"), lazy=True)

    def __str__(self):
        return self.title

class Revoked_Token(db.Model):
    id = db.Column("id", db.Integer, primary_key=True)
    jti = db.Column("token", db.String(255), nullable=False)
    revoked_at = db.Column("revoked_at", db.DateTime, default=db.func.now())
