const TelegramBot = require('node-telegram-bot-api');
const config = require('./config')
const YTSModule = require('./yts')
const Aria2Module = require('./aria2')
const utils = require('./utils')

const areWeDebugging = config.debug

utils.shortenLink('http://www.gonxas.com')

// Create a bot that uses 'polling' to fetch new updates
const bot = new TelegramBot(config.token, { polling: true });


const logginIn = {}
const sessions = {}
const searchingMovie = {}

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
  return { text: `${torrent.quality} ${size}`, callback_data: torrent.shortLink }
}

const summaryButton = (movieId) => {
  return [{ text: 'Full Summary', callback_data: `SUM: ${movieId}` }]
}

const siteButton = (movieData) => {
  return [{ text: 'Open Site', url: movieData.url }]
}

const searchMovie = (chatId, query) => {
  YTSModule.search(query).then(movies => {
    if (!movies || movies.length === 0) {
      bot.sendMessage(chatId, "Ain't Nobody Here but Us Chickens");
    } else {
      const buttons = []
      movies.map(movie => {
        movie.chatId = chatId
        buttons.push(movieButton(movie))
      })
      bot.sendMessage(chatId, 'This is what I found for you 👀', { reply_markup: { inline_keyboard: buttons } });
    }
  }).catch(() => {
    bot.sendMessage(chatId, 'Well this is embarrassing...');
  })
}

const userSelectedMovie = (chatId, movieId) => {
  YTSModule.getMovieDetails(movieId).then(movieData => {
    let tempArray = []
    const buttons = []
    const promises = []

    const torrents = movieData.torrents

    torrents.map(torrent => {
      const p = utils.shortenLink(torrent.url).then((shortLink) => {
        torrent.shortLink = shortLink
      }).catch(() => {
        bot.sendMessage(chatId, 'Well this is embarrassing...');
      })
      promises.push(p)
    })

    Promise.all(promises).then(() => {
      torrents.map(torrent => {
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
    }).catch(error => {
      console.error('Error awaiting short urls, ', error)
      bot.sendMessage(chatId, 'Well this is embarrassing....');
    })
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

const downloadYTSMovie = (chatId, url) => {
  Aria2Module.downlaodTorrent(bot, chatId, url)
}

// Button's Handler
bot.on('callback_query', function onCallbackQuery(button) {

  const data = button.data

  if (data.indexOf('movie: ') !== -1) {
    userSelectedMovie(button.from.id, data.replace('movie: ', ''))
  } else if (data.indexOf('SUM: ') !== -1) {
    displaySummary(button.from.id, data.replace('SUM: ', ''))
  } else {
    downloadYTSMovie(button.from.id, 'https://bit.ly/' + data)
  }

})





//--------- COMMAND METHODS

bot.onText(/\/Start/i, (msg) => {
  const chatId = msg.chat.id;
  bot.sendMessage(chatId, 'Beep Boop. 🤖')
});

bot.onText(/\/Stop/i, (msg) => {
  const chatId = msg.chat.id;
  bot.sendMessage(chatId, "Don't stop me now")
  setTimeout(() => {
    bot.sendMessage(chatId, "'Cause I'm having a good time")
  }, 1000)
  setTimeout(() => {
    bot.sendMessage(chatId, "Don't stop me now")
  }, 2000)
  setTimeout(() => {
    bot.sendMessage(chatId, "Yes I'm havin' a good time\nI don't want to stop at all.")
  }, 3000)

});

// Matches "/Search [whatever]"
bot.onText(/\/Search(.*)/i, (msg, match) => {
  // 'msg' is the received Message from Telegram
  // 'match' is the result of executing the regexp above on the text content
  // of the message

  const chatId = msg.chat.id;

  if (areWeDebugging || sessions[chatId]) {

    const query = match[1].trim() // the captured "whatever"

    if (query)
      searchMovie(chatId, query)
    else {
      bot.sendMessage(chatId, 'What are we looking for?');
      searchingMovie[chatId] = true
    }



  } else {
    validateUser(chatId, msg)
  }
});

//--------- 


// Listen for any kind of message. There are different kinds of
// messages.
bot.on('message', (msg) => {

  const chatId = msg.chat.id;

  if (searchingMovie[chatId]) {
    searchingMovie[chatId] = false
    searchMovie(chatId, msg.text)
    return
  }

  let command = false
  msg.entities?.map(entitie => {
    if (entitie.type === 'bot_command')
      command = true
  })

  //commands will be captured in their own methods. Here's pure talk.
  if (!command) {

    // console.log(`${ msg.from.username } : ${ msg.chat.id } `)

    if (areWeDebugging || sessions[chatId]) {
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

    } else
      validateUser(chatId, msg)
  }
})
