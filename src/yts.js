const axios = require('axios')

const baseUrl = 'https://yts.proxyninja.org/api/v2/'

const search = (query) => {
    const promise = new Promise((resolve, reject) => {
        const url = `${baseUrl}list_movies.json?query_term=${query}`
        axios.get(url).then((resp) => {

            const movies = resp?.data?.data?.movies
            if (!movies) {
                resolve()
            } else {
                const parsedMovies = []
                movies.map(movie => {
                    const movieData = {
                        id: movie.id,
                        title: `(${movie.year}) - ${movie.title}`,
                    }
                    parsedMovies.push(movieData)
                })

                resolve(parsedMovies)
            }
        })
            .catch((error) => {
                console.log('movie search error', error)
                reject()
            })

    });

    return promise
}

const getMovieDetails = (movieId) => {
    const promise = new Promise((resolve, reject) => {
        const url = `${baseUrl}movie_details.json?movie_id=${movieId}`
        axios.get(url).then((resp) => {
            const movie = resp?.data?.data?.movie

            const movieId = movie.id
            const torrents = []
            movie.torrents.map(torrent => {
                torrents.push({
                    movieId,
                    url: torrent.url,
                    quality: torrent.quality,
                    size: torrent.size,
                })
            })

            const movieData = {
                id: movieId,
                title: `(${movie.year}) - ${movie.title}`,
                language: movie.language,
                image: movie.medium_cover_image,
                summary: movie.description_full,
                torrents: torrents,
                url: movie.url,
            }
            resolve(movieData)
        }).catch((error) => {
            console.log('movie data error', error)
            reject()
        })
    })

    return promise
}


module.exports = {
    search,
    getMovieDetails,
}