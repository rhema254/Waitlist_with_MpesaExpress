from exts import db


class user(db.Model):
    
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    email = db.Column(db.String(80), nullable=False)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(), nullable=False)
    verified = db.Column(db.Boolean(), default=False)

    def __repr__(self):
        return f"<User {self.username} with email {self.email} >"
    
    ## Methods for convenience

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self, email, username, password):
        if email:
            self.email = email
        if username:
            self.username = username
        if password:
                self.password = password    
        
        db.session.commit()

    def verify(self):
        self.verified = True

        db.session.commit()