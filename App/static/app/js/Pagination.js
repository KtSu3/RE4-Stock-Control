// scripts.js
document.addEventListener('DOMContentLoaded', () => {
    const data = generateDummyData(100); // Gerar 100 linhas de dados dummy
    const rowsPerPage = 10;
    let currentPage = 1;

    const tableBody = document.getElementById('table-body');
    const prevButton = document.getElementById('prev-button');
    const nextButton = document.getElementById('next-button');
    const pageInfo = document.getElementById('page-info');

    function generateDummyData(numRows) {
        const data = [];
        for (let i = 1; i <= numRows; i++) {
            data.push({ col1: `Dado ${i} - 1`, col2: `Dado ${i} - 2`, col3: `Dado ${i} - 3` });
        }
        return data;
    }

    function displayTable(data, page, rowsPerPage) {
        tableBody.innerHTML = '';
        const start = (page - 1) * rowsPerPage;
        const end = start + rowsPerPage;
        const paginatedData = data.slice(start, end);

        paginatedData.forEach(row => {
            const tr = document.createElement('tr');
            Object.values(row).forEach(cellData => {
                const td = document.createElement('td');
                td.textContent = cellData;
                tr.appendChild(td);
            });
            tableBody.appendChild(tr);
        });

        pageInfo.textContent = `Página ${page} de ${Math.ceil(data.length / rowsPerPage)}`;
    }

    function updatePaginationButtons(page, totalPages) {
        prevButton.disabled = page === 1;
        nextButton.disabled = page === totalPages;
    }

    prevButton.addEventListener('click', () => {
        if (currentPage > 1) {
            currentPage--;
            displayTable(data, currentPage, rowsPerPage);
            updatePaginationButtons(currentPage, Math.ceil(data.length / rowsPerPage));
        }
    });

    nextButton.addEventListener('click', () => {
        if (currentPage < Math.ceil(data.length / rowsPerPage)) {
            currentPage++;
            displayTable(data, currentPage, rowsPerPage);
            updatePaginationButtons(currentPage, Math.ceil(data.length / rowsPerPage));
        }
    });

    // Inicializar tabela e botões de paginação
    displayTable(data, currentPage, rowsPerPage);
    updatePaginationButtons(currentPage, Math.ceil(data.length / rowsPerPage));
});
