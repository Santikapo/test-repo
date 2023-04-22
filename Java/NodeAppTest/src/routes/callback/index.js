const callRouter = require('express').Router()
require('dotenv').config({ path: `./.env`})
const events = require('events')
const sr = require('../../middlewares/sprequests');




const headers = {
    "Authorization" : null,
    "Content-Type" : "application/x-www-form-urlencoded"
  }

callRouter.get('/', async (req, res) => {


    code = req.query.code
    auth_string = process.env.CLIENT_ID + ":" + process.env.CLIENT_SECRET
    auth = Buffer.from(auth_string).toString('base64')
  
    headers["Authorization"] = "Basic " + auth
  
    var data = new URLSearchParams()
    data.append("grant_type", "authorization_code");
    data.append("code", code)
    data.append("redirect_uri", process.env.REDIRECT_URI)
  
    token = (await sr.spreq('POST', 'https://accounts.spotify.com/api/token', auth, data)).access_token
    
    
    

    res.render('callback', {title : 'actions'})
    
  })



module.exports = callRouter