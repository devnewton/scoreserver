from django.db import models

class Game(models.Model):
    slug = models.SlugField(max_length=80, unique=True)
    name = models.CharField(max_length=80)
    description = models.TextField()
    def __unicode__(self):
        return self.name
    @models.permalink
    def get_absolute_url(self):
        return ('scorekeeper.views.game_detail', [str(self.slug)])
    
class Level(models.Model):
    slug = models.SlugField(max_length=80, unique=True)
    name = models.CharField(max_length=80)
    game=models.ForeignKey(Game)
    def __unicode__(self):
        return self.name
    @models.permalink
    def get_absolute_url(self):
        return ('scorekeeper.views.level_detail', [str(self.slug)])
    def sorted_scores(self):
        return self.score_set.all().order_by('-score')

class Player(models.Model):
    slug = models.SlugField(max_length=80, unique=True)
    secret = models.SlugField(max_length=80, unique=True)    
    def __unicode__(self):
        return self.slug

class Score(models.Model):
    player = models.ForeignKey(Player)
    level = models.ForeignKey(Level)
    score = models.IntegerField()
    def __unicode__(self):
        return self.level.name + ': ' + self.player.slug + ' = ' + str(self.score )    
