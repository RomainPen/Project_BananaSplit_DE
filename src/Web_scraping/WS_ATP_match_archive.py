# WS ATP_matches_archive

# Step :
# - Fonction pour changer les critère (Click)
# - Fonction pour la loop item
# - Fonction pour l'extraction des donnees
# - Fonction pour exporter la data sous excel
# - Fonction pour la pagination


# import package :
import logging
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
import time
from tqdm import tqdm

logging.basicConfig(level=logging.INFO,
                    filename="./src/log/WS_ATP_matches_archive.log",
                    filemode="w",
                    format="%(asctime)s - %(levelname)s - %(message)s",
                    datefmt="%d-%m-%Y | %H:%M:%S"
                    )




def extract_tournament_link(browser, url) :
    page = browser.new_page()
    page.goto(url)

    # accept cookies
    try : 
        page.wait_for_selector('xpath=//a[@class="atp_button atp_button--invert atp_button--continue"]', timeout=20000)
        page.locator('xpath=//a[@class="atp_button atp_button--invert atp_button--continue"]').click()
    
    except PlaywrightTimeoutError as e :
        logging.error(f"Accept cookies button doesn't exist : {e}")
        pass


    # extract_tournament_link
    all_tournament_link_html = page.locator('div.non-live-cta > a.results').all()
    list_tournament_link = []
    for html_element in all_tournament_link_html :
        tournament_link = html_element.get_attribute('href')
        list_tournament_link.append(tournament_link)
        
    page.close()
    
    return list_tournament_link




def extract_matches_link(browser, url):
    page = browser.new_page()
    page.goto(url)

    # accept cookies
    try : 
        page.wait_for_selector('xpath=//a[@class="atp_button atp_button--invert atp_button--continue"]', timeout=20000)
        page.locator('xpath=//a[@class="atp_button atp_button--invert atp_button--continue"]').click()
    
    except PlaywrightTimeoutError as e :
        logging.error(f"Accept cookies button doesn't exist : {e}")
        pass
    

    # title :
    title = page.locator('div.status-country > h3.title > a').text_content()

    # date : 
    date = page.locator('div.date-location > span:last-child').text_content()


    # extract specific tournament_info : 
    tournament_info_url = page.locator('div.rotator-content > div.rotator-next > a').get_attribute('href')
    page_2 = browser.new_page()
    page_2.goto(f"https://www.atptour.com{tournament_info_url}")
    
    try : 
        # location :
        location = page_2.locator('ul.td_right > li:has(span:text-is("Location")) > span:last-child').text_content()
        # surface : 
        surface = page_2.locator('ul.td_left > li:has(span:text-is("Surface")) > span:last-child').text_content()

    except : 
        # location :
        location = "None"
        # surface : 
        surface = "None"

    page_2.close()
    

    # list_match_link :
    all_match_link_html = page.locator('div.match > div.match-footer > div.match-cta > a:text("Stats")').all()
    list_match_link = []
    for html_element in all_match_link_html:
        match_link = html_element.get_attribute('href')
        list_match_link.append(match_link)

    page.close()

    return {f"{title}" : [{"date" : date, "location" : location, "surface" : surface} , list_match_link]}




