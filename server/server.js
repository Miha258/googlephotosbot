const express = require('express')
const app = express()
const path = require('path')
const procces = require('process')


const port = procces.env.PORT || 3000

app.set('view engine','ejs')
app.set('views',path.resolve(__dirname,'ejs'))

app.get('/',(req,res) => {
    const code = req.query.code
    res.render('code',{code: code})
})

app.listen(port,() => {
    console.log(port)
    console.log('Server started')
})
