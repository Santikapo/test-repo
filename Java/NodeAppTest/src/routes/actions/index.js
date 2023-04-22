const actRouter = require('express').Router();
const token = require('../../middlewares/events').token


// Current Route
actRouter.get('/', (req, res) => {
    res.send('hey')
    //res.render('index', {title: 'Home', test: 'yo'});
})

// Middleware that is specific to this router
actRouter.use((req, res, next) => {
    next()
})


// Route to results
actRouter.get('/top', async (req, res) => {
    res.render('info', {title: 'Top Songs', content: await require('./top')()})
})


module.exports = actRouter;