#!D:/Users/gorno/AppData/Local/Programs/Python/Python35-32/python.exe
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.action_chains import ActionChains
from pyvirtualdisplay import Display
import time
import os


def __settings():
    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    phantomjs = os.path.join(SITE_ROOT, "static", "phantomjs.exe")
    ghostdriver = os.path.join(SITE_ROOT, "static", "ghostdriver.log")
    dcap = dict(DesiredCapabilities.PHANTOMJS)
    dcap["phantomjs.page.settings.userAgent"] = ("Mozilla/5.0 (Windows NT 10.0; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0")
    browser = webdriver.PhantomJS(executable_path=phantomjs, desired_capabilities=dcap, service_log_path=ghostdriver)
    browser.set_window_size(1024, 768)
    return browser


def __firefox():
    """SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    wires = os.path.join(SITE_ROOT, "static", "wires.exe")
    firefox_capabilities = DesiredCapabilities.FIREFOX
    firefox_capabilities['marionette'] = True
    browser = webdriver.Firefox(capabilities=firefox_capabilities, executable_path=wires)"""
    return webdriver.Firefox()


def is_user_exists(login, password):
    browser = __settings()
    browser.get("https://qiwi.com")
    # Finding and accepting login form
    browser.find_element_by_class_name("header-login-item-login").click()
    log = browser.find_element_by_name("login")
    log.clear()
    log.send_keys(login)
    browser.find_element_by_name("password").send_keys(password)
    log.send_keys(Keys.RETURN)
    time.sleep(3)
    browser.execute_script('window.stop();')
    for i in range(25):
        time.sleep(1)
        if 'https://qiwi.com/main.action' == browser.current_url:
            browser.quit()
            return True
    browser.quit()
    return False


def __quit(browser):
    if browser.find_element_by_class_name('logout'):
        browser.find_element_by_class_name('logout').find_element_by_tag_name('a').click()


def __login(login, password, browser):
    log = browser.find_element_by_name("login")
    log.clear()
    log.send_keys(login)
    time.sleep(1)
    browser.find_element_by_name("password").send_keys(password)
    time.sleep(1)
    log.send_keys(Keys.RETURN)
    time.sleep(3)


def _qiwi(login, password, req, sum, browser):
    browser.get("https://qiwi.com/payment/form.action?provider=99")
    browser.find_element_by_class_name('signinBtn').click()
    for i in range(20):
        time.sleep(1)
        if 'вход' or 'sign' in browser.page_source.lower():
            __login(login, password, browser)
            break
    time.sleep(5)
    requisites = browser.find_element_by_css_selector(".qiwi-textinput.ui-mask")
    ActionChains(browser).move_to_element(requisites).perform()
    requisites.click()
    time.sleep(1)
    requisites.send_keys(req)
    time.sleep(1)
    browser.find_element_by_class_name('qiwi-payment-amount-control').find_element_by_tag_name('input').send_keys(sum)
    time.sleep(1)
    submit = browser.find_element_by_css_selector(".goog-inline-block.qiwi-orange-button")
    ActionChains(browser).move_to_element(submit).perform()
    time.sleep(2)
    submit.click()
    while browser.current_url != 'https://qiwi.com/payment/form.action?provider=99&state=confirm':
        time.sleep(1)
    submit = browser.find_elements_by_css_selector(".goog-inline-block.qiwi-orange-button")[1]
    ActionChains(browser).move_to_element(submit).perform()
    time.sleep(2)
    submit.click()
    time.sleep(3)
    if 'успешно' in browser.page_source.lower() or 'success' in browser.page_source.lower():
        browser.get_screenshot_as_file("success.png")
        browser.close()
        return True
    else:
        browser.get_screenshot_as_file("error.png")
        browser.close()
        return False


