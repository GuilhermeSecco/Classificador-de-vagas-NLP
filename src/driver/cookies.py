import json
import time

def carregar_cookies(driver, caminho="config/cookies.json"):
    driver.get("https://www.linkedin.com")
    time.sleep(2)
    with open(caminho, "r") as json_file:
        cookies = json.load(json_file)
        for cookie in cookies:
            if "sameSite" in cookie:
                cookie.pop("sameSite", None)
            driver.add_cookie(cookie)

    driver.refresh()
    time.sleep(2)
