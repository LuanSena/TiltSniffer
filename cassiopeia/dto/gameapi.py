import cassiopeia.dto.requests
import cassiopeia.type.dto.game


def get_recent_games(summoner_id):
    request = "{version}/game/by-summoner/{summoner_id}/recent".format(version=cassiopeia.dto.requests.api_versions["game"], summoner_id=summoner_id)
    return cassiopeia.type.dto.game.RecentGames(cassiopeia.dto.requests.get(request))
