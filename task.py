import sys
from argparse import ArgumentParser

import urllib.request
import urllib.error
import http.cookiejar
from html.parser import HTMLParser


def eprint(*args, **kwargs) -> None:
    """Write to stderr and exit the process."""
    print(*args, file=sys.stderr, **kwargs)
    sys.exit(1)


class HtmlFetcher:
    def get_html(self, url: str) -> None:
        """Get the html content or exit the process if failed."""
        try:
            opener = self._opener_with_cookie_handler()
            response = opener.open(url)
            html = response.read().decode("utf-8")
            return html
        except urllib.error.HTTPError as e:
            eprint(f"HTTP error: {e.code} - {e.reason}")
        except urllib.error.URLError as e:
            eprint(f"URL error: {e.reason}")
        except Exception as e:
            eprint(f"Unexpected error: {e}")

    def _opener_with_cookie_handler(self) -> urllib.request.OpenerDirector:
        """Opener mimicking a browser, trying to avoid http error 403."""
        cookie_jar = http.cookiejar.CookieJar()
        cookie_handler = urllib.request.HTTPCookieProcessor(cookie_jar)
        opener = urllib.request.build_opener(cookie_handler)
        opener.addheaders = [('User-Agent', 'Mozilla/5.0')]
        return opener


class UnorderedListParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.results: list[int] = [] # stores numbers of list items of each unordered list
        self.ul_stack: list[int] = [] # last element in the stack is current unordered list
        self.is_li: bool = False

    def handle_starttag(self, tag, attrs):
        if tag == 'ul':
            self.ul_stack.append(0) # add new unordered list to the stack

        if tag == 'li' and self.ul_stack:
            self.is_li = True
            self.ul_stack[-1] += 1 # increment count of the current list by 1

    def handle_endtag(self, tag):
        if tag == 'ul' and self.ul_stack:
            completed_count = self.ul_stack.pop() # remove closing list from the stack
            self.results.append(completed_count) # add closing lists items count to the results list

        if tag == 'li' and self.is_li:
            self.is_li = False


if __name__ == "__main__":
    arg_parser = ArgumentParser()
    arg_parser.add_argument('URL')
    args = arg_parser.parse_args()
    url = args.URL

    html_fetcher = HtmlFetcher()
    ul_parser = UnorderedListParser()

    html = html_fetcher.get_html(url)
    ul_parser.feed(html)
    counts = ul_parser.results
    if not counts:
        print("No unordered lists found in html content")
        sys.exit(0)
    result = max(counts)
    print(f"Most direct children in unordered list: {result}")
