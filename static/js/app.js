// Fungsi bantu format durasi (dalam menit) ke jam:menit
function formatDurasi(minutes) {
    if (!minutes) return "0j 0m";
    const jam = Math.floor(minutes / 60);
    const menit = minutes % 60;
    return `${jam}j ${menit}m`;
}


// Fungsi bantu format angka ke Rupiah
function formatRupiah(angka) {
    return 'Rp ' + angka.toLocaleString('id-ID');
}

function loadData() {
    fetch('/api/transaksi')
        .then(res => res.json())
        .then(data => {

            // --- TABEL CHECK-IN ---
            const inTable = document.getElementById('checkin');
            inTable.innerHTML = '';
            data.checkin.forEach(d => {
                inTable.innerHTML += `
                <tr>
                    <td>${d.card_id}</td>
                    <td>${d.checkin_time}</td>
                </tr>`;
            });

            // --- TABEL CHECK-OUT ---
            const outTable = document.getElementById('checkout');
            outTable.innerHTML = '';
            data.checkout.forEach(d => {
                outTable.innerHTML += `
                <tr>
                    <td>${d.card_id}</td>
                    <td>${formatRupiah(d.fee)}</td>
                    <td>${formatDurasi(d.duration)}</td>
                    <td>
                        <button class="btn btn-success"
                            onclick="bukaPalang(${d.id})">
                            Buka Palang
                        </button>
                    </td>
                </tr>`;
            });

            // --- TABEL LOG ---
            const logTable = document.getElementById('log');
            logTable.innerHTML = '';
            data.log.forEach(d => {
                logTable.innerHTML += `
        <tr>
            <td>${d.card_id}</td>
            <td>${formatDurasi(d.duration)}</td>
            <td>${formatRupiah(d.fee)}</td>
        </tr>`;
            });

        })
        .catch(err => console.error('Gagal load data:', err));
}

function bukaPalang(id) {
    if (!confirm("Yakin buka palang? Pembayaran sudah diterima?")) return;

    fetch(`/buka/${id}`)
        .then(() => {
            alert("Palang dibuka");
            loadData();
        });
}

// Auto refresh tiap 5 detik
setInterval(loadData, 5000);
window.onload = loadData;
