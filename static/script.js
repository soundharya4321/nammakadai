// Open a modal
function openModal(modalId) {
    document.getElementById(modalId).style.display = 'flex';
}

// Close a modal
function closeModal(modalId) {
    document.getElementById(modalId).style.display = 'none';
}

// Fetch data and populate modal content
function fetchData(endpoint, modalId) {
    fetch(endpoint)
        .then(response => response.json())
        .then(data => {
            const contentDiv = document.getElementById(`${modalId}Content`);
            contentDiv.innerHTML = '<pre>' + JSON.stringify(data, null, 2) + '</pre>';
            openModal(modalId);
        })
        .catch(err => console.error('Error fetching data:', err));
}

// Add item form submission
document.getElementById('add-item-form').addEventListener('submit', function (e) {
    e.preventDefault();
    
    const itemName = document.getElementById('item-name').value;
    const itemPrice = parseFloat(document.getElementById('item-price').value);
    const itemQuantity = parseInt(document.getElementById('item-quantity').value, 10);

    const payload = {
        item_name: itemName,
        price: itemPrice,
        quantity: itemQuantity
    };

    fetch('/items', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
    })
        .then(response => response.json())
        .then(data => {
            alert(data.message);
            fetchItems(); // Refresh items after adding
            document.getElementById('add-item-form').reset();
        })
        .catch(err => console.error('Error adding item:', err));
});

// Fetch and display items
function fetchItems() {
    fetch('/items')
        .then(response => response.json())
        .then(items => {
            const itemsList = document.getElementById('items-list');
            itemsList.innerHTML = ''; // Clear existing items
            items.forEach(item => {
                const itemDiv = document.createElement('div');
                itemDiv.textContent = `ID: ${item.item_id}, Name: ${item.item_name}, Quantity: ${item.quantity}, Price: ${item.price}`;
                itemsList.appendChild(itemDiv);
            });
        })
        .catch(err => console.error('Error fetching items:', err));
}

// Record purchase form submission
document.getElementById('purchase-form').addEventListener('submit', function (e) {
    e.preventDefault();

    const purchaseItemId = parseInt(document.getElementById('purchase-item-id').value, 10);
    const purchaseRate = parseFloat(document.getElementById('purchase-rate').value);
    const purchaseQty = parseInt(document.getElementById('purchase-qty').value, 10);

    const payload = {
        item_id: purchaseItemId,
        rate: purchaseRate,
        qty: purchaseQty
    };

    fetch('/purchase', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
    })
        .then(response => response.json())
        .then(data => {
            alert(data.message);
            fetchItems(); // Refresh items after purchase
            document.getElementById('purchase-form').reset();
        })
        .catch(err => console.error('Error recording purchase:', err));
});

// Record sale form submission
document.getElementById('sales-form').addEventListener('submit', function (e) {
    e.preventDefault();

    const saleItemId = parseInt(document.getElementById('sale-item-id').value, 10);
    const saleRate = parseFloat(document.getElementById('sale-rate').value);
    const saleQty = parseInt(document.getElementById('sale-qty').value, 10);

    const payload = {
        item_id: saleItemId,
        rate: saleRate,
        qty: saleQty
    };

    fetch('/sales', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
    })
        .then(response => response.json())
        .then(data => {
            alert(data.message);
            fetchItems(); // Refresh items after sale
            document.getElementById('sales-form').reset();
        })
        .catch(err => console.error('Error recording sale:', err));
});

// Fetch report data
function fetchReport() {
    fetch('/report')
        .then(response => response.json())
        .then(reportData => {
            const reportDiv = document.getElementById('report-data');
            reportDiv.innerHTML = ''; // Clear existing report
            reportData.forEach(entry => {
                const reportItem = document.createElement('div');
                reportItem.textContent = `${entry.description}: ${entry.value}`;
                reportDiv.appendChild(reportItem);
            });
        })
        .catch(err => console.error('Error fetching report:', err));
}

// Initial fetch of items on page load
document.addEventListener('DOMContentLoaded', fetchItems);
