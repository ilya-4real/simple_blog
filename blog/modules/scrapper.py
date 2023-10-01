import xml.etree.ElementTree as ET
from requests import get
from time import time


class Scraper:

    def __init__(self, url):
        self.url = url
        self.file_name = 'rssdata.xml'
        self.response = None
        self.get_data(url)
        self.tree = ET.parse(self.file_name)

    def get_data(self, url):
        begin = time()
        self.response = get(url)
        with open(self.file_name, 'wb') as f:
            f.write(self.response.content)
        print(time()-begin, 'url accessing and file writing time')

    def scrap_channel(self):
        """
        method that scraps data about channel
        """
        tag_list = ('title', 'link', 'description', 'category', 'language'
                    'lastBuildDate', 'managingEditor', 'pubDate')
        data = {}
        for i in tag_list:
            root = self.tree.getroot().find(f'./channel/{i}')
            if root is not None:
                data[i] = root.text[:120]
        return data

    def scrap_item(self, limit: int) -> list:
        """
        method that scraps items in the channel
        :param limit: limit of items scraped
        :return: json
        """
        tag_list = ('title', 'author', 'pubDate', 'link', 'category', 'description')
        res = []
        root = self.tree.getroot().findall('./channel/item')

        if limit is None:
            limit = len(root)

        for i in range(min(limit, len(root))):
            dict_of_data = {}
            for j in tag_list:
                found = root[i].find(f'./{j}')
                if found is not None:
                    if j == 'title':
                        dict_of_data[j] = found.text[:120] + '...'
                    else:
                        dict_of_data[j] = found.text
            res.append(dict_of_data)
        return res
