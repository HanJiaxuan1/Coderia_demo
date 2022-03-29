from django.db import models

# Create your models here.
from django.db import models

# Create your models here.
from django.conf import settings

# 帖子编辑的表单设计
from django.utils import timezone
from django.utils.html import strip_tags
from werkzeug.security import generate_password_hash, check_password_hash


class User(models.Model):
    uid = models.AutoField(primary_key=True, unique=True)
    username = models.CharField(max_length=64, unique=True, db_index=True)
    first_name = models.CharField(max_length=64, null=True)
    last_name = models.CharField(max_length=64, null=True)
    password_hash = models.CharField(max_length=64)
    telephone = models.CharField(max_length=11, null=True, unique=True)
    avatar = models.ImageField(upload_to='avatar', default='pic1.jpg', null=True, verbose_name='avatar')
    region = models.CharField(max_length=32, null=True)
    email = models.CharField(max_length=64, null=True, unique=True)
    birthday = models.CharField(max_length=64, null=True)

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

    def is_collect(self, note):
        if note.note_id is None:
            return False
        return UserCollectNote.objects.filter(user_id=self.uid, note_id=note.note_id).first() is not None

    def collect(self, note):
        if not self.is_collect(note):
            user_note = UserCollectNote(user=self, note=note)
            user_note.save()

    def cancel_collect(self, note):
        if self.is_collect(note):
            user_note = UserCollectNote.objects.filter(user_id=self.uid, note_id=note.note_id).first()
            user_note.delete()
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

class Category(models.Model):
    name = models.CharField(max_length=32, verbose_name='Category')
    detail = models.CharField(max_length=100, verbose_name='Detail', null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Category'


class Tag(models.Model):
    name = models.CharField(max_length=32, verbose_name='Tag')
    detail = models.CharField(max_length=100, verbose_name='Detail', null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tag'


class Note(models.Model):
    note_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=64, verbose_name='note title', db_index=True)
    content = models.TextField(verbose_name='note content')
    content_html = models.TextField(verbose_name='note content html version')
    excerpt = models.CharField(max_length=200, blank=True, verbose_name='note excerpt')
    create_time = models.DateTimeField(default=timezone.now, db_index=True, verbose_name='create time')
    uid = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='author')
    important = models.IntegerField(default=0)
    recent_activity = models.DateTimeField(default=timezone.now, db_index=True)

    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='category', default=None)
    tags = models.ManyToManyField(Tag, blank=True, verbose_name='Tag')
    views = models.IntegerField(default=0, verbose_name='the number of views')

    def increase_views(self):
        self.views += 1
        self.save(update_fields=['views'])

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if not self.excerpt:
            self.excerpt = strip_tags(self.content_html)[:120]
            super(Note, self).save()
        else:
            super(Note, self).save()

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

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-create_time']
        verbose_name = 'note manage'
        verbose_name_plural = 'note manage'


class Comment(models.Model):
    cid = models.AutoField(primary_key=True)
    # 记录comment所属的用户
    uid = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='author')
    # 记录comment所属的note
    note_id = models.ForeignKey(Note, on_delete=models.CASCADE, verbose_name='note')
    content = models.TextField(verbose_name='note content')
    content_html = models.TextField(verbose_name='note content html version')
    create_time = models.DateTimeField(default=timezone.now, db_index=True, verbose_name='create time')
    # 记录views的数量
    views = models.IntegerField(default=0, verbose_name='the number of views')

    def increase_views(self):
        self.views += 1
        self.save(update_fields=['views'])


# 防止模型的参数过于复杂，直接分离reply和comment
class Reply(models.Model):
    rid = models.AutoField(primary_key=True)
    # 记录reply所属的用户
    uid = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='author')
    # 记录reply所属的comment
    cid = models.ForeignKey(Note, on_delete=models.CASCADE, verbose_name='comment')
    # 记录这条reply是否为回复他人的reply
    # 这里直接记录target的id，可能会没有这个target_id因此不用外键
    target_id = models.IntegerField(default=-1, verbose_name="the id of the target user")
    content = models.TextField(verbose_name='note content')
    content_html = models.TextField(verbose_name='note content html version')
    create_time = models.DateTimeField(default=timezone.now, db_index=True, verbose_name='create time')
    # 记录views的数量
    views = models.IntegerField(default=0, verbose_name='the number of views')

    def increase_views(self):
        self.views += 1
        self.save(update_fields=['views'])


class UserCollectNote(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='user')
    note = models.ForeignKey(Note, on_delete=models.CASCADE, verbose_name='note')


class UserLikeNote(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='user')
    note = models.ForeignKey(Note, on_delete=models.CASCADE, verbose_name='note')
