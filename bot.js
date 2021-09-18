const TelegramBot = require('node-telegram-bot-api');
const config = require ('./config')
// replace the value below with the Telegram token you receive from @BotFather

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

// Matches "/echo [whatever]"
// bot.onText(/\/echo (.+)/, (msg, match) => {
//   // 'msg' is the received Message from Telegram
//   // 'match' is the result of executing the regexp above on the text content
//   // of the message

//   const chatId = msg.chat.id;
//   const resp = match[1]; // the captured "whatever"
//   // managed = true

//   // send back the matched "whatever" to the chat
//   bot.sendMessage(chatId, resp);
// });

// Listen for any kind of message. There are different kinds of
// messages.
bot.on('message', (msg) => {
  const chatId = msg.chat.id;

  console.log(`${msg.from.username} : ${msg.chat.id}`)

  if (msg.text.toLowerCase() === '/start') {
    bot.sendMessage(chatId, 'Beep Boop. 🤖');
  } else {

    if (sessions[chatId])
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
})
