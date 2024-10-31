from lxml import html
import re
class Parser:
    def parse_main_page(self, html_text):
        tree = html.fromstring(html_text)

        # 추출기
        images = tree.xpath('//tbody//tr//td[4]//div[@class="wrap"]//a//img/@src')
        titles = tree.xpath('//tbody//tr//td[6]//div[@class="wrap"]//div//div[1]//span//a/text()')
        artists = tree.xpath('//tbody//tr//td[6]//div[@class="wrap"]//div//div[2]/a[1]/text()')
        albums = tree.xpath('//tbody//tr//td[7]//div/div/a/text()')
        song_ids = tree.xpath('//tbody//tr/@data-song-no')
        artist_ids = [i.split("'")[1] for i in tree.xpath('//tbody//tr/td[6]/div/div/div[2]/a/@href')]

        # 데이터 구조화

        songs = []
        for i in range(len(song_ids)):
            song = {
                'image' : images[i],
                'title' : titles[i],
                'artist' : artists[i],
                'album' : albums[i],
                'song_id' : song_ids[i],
                'artist_id' : artist_ids[i],
            }
            songs.append(song)
        return songs

    def parse_song_detail(self, html_text):
        tree = html.fromstring(html_text)
        # 필요한 데이터 추출
        artist_href = tree.xpath('//div[@class="info"]/div[2]/a/@href')
        artist_id = artist_href[0].split("'")[1] if artist_href else 'Unknown Artist'

        sys_date_list = tree.xpath('//div[@class="meta"]/dl/dd[2]/text()')
        sys_date = sys_date_list[0].strip() if sys_date_list else 'Unknown Date'

        genre_list = tree.xpath('//div[@class="meta"]/dl/dd[3]/text()')
        genre = genre_list[0].strip() if genre_list else 'Unknown Genre'

        flac_list = tree.xpath('//div[@class="meta"]/dl/dd[4]/text()')
        flac = flac_list[0].strip() if flac_list else 'Unknown Quality'

        album_href = tree.xpath('//div[@class="meta"]/dl/dd[1]/a/@href')
        album_id = album_href[0].split("'")[1] if album_href else 'Unknown Album'

        lyric_list = tree.xpath('//div[@class="wrap_lyric"]/div/text()')
        lyric = ' '.join(lyric_list).strip() if lyric_list else 'No Lyrics Available'

        song_detail = {
            'artist_id': artist_id,
            'sys_date': sys_date,
            'genre': genre,
            'flac': flac,
            'album_id': album_id,
            'lyric': lyric
        }
        return song_detail

    def parse_artist_detail(self, html_text):
        tree = html.fromstring(html_text)
        # 필요한 데이터 추출
        debut_date_list = tree.xpath('//dl[@class="atist_info clfix"]/dd[1]/span/text()')
        debut_date = debut_date_list[0] if debut_date_list else 'Unknown Debut Date'

        pattern = r'^\s*$'
        art_info_list = tree.xpath('//dl[@class="atist_info clfix"]/dd/text()')
        art_info = [s.strip() for s in art_info_list if not re.match(pattern, s.strip())] or ['Unknown Artist Info']

        awards = tree.xpath('//dl[@class="atist_info clfix"]/dd[@class="awarded"]/span/text()')
        awards = awards if awards else ['No Awards']

        artist_detail = {
            'debut_date': debut_date,
            'art_info': art_info,
            'awards': awards
        }
        return artist_detail