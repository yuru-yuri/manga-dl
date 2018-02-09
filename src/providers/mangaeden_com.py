from src.provider import Provider


class MangaEdenCom(Provider):
    uriRegex = r'/[^/]+/([^/]+\-manga)/([^/]+)/?'

    def get_archive_name(self) -> str:
        idx = self.get_chapter_index().split('-')
        return 'vol_{}-{}'.format(*idx)

    def get_chapter_index(self) -> str:
        idx = self.re.search(r'\-manga/[^/]+/(\d+)', self.get_current_chapter()).group(1)
        return '{}-0'.format(idx)

    def get_main_content(self):
        result = self.re.search(self.uriRegex, self.get_url())
        groups = result.groups()
        return self.http_get('{}/en/{}/{}/'.format(self.get_domain(), *groups))

    def get_manga_name(self) -> str:
        return self.re.search(self.uriRegex, self.get_url()).group(2)

    def get_chapters(self):
        return self.html_fromstring(self.get_storage_content(), 'a.chapterLink')

    def get_files(self):
        content = self.http_get(self.get_current_chapter())
        result = self.re.search(r'var\s+pages\s+=\s+(\[{.+}\])', content)
        items = []
        if not result:
            return []
        for i in self.json.loads(result.group(1)):
            items.append('http:' + i['fs'])
        return items


main = MangaEdenCom