def extract_match_stats(browser, url) :
    page = browser.new_page()
    page.goto(url)

    # accept cookies
    try : 
        page.wait_for_selector('xpath=//a[@class="atp_button atp_button--invert atp_button--continue"]', timeout=20000)
        page.locator('xpath=//a[@class="atp_button atp_button--invert atp_button--continue"]').click()
    
    except PlaywrightTimeoutError as e :
        logging.error(f"Accept cookies button doesn't exist : {e}")
        pass
    

    # player name :
    player_1 = page.locator('div.player-team > div.names > div.name > a').text_content()
    player_2 = page.locator('div.opponent-team > div.names > div.name > a').text_content()
    country_p1 = page.locator('div.player-team > div.names > div.name > span.country').text_content()
    country_p2 = page.locator('div.opponent-team > div.names > div.name > span.country').text_content()

    
    # service_stat : 
    serve_rating_p1 = page.locator('li:has(div.stats-item-legend:text-is("Serve Rating")) .player-stats-item div.value').text_content()
    aces_p1 = page.locator('li:has(div.stats-item-legend:text-is("Aces")) .player-stats-item div.value').text_content()
    double_faults_p1 =page.locator('li:has(div.stats-item-legend:text-is("Double Faults")) .player-stats-item div.value').text_content()
    first_serve_p1 =page.locator('li:has(div.stats-item-legend:text-is("1st Serve")) .player-stats-item div.value').text_content()
    first_serve_pts_won_p1 =page.locator('li:has(div.stats-item-legend:text-is("1st Serve Points Won")) .player-stats-item div.value').text_content()
    second_serve_pts_won_p1 =page.locator('li:has(div.stats-item-legend:text-is("2nd Serve Points Won")) .player-stats-item div.value').text_content()
    break_pts_saved_p1 =page.locator('li:has(div.stats-item-legend:text-is("Break Points Saved")) .player-stats-item div.value').text_content()
    service_game_played_p1 = page.locator('li:has(div.stats-item-legend:text-is("Service Games Played")) .player-stats-item div.value').text_content()

    serve_rating_p2= page.locator('li:has(div.stats-item-legend:text-is("Serve Rating")) .opponent-stats-item div.value').text_content()
    aces_p2= page.locator('li:has(div.stats-item-legend:text-is("Aces")) .opponent-stats-item div.value').text_content()
    double_faults_p2=page.locator('li:has(div.stats-item-legend:text-is("Double Faults")) .opponent-stats-item div.value').text_content()
    first_serve_p2=page.locator('li:has(div.stats-item-legend:text-is("1st Serve")) .opponent-stats-item div.value').text_content()
    first_serve_pts_won_p2=page.locator('li:has(div.stats-item-legend:text-is("1st Serve Points Won")) .opponent-stats-item div.value').text_content()
    second_serve_pts_won_p2=page.locator('li:has(div.stats-item-legend:text-is("2nd Serve Points Won")) .opponent-stats-item div.value').text_content()
    break_pts_saved_p2 =page.locator('li:has(div.stats-item-legend:text-is("Break Points Saved")) .opponent-stats-item div.value').text_content()
    service_game_played_p2=page.locator('li:has(div.stats-item-legend:text-is("Service Games Played")) .opponent-stats-item div.value').text_content()


    #return_stat :
    return_rating_p1 = page.locator('li:has(div.stats-item-legend:text-is("Return Rating")) .player-stats-item div.value').text_content()
    first_serve_return_pts_won_p1 =page.locator('li:has(div.stats-item-legend:text-is("1st Serve Return Points Won")) .player-stats-item div.value').text_content()
    second_serve_return_pts_won_p1 =page.locator('li:has(div.stats-item-legend:text-is("2nd Serve Return Points Won")) .player-stats-item div.value').text_content()
    break_pts_converted_p1 = page.locator('li:has(div.stats-item-legend:text-is("Break Points Converted")) .player-stats-item div.value').text_content()
    return_games_played_p1 =page.locator('li:has(div.stats-item-legend:text-is("Return Games Played")) .player-stats-item div.value').text_content()

    return_rating_p2= page.locator('li:has(div.stats-item-legend:text-is("Return Rating")) .opponent-stats-item div.value').text_content()
    first_serve_return_pts_won_p2=page.locator('li:has(div.stats-item-legend:text-is("1st Serve Return Points Won")) .opponent-stats-item div.value').text_content()
    second_serve_return_pts_won_p2=page.locator('li:has(div.stats-item-legend:text-is("2nd Serve Return Points Won")) .opponent-stats-item div.value').text_content()
    break_pts_converted_p2= page.locator('li:has(div.stats-item-legend:text-is("Break Points Converted")) .opponent-stats-item div.value').text_content()
    return_games_played_p2=page.locator('li:has(div.stats-item-legend:text-is("Return Games Played")) .opponent-stats-item div.value').text_content()
    
    
    #pts_stats :
    service_pts_won_p1 = page.locator('li:has(div.stats-item-legend:text-is("Service Points Won")) .player-stats-item div.value').text_content()
    return_pts_won_p1 =page.locator('li:has(div.stats-item-legend:text-is("Return Points Won")) .player-stats-item div.value').text_content()
    total_point_won_p1 =page.locator('li:has(div.stats-item-legend:text-is("Total Points Won")) .player-stats-item div.value').text_content()

    service_pts_won_p2= page.locator('li:has(div.stats-item-legend:text-is("Service Points Won")) .opponent-stats-item div.value').text_content()
    return_pts_won_p2=page.locator('li:has(div.stats-item-legend:text-is("Return Points Won")) .opponent-stats-item div.value').text_content()
    total_point_won_p2=page.locator('li:has(div.stats-item-legend:text-is("Total Points Won")) .opponent-stats-item div.value').text_content()
    

    page.close()
    return {"player_1" : player_1,
            "player_2" : player_2, 
            "country_p1" : country_p1,
            "country_p2" : country_p2,
            
            "serve_rating_p1" : serve_rating_p1,
            "aces_p1" : aces_p1,
            "double_faults_p1" :double_faults_p1,
            "first_serve_p1" :first_serve_p1,
            "first_serve_pts_won_p1" :first_serve_pts_won_p1,
            "second_serve_pts_won_p1" :second_serve_pts_won_p1,
            "break_pts_saved_p1" :break_pts_saved_p1,
            "service_game_played_p1" : service_game_played_p1,

            "serve_rating_p2": serve_rating_p2,
            "aces_p2": aces_p2,
            "double_faults_p2":double_faults_p2,
            "first_serve_p2":first_serve_p2,
            "first_serve_pts_won_p2":first_serve_pts_won_p2,
            "second_serve_pts_won_p2":second_serve_pts_won_p2,
            "break_pts_saved_p2" :break_pts_saved_p2,
            "service_game_played_p2":service_game_played_p2,

            "return_rating_p1" : return_rating_p1,
            "first_serve_return_pts_won_p1" :first_serve_return_pts_won_p1,
            "second_serve_return_pts_won_p1" :second_serve_return_pts_won_p1,
            "break_pts_converted_p1" : break_pts_converted_p1,
            "return_games_played_p1" :return_games_played_p1,

            "return_rating_p2": return_rating_p2 ,
            "first_serve_return_pts_won_p2":first_serve_return_pts_won_p2,
            "second_serve_return_pts_won_p2":second_serve_return_pts_won_p2,
            "break_pts_converted_p2": break_pts_converted_p2,
            "return_games_played_p2":return_games_played_p2,
            
            "service_pts_won_p1" : service_pts_won_p1,
            "return_pts_won_p1" :return_pts_won_p1,
            "total_point_won_p1" :total_point_won_p1,

            "service_pts_won_p2": service_pts_won_p2,
            "return_pts_won_p2":return_pts_won_p2,
            "total_point_won_p2":total_point_won_p2
            }






