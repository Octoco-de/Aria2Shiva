import aiohttp
import logging
import requests

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

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()

        data = response.json()
        movie = data.get("data", {}).get("movie", {})

        torrents = [
            {
                "movieId": movie["id"],
                "url": torrent["url"],
                "quality": torrent["quality"],
                "size": torrent["size"],
            }
            for torrent in movie.get("torrents", [])
        ]

        movie_data = {
            "id": movie["id"],
            "title": f"({movie['year']}) - {movie['title']}",
            "language": movie["language"],
            "image": movie["medium_cover_image"],
            "summary": movie["description_full"],
            "torrents": torrents,
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
