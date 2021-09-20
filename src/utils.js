const constrainTextToLenght = (text, lenght) => {
    let result = text
    if (result.length > lenght) {
        result = `${result.slice(0, lenght)}...`
    }
    return result
}


module.exports = { constrainTextToLenght }