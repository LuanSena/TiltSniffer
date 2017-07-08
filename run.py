from opgg import Opgg
from riotapi import RiotApi


def main():
    riot = RiotApi()
    opgg = Opgg()
    active_match = riot.get_summoner_active_match("")

    for participant in active_match.participants:
        champion = participant.champion
        summoner_name = participant.summoner_name
        summoner_id = participant.summoner.id
        team = participant.side.name
        opgg.refresh_summoner_info(summoner_id)
        summoner_winrate = opgg.get_summoner_recent_winrate(summoner_name)
        print("{name} playing with {champion} on team:{team}. Actual Winrate:{winrate}".format(
            name=summoner_name, champion=champion, team=team, winrate=summoner_winrate
        ))


if __name__ == '__main__':
    main()
