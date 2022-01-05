
import time as tm
import pandas as pd
import undetected_chromedriver as uc
from smsactivateru import  Sms, SmsTypes, SmsService, GetBalance, GetNumber, SetStatus, GetStatus
import random
import colorama
import names
import re
import os
import zipfile
from colorama import Fore, Back, Style
#to do list


#detect if suspitions activity

#add print to every action


#make sure all options work no matter what
#name everything with comments






def testaccount():
    #confirms if account is not banned
    print(colorama.Fore.YELLOW + 'Testing account')
def append_df_to_excel(df, excel_path):
    #rewrites excell adding new account
    df_excel = pd.read_excel(excel_path)
    result = pd.concat([df_excel, df], ignore_index=True)
    result.to_excel(excel_path, index=False)




def createinstaaccounts():

    #get settings from config
    try:
        c = open("D:\documents\instagrambotaccmaker\config.txt", "r")
        cdf = pd.DataFrame(c, columns=['config'])
        try:
            testlogin = cdf.loc[2, "config"]
            testlogin = re.findall(r'"([^"]*)"', testlogin)

            delay = cdf.loc[3, "config"]
            delay = re.findall(r'"([^"]*)"', delay)

            usernamemaxnumber = cdf.loc[4, "config"]
            usernamemaxnumber = re.findall(r'"([^"]*)"', usernamemaxnumber)

            connectiontime = cdf.loc[5, "config"]
            connectiontime = re.findall(r'"([^"]*)"', connectiontime)



            phonenumbertimeout = cdf.loc[8, "config"]
            phonenumbertimeout = re.findall(r'"([^"]*)"', phonenumbertimeout)

            instagramnumberprice = cdf.loc[9, "config"]
            instagramnumberprice = re.findall(r'"([^"]*)"', instagramnumberprice)

            twocapapi = cdf.loc[11, "config"]
            twocapapi = re.findall(r'"([^"]*)"', twocapapi)





        except:
            print(colorama.Fore.RED + "error:")


    except:
        print(colorama.Fore.RED + "error: could not open config.txt")
        input(colorama.Fore.RED + "please make sure config.txt is in correct location and press enter to quit")
        quit()
    colorama.init()

    failed = 0
    successfull = 0
    # ask for number of entrys
    goodanswer = 0
    while goodanswer == 0:

        entryamount = int(input(colorama.Fore.BLUE + "how many entrys? (must be above 0)"))
        if entryamount > 0:
            goodanswer = 1
    goodanswer = 0
    proxyamount = 0
    try:
        wrapper = cdf.loc[8, "config"]
        wrappertext = str(re.findall(r'"([^"]*)"', wrapper))

        wrapper = Sms(re.findall(r'"([^"]*)"', wrapper))


    except:
        print(colorama.Fore.RED + 'error: invalid getSms-activate api  key')
        input(colorama.Fore.RED + 'Please get new key, enter new key in config.txt')


    getactivatebal = GetBalance().request(wrapper)
    howmanynumbersleft = getactivatebal / int(instagramnumberprice[0])
    if getactivatebal < int(instagramnumberprice[0]) + 1:
        print(colorama.Fore.RED + "error: no balance (getsmsactivate)")
        input(colorama.Fore.RED + 'please top up! press enter to quit')
        quit()









    # set up each proxy



    #checks for proxy file, and loads into pandas dataframe
    try:
        f = open("D:\documents\instagrambotaccmaker\proxies.txt", "r")
        df = pd.DataFrame(f, columns=['proxys'])
        proxyamount = len(df)
        print(colorama.Fore.YELLOW +'Loaded ' + colorama.Fore.BLUE + str(proxyamount) + colorama.Fore.YELLOW + ' Proxys | GetSmsActivate Balance: ' + colorama.Fore.BLUE + str(getactivatebal) + colorama.Fore.YELLOW + ' | ' + "Loaded " + colorama.Fore.BLUE + " Config.txt " + colorama.Fore.YELLOW + "| API key Loaded '"+ colorama.Fore.BLUE + wrappertext + colorama.Fore.YELLOW + "' |")
        print(colorama.Fore.YELLOW + '------------------------------------------------------------------------------------------------------------------------------')
    except:
        print(colorama.Fore.RED + "error: cannot locate proxy excel sheet from (D:\documents\instagrambotaccmaker\proxies.txt)")
        input(colorama.Fore.YELLOW + "Please fix proxies.txt before use, press enter to exit")
        quit()

    accountscreated = 0
    #starts loop to create each account
    for ind in df.index:
        if failed == int(connectiontime[0]):
            print(colorama.Fore.RED + 'error: tryed to connect ' + str(connectiontime[0]) + ' times which is your max retrys')
            input(colorama.Fore.MAGENTA + "Press enter to quit, please try again later")
            quit()
        #this try is for page loading
        try:
            # grabs proxy from txt
            proxybeforesplit = df.loc[random.randrange(5, proxyamount, 1), "proxys"]
            print(colorama.Fore.YELLOW + 'PROXY:' +  proxybeforesplit)
            splitproxy = proxybeforesplit.split(":")
            puser = splitproxy[2]
            ppass = splitproxy[3]
            pport = splitproxy[1]
            phost = splitproxy[0]
            PROXY_HOST = phost
            PROXY_PORT = pport
            PROXY_USER = puser
            PROXY_PASS = ppass

            # sets up proxy auth plugin
            manifest_json = """
                    {
                        "version": "1.0.0",
                        "manifest_version": 2,
                        "name": "Chrome Proxy",
                        "permissions": [
                            "proxy",
                            "tabs",
                            "unlimitedStorage",
                            "storage",
                            "<all_urls>",
                            "webRequest",
                            "webRequestBlocking"
                        ],
                        "background": {
                            "scripts": ["background.js"]
                        },
                        "minimum_chrome_version":"22.0.0"
                    }
                    """

            background_js = """
                    var config = {
                            mode: "fixed_servers",
                            rules: {
                              singleProxy: {
                                scheme: "http",
                                host: "%s",
                                port: parseInt(%s)
                              },
                              bypassList: ["localhost"]
                            }
                          };

                    chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});

                    function callbackFn(details) {
                        return {
                            authCredentials: {
                                username: "%s",
                                password: "%s"
                            }
                        };
                    }

                    chrome.webRequest.onAuthRequired.addListener(
                                callbackFn,
                                {urls: ["<all_urls>"]},
                                ['blocking']
                    );
                    """ % (PROXY_HOST, PROXY_PORT, PROXY_USER, PROXY_PASS)
            use_proxy = True
            user_agent = None
            path = os.path.dirname(os.path.abspath(__file__))
            chrome_options = uc.ChromeOptions()
            if use_proxy:
                pluginfile = 'proxy_auth_plugin.zip'

                with zipfile.ZipFile(pluginfile, 'w') as zp:
                    zp.writestr("manifest.json", manifest_json)
                    zp.writestr("background.js", background_js)
                chrome_options.add_extension(pluginfile)
            if user_agent:
                chrome_options.add_argument('--user-agent=%s' % user_agent)
            driver = uc.Chrome(
                chrome_options=chrome_options)

            # opens webdriver
            pagetrycount = 0

            page1numbererrors = 0
            page1usernameerror = 0
            while page1numbererrors == 0:
                pagetrycount += 1
                driver.get('https://www.instagram.com/accounts/emailsignup/')

                tm.sleep(3)
                # accepts cookies
                if pagetrycount == 1:

                        cookiesacceptpath = driver.find_element_by_xpath(
                            '/html/body/div[2]/div/div/div/div[2]/button[1]')
                        cookiesacceptpath.click()



                tm.sleep(2)

                hasnum = 0
                countofnumbers = 0
                tm.sleep(3)
                # starts inputting first sheet of data

                while hasnum != 1:
                    # trys to grab phone number

                    try:
                        # grabs api for sms activate


                        activation = GetNumber(SmsService().Instagram).request(wrapper)
                        print(colorama.Fore.GREEN + 'successfully grabbed number')

                        number = str(str(activation.phone_number))
                        normalnum = number[2:]
                        normalnum = '0' + normalnum
                        hasnum = 1
                        print(colorama.Fore.GREEN + str(countofnumbers + 1) + ' trys before success')

                        print(colorama.Fore.GREEN + "Number Being used: " + str(normalnum))
                    except:
                        countofnumbers += 1
                        hasnum = 0
                        if countofnumbers == phonenumbertimeout:
                            print(colorama.Fore.RED + "error: reached max number retrys")
                            input(colorama.Fore.RED + "press enter to quit")
                            quit()
                        print(colorama.Fore.RED +  'ERROR: tryed to grab number')
                        tm.sleep(3)
                # enters number
                numberpath = driver.find_element_by_xpath(
                    '/html/body/div[1]/section/main/div/div/div[1]/div/form/div[3]/div/label/input')
                numberpath.send_keys(normalnum)
                # enters names

                firstname = names.get_first_name()
                lastname = names.get_last_name()
                fullname = firstname + ' ' + lastname
                tm.sleep(2)

                fullnamepath = driver.find_element_by_xpath \
                    ('/html/body/div[1]/section/main/div/div/div[1]/div/form/div[4]/div/label/input')
                fullnamepath.send_keys(fullname)

                tm.sleep(3)
                usernameerror = 0
                countofusernametrys = 0
                # enters username

                countofusernametrys += 1
                randomnum = random.randrange(1, int(usernamemaxnumber[0]), 1)
                username = firstname + lastname + str(randomnum)
                usernamepath = driver.find_element_by_xpath(
                    '/html/body/div[1]/section/main/div/div/div[1]/div/form/div[5]/div/label/input')

                print(colorama.Fore.GREEN +   'adding username')
                usernamepath.send_keys(username)

                tm.sleep(2)
                count = 0

                password = ""
                # creates random password with first digit uppercase

                while count != 9:
                    count += 1
                    if count == 1:
                        password = password + chr(random.randrange(65, 90, 1))
                    else:
                        password = password + chr(random.randrange(33, 122, 1))

                passwordlink = driver.find_element_by_xpath(
                    '/html/body/div[1]/section/main/div/div/div[1]/div/form/div[6]/div/label/input')  #
                if countofusernametrys == 1:
                    passwordlink.send_keys(password)
                findxforusername = 0
                # detects if username or phone is invalid
                # presses next

                press = driver.find_element_by_xpath(
                    '/html/body/div[1]/section/main/div/div/div[1]/div/form/div[7]/div/button')
                press.click()
                tm.sleep(2)

                # waits for page 2 to load
                waitingforload = 0
                while waitingforload == 0:
                    try:
                        optionpick = str(
                            '/html/body/div[1]/section/main/div/div/div[1]/div/div[4]/div/div/span/span[1]/select/option[') + str(
                            random.randrange(1, 12, 1)) + str(']')
                        month = driver.find_element_by_xpath(optionpick)
                        waitingforload = 1
                        page1numbererrors = 1
                    except:
                        try:
                            print(colorama.Fore.YELLOW + 'trying to find bad phone or username')
                            badnumber = driver.find_element_by_xpath('/html/body/div[1]/section/main/div/div/div[1]/div/form/div[5]/div/div/span')
                            print(colorama.Fore.RED +  'error: bad Username')

                            page1numbererrors = 0
                        except:
                            try:
                                print(colorama.Fore.YELLOW + 'trying to find bad phone or username')
                                badnumber = driver.find_element_by_xpath(
                                    '/html/body/div[1]/section/main/div/div/div[1]/div/form/div[3]/div/div/span')
                                print(colorama.Fore.RED + 'error: bad Number')

                                page1numbererrors = 0
                            except:
                                print(colorama.Fore.GREEN + 'Number and username good')
                                page1numbererrors = 1


                        tm.sleep(5)
                        # if either number or username is bad, returns a error to restart
                        if page1numbererrors == 0:
                            driver.quit
                            errorcreate = driver.find_element_by_xpath('eroorrorooro')
                        print(colorama.Fore.RED + "error: page 2 not loaded")
                        tm.sleep(1)
                        waitingforload = 0

            # page 2 date of birth
            # enters month on page 2

            month.click()
            tm.sleep(2)
            usernameerror = 1

            # page 2 date of birth

            optionpick = str(
                '/html/body/div[1]/section/main/div/div/div[1]/div/div[4]/div/div/span/span[2]/select/option[') + str(
                random.randrange(1, 28, 1)) + str(']')
            day = driver.find_element_by_xpath(optionpick)
            day.click()
            tm.sleep(3)

            optionpick = str(
                '/html/body/div[1]/section/main/div/div/div[1]/div/div[4]/div/div/span/span[3]/select/option[') + str(
                random.randrange(22, 60, 1)) + str(']')
            year = driver.find_element_by_xpath(optionpick)
            year.click()
            tm.sleep(3)
            # writes to excell
            fileopen = open('D:\documents\instagrambotaccmaker\instagramaccount.txt', "a")
            data = normalnum + "}" + username + "}" + password + "}" + proxybeforesplit
            print(data)

            fileopen.write('\n' + data)

            fileopen.close()




            clicknext = driver.find_element_by_xpath('/html/body/div[1]/section/main/div/div/div[1]/div/div[6]/button')
            clicknext.click()
            tm.sleep(10)
            codefound = 0

            while codefound != 1:
                try:
                    while True:
                        code = GetStatus(id=activation.id).request(wrapper)
                        if code['code']:
                            # print('Your code:' + format(code['code']))
                            code = format(code['code'])
                            break

                    codebox = driver.find_element_by_xpath(
                        '/html/body/div[1]/section/main/div/div/div[1]/div/div/div/form/div[1]/div/label/input')
                    codebox.send_keys(code)
                    tm.sleep(2)
                    codefound = 1
                except:
                    print(colorama.Fore.RED + 'Error:failed getting code')
                    codefound = 0
                    tm.sleep(5)

            tm.sleep(3)
            pressnext = driver.find_element_by_xpath(
                '/html/body/div[1]/section/main/div/div/div[1]/div/div/div/form/div[2]/button')
            pressnext.click()
            accountscreated += 1
            successfull += 1
            tm.sleep(15)

            try:
                set_as_end = SetStatus(id=activation.id, status=SmsTypes.Status.End).request(wrapper)
                print(colorama.Fore.GREEN + "Cancelled number")
            except:
                print(colorama.Fore.RED + "error: could not cancel number")


            driver.quit()




            if int(ind) == int(entryamount - 1):
                break
            tm.sleep(5)


        except:

            print(colorama.Fore.RED + 'error: page failed to load, retrying with new proxy')
            try:
                set_as_end = SetStatus(id=activation.id, status=SmsTypes.Status.End).request(wrapper)
            except:
                pass

            entryamount += 1
            failed += 1
            driver.quit()

    print(colorama.Fore.LIGHTBLUE_EX + "Account creation complete")
    print(colorama.Fore.LIGHTBLUE_EX +'Failed attempts: ' + str(failed) + ' Success: ' + str(successfull))
    print(colorama.Fore.LIGHTBLUE_EX +"Created: " + str(accountscreated) + " Accounts")
    print(colorama.Fore.LIGHTBLUE_EX +"All files Saved To Instagramaccounts.xlsx and have been added to th bottom of the list")
    exiter = input(colorama.Fore.BLUE +"Press Enter To Quit")
    return exiter

def menuchoice():
    print(colorama.Fore.MAGENTA + "1) create instagram accounts")
    print(colorama.Fore.MAGENTA + "5) Exit")
    menuchoices = str(input(colorama.Fore.MAGENTA + "selection:"))
    return menuchoices


menuchosen = menuchoice()
if menuchosen == '1':


    createinstaaccounts()
if menuchosen == '5':
    exit()








