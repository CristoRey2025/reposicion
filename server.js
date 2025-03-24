const express = require('express');
const session = require('express-session');
const authRoutes = require('./routes/auth');
require('dotenv').config();

const app = express();

app.use(express.json());
app.use(session({
    secret: 'mi_secreto',
    resave: false,
    saveUninitialized: true
}));

app.use('/auth', authRoutes);

app.listen(3000, () => {
    console.log('Servidor corriendo en http://localhost:3000');
});
