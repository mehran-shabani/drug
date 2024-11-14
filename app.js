const apiBaseUrl = "http://127.0.0.1:8000/api/drugs";  // آدرس API خود را تنظیم کنید

// تابع جستجوی داروها
function searchDrugs() {
    const query = document.getElementById('searchInput').value;
    const resultsList = document.getElementById('results');
    resultsList.innerHTML = ''; // پاک کردن نتایج قبلی
    const loadingElement = document.getElementById('loading');
    
    // نمایش loading
    loadingElement.style.display = 'block';

    fetch(`${apiBaseUrl}/search/?q=${query}`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        },
        credentials: 'include'  // اضافه کردن credentials برای ارسال کوکی‌ها (در صورت نیاز)
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();  // تبدیل پاسخ به JSON
    })
    .then(data => {
        // پنهان کردن loading
        loadingElement.style.display = 'none';

        if (Array.isArray(data.results)) {
            data.results.forEach(drug => {
                const li = document.createElement('li');
                li.textContent = `${drug.generic_name_eng} (${drug.drug_dose})`;
                // هدایت به صفحه جدید با ID دارو
                li.onclick = () => window.location.href = `drug-details.html?id=${drug.id}`;
                resultsList.appendChild(li);
            });
        } else {
            resultsList.innerHTML = '<li>No results found</li>';
        }
    })
    .catch(error => {
        console.error('Fetch error:', error);
        loadingElement.style.display = 'none';
        resultsList.innerHTML = '<li>Error fetching results</li>';
    });
}