def _alpha_card(login, password,  req, month, year, sum, browser):
    browser.get("https://qiwi.com/payment/form.action?provider=464")
    browser.find_element_by_class_name('signinBtn').click()
    for i in range(20):
        time.sleep(1)
        if 'вход' or 'sign' in browser.page_source.lower():
            __login(login, password, browser)
            break
    time.sleep(5)
    type = browser.find_element_by_css_selector(".qiwi-radio-menu-item.goog-option")
    ActionChains(browser).move_to_element(type).perform()
    type.click()
    time.sleep(1)

    # choosing month
    months = browser.find_element_by_class_name("qiwi-year-month-month")
    ActionChains(browser).move_to_element(months).perform()
    time.sleep(1)
    months.click()
    time.sleep(1)
    mnth = browser.find_elements_by_css_selector(".qiwi-select-menu.qiwi-select-menu-vertical")[0].find_elements_by_class_name("qiwi-select-menu-item-content")[int(month) - 1]
    time.sleep(1)
    ActionChains(browser).move_to_element(mnth).perform()
    time.sleep(1)
    text = mnth.text
    mnth.click()
    time.sleep(1)
    browser.execute_script("document.getElementsByClassName('goog-inline-block qiwi-select-caption')[0].textContent= '"+text+"'")
    browser.execute_script("document.getElementsByClassName"
                           "('qiwi-select-menu qiwi-select-menu-vertical')"
                           "[0].getElementsByClassName('qiwi-select-menu-item')"
                           "["+str(int(month)-1)+"].setAttribute('role', 'option')")
    browser.execute_script("document.getElementsByClassName('qiwi-select-menu qiwi-select-menu-vertical')[0]"
                           ".setAttribute('aria-activedescedant', '"+mnth.id+"')")

    # choosing year
    years = browser.find_element_by_class_name("qiwi-year-month-year")
    ActionChains(browser).move_to_element(years).perform()
    time.sleep(1)
    years.click()
    time.sleep(1)
    yer = browser.find_elements_by_css_selector(".qiwi-select-menu.qiwi-select-menu-vertical")[1].find_elements_by_class_name("qiwi-select-menu-item-content")[int(year) - 1]
    time.sleep(1)
    ActionChains(browser).move_to_element(yer).perform()
    time.sleep(1)
    text = yer.text
    yer.click()
    browser.execute_script("document.getElementsByClassName('goog-inline-block qiwi-select-caption')[1].textContent= '" + text + "'")
    browser.execute_script(
        "document.getElementsByClassName('qiwi-select-menu qiwi-select-menu-vertical')[1].getElementsByClassName('qiwi-select-menu-item')[" + str(
            int(year) - 1) + "].setAttribute('role', 'option')")
    browser.execute_script(
        "document.getElementsByClassName('qiwi-select-menu qiwi-select-menu-vertical')[1].setAttribute('aria-activedescedant', '" + yer.id + "')")
    requisites = browser.find_element_by_css_selector(".qiwi-textinput.ui-mask")
    ActionChains(browser).move_to_element(requisites).perform()
    requisites.click()
    requisites.send_keys(req)
    time.sleep(1)
    browser.find_element_by_class_name('qiwi-payment-amount-control').find_element_by_tag_name('input').send_keys(sum)
    time.sleep(1)
    submit = browser.find_element_by_css_selector(".goog-inline-block.qiwi-orange-button")
    ActionChains(browser).move_to_element(submit).perform()
    time.sleep(2)
    submit.click()
    while browser.current_url != 'https://qiwi.com/payment/form.action?provider=464&state=confirm':
        time.sleep(1)
    submit = browser.find_elements_by_css_selector(".goog-inline-block.qiwi-orange-button")[1]
    ActionChains(browser).move_to_element(submit).perform()
    time.sleep(2)
    submit.click()
    time.sleep(3)
    if 'успешно' in browser.page_source.lower() or 'success' in browser.page_source.lower():
        browser.get_screenshot_as_file("success.png")
        browser.close()
        return True
    else:
        browser.get_screenshot_as_file("error.png")
        browser.close()
        return False


