import time
import random
from scrapy.selector import Selector
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_2) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
]

options = uc.ChromeOptions()
options.add_argument(f"user-agent={random.choice(USER_AGENTS)}")
driver = uc.Chrome(options=options, headless=False)

try:
    url = 'https://medium.com/@suraj_bansal/build-your-own-ai-chatbot-a-beginners-guide-to-rag-and-langchain-0189a18ec401'
    driver.get(url)
    time.sleep(2)

    sel = Selector(text = driver.page_source)
    XPATH_TARGETS = """
            //h1//text() |
            //h2//text() |
            //h3//text() |
            //h4//text() |
            //h5//text() |
            //h6//text() |
            //p//text()  |
            //li//text() |
            //span//text() |
            //strong//text() |
            //em//text() |
            //blockquote//text()
        """

    raw_text = sel.xpath(XPATH_TARGETS).getall()

    cleaned = [t.strip() for t in raw_text if t.strip()]

    print("\n=== FULL TEXT EXTRACTED ===\n")
    for t in cleaned:
        print(t)


    # headers = driver.find_elements(By.XPATH,'//h1 | //h2 | //h3 | //h4 | //h5 | //h6')
    # headers_text = [h.text.strip() for h in headers]
    #
    # content = driver.find_elements(By.TAG_NAME,'p')
    # content_text = [p.text.strip() for p in content]
    #
    # print("Headrs are ",headers_text)
    # print("\n")
    # print("Content are",content_text)

finally:
    driver.quit()