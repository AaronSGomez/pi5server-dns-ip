// index.js (Corre en Vercel)
// Lee el archivo ip.txt directamente desde la URL RAW de GitHub (solución robusta).

// Necesita la librería 'node-fetch' para hacer peticiones HTTP.
const fetch = require('node-fetch');

// URL RAW de tu archivo ip.txt en GitHub. 
// ¡Asegúrate de que la URL sea la tuya, con tu usuario y repo!
const GITHUB_RAW_IP_URL = "https://raw.githubusercontent.com/AaronSgomez/pi5server-dns-ip/main/ip.txt";

module.exports = async (req, res) => {
    try {
        // 1. Petición HTTP directa a GitHub para obtener el contenido del archivo ip.txt
        const response = await fetch(GITHUB_RAW_IP_URL);
        
        if (!response.ok) {
            res.statusCode = 500;
            res.end(`Error: No se pudo obtener la IP de GitHub. Código: ${response.status}`);
            return;
        }

        const ip = (await response.text()).trim();
        
        // 2. Construye la URL de destino
        const protocol = 'http'; 
        const port = 80; // Puerto HTTP. Si quieres acceder a tu BBDD, usarás un puerto diferente en Java.

        // Mantiene la ruta original (ej. /dashboard)
        const destination = `${protocol}://${ip}:${port}${req.url}`;
        
        // 3. Redirección
        res.writeHead(302, {
            'Location': destination
        });
        res.end();

    } catch (error) {
        res.statusCode = 500;
        res.end(`Internal Server Error: ${error.message}`);
    }
};