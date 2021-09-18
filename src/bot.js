const TelegramBot = require('node-telegram-bot-api');
const config = require ('./config')
const YTSModule = require('./yts')

const areWeDebugging = config.debug

// Create a bot that uses 'polling' to fetch new updates
const bot = new TelegramBot(config.token, {polling: true});


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
    bot.sendMessage(chatId, "Speak 'friend' and enter");
  } else if (msg.text === pass) {
    logginIn[chatId] = false
    bot.sendMessage(chatId, 'Welcome to Khazad-dûm, how can I serve you?');
    sessions[chatId] = true
    setTimeout(()=>{
      sessions[chatId] = false
    }, config.sessionDuration)
  } else {
    bot.sendMessage(chatId,'_Mellon_ worked for Gandalf...')
  }

}

// Matches "/Search [whatever]"
bot.onText(/\/Search (.+)/i, (msg, match) => {
  console.log('gonxas search', msg)
  // 'msg' is the received Message from Telegram
  // 'match' is the result of executing the regexp above on the text content
  // of the message

  const chatId = msg.chat.id;
  const query = match[1]; // the captured "whatever"
  YTSModule.search(query).then(movies =>{
    console.log(movies)
    if (movies.length === 0) {
      bot.sendMessage(chatId, "Ain't Nobody Here but Us Chickens");  
    } else {
      console.log('movies', movies)
    }
  }).catch(() =>{
    bot.sendMessage(chatId, 'Appologies, there was an error looking for your movie');
  })
  // managed = true

  // send back the matched "whatever" to the chat
  // bot.sendMessage(chatId, resp);
});

// Listen for any kind of message. There are different kinds of
// messages.
bot.on('message', (msg) => {
  let command = false
  msg.entities.map(entitie =>{
    if (entitie.type === 'bot_command')
      command = true
  }) 

  if (!command) {

  console.log('gonxas message', msg)
  const chatId = msg.chat.id;

  console.log(`${msg.from.username} : ${msg.chat.id}`)

  if (msg.text.toLowerCase() === '/start') {
    bot.sendMessage(chatId, 'Beep Boop. 🤖');
  } else {

    if (areWeDebugging || sessions[chatId])
      // send a message to the chat acknowledging receipt of their message
      switch(msg.text.toLowerCase()) {
        case 'brainz':
          bot.sendMessage(chatId, '🧟');
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
          bot.sendMessage(chatId, `Greetings ${msg.from.first_name}`);
          break
        default:
          bot.sendMessage(chatId, 'nani');
      }
    
    else
      validateUser(chatId, msg)
  }
}
})
