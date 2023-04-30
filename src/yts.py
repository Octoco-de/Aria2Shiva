import aiohttp
import asyncio

base_url = 'https://yts.proxyninja.org/api/v2/'

async def search(query):
    async with aiohttp.ClientSession() as session:
        url = f'{base_url}list_movies.json?query_term={query}'
        try:
            async with session.get(url) as response:
                response.raise_for_status()
                data = await response.json()

                movies = data.get('data', {}).get('movies', [])

                parsed_movies = []
                for movie in movies:
                    movie_data = {
                        'id': movie['id'],
                        'title': f"({movie['year']}) - {movie['title']}",
                    }
                    parsed_movies.append(movie_data)

                return parsed_movies
        except aiohttp.ClientError as error:
            print(f'movie search error: {error}')
            return None


def get_movie_details(movie_id):
    url = f'{base_url}movie_details.json?movie_id={movie_id}'
    response = requests.get(url)

    try:
        response.raise_for_status()
        data = response.json()

        movie = data.get('data', {}).get('movie', {})

        torrents = [
            {
                'movieId': movie['id'],
                'url': torrent['url'],
                'quality': torrent['quality'],
                'size': torrent['size'],
            }
            for torrent in movie.get('torrents', [])
        ]

        movie_data = {
            'id': movie['id'],
            'title': f"({movie['year']}) - {movie['title']}",
            'language': movie['language'],
            'image': movie['medium_cover_image'],
            'summary': movie['description_full'],
            'torrents': torrents,
            'url': movie['url'],
        }

        return movie_data
    except requests.exceptions.RequestException as error:
        print(f'movie details error: {error}')
        return None

if __name__ == "__main__":
    # Example usage
    query = 'inception'
    search_results = search(query)
    print(search_results)

    movie_id = search_results[0]['id']
    movie_details = get_movie_details(movie_id)
    print(movie_details)
