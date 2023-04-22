
let checking = new Boolean(false)
let observer = new MutationObserver(checkSong)
let heart, next, songName

setTimeout(() => {
    heart = document.getElementsByTagName('button')[5]
    next = document.getElementsByClassName('mnipjT4SLDMgwiDCEnRC')[0]
    songName = document.querySelectorAll('a')[33];
    //songName = document.getElementsByClassName('Q_174taY6n64ZGC3GsKj')[0]
    observer.observe(songName, {
        childList: true, // observe direct children
        subtree: true, // lower descendants too
        characterDataOldValue: true, // pass old data to callback)
        attributes: true,
        attributeOldValue: true,
        characterData: true,
        characterDataOldValue : true,  

    });
    if (heart.getAttribute('Aria-Label') === 'Remove from Your Library') {
        console.log('liked')
    }
    
}, 5200)


chrome.runtime.onMessage.addListener(
    function(request, sender, sendResponse) {
        if (request['state'] == 'ON') {
            checking = true
            console.log('on')
            checkSong()
        }
        else {
            console.log('off')
            checking = false
        }
    }
)


function checkSong() {
    console.log(checking, next)
    if (heart.getAttribute('Aria-Label') === 'Remove from Your Library' && checking === true) {
        next.click()
    }
}
