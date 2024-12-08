# import package :
import logging
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
import time










def main():
    with sync_playwright() as p :
        
        #connect to chromium 1 :
        browser = p.chromium.launch(headless=False)

        # tennis_matches_url :
        list_url = ["https://www.atptour.com/en/scores/stats-centre/archive/2022/8888/ms011", "https://www.atptour.com/en/scores/stats-centre/archive/2022/8888/ms012", "https://www.atptour.com/en/scores/stats-centre/archive/2022/8888/ms021",
                    "https://www.atptour.com/en/scores/stats-centre/archive/2022/8888/ms011", "https://www.atptour.com/en/scores/stats-centre/archive/2022/8888/ms012", "https://www.atptour.com/en/scores/stats-centre/archive/2022/8888/ms021",
                    "https://www.atptour.com/en/scores/stats-centre/archive/2022/8888/ms011", "https://www.atptour.com/en/scores/stats-centre/archive/2022/8888/ms012", "https://www.atptour.com/en/scores/stats-centre/archive/2022/8888/ms021",
                    "https://www.atptour.com/en/scores/stats-centre/archive/2022/8888/ms011", "https://www.atptour.com/en/scores/stats-centre/archive/2022/8888/ms012", "https://www.atptour.com/en/scores/stats-centre/archive/2022/8888/ms021"]
        

        # open page : #########################################################################################
        a = 0
        for url in list_url :
            print(f"-------------------------- MATCH {a} --------------------------------------")

            extra_http_headers = {'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                                    'accept-encoding': 'gzip, deflate, br',
                                    'accept-language': 'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7',
                                    'cache-control': 'max-age=0',
                                    'sec-fetch-dest': 'document',
                                    'sec-fetch-mode': 'navigate',
                                    'sec-fetch-site': 'same-origin',
                                    'sec-fetch-user': '?1',
                                    'upgrade-insecure-requests': '1',
                                    'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Mobile Safari/537.36'}
            
            page = browser.new_page(extra_http_headers=extra_http_headers) 
            page.goto(url, timeout=100000)




            # accept cookies
            page.wait_for_selector('xpath=//a[@class="atp_button atp_button--invert atp_button--continue"]', timeout=20000)
            page.locator('xpath=//a[@class="atp_button atp_button--invert atp_button--continue"]').click()





            # Time play : ###############################################
            playing_time = page.locator('div.match > div.match-header > span:last-child').text_content()
            print(playing_time)





            # Score : ################################################
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

            dict_match_score = {}
            for i in range(len(player1_sets)):
                set_num = i + 1
                dict_match_score[f"set_{set_num}"] = {"player_1" : f"{player1_sets[i]} ({player1_tiebreaks[i]})", 
                                                    "player_2" : f"{player2_sets[i]} ({player2_tiebreaks[i]})", 
                                                    }
            
            print(dict_match_score)




            
            # extract player info : ######################################################################
            player_1 = page.locator('div.player-team > div.names > div.name > a').text_content()
            player_2 = page.locator('div.opponent-team > div.names > div.name > a').text_content()
            country_p1 = page.locator('div.player-team > div.names > div.name > span.country').text_content()
            country_p2 = page.locator('div.opponent-team > div.names > div.name > span.country').text_content()

            # stat in dict_stat :
            dict_stat = {"player_1" : player_1,
                "player_2" : player_2, 
                "country_p1" : country_p1,
                "country_p2" : country_p2}
            
            # print dict_stat :
            print(dict_stat)
            






            # Match stat : ##################################################################################
            # serve :
            service_rate_p1 = page.locator('div.desktopView:has(.labelBold:text-is("Serve Rating")) .player1.non-speed a').text_content()
            service_rate_p2 = page.locator('div.desktopView:has(.labelBold:text-is("Serve Rating")) .player2.non-speed a').text_content()
            print("--------------------")
            print(f"serv_rate_p1 : {service_rate_p1}")
            print(f"serv_rate_p2 : {service_rate_p2}")
            print("--------------------")


            ace_p1 = page.locator('div.desktopView:has(.labelBold:text-is("Aces")) .player1.non-speed span').text_content()
            ace_p2 = page.locator('div.desktopView:has(.labelBold:text-is("Aces")) .player2.non-speed span').text_content()
            print("--------------------")
            print(f"ace_p1 : {ace_p1}")
            print(f"ace_p2 : {ace_p2}")
            print("--------------------")


            df_p1 = page.locator('div.desktopView:has(.labelBold:text-is("Double Faults")) .player1.non-speed span').text_content()
            df_p2 = page.locator('div.desktopView:has(.labelBold:text-is("Double Faults")) .player2.non-speed span').text_content()
            print("--------------------")
            print(f"df_p1 : {df_p1}")
            print(f"df_p2 : {df_p2}")
            print("--------------------")


            fs_p1 = page.locator('div.desktopView:has(.labelBold:text-is("First serve")) .player1.non-speed span').text_content()
            fs_p2 = page.locator('div.desktopView:has(.labelBold:text-is("First serve")) .player2.non-speed span').text_content()
            print("--------------------")
            print(f"fs_p1 : {fs_p1}")
            print(f"fs_p2 : {fs_p2}")
            print("--------------------")


            fs_pw_p1 = page.locator('div.desktopView:has(.labelBold:text-is("1st serve points won")) .player1.non-speed span').text_content()
            fs_pw_p2 = page.locator('div.desktopView:has(.labelBold:text-is("1st serve points won")) .player2.non-speed span').text_content()
            print("--------------------")
            print(f"fs_pw_p1 : {fs_pw_p1}")
            print(f"fs_pw_p2 : {fs_pw_p2}")
            print("--------------------")


            ss_pw_p1 = page.locator('div.desktopView:has(.labelBold:text-is("2nd serve points won")) .player1.non-speed span').text_content()
            ss_pw_p2 = page.locator('div.desktopView:has(.labelBold:text-is("2nd serve points won")) .player2.non-speed span').text_content()
            print("--------------------")
            print(f"ss_pw_p1 : {ss_pw_p1}")
            print(f"ss_pw_p2 : {ss_pw_p2}")
            print("--------------------")


            bps_p1 = page.locator('div.desktopView:has(.labelBold:text-is("Break Points Saved")) .player1.non-speed span').text_content()
            bps_p2 = page.locator('div.desktopView:has(.labelBold:text-is("Break Points Saved")) .player2.non-speed span').text_content()
            print("--------------------")
            print(f"bps_p1 : {bps_p1}")
            print(f"bps_p2 : {bps_p2}")
            print("--------------------")


            sgp_p1 = page.locator('div.desktopView:has(.labelBold:text-is("Service Games Played")) .player1.non-speed span').text_content()
            sgp_p2 = page.locator('div.desktopView:has(.labelBold:text-is("Service Games Played")) .player2.non-speed span').text_content()
            print("--------------------")
            print(f"sgp_p1 : {sgp_p1}")
            print(f"sgp_p2 : {sgp_p2}")
            print("--------------------")





            #return_stat :
            rr_p1 = page.locator('div.desktopView:has(.labelBold:text-is("Return Rating")) .player1.non-speed a').text_content()
            rr_p2 = page.locator('div.desktopView:has(.labelBold:text-is("Return Rating")) .player2.non-speed a').text_content()
            print("--------------------")
            print(f"rr_p1 : {rr_p1}")
            print(f"rr_p2 : {rr_p2}")
            print("--------------------")


            fs_rpw_p1 = page.locator('div.desktopView:has(.labelBold:text-is("1st Serve Return Points Won")) .player1.non-speed span').text_content()
            fs_rpw_p2 = page.locator('div.desktopView:has(.labelBold:text-is("1st Serve Return Points Won")) .player2.non-speed span').text_content()
            print("--------------------")
            print(f"fs_rpw_p1 : {fs_rpw_p1}")
            print(f"fs_rpw_p2 : {fs_rpw_p2}")
            print("--------------------")


            ss_rpw_p1 = page.locator('div.desktopView:has(.labelBold:text-is("2nd Serve Return Points Won")) .player1.non-speed span').text_content()
            ss_rpw_p2 = page.locator('div.desktopView:has(.labelBold:text-is("2nd Serve Return Points Won")) .player2.non-speed span').text_content()
            print("--------------------")
            print(f"ss_rpw_p1 : {ss_rpw_p1}")
            print(f"ss_rpw_p2 : {ss_rpw_p2}")
            print("--------------------")


            bpc_p1 = page.locator('div.desktopView:has(.labelBold:text-is("Break Points Converted")) .player1.non-speed span').text_content()
            bpc_p2 = page.locator('div.desktopView:has(.labelBold:text-is("Break Points Converted")) .player2.non-speed span').text_content()
            print("--------------------")
            print(f"bpc_p1 : {bpc_p1}")
            print(f"bpc_p2 : {bpc_p2}")
            print("--------------------")


            rgp_p1 = page.locator('div.desktopView:has(.labelBold:text-is("Return Games Played")) .player1.non-speed span').text_content()
            rgp_p2 = page.locator('div.desktopView:has(.labelBold:text-is("Return Games Played")) .player2.non-speed span').text_content()
            print("--------------------")
            print(f"rgp_p1 : {rgp_p1}")
            print(f"rgp_p2 : {rgp_p2}")
            print("--------------------")


        

            # pts stat :
            spw_p1 = page.locator('div.desktopView:has(.labelBold:text-is("Service Points Won")) .player1.non-speed span').text_content()
            spw_p2 = page.locator('div.desktopView:has(.labelBold:text-is("Service Points Won")) .player2.non-speed span').text_content()
            print("--------------------")
            print(f"spw_p1 : {spw_p1}")
            print(f"spw_p2 : {spw_p2}")
            print("--------------------")


            rpw_p1 = page.locator('div.desktopView:has(.labelBold:text-is("Return Points Won")) .player1.non-speed span').text_content()
            rpw_p2 = page.locator('div.desktopView:has(.labelBold:text-is("Return Points Won")) .player2.non-speed span').text_content()
            print("--------------------")
            print(f"rpw_p1 : {rpw_p1}")
            print(f"rpw_p2 : {rpw_p2}")
            print("--------------------")


            tpw_p1 = page.locator('div.desktopView:has(.labelBold:text-is("Total Points Won")) .player1.non-speed span').text_content()
            tpw_p2 = page.locator('div.desktopView:has(.labelBold:text-is("Total Points Won")) .player2.non-speed span').text_content()
            print("--------------------")
            print(f"tpw_p1 : {tpw_p1}")
            print(f"tpw_p2 : {tpw_p2}")
            print("--------------------")



            # close page : ###########################################################
            page.close()



            # Change IP : ###############################################################
            if (a % 4 == 0) and (a != 0) :
                print("------------------------------- Change IP ------------------------------------")
                time.sleep(15)
            else :
                pass

            a+=1



if __name__ == "__main__" :
    main()