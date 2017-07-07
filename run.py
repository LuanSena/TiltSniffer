from time import sleep

from bs4 import BeautifulSoup
import requests

champion_gg_url = "http://champion.gg/champion/{champion_name}"
OP_GG_URL = "https://br.op.gg/summoner/userName={summoner_name}"
counters = "col-xs-12 col-sm-12 col-md-6 counter-column"


class OpGg(object):
    @staticmethod
    def get_sumonner_data(name):
        print("First request")
        r = requests.get(OP_GG_URL.format(summoner_name=name))
        print("First request ok.")
        sumonner_data = dict()
        sumonner_data["name"] = name

        print("Getting sumonner ID from request result.")
        data = r.text
        soup = BeautifulSoup(data, 'html.parser')
        content = soup.findAll("div", {"class": "MostChampionContent"})
        for link in content:
            sumonner_data["id"] = link.attrs["data-summoner-id"]
            print("Sumonner id found: {s_id}".format(s_id=sumonner_data["id"]))
            break

        print("Post refresh for sumonner id {s_id} profile".format(s_id=sumonner_data["id"]))
        refresh = OpGg.refresh_sumonner_info(sumonner_data["id"])
        print("Post status code:{status}".format(status=refresh))
        print("Getting new request for same sumonner")
        response = requests.get(OP_GG_URL.format(summoner_name=name))

        refreshed_data = response.text
        refreshed_soup = BeautifulSoup(refreshed_data, 'html.parser')
        content = refreshed_soup.findAll("div", {"class": "Text"})
        for link in content:
            if len(link.attrs['class']) == 1:
                sumonner_data["winrate"] = link.text[0:len(link.text)-1]
                break



        return sumonner_data

    @staticmethod
    def refresh_sumonner_info(sumonner_id):
        headers = {"x-requested-with": "XMLHttpRequest"}
        body = {"summonerId": "{id}".format(id=sumonner_id)}
        r = requests.post("https://br.op.gg/summoner/ajax/renew.json/", headers=headers, data=body)
        sleep(5)
        return r.status_code


summoner_name = ""

sumonner = OpGg.get_sumonner_data(summoner_name)
print(sumonner)
