document.addEventListener('DOMContentLoaded', function() {
    // === DATA ITEM ===
    const items = {
        pakaian: 0,
        cd: 0,
        bh: 0,
        kaoskaki: 0,
        lainnya: 0
    };

    // === STEppER LOGIC ===
    document.querySelectorAll('.stepper').forEach(stepper => {
        const minus = stepper.querySelector('.minus');
        const plus = stepper.querySelector('.plus');
        const valueEl = stepper.querySelector('.stepper-value');
        const field = stepper.closest('.item-row').dataset.field;

        minus.addEventListener('click', () => {
            if (items[field] > 0) {
                items[field]--;
                valueEl.textContent = items[field];
                updateTotal();
            }
        });

        plus.addEventListener('click', () => {
            items[field]++;
            valueEl.textContent = items[field];
            updateTotal();
        });
    });

    function updateTotal() {
        const total = Object.values(items).reduce((a, b) => a + b, 0);
        document.getElementById('total-display').textContent = total;
    }

    // === KIRIM KE BOT ===
    document.getElementById('submitBtn').addEventListener('click', function() {
        const nama = document.getElementById('nama').value.trim();
        const nota = document.getElementById('nota').value.trim();
        const statusMsg = document.getElementById('statusMessage');

        if (!nama || !nota) {
            statusMsg.className = 'error';
            statusMsg.textContent = '❌ Nama dan No. Nota wajib diisi!';
            return;
        }

        const totalItem = Object.values(items).reduce((a, b) => a + b, 0);
        if (totalItem === 0) {
            statusMsg.className = 'error';
            statusMsg.textContent = '❌ Minimal 1 item!';
            return;
        }

        // Format data
        const data = {
            action: 'print_struk',
            nama: nama,
            nota: nota,
            items: {
                pakaian: items.pakaian,
                cd: items.cd,
                bh: items.bh,
                kaoskaki: items.kaoskaki,
                lainnya: items.lainnya
            },
            total: totalItem
        };

        // Kirim ke Telegram WebApp
        if (window.Telegram && window.Telegram.WebApp) {
            window.Telegram.WebApp.sendData(JSON.stringify(data));
            statusMsg.className = 'success';
            statusMsg.textContent = '✅ Data terkirim! Cetak struk...';
        } else {
            // Fallback: tampilkan JSON (testing di browser biasa)
            statusMsg.className = 'success';
            statusMsg.innerHTML = '✅ Mode testing:
 0 ';
            console.log('DATA STRUK:', data);
        }
    });
});