def _alpha(login, password,  req, sum, browser):
    browser.get("https://qiwi.com/payment/form.action?provider=464")
    browser.find_element_by_class_name('signinBtn').click()
    for i in range(20):
        time.sleep(1)
        if 'вход' or 'sign' in browser.page_source.lower():
            __login(login, password, browser)
            break
    time.sleep(1)
    type = browser.find_elements_by_css_selector(".qiwi-radio-menu-item.goog-option")[1]
    ActionChains(browser).move_to_element(type).perform()
    type.click()
    time.sleep(1)

    requisites = browser.find_element_by_css_selector(".qiwi-textinput.ui-mask")
    ActionChains(browser).move_to_element(requisites).perform()
    requisites.click()
    requisites.send_keys(str(req))
    time.sleep(1)
    browser.find_element_by_class_name('qiwi-payment-amount-control').find_element_by_tag_name('input').send_keys(sum)
    time.sleep(1)
    submit = browser.find_element_by_css_selector(".goog-inline-block.qiwi-orange-button")
    ActionChains(browser).move_to_element(submit).perform()
    time.sleep(2)
    submit.click()
    while browser.current_url != 'https://qiwi.com/payment/form.action?provider=464&state=confirm':
        time.sleep(1)
    submit = browser.find_elements_by_css_selector(".goog-inline-block.qiwi-orange-button")[1]
    ActionChains(browser).move_to_element(submit).perform()
    time.sleep(2)
    submit.click()
    time.sleep(3)
    if 'успешно' in browser.page_source.lower() or 'success' in browser.page_source.lower():
        browser.get_screenshot_as_file("success.png")
        browser.close()
        return True
    else:
        browser.get_screenshot_as_file("error.png")
        browser.close()
        return False


def _visa(login, password, req, sum, browser):
    browser.get("https://qiwi.com/payment/form.action?provider=22351")
    browser.find_element_by_class_name('signinBtn').click()
    for i in range(20):
        time.sleep(1)
        if 'вход' or 'sign' in browser.page_source.lower():
            __login(login, password, browser)
            break
    requisites = browser.find_element_by_css_selector(".qiwi-textinput.ui-mask")
    ActionChains(browser).move_to_element(requisites).perform()
    requisites.click()
    requisites.clear()
    requisites.send_keys(req)
    time.sleep(5)
    browser.find_element_by_class_name('qiwi-payment-amount-control').find_element_by_tag_name('input').send_keys(sum)
    time.sleep(1)
    submit = browser.find_element_by_css_selector(".goog-inline-block.qiwi-orange-button")
    ActionChains(browser).move_to_element(submit).perform()
    time.sleep(2)
    submit.click()
    while browser.current_url != 'https://qiwi.com/payment/form.action?provider=22351&state=confirm':
        time.sleep(1)
    submit = browser.find_elements_by_css_selector(".goog-inline-block.qiwi-orange-button")[1]
    ActionChains(browser).move_to_element(submit).perform()
    time.sleep(2)
    submit.click()
    time.sleep(3)
    if 'успешно' in browser.page_source.lower() or 'success' in browser.page_source.lower():
        browser.get_screenshot_as_file("success.png")
        browser.close()
        return True
    else:
        browser.get_screenshot_as_file("error.png")
        browser.close()
        return False


def transfer(login, password, type, req, sum):
    display = Display(visible=0, size=(800, 600))
    display.start()
    browser = __firefox()
    if type == 'qiwi':
        _qiwi(login, password, req, sum, browser)
    elif type == 'alpha-card':
        # _alpha_card(login, password, req, str(req).split("#")[1], str(req).split("#")[2], sum, browser)
        return 'not supported'
    elif type == 'alpha':
        _alpha(login, password, req, sum, browser)
    elif type == 'visa/mastercard':
        _visa(login, password, req, sum, browser)
    else:
        return '404'
    browser.quit()
    display.stop()

def get_balance(login, password):
    browser = __settings()
    time.sleep(2)
    browser.get("https://qiwi.com")
    # Finding and accepting login form
    browser.find_element_by_class_name("header-login-item-login").click()
    log = browser.find_element_by_name("login")
    log.clear()
    log.send_keys(login)
    browser.find_element_by_name("password").send_keys(password)
    log.send_keys(Keys.RETURN)
    while 'настройки' not in browser.page_source.lower():
        time.sleep(0.5)
    response = browser.find_element_by_class_name('account_current_amount').text.strip()
    browser.quit()
    return response
