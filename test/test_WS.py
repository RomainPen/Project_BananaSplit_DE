# import package :
import logging
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
import time










def main():
    with sync_playwright() as p :
        browser = p.chromium.launch(headless=False)

        # open page :
        url = "https://www.atptour.com/en/scores/match-stats/archive/2010/580/ms005"
        page = browser.new_page()
        page.goto(url)

        # accept cookies
        page.wait_for_selector('xpath=//a[@class="atp_button atp_button--invert atp_button--continue"]', timeout=20000)
        page.locator('xpath=//a[@class="atp_button atp_button--invert atp_button--continue"]').click()




        playing_time = page.locator('div.match > div.match-header > span:last-child').text_content()
        print(playing_time)








        #########################################################
        player1_sets = []
        player1_tiebreaks = []
        player2_sets = []
        player2_tiebreaks = []

        # Pour le premier joueur
        for item in page.locator('div.stats-item:first-child div.scores > div.score-item').all():
            scores = item.locator('span').all()
            if len(scores) == 1:
                # Set normal sans tie-break
                player1_sets.append(scores[0].text_content())
                player1_tiebreaks.append(None)
            elif len(scores) == 2:
                # Set avec tie-break
                player1_sets.append(scores[0].text_content())
                player1_tiebreaks.append(scores[1].text_content())

        # Pour le deuxième joueur
        for item in page.locator('div.stats-item:last-child div.scores > div.score-item').all():
            scores = item.locator('span').all()
            if len(scores) == 1:
                # Set normal sans tie-break
                player2_sets.append(scores[0].text_content())
                player2_tiebreaks.append(None)
            elif len(scores) == 2:
                # Set avec tie-break
                player2_sets.append(scores[0].text_content())
                player2_tiebreaks.append(scores[1].text_content())


        # Afficher les résultats
        dict_match_score = {}
        for i in range(len(player1_sets)):
            set_num = i + 1
            dict_match_score[f"set_{set_num}"] = {"player_1" : f"{player1_sets[i]} ({player1_tiebreaks[i]})", 
                                                "player_2" : f"{player2_sets[i]} ({player2_tiebreaks[i]})", 
                                                }
        
        print(dict_match_score)
        #########################################################





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