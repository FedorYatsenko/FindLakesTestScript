import requests
from lxml import html


url = "https://en.wikipedia.org/wiki/List_of_lakes_of_England"
base_url = "https://en.wikipedia.org"
# base_url is needed for creating link
# get_links return relative path (like '/wiki/Abberton_Reservoir')

params = {  # name:lxml_regex_for_finding
    'name': '//h1[@id="firstHeading"]',
    'latitude': '//span[@class="latitude"]',
    'longitude': '//span[@class="longitude"]'
}


def get_links(html_page):
    tree = html.fromstring(html_page)

    list_li = tree.xpath('.//div[@class="mw-parser-output"]//li')

    links = []

    for li in list_li:
        if len(li) == 2 and li[0].tag == 'a' and li[1].tag == 'a':
            link = li[0].get('href')

            if link[:3] != '/w/':  # check if page exists
                links.append(link)

    return links


def get_data(html_page):
    data = {}

    tree = html.fromstring(html_page)

    for p_name, p_regex in params.items():
        find_result = tree.xpath(p_regex)
        if len(find_result) > 0:
            data[p_name] = find_result[0].text

    return data


def main():
    req = requests.get(url)

    lakes_links = get_links(req.content)

    for lake in lakes_links:
        req = requests.get(base_url + lake)

        print(get_data(req.content))


if __name__ == "__main__":
    main()
