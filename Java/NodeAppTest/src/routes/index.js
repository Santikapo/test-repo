module.exports = function(app) {
    app.use('/', require('./home'))
    app.use('/home', require('./home'))
    app.use('/auth', require('./authrequest'))
    app.use('/callback', require('./callback'))
    app.use('/actions', require('./actions'))
}
