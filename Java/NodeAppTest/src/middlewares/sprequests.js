const http = require('http')
const bp = require('body-parser')
const { URL } = require('url')
const { url } = require('inspector')

let code, auth_string, auth


// creates request to Spotify API
async function spreq(method, url, auth=null, data=null) {


    let info

    switch(method) {
      case 'GET':
        return await fetch(url, {
          method: method,
          headers: {
            "Authorization" : "Bearer " + token,
            "Content-Type" : "application/json"
          }
        })
        .then((response) => response.json())
        .then((json) => info = json);

        break
      case 'POST':
        return await fetch(url, {
          method: method,
          body: data,
          headers: {
            "Authorization" : "Basic " + auth,
            "Content-Type" : "application/x-www-form-urlencoded"
          }
        })
        .then((response) => response.json())
        .then((json) => info = json);

        break

      default:
        throw new Error('idiot')
    }
}

/*
class Spotifyrequest {
    constructor(method, url, gheaders, data) {
        this.method = method
        this.url = url
        this.headers = new Headers().append.gheaders
        this.data = data
    }

    send() {

        const info = {
            method: this.method,
            headers: this.headers,
            mode: 'cors',
            cache: 'default'
        }

        const myRequest = new Request('test', info)
        console.log(myRequest)
    }
}
*/

exports.spreq = spreq