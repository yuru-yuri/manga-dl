import html

from libs.provider import Provider


class MangaHubRu(Provider):

    def get_archive_name(self) -> str:
        idx = self.get_chapter_index().split('-')
        return 'vol_{:0>3}-{}'.format(*idx)

    def get_chapter_index(self) -> str:
        idx = self.re.search('/read/[^/]+/[^\\d]+(\\d+)/(\\d+)/', self.get_current_chapter()).groups()
        return '{}-{}'.format(*idx)

    def get_main_content(self):
        url = '{}/{}'.format(self.get_domain(), self.get_manga_name())
        return self.http_get(url)

    def get_manga_name(self) -> str:
        return self.re.search('\\.ru/([^/]+)/?', self.get_url())

    def get_chapters(self):
        parser = self.document_fromstring(self.storage_main_content(), '.b-catalog-list__name a[href^="/"]')
        return [self.get_domain() + i.get('href') for i in parser]

    def prepare_cookies(self):
        pass

    def get_files(self):
        parser = self.html_fromstring(self.get_current_chapter(), '.b-main-container .b-reader__full')
        if not parser:
            return []
        result = parser[0].get('data-js-scans')
        result = self.json.loads(html.unescape(result.replace('\/', '/')))
        return [self.get_domain() + i['src'] for i in result]

    def _loop_callback_chapters(self):
        pass

    def _loop_callback_files(self):
        pass


main = MangaHubRu