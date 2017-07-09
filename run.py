from opgg import Opgg
from riotapi import RiotApi


def main():
    riot = RiotApi()
    name = input("enter summoner name:")
    active_match = riot.get_summoner_active_match(name)

    for participant in active_match.participants:
        get_participant_info(participant)


def get_participant_info(participant): #TODO make this async
    opgg = Opgg()
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
