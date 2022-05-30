const express = require('express')
const app = express()
const path = require('path')
const ConfigParser = require('configparser')

const config = new ConfigParser()
config.read(path.resolve(__dirname,'server.config'))
const host = config.get('serverconfig','HOST')
const port = config.get('serverconfig','PORT')
console.log(`http://${host}:${port}`)

app.set('view engine','ejs')
app.set('views',path.resolve(__dirname,'ejs'))

app.get('/',(req,res) => {
    const code = req.query.code
    res.render('code',{code: code})
})


app.listen(port,() => {
    console.log('Server started')
})