# Main :
def main():

    for year_season in range(2010, 2011) :
        
        with sync_playwright() as p :

            # Connection to Chromium :
            browser = p.chromium.launch(headless=False) #connect_over_cdp(SBR_WS_CDP) #.launch(headless=False)

            # Parametrisation :
            url_year_season = f"https://www.atptour.com/en/scores/results-archive?tournamentType=atpgs&year={year_season}"


            # extract_tournament_link :
            list_tournament_link = extract_tournament_link(browser=browser, url=url_year_season)
            print("extract_tournament_link OK")


            # extract tournament_info + matches_link :
            list_match_link_per_tournament = []
            for tournament_link in list_tournament_link : 
                list_match_link_per_tournament.append(extract_matches_link(browser=browser, url=f"https://www.atptour.com{tournament_link}"))
                time.sleep(5)
            print("extract tournament_info + matches_link OK")


            # extract_match_stats :
            dict_match_stats = {}
            for dict_tournament in list_match_link_per_tournament :
                tournament_name = list(dict_tournament.keys())[0]

                dict_match_stats[tournament_name] = [dict_tournament[tournament_name][0]]
                for match_link in tqdm(dict_tournament[tournament_name][1]) :
                    dict_match_stats[tournament_name].append({f"{match_link.split("/")[-1]}" : extract_match_stats(browser=browser, url=f"https://www.atptour.com{match_link}")})
                    time.sleep(5)
            print("extract_match_stats OK")



            # Update ATP_match_archive_{year_season}.txt :
            with open(f'./data/1_data_bronze/03_ATP_website/ATP_matches_archive/ATP_match_archive_{year_season}.txt', 'w') as file:
                file.write(str(dict_match_stats))
        







if __name__ == "__main__":
    # compute time running :
    start_time = time.time()
    
    # run main :
    main()

    # End the timer
    end_time = time.time()

    # Calculate and print the duration
    duration = (end_time - start_time)/60
    print(f"Time taken: {duration:.2f} minutes")