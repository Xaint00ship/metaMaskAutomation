from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from seleniumwire import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
import os 
# # переменные для тестов тут
metamask_pass = "22061973"
antik_id = "Profile 3"
phrase = "cliff moon around emotion direct monitor very play ginger aim science roof"


class MetaMask:

    def __init__(self, antikId, phrase, metamaskPass):
        self.antikId = antikId
        self.phrase = phrase
        self.metamaskPass = metamaskPass
        self.driver = self.createChromeDriverSession()
        self.__path = os.path.dirname(os.path.abspath(__file__))

    def createChromeDriverSession(self): # создается/подключается профиль хрома
        options = webdriver.ChromeOptions()
        options.add_argument('--profiling-flush=n')
        options.add_argument('--allow-profiles-outside-user-dir')
        options.add_argument('--enable-profile-shortcut-manager')
        options.add_argument(r'user-data-dir=D:/projects/metaMaskAutomation/Profiles/User')  # сделать определение PATH
        options.add_argument(f'--profile-directory={antik_id}')

        return webdriver.Chrome(ChromeDriverManager().install(), options=options)


    def installMetaMask(self): # не до конца сделано, проблема в модальном окне
        self.driver.get('https://chrome.google.com/webstore/detail/metamask/nkbihfbeogaeaoehlefnkodbefgpgknn')
        sleep(5)
        self.driver.find_element(By.CLASS_NAME, 'webstore-test-button-label').click()
        sleep(100)


    def importWallet(self): # импорт кошелька
        self.driver.get(
            'chrome-extension://nkbihfbeogaeaoehlefnkodbefgpgknn/home.html#initialize/create-password/import-with-seed-phrase')
        sleep(10)

        # создадим из фразы список слов
        list_phrase = list(self.phrase.split(" "))
        # вставить слова в соответствующие поля
        index = 0
        for word in list_phrase:
            inputId = 'import-srp__srp-word-' + str(index)
            import_input = self.driver.find_element(By.ID, inputId)
            import_input.send_keys(word)
            index = index + 1

        # пароль вставить из переменной
        passwordForm = self.driver.find_element(By.ID, 'password')
        passwordForm.send_keys(self.metamaskPass)
        passwordConfitmForm = self.driver.find_element(By.ID, 'confirm-password')
        print(type(passwordConfitmForm))
        passwordConfitmForm.send_keys(self.metamaskPass)
        sleep(1)

        # клик на чекбокс
        checkboxImport = self.driver.find_element(By.ID, 'create-new-vault__terms-checkbox')
        checkboxImport.click()
        sleep(1)

        # клик на import
        importButton = self.driver.find_element(By.TAG_NAME, 'button')
        importButton.click()
        sleep(20)

        # новая страница, клик по button
        alldoneButton = self.driver.find_element(By.TAG_NAME, 'button')
        alldoneButton.click()
        sleep(5)

        self.driver.quit()


    # def testAbuse(self):
    #     self.driver.get("https://portal.zksync.io/bridge")
    #     sleep(15)
    #     print(self.driver.window_handles)
    #     self.importWallet()
    #     sleep(35)
    #     self.confirmTransaction()
    #     sleep(1000)


    def importWallet(self): # вход в метамаск по паролю
        self.driver.switch_to.window(self.driver.window_handles[1]) # переключение на 2 окно(метамаск)
        sleep(10)
        self.driver.find_element(By.ID, "password").send_keys(self.metamaskPass)
        self.driver.find_element(By.CLASS_NAME, "btn--rounded").click()


    def confirmTransaction(self): # подтверждение транзакции
        self.driver.switch_to.window(self.driver.window_handles[1]) # переключение на 2 окно(метамаск)
        sleep(10)
        self.driver.find_element(By.CLASS_NAME, "btn-primary").click()


    def changeNetwork(self, nameNetwork, UrlRpc, numberChain, symbolCurrency, ExplorerBlockURL = ""):
        self.driver.get("chrome-extension://nkbihfbeogaeaoehlefnkodbefgpgknn/home.html#settings/networks")
        sleep(12)
        self.driver.find_element(By.CLASS_NAME, "identicon__address-wrapper").click()
        sleep(1)
        self.driver.find_elements(By.CLASS_NAME, "account-menu__item--clickable")[5].click()
        sleep(1)
        self.driver.find_elements(By.CLASS_NAME, "tab-bar__tab")[5].click()
        sleep(10)
        self.driver.execute_script(f"document.querySelectorAll('.form-field__input')[0].value='{nameNetwork}'")
        self.driver.execute_script(f"document.querySelectorAll('.form-field__input')[0].value='{UrlRpc}'")
        self.driver.execute_script(f"document.querySelectorAll('.form-field__input')[0].value='{numberChain}'")
        self.driver.execute_script(f"document.querySelectorAll('.form-field__input')[0].value='{symbolCurrency}'")
        self.driver.execute_script(f"document.querySelectorAll('.form-field__input')[0].value='{ExplorerBlockURL}'")
        sleep(10)
        # self.driver.find_elements(By.CLASS_NAME, "form-field__input")[0].send_keys(f"{nameNetwork}")
        # self.driver.find_elements(By.CLASS_NAME, "form-field__input")[1].send_keys(f"{UrlRpc}")
        # self.driver.find_elements(By.CLASS_NAME, "form-field__input")[2].send_keys(f"{numberChain}")
        # self.driver.find_elements(By.CLASS_NAME, "form-field__input")[3].send_keys(f"{symbolCurrency}")
        # self.driver.find_elements(By.CLASS_NAME, "form-field__input")[4].send_keys(f"{ExplorerBlockURL}")

        self.driver.find_element(By.CLASS_NAME, "btn-primary").click()
        sleep(3)




if __name__ == '__main__':

    MM = MetaMask(antik_id, phrase, metamask_pass)
    MM.changeNetwork("Test", "https://goerli.optimism.io", "420", "ETH")