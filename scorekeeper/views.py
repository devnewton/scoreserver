from django.http import HttpResponse
from django.template import RequestContext, loader
from django.views.generic import list_detail
from scorekeeper.models import Game, Level, Player, Score
from django.conf import settings

def index(request):
    games = Game.objects.all().order_by('-name')
    t = loader.get_template('scorekeeper/templates/index.html')
    c = RequestContext(request, {
        'games' : games,
    })
    return HttpResponse(t.render(c))
    
def game_detail(request, game_slug):
    return list_detail.object_detail( request, queryset= Game.objects.all(), slug=game_slug, slug_field='slug', template_name='scorekeeper/templates/game_detail.html'  )
    
def level_detail(request, level_slug):
    return list_detail.object_detail( request, queryset= Level.objects.all(), slug=level_slug, slug_field='slug', template_name='scorekeeper/templates/level_detail.html'  )

def player_detail(request, player_slug):
    return list_detail.object_detail( request, queryset= Player.objects.all(), slug=player_slug, slug_field='slug', template_name='scorekeeper/templates/player_detail.html'  )

def score(request):
    level = Level.objects.get(slug=request.REQUEST['level'])
    player, isNewPlayer = Player.objects.get_or_create(slug=request.REQUEST['player'], defaults={'secret':request.REQUEST['secret']})
    if not isNewPlayer and player.secret != request.REQUEST['secret']:
        return HttpResponse("invalid player secret")
    score, isNewScore = Score.objects.get_or_create( level = level, player = player, defaults={'score':request.REQUEST['score']} )
    if not isNewScore:
        score.score = request.REQUEST['score']
        score.save()
    if level.score_set.count() > settings.SCORESERVER_MAX_SCORE_TO_KEEP:
        for scoreToDelete in level.score_set.all().order_by('-score')[settings.SCORESERVER_MAX_SCORE_TO_KEEP:]:
            scoreToDelete.delete()
    return HttpResponse("score saved")
