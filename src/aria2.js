const downlaodTorrent = (bot, chatId, torrentUrl) => {
    bot.sendMessage(chatId, `Here we'll download torrent ${torrentUrl}`);
}

const downlaodMagnet = (bot, chatId, magnetUrl) => {
    bot.sendMessage(chatId, `Here we'll download magnet ${magnetUrl}`);
}

module.exports = {
    downlaodTorrent,
    downlaodMagnet,
}