const express = require('express');
const router = express.Router();
const User = require('../models/User');
const bcrypt = require('bcryptjs');

router.post('/register', async (req, res) => {
    const { username, password } = req.body;
    try {
        await User.createUser(username, password);
        res.json({ message: 'Usuario registrado' });
    } catch (err) {
        res.status(500).json({ error: 'Error registrando usuario' });
    }
});

router.post('/login', async (req, res) => {
    const { username, password } = req.body;
    try {
        const user = await User.findUser(username);
        if (!user) return res.status(400).json({ error: 'Usuario no encontrado' });

        const isMatch = await bcrypt.compare(password, user.password);
        if (!isMatch) return res.status(400).json({ error: 'Contraseña incorrecta' });

        req.session.user = user;
        res.json({ message: 'Inicio de sesión exitoso' });
    } catch (err) {
        res.status(500).json({ error: 'Error en el inicio de sesión' });
    }
});

module.exports = router;
