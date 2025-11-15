// api/index.js
const GITHUB_RAW_IP_URL = "https://raw.githubusercontent.com/AaronSgomez/pi5server-dns-ip/main/ip.txt";

export default async function handler(req, res) {
    try {
        const response = await fetch(GITHUB_RAW_IP_URL);

        if (!response.ok) {
            res.status(500).send(`Error: No se pudo obtener la IP de GitHub. Código: ${response.status}`);
            return;
        }

        const ip = (await response.text()).trim();

        const protocol = "http";
        const port = 80;
        const destination = `${protocol}://${ip}:${port}${req.url}`;

        res.writeHead(302, { Location: destination });
        res.end();
    } catch (error) {
        res.status(500).send(`Internal Server Error: ${error.message}`);
    }
}
