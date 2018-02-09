from src.provider import Provider


class MangaLibMe(Provider):

    def get_archive_name(self) -> str:
        idx = self.get_chapter_index().split('-')
        return 'vol_{:0>3}-{}'.format(*idx)

    def get_chapter_index(self) -> str:
        selector = r'\.me/[^/]+/[^\d]+(\d+)/[^\d]+([^/]+)'
        idx = self.re.search(selector, self.get_current_chapter()).groups()
        return '{}-{}'.format(*idx)

    def get_main_content(self):
        return self.http_get('{}/{}'.format(self.get_domain(), self.get_manga_name()))

    def get_manga_name(self) -> str:
        return self.re.search(r'\.me/([^/]+)', self.get_url()).group(1)

    def get_chapters(self):
        c, s = self.get_storage_content(), '.chapters-list .chapter-item__name a'
        return self.document_fromstring(c, s)

    def get_files(self):
        content = self.http_get(self.get_current_chapter())
        base_url = self.re.search(r'\.scan\-page.+src\'.+?\'([^\'"]+)\'', content).group(1)
        images = self.re.search(r'var\s+pages\s*=\s*(\[\{.+\}\])', content).group(1)
        imgs = ['{}/{}'.format(base_url, i.get('page_image')) for i in self.json.loads(images)]
        return imgs


main = MangaLibMe