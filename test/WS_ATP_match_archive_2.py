import logging
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
import time
from tqdm import tqdm
import yaml
from concurrent.futures import ThreadPoolExecutor
from typing import List, Dict, Any
import json

logging.basicConfig(
    level=logging.INFO,
    filename="./src/log/WS_ATP_matches_archive.log",
    filemode="w",
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%d-%m-%Y | %H:%M:%S"
)

def safe_locator_extract(page, selector: str, default: str = "N/A") -> str:
    """Extrait le texte d'un élément de manière sécurisée"""
    try:
        element = page.locator(selector)
        return element.text_content() if element.count() > 0 else default
    except Exception as e:
        logging.warning(f"Error extracting {selector}: {str(e)}")
        return default

def handle_cookies(page):
    """Gère la popup des cookies"""
    try:
        page.wait_for_selector('xpath=//a[@class="atp_button atp_button--invert atp_button--continue"]', timeout=5000)
        page.locator('xpath=//a[@class="atp_button atp_button--invert atp_button--continue"]').click()
    except PlaywrightTimeoutError:
        pass

def extract_tournament_link(browser, url: str) -> List[str]:
    page = browser.new_page()
    try:
        page.goto(url)
        handle_cookies(page)

        # Configuration des timeouts et attentes
        page.set_default_navigation_timeout(30000)
        page.wait_for_load_state('networkidle')

        all_tournament_link_html = page.locator('div.non-live-cta > a.results').all()
        return [html_element.get_attribute('href') for html_element in all_tournament_link_html]
    except Exception as e:
        logging.error(f"Error in extract_tournament_link: {str(e)}")
        return []
    finally:
        page.close()

def extract_matches_link(browser, url: str) -> Dict[str, Any]:
    page = browser.new_page()
    try:
        page.goto(url)
        handle_cookies(page)
        page.wait_for_load_state('networkidle')

        # Extraction des informations principales
        title = safe_locator_extract(page, 'div.status-country > h3.title > a')
        date = safe_locator_extract(page, 'div.date-location > span:last-child')
        
        # Extraction des liens des matches
        all_match_link_html = page.locator('div.match > div.match-footer > div.match-cta > a:text("Stats")').all()
        list_match_link = [html_element.get_attribute('href') for html_element in all_match_link_html]

        # Extraction des informations du tournoi
        tournament_info = {"date": date, "location": "None", "surface": "None"}
        
        try:
            tournament_info_url = page.locator('div.rotator-content > div.rotator-next > a').get_attribute('href')
            if tournament_info_url:
                page_2 = browser.new_page()
                try:
                    page_2.goto(f"https://www.atptour.com{tournament_info_url}")
                    tournament_info.update({
                        "location": safe_locator_extract(page_2, 'ul.td_right > li:has(span:text-is("Location")) > span:last-child'),
                        "surface": safe_locator_extract(page_2, 'ul.td_left > li:has(span:text-is("Surface")) > span:last-child')
                    })
                finally:
                    page_2.close()
        except Exception as e:
            logging.warning(f"Error extracting tournament info: {str(e)}")

        return {title: [tournament_info, list_match_link]}
    except Exception as e:
        logging.error(f"Error in extract_matches_link: {str(e)}")
        return {}
    finally:
        page.close()

