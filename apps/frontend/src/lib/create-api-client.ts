export default function createAPIClient(apiVersion: string) {
    if (!apiVersion)
        return null
    const API_BASE_URL = process.env.API_BASE_URL;

    return {
        async fetch(url: string, options : RequestInit = {}) {
            const res = await fetch(`${API_BASE_URL}/api/${apiVersion}/${url}`, options);
            return res.json()
        }
    };
}
