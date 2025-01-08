from marshmallow import Schema, fields


class UserSchema(Schema):
    id = fields.Int()
    username = fields.Str() 
    email = fields.Str()   

class BlogSchema(Schema):
    id = fields.Int()
    title = fields.Str()
    content = fields.Str()
    author = fields.Str()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()
