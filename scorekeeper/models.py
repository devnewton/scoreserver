from django.db import models
from django.conf import settings
from django.utils.encoding import smart_str    

class Game(models.Model):
    slug = models.SlugField(max_length=80, unique=True)
    name = models.CharField(max_length=80)
    description = models.TextField()
    nbScoreSubmitted = models.PositiveIntegerField(default=0);
    def __unicode__(self):
        return self.name
    @models.permalink
    def get_absolute_url(self):
        return ('scorekeeper.views.game_detail', [smart_str(self.slug)])
    
class Level(models.Model):
    slug = models.SlugField(max_length=80, unique=True)
    name = models.CharField(max_length=80)
    game=models.ForeignKey(Game)
    def __unicode__(self):
        return self.name
    @models.permalink
    def get_absolute_url(self):
        return ('scorekeeper.views.level_detail', [smart_str(self.slug)])
    def sorted_scores(self):
        return self.score_set.all().order_by('-score')
    def cleanup(self):
        if self.score_set.count() > settings.SCORESERVER_MAX_SCORE_TO_KEEP:
            for scoreToDelete in self.score_set.all().order_by('-score')[settings.SCORESERVER_MAX_SCORE_TO_KEEP:]:
                scoreToDelete.delete()

class Player(models.Model):
    slug = models.SlugField(max_length=80, unique=True)
    secret = models.SlugField(max_length=80)
    registered = models.BooleanField(default=False)
    @models.permalink
    def get_absolute_url(self):
        return ('scorekeeper.views.player_detail', [smart_str(self.slug)])
    def __unicode__(self):
        return self.slug
    def sorted_scores(self):
        return self.score_set.all().order_by('-level__name', '-score')
    @staticmethod
    def cleanup():
        for player in Player.objects.annotate(num_scores = models.Count('score')).filter(num_scores = 0, registered=False):
            player.delete()

class Score(models.Model):
    player = models.ForeignKey(Player)
    level = models.ForeignKey(Level)
    score = models.IntegerField()
    def __unicode__(self):
        return self.level.name + ': ' + self.player.slug + ' = ' + smart_str(self.score )    
