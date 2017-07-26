from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from courses.models import Topic, Resource


class UserProfile(models.Model):

    USER_TYPES = (
        ('b', 'Blogger'),
        ('r', 'Reader')
    )

    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                related_name='profile')
    avatar = models.ImageField(blank=True)
    about = models.TextField(blank=True)
    user_type = models.CharField(max_length=1, choices=USER_TYPES, default='b')

    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        if self.id and self.avatar:
            current_avatar = UserProfile.objects.get(pk=self.id).avatar
            if current_avatar != self.avatar:
                current_avatar.delete()
        super(UserProfile, self).save(*args, **kwargs)

    def get_absolute_url(self):
        target = reverse('authapp:profile', args=[self.user.username])
        return target

    def is_blogger(self):
        return self.user_type == 'b'

    def is_reader(self):
        return self.user_type == 'r'


class SavedResource(models.Model):
    user = models.ForeignKey(User)
    resource = models.ForeignKey(Resource)
    saved_at = models.DateTimeField(auto_now_add=True,editable=False)
    
    class Meta:
        unique_together = (('user', 'resource'),)

    def __unicode__(self):
        return '%s %s'  %(self.user,self.resource) 

class TopicFollow(models.Model):
    user = models.ForeignKey(User)
    topic = models.ForeignKey(Topic)
    followed_at = models.DateTimeField(auto_now_add=True,editable=False)
    
    class Meta:
        unique_together = (('user','topic'),)

    def __unicode__(self):
        return '%s %s' %(self.user,self.topic)
            
