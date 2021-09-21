const config = require('./config')
const axios = require('axios')

const constrainTextToLenght = (text, lenght) => {
    let result = text
    if (result.length > lenght) {
        result = `${result.slice(0, lenght)}...`
    }
    return result
}

const shortLink = (link) => {
    const promise = new Promise((resolve, reject) => {
        const url = 'https://api-ssl.bitly.com/v4/shorten'
        const data = {
            "group_guid": "Aria2Shiva",
            "domain": "octoco.de",
            "long_url": link
        }
        axios.get(url).then((resp) => {
            console.log('gonxas response', resp)
        }).catch((error) => {
            console.log('Bitly error', error)
        })
    })
}


module.exports = { constrainTextToLenght, shortLink }