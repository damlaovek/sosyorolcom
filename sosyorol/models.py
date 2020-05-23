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
    post_status = models.TextField()
    guid = models.TextField()
    post_type = models.TextField() 
    class Meta:
        db_table = "wpmu_posts"

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
    class Meta:
        db_table = "wpmu_terms"

class CommunityMeta(models.Model):
    meta_id = models.BigIntegerField(primary_key = True)
    term_id = models.BigIntegerField()
    meta_key = models.TextField()
    meta_value = models.TextField()
    class Meta:
        db_table = "wpmu_termmeta"



