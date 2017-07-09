import time

from opgg import Opgg
from riotapi import RiotApi
import asyncio

@asyncio.coroutine
def get_participant_info(participant):
    opgg = Opgg()
    champion = participant.champion
    summoner_name = participant.summoner_name
    summoner_id = participant.summoner.id
    team = participant.side.name
    opgg.refresh_summoner_info(summoner_id)
    summoner_winrate = opgg.get_summoner_recent_winrate(opgg.get_summoner_request_result(summoner_name))

    print("{name} playing with {champion} on team:{team}. Actual Winrate:{winrate}".format(
        name=summoner_name, champion=champion, team=team, winrate=summoner_winrate
    ))

def main():
    print("Started:")
    start = time.time()
    print(start)
    riot = RiotApi()
    name = input("enter summoner name:")
    active_match = riot.get_summoner_active_match(name)

    tasks = [asyncio.async(get_participant_info(participant)) for participant in active_match.participants]
    yield from asyncio.wait(tasks)
    print("Ended:")
    end = (time.time() - start)
    print(end)


ioloop = asyncio.get_event_loop()
ioloop.run_until_complete(main())
ioloop.close()

if __name__ == '__main__':
    main()
