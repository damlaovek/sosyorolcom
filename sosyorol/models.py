from math import inf
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
    followers = models.QuerySet()
    followings = models.QuerySet()
    blocked = models.QuerySet()
    posts = models.QuerySet()
    employments = ""
    educations = ""
    languages = ""
    locations = ""
    relatives = ""
    birthday = dict()
    employment_credentials = []
    education_credentials = []
    language_credentials = []
    location_credentials = []
    website = ""
    class Meta:
        db_table = "wpmu_users"
    
    def set_description(self, user_desc):
        self.description = user_desc
    
    def set_avatar(self, img_url):
        self.avatar_url = img_url

class UserMeta(models.Model):
    umeta_id = models.BigIntegerField(primary_key = True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    meta_key = models.TextField()
    meta_value = models.TextField()
    class Meta:
        db_table = "wpmu_usermeta"

class UserRelation(models.Model):
    ID = models.BigIntegerField(primary_key = True)
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follower')
    date = models.DateTimeField()
    class Meta:
        db_table = "user_relations"

class UserData(models.Model):
    field_id = models.BigIntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    value = models.TextField()
    class Meta:
        db_table = "wpmu_bp_xprofile_data"

class BlockedUsers(models.Model):
    ID = models.BigIntegerField(primary_key = True)
    blocker = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blocker')
    blocking = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blocking')
    date = models.DateTimeField()
    class Meta:
        db_table = "blocked_accounts"

# Post related models.
class Post(models.Model):
    ID = models.BigIntegerField(primary_key = True)
    post_author = models.BigIntegerField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    hex_id = ""
    post_date = models.DateTimeField()
    post_modified = models.DateTimeField()
    post_content = models.TextField()
    post_title = models.TextField()
    post_excerpt = models.TextField()
    post_parent = models.BigIntegerField()
    post_status = models.TextField()
    guid = models.TextField()
    post_type = models.TextField() 
    to_ping = models.TextField() 
    pinged = models.TextField()
    post_content_filtered = models.TextField()
    parent = None
    rating = 0
    likes = models.QuerySet()
    dislikes = models.QuerySet()
    repost = models.QuerySet()
    short_content = ""
    preview = ""
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
    communities = models.QuerySet()
    flairs = models.QuerySet()
    first_community = ""
    quiz_questions = []
    quiz_results = []
    media_type = ""
    media_url = ""
    answers = models.QuerySet()
    quiz_type = ""
    isanswered = False
    isfollowed = 0
    class Meta:
        db_table = "wpmu_posts"

class PostRating(models.Model):
    ID = models.BigIntegerField(primary_key = True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
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

class FollowedPosts(models.Model):
    ID = models.BigIntegerField(primary_key = True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField()
    following = models.IntegerField()
    class Meta:
        db_table = "followed_posts"

class PostRequest(models.Model):
    ID = models.BigIntegerField(primary_key = True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    post_type = models.TextField()
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sender")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="receiver")
    date = models.DateTimeField()
    answered = models.IntegerField()
    class Meta:
        db_table = "post_requests"

class SimilarPosts(models.Model):
    ID = models.BigIntegerField(primary_key = True)
    post1 = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="post1")
    post2 = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="post2")
    similarity = models.FloatField()
    class Meta:
        db_table = "post_similarities"

# Comment related models.
class Comment(models.Model):
    comment_ID = models.BigIntegerField(primary_key = True)
    comment_post_ID = models.BigIntegerField()
    comment_content = models.TextField()
    comment_approved = models.SmallIntegerField()
    comment_author = models.TextField()
    comment_parent = models.BigIntegerField()
    comment_author_email = models.TextField()
    child_comments = models.QuerySet()
    comment_date = models.DateTimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    class Meta:
        db_table = "wpmu_comments"

# Community related models.
class Community(models.Model):
    term_id = models.BigIntegerField(primary_key = True)
    name = models.TextField()
    slug = models.TextField()
    tag_img = ""
    tag_color = ""
    count = 0
    metadesc = ""
    lower_name = ""
    description = models.TextField()
    cover_img = models.TextField()
    profile_img = models.TextField()
    profile_img_small = models.TextField()
    nsfw = models.IntegerField()
    cover_color = models.TextField()
    is_public = models.TextField()
    date_created = models.DateTimeField()
    views = models.BigIntegerField()
    posts = models.QuerySet()
    flairs = models.QuerySet()
    followers = models.QuerySet()
    score = models.BigIntegerField()
    popularity_change = ""
    rank = 0
    is_followed = False
    class Meta:
        db_table = "communities"

class Flairs(models.Model):
    ID = models.BigIntegerField(primary_key = True)
    term = models.ForeignKey(Community, on_delete=models.CASCADE)
    flair = models.TextField()
    flair_type = models.TextField()
    background_color = models.TextField()
    text_color = models.TextField()
    class Meta:
        db_table = "community_flairs"

class PostFlair(models.Model):
    ID = models.BigIntegerField(primary_key = True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    flair = models.ForeignKey(Flairs, on_delete=models.CASCADE)
    class Meta:
        db_table = "post_flair"

class CommunityCategories(models.Model):
    term_id = models.BigIntegerField(primary_key = True)
    name = models.TextField()
    slug = models.TextField()
    class Meta:
        db_table = "community_categories"

class CommunityCategoryRelation(models.Model):
    ID = models.BigIntegerField(primary_key = True)
    community = models.ForeignKey(Community, on_delete=models.CASCADE)
    category = models.ForeignKey(CommunityCategories, on_delete=models.CASCADE)
    relation = models.IntegerField()
    class Meta:
        db_table = "community_category_relation"

class TermTaxonomy(models.Model):
    term_taxonomy_id = models.BigIntegerField(primary_key = True)
    term = models.ForeignKey(Community, on_delete=models.CASCADE)
    taxonomy = models.TextField()
    description = models.TextField()
    count = models.BigIntegerField()
    parent = models.BigIntegerField()
    class Meta:
        db_table = "wpmu_term_taxonomy"

class TermRelationship(models.Model):
    object_id = models.BigIntegerField()
    term_taxonomy_id = models.BigIntegerField()
    term_order = models.BigIntegerField()
    class Meta:
        db_table = "wpmu_term_relationships"

class FollowedCommunities(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    term = models.ForeignKey(Community, on_delete=models.CASCADE)
    date = models.DateTimeField()
    role = models.TextField()
    is_active = models.IntegerField()
    class Meta:
        db_table = "term_members"

class CommunityMeta(models.Model):
    meta_id = models.BigIntegerField(primary_key = True)
    term = models.ForeignKey(Community, on_delete=models.CASCADE)
    meta_key = models.TextField()
    meta_value = models.TextField()
    class Meta:
        db_table = "wpmu_termmeta"

class YoastMetaFields(models.Model):
    object_id = models.BigIntegerField()
    title = models.TextField()
    description = models.TextField()
    class Meta:
        db_table = "wpmu_yoast_indexable"

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

# Country Code
class Country(models.Model):
    ID = models.BigIntegerField(primary_key = True)
    iso = models.TextField()
    nicename = models.TextField()
    phonecode = models.TextField()
    class Meta:
        db_table = "country_phone_code"


# History
class SearchHistory(models.Model):
    ID = models.BigIntegerField(primary_key = True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='search_history_user')
    search_term = models.TextField()
    date = models.DateTimeField()
    history_type="search"
    is_deleted = models.IntegerField()
    counter = models.BigIntegerField()
    class Meta:
        db_table = "search_history"

class PostHistory(models.Model):
    ID = models.BigIntegerField(primary_key = True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='post_history_user')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_history_post')
    date = models.DateTimeField()
    history_type="post"
    is_deleted = models.IntegerField()
    counter = models.BigIntegerField()
    class Meta:
        db_table = "post_history"

class CommunityHistory(models.Model):
    ID = models.BigIntegerField(primary_key = True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='community_history_user')
    term = models.ForeignKey(Community, on_delete=models.CASCADE, related_name='community_history_community')
    date = models.DateTimeField()
    history_type="community"
    is_deleted = models.IntegerField()
    counter = models.BigIntegerField()
    class Meta:
        db_table = "community_history"

class UserHistory(models.Model):
    ID = models.BigIntegerField(primary_key = True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_history_user')
    visited_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_history_visited_user')
    date = models.DateTimeField()
    history_type="profile"
    is_deleted = models.IntegerField()
    counter = models.BigIntegerField()
    class Meta:
        db_table = "user_history"

# Notifications
class Notification(models.Model):
    ID = models.BigIntegerField(primary_key = True)
    notification_variable = models.TextField()
    notification = ""
    date = models.DateTimeField()
    seen = models.IntegerField()
    opened = models.IntegerField()
    url = models.TextField()
    from_u = models.ForeignKey(User, on_delete=models.CASCADE, related_name='from_user')
    to_u = models.ForeignKey(User, on_delete=models.CASCADE, related_name='to_user')
    related_obj = models.BigIntegerField()
    date_diff = ""
    class Meta:
        db_table = "notifications"


