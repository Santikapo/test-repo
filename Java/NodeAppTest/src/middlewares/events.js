const events = require('events')
const myEmitter = new events.EventEmitter()

let token = undefined



// Detects new Auth
myEmitter.on('newToken', (newToken) => {
    token = newToken
})

function test() {
    myEmitter.emit('newToken', 1234)
    return
}


exports.emmiter = myEmitter