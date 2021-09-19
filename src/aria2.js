const downlaodTorrent = (torrentUrl) => {
    console.log(`Here we'll download torrent ${torrentUrl}`)
}

const downlaodMagnet = (magnetUrl) => {
    console.log(`Here we'll download magnet ${magnetUrl}`)
}

module.exports = {
    downlaodTorrent,
    downlaodMagnet,
}