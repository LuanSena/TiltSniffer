from time import sleep

from bs4 import BeautifulSoup
import requests

champion_gg_url = "http://champion.gg/champion/{champion_name}"
counters = "col-xs-12 col-sm-12 col-md-6 counter-column"


class Opgg(object):
    def __init__(self):
        self.url_api_op_gg_br = "https://br.op.gg/summoner/ajax/renew.json/"
        self.url_op_gg_br = "https://br.op.gg/summoner/userName={summoner_name}"

    def get_summoner_recent_winrate(self, name):
        """Return an INT with player winrate"""
        result = requests.get(self.url_op_gg_br.format(summoner_name=name))

        data = result.text
        refreshed_soup = BeautifulSoup(data, 'html.parser')
        content = refreshed_soup.findAll("div", {"class": "Text"})

        for link in content:
            if len(link.attrs['class']) == 1:
                return int(link.text[0:len(link.text) - 1])
        return -1

    def get_summoner_id(self, name):
        """Return player summoner ID from https://br.op.gg"""
        result = requests.get(self.url_op_gg_br.format(summoner_name=name))

        data = result.text
        soup = BeautifulSoup(data, 'html.parser')
        content = soup.findAll("div", {"class": "MostChampionContent"})

        for link in content:
            return link.attrs["data-summoner-id"]
        return -1

    def get_summoner_data(self, name):
        """Return an dict with ID, NAME and WINRATE"""
        r = requests.get(self.url_op_gg_br.format(summoner_name=name))
        summoner_data = dict()
        summoner_data["name"] = name

        data = r.text
        soup = BeautifulSoup(data, 'html.parser')
        content = soup.findAll("div", {"class": "MostChampionContent"})
        for link in content:
            summoner_data["id"] = link.attrs["data-summoner-id"]
            break

        refresh = Opgg.refresh_summoner_info(summoner_data["id"])
        response = requests.get(self.url_op_gg_br.format(summoner_name=name))

        refreshed_data = response.text
        refreshed_soup = BeautifulSoup(refreshed_data, 'html.parser')
        content = refreshed_soup.findAll("div", {"class": "Text"})
        for link in content:
            if len(link.attrs['class']) == 1:
                summoner_data["winrate"] = link.text[0:len(link.text)-1]
                break
        return summoner_data

    def refresh_summoner_info(self, summoner_id):
        """Return status code from op.gg api"""
        headers = {"x-requested-with": "XMLHttpRequest"}
        body = {"summonerId": "{id}".format(id=summoner_id)}
        r = requests.post(self.url_api_op_gg_br, headers=headers, data=body)
        sleep(5)
        return r.status_code
