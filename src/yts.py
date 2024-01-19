import aiohttp
import logging
import requests
import urllib.parse

base_url = "https://yts.proxyninja.net/api/v2/"
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def search(query):
    # logger.info(f"search_movie: {query}")
    url = f"{base_url}list_movies.json"
    params = {
        "query_term": query,
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Will raise an HTTPError if the HTTP request returned an unsuccessful status code

        # Logging the successful response
        # logger.info(f"Response received: {response.json()}")

        data = response.json()

        # logger.info(f"Received data: {data}")

        movies = data.get("data", {}).get("movies", [])

        parsed_movies = []
        for movie in movies:
            movie_data = {
                "id": movie["id"],
                "title": f"({movie['year']}) - {movie['title']}",
            }
            parsed_movies.append(movie_data)

        # logger.info(f"parsed_movies: {parsed_movies}")
        return parsed_movies

    except requests.HTTPError as http_err:
        logger.error(f"HTTP error occurred: {http_err}")
    except Exception as err:
        logger.error(f"Other error occurred: {err}")

    return None


async def get_movie_details(movie_id):
    url = f"{base_url}movie_details.json"
    params = {"movie_id": movie_id}

    trackers = [
        "udp://glotorrents.pw:6969/announce",
        "udp://tracker.opentrackr.org:1337/announce",
        "udp://torrent.gresille.org:80/announce",
        "udp://tracker.openbittorrent.com:80",
        "udp://tracker.coppersurfer.tk:6969",
        "udp://tracker.leechers-paradise.org:6969",
        "udp://p4p.arenabg.ch:1337",
        "udp://tracker.internetwarriors.net:1337",
        "udp://open.demonii.com:1337/announce",
        "udp://p4p.arenabg.com:1337",
    ]
    tracker_str = "&tr=" + "&tr=".join(trackers)

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()

        data = response.json()
        movie = data.get("data", {}).get("movie", {})

        logger.info(f"movie data response: {movie}")

        torrents = movie.get("torrents", [])
        encoded_movie_title = urllib.parse.quote_plus(movie["title"])

        magnet_links = []
        for torrent in torrents:
            magnet_url = f"magnet:?xt=urn:btih:{torrent['hash']}&dn={encoded_movie_title}{tracker_str}"
            magnet_links.append(
                {
                    "movieId": movie["id"],
                    "url": magnet_url,
                    "quality": torrent["quality"],
                    "size": torrent["size"],
                }
            )

        movie_data = {
            "id": movie["id"],
            "title": movie["title"],
            "language": movie["language"],
            "image": movie["medium_cover_image"],
            "summary": movie["description_full"],
            "torrents": magnet_links,
            "url": movie["url"],
        }

        return movie_data

    except requests.HTTPError as http_err:
        logger.error(f"HTTP error occurred: {http_err}")
    except Exception as err:
        logger.error(f"Other error occurred: {err}")

    return None


if __name__ == "__main__":
    # Example usage
    query = "How to train your dragon"
    search_results = search(query)
    print(search_results)

    movie_id = search_results[0]["id"]
    movie_details = get_movie_details(movie_id)
    print(movie_details)
