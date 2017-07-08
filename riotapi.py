import os
from cassiopeia import riotapi
from cassiopeia.type.core.common import LoadPolicy


class RiotApi():
    def __init__(self):
        self.riotapi = riotapi
        self.key = os.environ["DEV_KEY"]

        self.riotapi.set_region("BR")
        self.riotapi.print_calls(False)
        self.riotapi.set_api_key(self.key)
        self.riotapi.set_load_policy(LoadPolicy.lazy)

    def get_summoner_leagues(self, name):
        try:
            summoner = self.riotapi.get_summoner_by_name(name)
            return self.riotapi.get_leagues_by_summoner(summoner)
        except:
            return "Invocador não encontrado"

    def get_summoner_active_match(self, name):
        try:
            summoner = self.riotapi.get_summoner_by_name(name)
            return self.riotapi.get_current_game(summoner)
        except Exception as e:
            print(str(e))
            return None
