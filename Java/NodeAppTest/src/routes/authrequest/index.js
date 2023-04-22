const authRouter = require('express').Router()
require('dotenv').config({ path: `./.env`})


authRouter.get('/', (req, res) => {
    var scopes = 'user-read-playback-state' + '%20' +
    'user-modify-playback-state' + '%20'+
    'playlist-read-private' + '%20'+
    'user-read-currently-playing' + '%20' +
    'user-read-playback-position' + '%20' +
    'user-library-modify' + '%20' +
    'user-library-read' + '%20' +
    'playlist-modify-private' + '%20' +
    'playlist-modify-public' + '%20' +
    'user-top-read'
  
  
    spotifyURL = 'https://accounts.spotify.com/authorize?'
    
  
    requestURL = `${spotifyURL}client_id=${process.env.CLIENT_ID}&response_type=code&redirect_uri=${process.env.REDIRECT_URI}&scope=${scopes}`
  
    //console.log(requestURL)
  
    res.redirect(requestURL)
})

module.exports = authRouter
