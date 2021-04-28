#encoding:utf-8

from exts import db
from datetime import datetime

# 定义关注、被关注模型
class Follow(db.Model):
    __tablename = 'follows'     # 数据库表名

    # 用户关注的人 id
    follower_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    # 用户粉丝 id
    followed_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    # 关注时间
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)


# 定义用户模型
class User(db.Model):
    __tablename__='user'
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)#用户id
    telephone=db.Column(db.String(11),nullable=False)           #手机号
    username=db.Column(db.String(50),nullable=False)            #用户名
    password=db.Column(db.String(100),nullable=False)           #密码
    comments = db.relationship('Comment',backref='author',lazy='dynamic')
    videos = db.relationship('Video',backref='author',lazy='dynamic')
    # 用户关注的人<关系>
    followed = db.relationship('Follow',
                               foreign_keys=[Follow.follower_id],       # 在 Follow 模型中自引用
                               backref=db.backref('follower', lazy='joined'),   # join 立即加载所有相关对象
                               lazy='dynamic',
                               cascade='all, delete-orphan')            # 删除所有记录
    # 用户的粉丝<关系>
    followers = db.relationship('Follow',
                                foreign_keys=[Follow.followed_id],      # 在 Follow 模型中自引用
                                backref=db.backref('followed', lazy='joined'),  # join 立即加载所有相关对象
                                lazy='dynamic',
                                cascade='all, delete-orphan')           # 删除所有记录


# 定义视频模型
class Video(db.Model):
    __tablename__ = 'video'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # 视频id
    name = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)  # 视频内容 用文本代替
    desc = db.Column(db.String(100), nullable=False)  # 视频简介
    # now()获取的是服务器第一次运行的时间
    # now就是每次创建一个模型的时候 都获取当前时间
    create_time = db.Column(db.DateTime, default=datetime.now)  # 发布时间
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # 发布者
    # comments = db.relationship('Comment',backref='video',lazy='dynamic')

# 定义问题模型
class Question(db.Model):
    __tablename__='question'
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    title=db.Column(db.String(100),nullable=False)
    content=db.Column(db.Text,nullable=False)
    # now()获取的是服务器第一次运行的时间
    # now就是每次创建一个模型的时候 都获取当前时间
    create_time=db.Column(db.DateTime,default=datetime.now)
    author_id=db.Column(db.Integer,db.ForeignKey('user.id'))
    author=db.relationship('User',backref=db.backref('questions'))


# 定义评论模型
class Answer(db.Model):
    __tablename__='answer'
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    content=db.Column(db.Text,nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)
    question_id=db.Column(db.Integer,db.ForeignKey('question.id'))
    author_id=db.Column(db.Integer,db.ForeignKey('user.id'))
    question=db.relationship('Question',backref=db.backref('answers'))
    author=db.relationship('User',backref=db.backref('answers'))

# 定义评论模型
class Comment(db.Model):
    __tablename__ = 'comment'  # 数据库表名
    id = db.Column(db.Integer, primary_key=True)  # 评论 id
    content = db.Column(db.Text, nullable=False)  # 评论内容
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)  # 评论时间
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # 作者 id
    video_id = db.Column(db.Integer, db.ForeignKey('video.id'))  # 视频 id
    video = db.relationship('Video', backref=db.backref('comments'))
