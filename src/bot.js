const TelegramBot = require('node-telegram-bot-api');
const config = require('./config')
const YTSModule = require('./yts')
const Aria2Module = require('./aria2')
const utils = require('./utils')

const areWeDebugging = config.debug

// Create a bot that uses 'polling' to fetch new updates
const bot = new TelegramBot(config.token, { polling: true });


const logginIn = {}
const sessions = {}

const validateUser = (chatId, msg) => {

  const pass = config.allowedIDs[chatId]

  if (!pass) {
    bot.sendAnimation(chatId, 'https://media.giphy.com/media/njYrp176NQsHS/giphy.gif')
    return false
  }

  if (!logginIn[chatId]) {
    logginIn[chatId] = true
    bot.sendMessage(chatId, "Speak friend and enter");
  } else if (msg.text === pass) {
    logginIn[chatId] = false
    bot.sendMessage(chatId, 'Welcome to Khazad-dûm, how can I serve you?');
    sessions[chatId] = true
    setTimeout(() => {
      sessions[chatId] = false
    }, config.sessionDuration)
  } else {
    bot.sendMessage(chatId, '_Mellon_ worked for Gandalf...', { parse_mode: "Markdown" })
  }

}

const movieButton = (movie) => {
  return [{ text: movie.title, callback_data: `movie: ${movie.id}` }]
}

const torrentButton = (torrent) => {
  let size = torrent.size.toUpperCase()
  if (size.indexOf(' MB') !== -1) {
    size = size.replace(' MB', '')
    size = Math.ceil(size) + ' MB'
  }
  return { text: `${torrent.quality} ${size}`, callback_data: torrent.movieId }
}

const summaryButton = (movieId) => {
  return [{ text: 'Full Summary', callback_data: `SUM: ${movieId}` }]
}

const siteButton = (movieData) => {
  return [{ text: 'Open Site', url: movieData.url }]
}

const userSelectedMovie = (chatId, movieId) => {
  YTSModule.getMovieDetails(movieId).then(movieData => {
    let tempArray = []
    const buttons = []
    movieData.torrents.map(torrent => {
      tempArray.push(torrentButton(torrent))
      if (tempArray.length === 2) {
        buttons.push(tempArray)
        tempArray = []
      }
    })
    if (tempArray.length > 0) {
      buttons.push(tempArray)
    }

    buttons.push(summaryButton(movieId))
    buttons.push(siteButton(movieData))

    let caption = movieData.title

    if (movieData.summary) {
      let summary = utils.constrainTextToLenght(movieData.summary, 150)
      caption = `${caption}\n\n\`${summary}\``
    }

    bot.sendPhoto(
      chatId,
      movieData.image,
      {
        caption,
        parse_mode: "Markdown",
        reply_markup: { inline_keyboard: buttons }
      },
    )
  }).catch(() => {
    bot.sendMessage(chatId, 'Well this is embarrassing....');
  })
}

const displaySummary = (chatId, movieId) => {
  YTSModule.getMovieDetails(movieId).then(movieData => {
    bot.sendMessage(chatId, `\`${movieData.summary}\``, { parse_mode: "Markdown" });
  }).catch(() => {
    bot.sendMessage(chatId, 'Well this is embarrassing....');
  })
}

// const downloadYTSMovie = (chatId, movieId, quality) => {
//   console('downloadYTSMovie', movieId, quality)
//   Aria2Module.downlaodTorrent(torrent.url)
// }

// Button's Handler
bot.on('callback_query', function onCallbackQuery(button) {

  const data = button.data

  if (data.indexOf('movie: ') !== -1) {
    userSelectedMovie(button.from.id, data.replace('movie: ', ''))
  } else if (data.indexOf('SUM: ') !== -1) {
    console.log('gonxas data', data)
    displaySummary(button.from.id, data.replace('SUM: ', ''))
  } else {
    // console.log('button', button)
    // console.log('caption_entities', button.caption_entities)
    // button.photo.map(object => {
    //   console.log('photo', object)
    // })
    // downloadYTSMovie(button.from.id, data, button.msg)
  }

})





//--------- COMMAND METHODS

bot.onText(/\/Start/i, (msg) => {
  const chatId = msg.chat.id;
  bot.sendMessage(chatId, 'Beep Boop. 🤖')
});

// Matches "/Search [whatever]"
bot.onText(/\/Search (.+)/i, (msg, match) => {
  // 'msg' is the received Message from Telegram
  // 'match' is the result of executing the regexp above on the text content
  // of the message

  const chatId = msg.chat.id;

  if (areWeDebugging || sessions[chatId]) {

    const query = match[1]; // the captured "whatever"
    YTSModule.search(query).then(movies => {
      if (!movies || movies.length === 0) {
        bot.sendMessage(chatId, "Ain't Nobody Here but Us Chickens");
      } else {
        const buttons = []
        movies.map(movie => {
          movie.chatId = chatId
          buttons.push(movieButton(movie))
        })
        bot.sendMessage(chatId, 'This is what we found for you 👀', { reply_markup: { inline_keyboard: buttons } });
      }
    }).catch(() => {
      bot.sendMessage(chatId, 'Well this is embarrassing...');
    })

  } else {
    validateUser(chatId, msg)
  }
});

//--------- 


// Listen for any kind of message. There are different kinds of
// messages.
bot.on('message', (msg) => {
  let command = false
  msg.entities.map(entitie => {
    if (entitie.type === 'bot_command')
      command = true
  })

  //commands will be captured in their own methods. Here's pure talk.
  if (!command) {

    const chatId = msg.chat.id;

    // console.log(`${ msg.from.username } : ${ msg.chat.id } `)

    if (areWeDebugging || sessions[chatId])
      // send a message to the chat acknowledging receipt of their message
      switch (msg.text.toLowerCase()) {
        case 'brainz':
          bot.sendMessage(chatId, '🧟');
          break
        case 'start':
          bot.sendMessage(chatId, 'Beep Boop. 🤖')
          break
        case 'beep boop':
          bot.sendMessage(chatId, 'Bop Beep? 🤖');
          break
        case 'ping':
          bot.sendMessage(chatId, 'Pong');
          break
        case 'test':
          bot.sendMessage(chatId, 'Tost!');
          break
        case 'hola':
        case 'halo':
        case 'alo':
        case 'elo':
        case 'hello':
          bot.sendMessage(chatId, `Greetings ${msg.from.first_name} `);
          break
        default:
          bot.sendMessage(chatId, 'nani');
      }

    else
      validateUser(chatId, msg)
  }
})
