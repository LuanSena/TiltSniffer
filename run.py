from bs4 import BeautifulSoup
from selenium import webdriver
import requests

champion_gg_url = "http://champion.gg/champion/{champion_name}"
op_gg_url = "https://br.op.gg/summoner/userName={summoner_name}"
counters = "col-xs-12 col-sm-12 col-md-6 counter-column"
live_match = "http://www.lolking.net/summoner/br/22000556/{sumonner_name}#live-game"


class OpGg(object):
    def __init__(self):
        pass

    def get_sumonner_actual_winrate(self, summoner_name):
        r = requests.get(op_gg_url.format(summoner_name=summoner_name))

        data = r.text
        soup = BeautifulSoup(data, 'html.parser')
        content = soup.findAll("div", {"class": "Text"})
        for link in content:
            if len(link.attrs['class']) == 1:
                return link.text[0:len(link.text)-1]

    def refresh_summoner_infos(self, summoner_name):
        driver = webdriver.Firefox()
        driver.get(op_gg_url.format(summoner_name=summoner_name))
        submit = driver.find_element_by_id("SummonerRefreshButton")
        submit.click()

op_gg = OpGg()
summoner = ""
# op_gg.refresh_summoner_infos(summoner)
print(op_gg.get_sumonner_actual_winrate(summoner))
