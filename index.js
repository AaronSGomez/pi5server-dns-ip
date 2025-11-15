// index.js (Corre en Vercel)
// Lee el archivo ip.txt (que está en el mismo proyecto) y redirige a la IP de tu RPi.

const fs = require('fs');
const path = require('path');

module.exports = (req, res) => {
    try {
        // Lee el archivo ip.txt. Vercel lo incluye durante el deployment.
        const ipFilePath = path.join(__dirname, 'ip.txt');
        const ip = fs.readFileSync(ipFilePath, 'utf8').trim();
        
        if (!ip) {
            res.statusCode = 500;
            res.end('Error: La IP no se pudo leer del archivo ip.txt.');
            return;
        }

        // Construye la URL de destino usando la IP y manteniendo la ruta
        // Usamos HTTP por defecto para que funcione sin un certificado SSL en el router.
        const protocol = 'http'; 
        const port = 80; // Puerto HTTP estándar. Si usas uno diferente, cámbialo aquí.
                         // Si quieres acceder a tu BBDD, usarás un puerto diferente!

        // Mantiene la ruta original (ej. /dashboard)
        const destination = `${protocol}://${ip}:${port}${req.url}`;
        
        // Redirección 302 (Temporalmente Encontrado). Esto es lo que expone la IP 
        // a tu navegador, pero te lleva a tu casa.
        res.writeHead(302, {
            'Location': destination
        });
        res.end();

    } catch (error) {
        res.statusCode = 500;
        res.end(`Internal Server Error: ${error.message}`);
    }
};