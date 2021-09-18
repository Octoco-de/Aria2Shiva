const axios = require('axios')

const baseUrl = 'https://yts.proxyninja.org/api/v2/'

const search = (query)=>{
    const promise = new Promise((resolve, reject) => {
        const url = `${baseUrl}list_movies.json?query_term=${query}`
        axios.get(url).then((resp) => {
        
        const movies = resp?.data?.data?.movies
        const parsedMovies = []
        movies.map(movie => {
            const movieData = {
                title:movie.title,
                language:movie.language,
                image: movie.medium_cover_image,
                summary: movie.summary,
                torrents: movie.torrents,
            }
            parsedMovies.push(movieData)
        })

        resolve(parsedMovies)  
    })
        .catch(() => {
            reject()
        })

    });

    return promise
}


module.exports = {
    search,
}