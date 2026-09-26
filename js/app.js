let stokIkanCache = [];

async function apiJson(url, options = {}) {
    const response = await fetch(url, {
        credentials: "same-origin",
        cache: "no-store",
        ...options
    });

    const data = await response.json().catch(() => ({}));

    if (!response.ok) {
        throw new Error(
            data.error ||
            data.message ||
            `HTTP ${response.status}`
        );
    }

    return data;
}

async function initStorage() {
    try {
        stokIkanCache = await apiJson("/api/ikan");
        return stokIkanCache;
    } catch (error) {
        console.error("Gagal mengambil data ikan:", error);
        return [];
    }
}

function getData(key) {
    if (key === "stok_ikan") {
        return stokIkanCache;
    }

    return [];
}

async function saveData(key, data) {
    if (key !== "stok_ikan") {
        throw new Error(
            "Data harus disimpan melalui API server."
        );
    }

    stokIkanCache = await apiJson(
        "/api/ikan",
        {
            method: "PUT",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data)
        }
    );

    return stokIkanCache;
}

function formatRupiah(number) {
    return new Intl.NumberFormat(
        "id-ID",
        {
            style: "currency",
            currency: "IDR",
            maximumFractionDigits: 0
        }
    ).format(Number(number) || 0);
}

async function deleteFish(id) {
    if (!confirm("Yakin ingin menghapus data ikan ini?")) {
        return false;
    }

    try {
        await apiJson(
            `/api/ikan/${encodeURIComponent(id)}`,
            {
                method: "DELETE"
            }
        );

        stokIkanCache =
            stokIkanCache.filter(
                item => item.id !== id
            );

        if (typeof renderTable === "function") {
            renderTable();
        }

        return true;
    } catch (error) {
        console.error("Gagal menghapus ikan:", error);
        alert(error.message);
        return false;
    }
}

document.addEventListener(
    "DOMContentLoaded",
    async () => {
        await initStorage();

        if (typeof renderTable === "function") {
            renderTable();
        }
    }
);
