// index.js (Corre en Vercel)
// Esta versión usa la función 'fetch' nativa de Node.js (Node 22.x)
// y elimina la dependencia 'node-fetch' para evitar errores 500.

// La función 'fetch' ahora es global en Node 22, no necesitamos importarla.
const GITHUB_RAW_IP_URL = "https://raw.githubusercontent.com/AaronSgomez/pi5server-dns-ip/main/ip.txt";

// La función principal debe ser 'async' y usar 'export default'
export default async function (req, res) {
    try {
        // 1. Petición HTTP directa a GitHub para obtener el contenido del archivo ip.txt
        // Usa la función global 'fetch'
        const response = await fetch(GITHUB_RAW_IP_URL);
        
        if (!response.ok) {
            res.statusCode = 500;
            res.end(`Error: No se pudo obtener la IP de GitHub. Código: ${response.status} (Revisar logs de GitHub)`);
            return;
        }

        const ip = (await response.text()).trim();
        
        // 2. Construye la URL de destino
        const protocol = 'http'; 
        const port = 80; // Puerto HTTP estándar

        // Mantiene la ruta original (ej. /dashboard)
        const destination = `${protocol}://${ip}:${port}${req.url}`;
        
        // 3. Redirección 302
        res.writeHead(302, {
            'Location': destination
        });
        res.end();

    } catch (error) {
        // Muestra el error de la función
        res.statusCode = 500;
        res.end(`Internal Server Error: ${error.message}`);
    }
};