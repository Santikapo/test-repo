// libraries
const http = require('http');
const express = require('express')
const mysql = require('mysql')
const bp = require('body-parser')
const bcrypt = require('bcrypt');
const { response } = require('express');
const { resolve } = require('path');
const { json } = require('body-parser');
const { URLSearchParams } = require('url');
const { error } = require('console');
const events = require('events')
require('dotenv').config({ path: `./.env`})

global.token = undefined



// create express app
const app = express()
const port = process.env.PORT || 3001
app.listen(port) // listen to HTTP requests on port
console.log('server: http://127.0.0.1:' + port)
app.use(express.static('public'))
app.use(express.urlencoded( {extended: false}))



// Set up routes
require('./src/routes')(app);


// connecting to database
const db = mysql.createConnection({
  host: process.env.DATABASE_HOST,
  user: process.env.DATABASE_USER,
  password: process.env.DATABASE_PASSWORD,
  database: process.env.DATABASE,
})

// register view engine
app.set('view engine', 'ejs')



/*

// login attempt
app.post('/login', (req, res) => {

  let body = req.body


  let myPromise = new Promise(function(myResolve, myReject) {
    db.query('SELECT password FROM users where email="' + body.email + '";', (err, result) => {
      if (result[0]) {
        //console.log(result[0]['password'], body.psw)
        if (result[0]['password'] == body.psw) {
          myResolve()
        }
        else {
          myReject()
        }
      }
      else {
        myReject()
      }
      
    })
  })

  myPromise.then(
    () => {
      console.log('success')
      res.send('success')
    },
    () => {
      console.log('noooo')
      res.render('login', {title: 'login', fail: true})
    }
  )
})

app.get('/register', (req, res) => {
  res.render('register', {title: 'register', exists: false})
})

app.post('/register', async (req, res) => {

  let body = req.body

  const hashedPassword = await bcrypt.hash(body.psw, 10)
  //console.log(hashedPassword)

  let query = `INSERT INTO users (email, password) VALUES ('${body.email}', '${hashedPassword}');`

  queryPromise = () => {
    return new Promise((resolve, reject) => {
      db.query(query, (err, result) => {
        if (err) {
          return reject(err)
        }
        return resolve(result)
      })
    })
  }


  try {
    const queryResponse = await queryPromise()

    res.redirect('/login')
    
  } catch {
    res.render('register', {title: 'register', exists: true})
  }
})


app.get('/actions', (req, res) => {
  res.render('actions', {title: 'actions', content: null})
})

*/

function isValid(body) {
  db.query('SELECT password FROM users where username="' + body.uname + '";', (err, result) => {
    if (result[0]) {
      if (result[0]['password'] == body.psw) {
        return true;
      }
    }
  })
}


// adding user to database
async function addUser(email, password) {

  let query = `INSERT INTO users (email, password) VALUES ('${email}', '${password}');`

  // checking if user email is already registered
  db.query(query, (err, result) => {
    console.log(result) 
    if (result) {
      console.log('yo1')
      return 'test'      
    }
  })
}