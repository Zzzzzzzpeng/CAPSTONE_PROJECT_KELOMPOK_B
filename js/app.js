let stokIkanCache = [];

async function initStorage() {
    try {
        stokIkanCache = await apiJson("/api/ikan");
        return stokIkanCache;
    } catch (error) {
        console.error(error);
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

async function deleteFish(id) {
    const fish = stokIkanCache.find(
        item => Number(item.id) === Number(id)
    );

    const name = fish?.nama || "ikan ini";

    if (!confirm(`Hapus ${name}? Data yang sudah memiliki histori tidak dapat dihapus.`)) {
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
                item => Number(item.id) !== Number(id)
            );

        if (typeof renderTable === "function") {
            renderTable();
        }

        showToast(
            `${name} berhasil dihapus.`,
            "success"
        );

        return true;
    } catch (error) {
        showToast(
            error.message,
            "error"
        );

        return false;
    }
}
