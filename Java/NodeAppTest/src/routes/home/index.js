const homeRouter = require('express').Router();


// Middleware that is specific to this router
homeRouter.use((req, res, next) => {
    next()
})

// Current Route
homeRouter.get('/', (req, res) => {
    res.render('index', {title: 'Home', test: 'yo'});
})

// About
homeRouter.get('/me', (req, res) => {
    res.send('/home/me')
    //res.render('register', {title: 'register', exists: false});
})


module.exports = homeRouter;