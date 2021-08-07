import time
from lxml import etree
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import re
import csv


class JD_spider(object):
    driver_path = r"C:\Users\叶良镇\AppData\Local\Google\Chrome\Application\chromedriver.exe"

    def __init__(self):
        self.driver = webdriver.Chrome(executable_path=JD_spider.driver_path)
        self.goods = []
        # 从这个网址开始爬取
        self.page_url = 'https://www.jd.com/'

    def run(self):
        self.driver.get(self.page_url)
        inputTag = self.driver.find_element_by_id("key")
        inputTag.send_keys('手机')
        button = self.driver.find_element_by_class_name("button")
        button.click()
        while True:
            source = self.driver.page_source
            WebDriverWait(driver=self.driver, timeout=20).until(
                EC.presence_of_all_elements_located((By.XPATH, "//div[@class='p-wrap']//a[@class='pn-next']"))
            )

            self.get_page(source)
            time.sleep(5)
            next_btn = self.driver.find_element_by_xpath("//div[@class='p-wrap']//a[@class='pn-next']")
            if "pn-next disabled" in next_btn.get_attribute("class"):
                break
            else:
                next_btn.click()

    def get_page(self, source):
        try:
            good = {}
            base = "https:"
            html = etree.HTML(source)
            divs = html.xpath("//ul[@class='gl-warp clearfix']//li[@class='gl-item']/div[@class='gl-i-wrap']")
            for div in divs:
                url = div.xpath(".//div[@class='p-img']/a/@href")[0]
                url = base + url
                shop = div.xpath(".//div[@class='p-shop']//span/a/text()")[0]
                title = div.xpath(".//div[@class='p-name p-name-type-2']//a/em")[0]
                title = title.xpath("string(.)").strip()
                price = div.xpath(".//div[@class='p-price']//text()")
                price = "".join(price).strip()
                commit = div.xpath(".//div[@class='p-commit']//strong//text()")
                commit = "".join(commit).strip()
                good = {"店铺": shop, "名称": title, "价格": price, "评论": commit, "网址": url}
                self.goods.append(good)
                headers = ["店铺", "名称", "价格", "评论","网址"]
                with open('jingdong_2.csv', 'w', encoding="utf-8", newline='') as f:
                    writer = csv.DictWriter(f, headers)
                    writer.writeheader()
                    writer.writerows(self.goods)
                print(good)
                print("--"*100)
        except Exception as e:
            print(e)


if __name__ == '__main__':
    jd = JD_spider()
    jd.run()
