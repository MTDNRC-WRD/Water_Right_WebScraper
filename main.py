import requests
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
import time
import pandas as pd
# need to convert to chrome to go headless


# test_url = r'https://dataportal.mt.gov/t/DOASITSDIBMDBA/views/DNRC_P/DNRCDash?%3AshowAppBanner=false&%3Adisplay_' \
#            r'count=n&%3AshowVizHome=n&%3Aorigin=viz_share_link&%3Aembed=yes&%3Alinktarget=_parent&Basin=76M&WR_' \
#            r'Number=30027375&Extension=&WR_Type=PROVISIONAL%20PERMIT'

driver_path = r'C:\Users\CND367\Documents\Python Scripts\WR_WebScraper\edgedriver_win64\msedgedriver.exe'
chrome_driver_path = r''
download_directory = r'C:\Users\CND367\Downloads\WR_downloads'
url_csv = r'C:\Users\CND367\Documents\Python Scripts\WR_WebScraper\ScannedWR_urls.csv'


def get_url_list(csv):
    df = pd.read_csv(csv)
    wr_list = df['WR#'].to_list()
    link_list = df['SCAN_DOC'].to_list()
    wr_dict = {wr_list[i]: link_list[i] for i in range(len(wr_list))}
    # print(wr_dict)
    return wr_dict


def get_pdf_link(link, wr_num):
    # options = webdriver.ChromeOptions()
    # options.add_argument("--headless=new")
    # driver = webdriver.Chrome(chrome_driver_path, options=options)
    driver = webdriver.Edge(driver_path)
    driver.get(link)
    original_window = driver.current_window_handle
    time.sleep(2)

    try:
        element = driver.find_element(By.XPATH, "//div[@aria-label='FILE, Updates. Press Space to toggle selection. Press Escape to go back to the left margin. Use arrow keys to navigate headers']")
        # print(element.get_attribute('outerHTML'))
        # driver.execute_script("arguments[0].click();", element)
        element.click()
        time.sleep(1)

        for window_handle in driver.window_handles:
            if window_handle != original_window:
                driver.switch_to.window(window_handle)
                break
        time.sleep(10)

        new_url = driver.current_url
        print(f"pdf_url = {new_url}")
        driver.quit()
        return new_url

    except:
        error_list.append(f"NA- {wr_num}")
        print(f"{wr_num} landing page not accessible")
        driver.quit()
        return 'error'


def download_pdf(link, wr_num):
    pdf_file_name = f'{wr_num}.pdf'
    try:
        response = requests.get(link, stream=True)
        if response.status_code == 200:
            # Save in current working directory
            filepath = os.path.join(download_directory, pdf_file_name)
            with open(filepath, 'wb') as pdf_object:
                pdf_object.write(response.content)
                print(f'{pdf_file_name} was successfully saved!')
                return True
        else:
            error_list.append(f"Download Error- {wr_num}")
            print(f'Uh oh! Could not download {pdf_file_name},')
            print(f'HTTP response status code: {response.status_code}')
            return False
    except requests.exceptions.RequestException as e:
        error_list.append(f"Connection Error- {wr_num}")
        print(f'Uh oh! Could not download {pdf_file_name},')
        print("Connection Error")
        return False


if __name__ == '__main__':
    url_dict = get_url_list(url_csv)
    error_list = []
    for key in url_dict:
        url = url_dict[key]
        myfile = os.path.join(download_directory, f'{key}.pdf')
        if os.path.exists(myfile) is True:
            print(f"{key}.pdf is already saved")
            pass
        else:
            pdf_url = get_pdf_link(url, key)
            if pdf_url == 'error':
                with open('error_list.txt', 'w') as file:
                    for i in error_list:
                        file.write("%s\n" % i)
            else:
                pdf = download_pdf(pdf_url, key)
                if pdf is False:
                    with open('error_list.txt', 'w') as file:
                        for i in error_list:
                            file.write("%s\n" % i)

    print(f"Error List: {error_list}")


# ToDO:
# go chrome/headless
# if pdf_url doesnt have fnds.mt.gov in it, re-run that step
# if file <100kb, try redownloading up to 5 times or change sleep time for that run?
