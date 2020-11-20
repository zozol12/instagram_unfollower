from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time

class InstagramUnfollower:

    _username = None
    _unfollow_list = []

    def __init__(self, username, password, unfollowing_speed):
        self.username = username # the username of your instagram account
        self.password = password # the password of your instagram account
        self.unfollowing_speed = unfollowing_speed
        self.driver = webdriver.Firefox(executable_path=r'C:\Program Files\geckodriver.exe') #specifies the driver which you want to use)

    def login(self): # method to login into your account
        driver = self.driver
        driver.get("https://www.instagram.com/")
        time.sleep(3)
        accept_cookies_button = driver.find_element_by_class_name("bIiDR")
        accept_cookies_button.click()
        username_box = driver.find_element_by_xpath("//input[@name='username']")
        username_box.clear()
        username_box.send_keys(self.username)
        password_box = driver.find_element_by_xpath("//input[@name='password']")
        password_box.clear()
        password_box.send_keys(self.password)
        password_box.send_keys(Keys.RETURN)
        time.sleep(5)
        not_now_button = driver.find_element_by_class_name("yWX7d")
        not_now_button.click()
        time.sleep(3)

    def find_username(self): # finds the username in the case of the program user is entered an e-mail adress instead of the username as a login info
        driver = self.driver
        self._username = driver.find_element_by_xpath("//a[@class='gmFkV']").text

    def find_followers(self, driver, buttons): # this functions finds the accounts who are following us
        # who follows us
        self.following_button = [button for button in buttons if 'following' in button.get_attribute('href')]
        self.following_button[0].click()
        time.sleep(2)
        follower_window = driver.find_element_by_xpath("//div[@role='dialog']//a")
        self.follower_number = driver.find_element_by_xpath( "//*[@id='react-root']/section/main/div/header/section/ul/li[3]/a/span").text
        counter = 0
        while counter < int( self.follower_number) / 10:
            counter+=1
            scroll_number = 1000 * counter
            driver.execute_script(f"document.getElementsByClassName('isgrP')[0].scroll(0, {scroll_number})")
            time.sleep(1)
        follower_accounts = driver.find_elements_by_class_name("_0imsa")
        self.follower_accounts = []
        for account in follower_accounts:
            self.follower_accounts.append(account.get_attribute('title'))

    def find_target_users(self): # method to find users who we follow but they don't follow us back
        driver = self.driver
        driver.get("https://www.instagram.com/" + self._username + "/")
        time.sleep(2)

        buttons = driver.find_elements_by_xpath("//a[@class='-nal3 ']")

        # who follows us
        self.find_followers(driver, buttons)

        time.sleep(2)
        self._unfollow_list = self.follower_accounts
        time.sleep(2)

    def unfollow_target_users(self):
        driver = self.driver
        self.following_window = driver.find_element_by_xpath("//div[@role='dialog']//a")
        self.follower_number = driver.find_element_by_xpath("//*[@id='react-root']/section/main/div/header/section/ul/li[2]/a/span").text
        self.unfollow_buttons = driver.find_elements_by_class_name("_8A5w5")
        for account in self._unfollow_list:
            self.unfollow_buttons[self._unfollow_list.index(str(account))].click()
            time.sleep(0.5)
            driver.find_element_by_xpath("//button[@class='aOOlW -Cab_   ']").click()
            time.sleep(self.unfollowing_speed)
        close_button = driver.find_elements_by_id("react-root")[0]
        action = ActionChains(driver)
        action.move_to_element_with_offset(close_button, 5, 5).click().perform() # closes the followers window
