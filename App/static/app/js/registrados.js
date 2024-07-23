function moverEquipamentosSelecionados() {
    const checkboxes = document.querySelectorAll('.equipamento-checkbox:checked');
    const tabelaEdicao = document.getElementById('equipamentos-editar-table');
    checkboxes.forEach(checkbox => {
        const row = checkbox.closest('tr');
        tabelaEdicao.querySelector('tbody').appendChild(row.cloneNode(true));
        row.remove();
    });
}


document.getElementById('editar-selecionados-btn').addEventListener('click', function() {
    moverEquipamentosSelecionados();
    
    window.location.href = "{% url 'outra_pagina' %}";
});


document.querySelectorAll('.mudar-status-btn').forEach(function(button) {
    button.addEventListener('click', function() {
        const equipamentoId = button.getAttribute('data-id');
        const confirmation = confirm('Deseja mudar o status do equipamento para Testar?');
        if (confirmation) {
           
            window.location.href = `/mudar_status/?equipamento_id=${equipamentoId}`;
        }
    });
});



