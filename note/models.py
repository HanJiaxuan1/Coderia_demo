from django.db import models

# Create your models here.
from django.db import models

# Create your models here.
from django.conf import settings


# 帖子编辑的表单设计
from django.utils import timezone
from werkzeug.security import generate_password_hash, check_password_hash


class User(models.Model):
    uid = models.AutoField(primary_key=True, unique=True)
    username = models.CharField(max_length=64, unique=True, db_index=True)
    password_hash = models.CharField(max_length=64)

    # notes = db.relationship('Note', backref='author', lazy='dynamic', cascade='all, delete-orphan')
    # # liked_note = db.relationship('Like', back_populates='liker', lazy='dynamic', cascade='all, delete-orphan')
    #
    def to_json(self):
        dict = self.__dict__
        if '_sa_instance_state' in dict:
            del dict['_sa_instance_state']
        return dict

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
    #
    # def like(self, note):
    #     if not self.is_liking(note):
    #         ll = Like(liker=self, liked_note=note)
    #         db.session.add(ll)
    #         db.session.commit()
    #
    # def is_liking(self, note):
    #     if note.id is None:
    #         return False
    #     return self.liked_note.filter_by(
    #         liked_note_id=note.note_id).first() is not None
    #
    # def cancel_like(self, note):
    #     ll = self.liked_note.filter_by(liked_note_id=note.note_id).first()
    #     if ll:
    #         db.session.delete(ll)
    #         db.session.commit()


class Profile(models.Model):
    uid = models.AutoField(primary_key=True, unique=True)
    email = models.CharField(max_length=64, unique=True)


class Video(models.Model):
    vid = models.AutoField(primary_key=True, unique=True)
    uid = models.IntegerField()
    name = models.CharField(max_length=64, unique=True)
    text = models.TextField()
    language = models.CharField(max_length=64)


# note_tag = db.Table('note_tag',
#                     db.Column('note_id', db.Integer, db.ForeignKey('notes.note_id'), primary_key=True),
#                     db.Column('tag_id', db.Integer, db.ForeignKey('tags.tag_id'), primary_key=True)
#                     )


class Note(models.Model):
    note_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=64, null=False, default='')
    content = models.TextField()
    content_html = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now, db_index=True)
    uid = models.ForeignKey(User, on_delete=models.CASCADE)
    important = models.IntegerField(default=0)
    recent_activity = models.DateTimeField(default=timezone.now, db_index=True)
    # tags = db.relationship('NoteTag', secondary=note_tag, backref=db.backref('notes'))

    # comments = db.relationship('Comment', back_populates='note', cascade='all, delete-orphan', lazy='dynamic')
    # liker = db.relationship('Like', back_populates='liked_post', lazy='dynamic', cascade='all')

    @staticmethod
    def on_changed_body(target, value, oldvalue, initiator):
        allowed_tags = ['a', 'abbr', 'acronym', 'b', 'blockquote', 'code',
                        'em', 'i', 'li', 'ol', 'pre', 'strong', 'ul',
                        'h1', 'h2', 'h3', 'p', 'img', 'div', 'iframe',
                        'p', 'br', 'span', 'hr', 'src', 'class',
                        'table', 'tr', 'th']
        allowed_attrs = {'*': ['class'],
                         'a': ['href', 'rel'],
                         'img': ['src', 'alt']}
        # target.body_html = bleach.linkify(bleach.clean(
        #     markdown(value, output_format='html'),
        #     tags=allowed_tags, strip=True, attributes=allowed_attrs))


# db.event.listen(Note.content, 'set', Note.on_changed_body)


# class NoteTag(models.Model):
#     __tablename__ = 'tags'
#     tag_id = db.Column(db.Integer, primary_key=True, autoincrement=True, index=True)
#     tag_name = db.Column(db.String(64), unique=True, index=True)
