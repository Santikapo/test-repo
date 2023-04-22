const sr = require('../../../middlewares/sprequests')


module.exports = async function() {
    let content
    let temp = []
    let test = 0
    let offset = 0



    while (true) {
        tempurl = 'https://api.spotify.com/v1/me/top/tracks?time_range=long_term&limit=50&offset=' + offset
        console.log(tempurl)
        content = await sr.spreq('GET', tempurl)
        //console.log(content)
        console.log(content['total'])
        if (content['total'] == 0) {
            break
        }
        content = content['items']
        content.forEach(song => {
            var newsong = {}
            newsong['name'] = song['name']
            newsong['artist'] = song['artists'][0]['name']
            //console.log(newsong)
    
            temp.push(newsong)
    
        });
        offset +=50
        console.log(test++)
    }
  

    return temp
}