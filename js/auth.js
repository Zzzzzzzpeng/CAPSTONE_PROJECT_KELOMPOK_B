async function checkAuth() {
    try {
        const response = await fetch("/api/auth/me", {
            method: "GET",
            credentials: "same-origin",
            cache: "no-store"
        });

        if (!response.ok) {
            window.location.replace("/");
            return false;
        }

        const data = await response.json();

        if (!data.authenticated) {
            window.location.replace("/");
            return false;
        }

        return true;
    } catch (error) {
        console.error("Authentication check failed:", error);
        window.location.replace("/");
        return false;
    }
}

async function logout() {
    try {
        await fetch("/api/auth/logout", {
            method: "POST",
            credentials: "same-origin"
        });
    } finally {
        window.location.replace("/");
    }
}

checkAuth();