def extract_match_stats(browser, url: str) -> Dict[str, str]:
    page = browser.new_page()
    try:
        page.goto(url)
        handle_cookies(page)
        page.wait_for_load_state('networkidle')

        # Fonction helper pour extraire les statistiques
        def get_stat(stat_name: str, player_type: str) -> str:
            return safe_locator_extract(
                page,
                f'li:has(div.stats-item-legend:text-is("{stat_name}")) .{player_type}-stats-item div.value'
            )

        # Extraction des informations des joueurs
        stats = {
            "player_1": safe_locator_extract(page, 'div.player-team > div.names > div.name > a'),
            "player_2": safe_locator_extract(page, 'div.opponent-team > div.names > div.name > a'),
            "country_p1": safe_locator_extract(page, 'div.player-team > div.names > div.name > span.country'),
            "country_p2": safe_locator_extract(page, 'div.opponent-team > div.names > div.name > span.country'),
        }

        # Liste des statistiques à extraire
        stat_fields = {
            "Serve Rating": "serve_rating",
            "Aces": "aces",
            "Double Faults": "double_faults",
            "1st Serve": "first_serve",
            "1st Serve Points Won": "first_serve_pts_won",
            "2nd Serve Points Won": "second_serve_pts_won",
            "Break Points Saved": "break_pts_saved",
            "Service Games Played": "service_game_played",
            "Return Rating": "return_rating",
            "1st Serve Return Points Won": "first_serve_return_pts_won",
            "2nd Serve Return Points Won": "second_serve_return_pts_won",
            "Break Points Converted": "break_pts_converted",
            "Return Games Played": "return_games_played",
            "Service Points Won": "service_pts_won",
            "Return Points Won": "return_pts_won",
            "Total Points Won": "total_point_won"
        }

        # Extraction des statistiques pour les deux joueurs
        for display_name, field_name in stat_fields.items():
            stats[f"{field_name}_p1"] = get_stat(display_name, "player")
            stats[f"{field_name}_p2"] = get_stat(display_name, "opponent")

        return stats
    except Exception as e:
        logging.error(f"Error in extract_match_stats for {url}: {str(e)}")
        return {}
    finally:
        page.close()

def process_tournament(browser, tournament_link: str) -> Dict:
    """Traite un tournoi complet"""
    try:
        return extract_matches_link(browser, f"https://www.atptour.com{tournament_link}")
    except Exception as e:
        logging.error(f"Error processing tournament {tournament_link}: {str(e)}")
        return {}

def process_match(browser, match_link: str) -> Dict:
    """Traite un match individuel"""
    try:
        stats = extract_match_stats(browser, f"https://www.atptour.com{match_link}")
        return {match_link.split("/")[-1]: stats}
    except Exception as e:
        logging.error(f"Error processing match {match_link}: {str(e)}")
        return {}

def main(years: range, max_workers: int = 2):
    for year_season in years:
        with sync_playwright() as p:
            browser = p.chromium.launch(
                headless=True,
                args=['--disable-dev-shm-usage', '--no-sandbox']
            )

            try:
                url_year_season = f"https://www.atptour.com/en/scores/results-archive?tournamentType=atpgs&year={year_season}"
                
                # Extraction des liens des tournois
                tournament_links = extract_tournament_link(browser, url_year_season)
                logging.info(f"Found {len(tournament_links)} tournaments for {year_season}")

                # Traitement parallèle des tournois
                list_match_link_per_tournament = []
                with ThreadPoolExecutor(max_workers=max_workers) as executor:
                    future_to_tournament = {
                        executor.submit(process_tournament, browser, link): link 
                        for link in tournament_links[:3]  # Limite pour test
                    }
                    
                    for future in tqdm(future_to_tournament):
                        try:
                            result = future.result()
                            if result:
                                list_match_link_per_tournament.append(result)
                        except Exception as e:
                            logging.error(f"Tournament processing failed: {str(e)}")

                # Traitement des matches
                dict_match_stats = {}
                for tournament_data in list_match_link_per_tournament:
                    tournament_name = list(tournament_data.keys())[0]
                    dict_match_stats[tournament_name] = [tournament_data[tournament_name][0]]
                    
                    with ThreadPoolExecutor(max_workers=max_workers) as executor:
                        future_to_match = {
                            executor.submit(process_match, browser, link): link 
                            for link in tournament_data[tournament_name][1]
                        }
                        
                        for future in tqdm(future_to_match):
                            try:
                                result = future.result()
                                if result:
                                    dict_match_stats[tournament_name].append(result)
                            except Exception as e:
                                logging.error(f"Match processing failed: {str(e)}")

                # Sauvegarde des données
                output_path = f'./data/1_data_bronze/03_ATP_website/ATP_matches_archive/ATP_match_archive_{year_season}.txt'
                with open(output_path, 'w', encoding='utf-8') as file:
                    json.dump(dict_match_stats, file, ensure_ascii=False, indent=2)

            finally:
                browser.close()

if __name__ == "__main__":
    with open('./config/config_WS_ATP_match_archive.yaml', 'r') as config_file:
        settings = yaml.safe_load(config_file)

    start_time = time.time()
    main(range(2010, 2011), max_workers=2)
    duration = (time.time() - start_time) / 60
    logging.info(f"Total execution time: {duration:.2f} minutes")