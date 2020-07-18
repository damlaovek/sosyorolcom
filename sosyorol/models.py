from django.db import models

class Languages(models.Model):
    var_name = models.TextField()
    lang_code = models.TextField()
    translation = models.TextField()
    class Meta:
        db_table = "languages"

# User related models.
class User(models.Model):
    ID = models.BigIntegerField(primary_key = True)
    user_login = models.TextField()
    user_pass = models.TextField()
    user_nicename = models.TextField()
    user_email = models.EmailField()
    user_url = models.TextField()
    user_registered = models.DateTimeField()
    display_name = models.TextField()
    description = ""
    avatar_url = ""
    class Meta:
        db_table = "wpmu_users"
    
    def set_description(self, user_desc):
        self.description = user_desc
    
    def set_avatar(self, img_url):
        self.avatar_url = img_url

class UserMeta(models.Model):
    umeta_id = models.BigIntegerField(primary_key = True)
    user_id = models.BigIntegerField()
    meta_key = models.TextField()
    meta_value = models.TextField()
    class Meta:
        db_table = "wpmu_usermeta"

# Post related models.
class Post(models.Model):
    ID = models.BigIntegerField(primary_key = True)
    post_author = models.BigIntegerField()
    post_date = models.DateTimeField()
    post_content = models.TextField()
    post_title = models.TextField()
    post_excerpt = models.TextField()
    post_parent = models.BigIntegerField()
    post_status = models.TextField()
    guid = models.TextField()
    post_type = models.TextField() 
    rating = 0
    likes = 0
    dislikes = 0
    short_content = ""
    preview = ""
    author = User()
    comments = models.QuerySet()
    post_images = []
    photo_from_url = ""
    time_diff = ""
    parent_title = ""
    poll_duration = ""
    number_options = 0
    poll_options = models.QuerySet()
    votes = models.QuerySet()
    poll_duration_left = ""
    voted = 0
    vote_percentages = []
    user_rate = ""
    class Meta:
        db_table = "wpmu_posts"

class PostRating(models.Model):
    ID = models.BigIntegerField(primary_key = True)
    post_id = models.BigIntegerField()
    user_id = models.BigIntegerField()
    opinion = models.TextField()
    date = models.DateTimeField()
    class Meta:
        db_table = "sosyorol_post_rating"

class Repost(models.Model):
    ID = models.BigIntegerField(primary_key = True)
    post_id = models.BigIntegerField()
    user_id = models.BigIntegerField()
    comment = models.TextField()
    date = models.DateTimeField()
    class Meta:
        db_table = "repost"

class PostMeta(models.Model):
    meta_id = models.BigIntegerField(primary_key = True)
    post_id = models.BigIntegerField()
    meta_key = models.TextField()
    meta_value = models.TextField()
    percentage = 0
    max_voted = False
    num_votes = 0
    class Meta:
        db_table = "wpmu_postmeta"

class SossyComments(models.Model):
    id = models.BigIntegerField(primary_key = True)
    post_id = models.BigIntegerField()
    user_id = models.BigIntegerField()
    comment = models.TextField()
    choice = models.IntegerField()
    class Meta:
        db_table = "sossy_comments"

class SavedPosts(models.Model):
    ID = models.BigIntegerField(primary_key = True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    saved_at = models.DateTimeField()
    class Meta:
        db_table = "saved_posts"

# Comment related models.
class Comment(models.Model):
    comment_ID = models.BigIntegerField(primary_key = True)
    comment_post_ID = models.BigIntegerField()
    comment_content = models.TextField()
    comment_approved = models.SmallIntegerField()
    comment_author = models.TextField()
    comment_author_email = models.TextField()
    class Meta:
        db_table = "wpmu_comments"

# Community related models.
class TermTaxonomy(models.Model):
    term_taxonomy_id = models.BigIntegerField(primary_key = True)
    term_id = models.BigIntegerField()
    taxonomy = models.TextField()
    count = models.BigIntegerField()
    parent = models.BigIntegerField()
    class Meta:
        db_table = "wpmu_term_taxonomy"

class FollowedCommunities(models.Model):
    user_id = models.BigIntegerField()
    term_id = models.BigIntegerField()
    date = models.DateTimeField()
    role = models.TextField()
    class Meta:
        db_table = "term_members"

class Community(models.Model):
    term_id = models.BigIntegerField(primary_key = True)
    name = models.TextField()
    slug = models.TextField()
    tag_img = ""
    tag_color = ""
    count = 0
    metadesc = ""
    lower_name = ""
    class Meta:
        db_table = "communities"

class CommunityMeta(models.Model):
    meta_id = models.BigIntegerField(primary_key = True)
    term_id = models.BigIntegerField()
    meta_key = models.TextField()
    meta_value = models.TextField()
    class Meta:
        db_table = "wpmu_termmeta"

# Media model
class Media(models.Model):
    ID = models.BigIntegerField(primary_key = True)
    title = models.CharField(max_length=255, blank=True)
    file = models.FileField(upload_to='media/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = "media"

# List related models
class List(models.Model):
    ID = models.BigIntegerField(primary_key = True)
    photo_small = models.TextField()
    photo_medium = models.TextField()
    photo_large = models.TextField()
    name = models.TextField()
    description = models.TextField()
    creator = models.BigIntegerField()
    creator_uname = ""
    created_at = models.DateTimeField()
    is_public = models.SmallIntegerField()
    color = models.TextField()
    url = models.TextField()
    posts = models.QuerySet()
    members = models.QuerySet()
    followers = models.QuerySet()
    is_mine = False
    is_followed = False
    class Meta:
        db_table = "lists"

class ListPost(models.Model):
    ID = models.BigIntegerField(primary_key = True)
    list_id = models.BigIntegerField()
    post_id = models.BigIntegerField()
    class Meta:
        db_table = "list_post"

class ListUser(models.Model):
    ID = models.BigIntegerField(primary_key = True)
    list_id = models.BigIntegerField()
    user_id = models.BigIntegerField()
    role = models.TextField()
    notifications = models.SmallIntegerField()
    date = models.DateTimeField()
    class Meta:
        db_table = "list_user"


