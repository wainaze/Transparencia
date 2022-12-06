from urllib.parse import urlparse, urljoin

url = "https://cpasbxl.brussels/"
href = "?p=107"

# join the URL if it's relative (not absolute link)
href = urljoin(url, href)
#parsed_href = urlparse(href)
# remove URL GET parameters, URL fragments, etc.
#href = parsed_href.scheme + "://" + parsed_href.netloc + parsed_href.path + parsed_href.params + parsed_href.query + parsed_href.fragment
print(href)

