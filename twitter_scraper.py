# imports
import csv  # used to ouput the data into a csv file (that we can analyze)
from getpass import getpass  # used to secretly type in the twitter password
# used to delay the scraping to allow for scrolling and secure for DDOS blocking of webpage
from time import sleep, time

# selenium library to navigate browser and scrape twitter
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
# we use the chrome browser for the twitter webscraping
from selenium.webdriver import Chrome

# functions
def get_tweet_data(card):
    """
    Extract data from tweet card using xpath searches for each important element of the tweet
    """
    username = card.find_element_by_xpath('.//span').text
    try:  # since advertised post dont have a handle and a postdate, we can easily filter them out using error handling
        handle = card.find_element_by_xpath(
            './/span[contains(text(), "@")]').text
    except NoSuchElementException:
        return

    try:
        postdate = card.find_element_by_xpath(
            './/time').get_attribute('datetime')
    except NoSuchElementException:
        return

    comment = card.find_element_by_xpath('.//div[2]/div[2]/div[1]').text
    responding = card.find_element_by_xpath('.//div[2]/div[2]/div[2]').text
    text = comment + responding
    reply_cnt = card.find_element_by_xpath('.//div[@data-testid="reply"]').text
    retweet_cnt = card.find_element_by_xpath(
        './/div[@data-testid="retweet"]').text
    like_cnt = card.find_element_by_xpath('.//div[@data-testid="like"]').text

    # concatenate all the scraped data into a tuple return it
    tweet = (username, handle, postdate, text,
             reply_cnt, retweet_cnt, like_cnt)

    return tweet


# global variables
PATH = '../webdrivers/chromedriver' # individual path to chromedriver


# classes
class Scraper:
    def __init__(self, source, username, password):
        self.data = []
        if source == "twitter":
            self.source = Twitter(username, password)

    def get_data(self):
        """
        Returns all the Scraped Data 
        """
        return self.data

    def scrape(self, searchterm):
        """
        Saves all the tweets from the Source Page given a specific Searchterm
        """
        self.source.login()
        self.source.search(searchterm)

        tweet_ids = set()  # we use this to make sure that our dataset consist of unique tweets
        timeout = time() + 30

        # while scrolling:
        while True:
            page_cards = self.source.driver.find_elements_by_xpath(
                '//div[@data-testid="tweet"]')
            for card in page_cards[-15:]:
                tweet = get_tweet_data(card)
                if tweet:
                    tweet_id = ''.join(tweet)  # make it unique
                    if tweet_id not in tweet_ids:
                        tweet_ids.add(tweet_id)
                        self.data.append(tweet)

            self.source.driver.execute_script(
                'window.scrollTo(0, document.body.scrollHeight);')
            sleep(3)

            # break out of the scraping after 30 seconds
            if time() > timeout:
                print('The scraping was finished after 30 seconds')
                break

        self.source.driver.close()

    def save_data(self, searchterm):
        with open(f"scraped_{searchterm}.csv", 'w', newline='', encoding='utf-8') as outfile:
            header = ['Username', 'Handle', 'Timestamp',
                      'Text', 'Comments', 'Likes', 'Retweets']
            writer = csv.writer(outfile)
            writer.writerow(header)
            writer.writerows(self.data)
        print(
            f"Your scraped Data was successfully saved to 'scraped_{searchterm}' within your current directory")


class Twitter:

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.driver = Chrome(PATH)

    def get_driver(self):
        """
        Returns the Driver used for the Scraping
        """
        return self.driver

    def set_driver(self, driver):
        if driver == 'chrome':
            self.driver = Chrome(PATH)
        elif driver == "edge":
            print('Sorry, this feature hasnt yet been implemented.')
        elif driver == "firefox":
            print('Sorry, this feature hasnt yet been implemented.')
        else:
            print('Sorry, I dont know this browser.')

    def login(self):
        # navigate to twitter login page using 'get' module
        self.driver.get('https://twitter.com/login/')
        sleep(2)

        # enter the username and password
        username = self.driver.find_element_by_xpath(
            '//input[@name="session[username_or_email]"]')
        username.send_keys(self.username)
        password = self.driver.find_element_by_xpath(
            '//input[@name="session[password]"]')  # enter the password
        password.send_keys(self.password)
        # login using the login button (similar action than to just press enter)
        password.send_keys(Keys.RETURN)
        sleep(2)

    def search(self, searchterm):
        # enter the searchterm
        search_input = self.driver.find_element_by_xpath(
            '//input[@aria-label="Search query"]')
        search_input.send_keys(searchterm)
        search_input.send_keys(Keys.RETURN)
        sleep(2)

        self.driver.find_element_by_link_text('Latest').click()
        sleep(1)


def main():
    twitterScraper = Scraper('twitter', 'scraper_python', "datascience")

    searchterm = input("What is your searchterm?: ")
    twitterScraper.scrape(searchterm)
    print(twitterScraper.get_data())
    print('-----------')
    twitterScraper.save_data(searchterm)


main()
