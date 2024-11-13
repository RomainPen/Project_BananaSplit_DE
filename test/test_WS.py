# import package :
import logging
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
import time










def main():
    with sync_playwright() as p :
        browser = p.chromium.launch(headless=False)

        # open page :
        url = "https://www.atptour.com/en/scores/match-stats/archive/2010/339/ms001"
        page = browser.new_page()
        page.goto(url)

        # accept cookies
        page.wait_for_selector('xpath=//a[@class="atp_button atp_button--invert atp_button--continue"]', timeout=20000)
        page.locator('xpath=//a[@class="atp_button atp_button--invert atp_button--continue"]').click()

        # extract stat :
        player_1 = page.locator('div.player-team > div.names > div.name > a').text_content()
        player_2 = page.locator('div.opponent-team > div.names > div.name > a').text_content()
        country_p1 = page.locator('div.player-team > div.names > div.name > span.country').text_content()
        country_p2 = page.locator('div.opponent-team > div.names > div.name > span.country').text_content()

        service_rate_p1 = page.locator('li:has(div.stats-item-legend:text-is("Serve Rating")) .player-stats-item div.value').text_content()
        service_rate_p2 = page.locator('li:has(div.stats-item-legend:text-is("Serve Rating")) .opponent-stats-item div.value').text_content()

        print("--------------------")
        print(f"serv_rate_p1 : {service_rate_p1}")
        print(f"serv_rate_p2 : {service_rate_p2}")
        print("--------------------")


        ############################### TO DROP ##################################################
        # TEST player 1 :
        list_all_p1 = page.locator('div.player-stats-item > div.value').all()
        list_all_value_p1 = []
        for stat in list_all_p1 :
            list_all_value_p1.append(stat.text_content())

        print(list_all_value_p1)
        #print(len(list_all_p1))

        # TEST player 2 :
        list_all_p2 = page.locator('div.opponent-stats-item > div.value').all()
        list_all_value_p2 = []
        for stat in list_all_p2 :
            list_all_value_p2.append(stat.text_content())

        print(list_all_value_p2)
        #print(len(list_all_p2))


        # TEST Extract_stat_name :
        list_all_stat_legend = page.locator('div.stats-item-legend').all()
        list_stat_legend_txt = []
        for legend in list_all_stat_legend :
            list_stat_legend_txt.append(legend.text_content())

        print(list_stat_legend_txt)
        #############################################################################################




        # close page :
        page.close()

        # stat in dict_stat :
        dict_stat = {"player_1" : player_1,
            "player_2" : player_2, 
            "country_p1" : country_p1,
            "country_p2" : country_p2}
        
        # print dict_stat :
        print(dict_stat)




if __name__ == "__main__" :
    main()