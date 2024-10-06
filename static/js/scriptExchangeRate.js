fetch('https://api.nbrb.by/exrates/rates?periodicity=0')
  .then(response => {
    if (!response.ok) {
      throw new Error('Network response was not ok');
    }
    return response.json();
  })
  .then(data => {
    const tableBody = document.querySelector('#currencyTable tbody');
    data.forEach(rate => {
      const tr = document.createElement('tr');
      const tdName = document.createElement('td');
      const tdRate = document.createElement('td');
      tdName.textContent = `${rate.Cur_Scale} ${rate.Cur_Name}`; // Используйте обратные кавычки
      tdRate.textContent = rate.Cur_OfficialRate;
      tr.appendChild(tdName);
      tr.appendChild(tdRate);
      tableBody.appendChild(tr);
    });
  })
  .catch(error => console.error('Error loading currency data:', error));