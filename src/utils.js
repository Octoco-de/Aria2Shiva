const config = require('./config')
const axios = require('axios')

const constrainTextToLenght = (text, lenght) => {
    let result = text
    if (result.length > lenght) {
        result = `${result.slice(0, lenght)}...`
    }
    return result
}

const shortenLink = (link) => {
    const promise = new Promise((resolve, reject) => {
        const url = 'https://api-ssl.bitly.com/v4/shorten'
        const data = {
            "group_guid": "Bl9knMjyJNh",
            "long_url": link
        }
        const conf = {
            headers: { Authorization: `Bearer ${config.bitlyToken}` }
        };
        axios.post(url, data, conf).then((resp) => {
            const link = resp?.data?.link
            if (link)
                resolve(link.replace('https://bit.ly/', ''))
            else
                reject()
        }).catch((error) => {
            console.log('Bitly error', `${error.response.status}: ${error.response.statusText}\n\n${error}`)
            reject()

        })
    })

    return promise
}


module.exports = { constrainTextToLenght, shortenLink }