const API = 'http://54.224.174.10:5000/api/filmes';

async function carregarFilmes() {
    const res = await fetch(API);
    const dados = await res.json();
    const lista = document.getElementById('lista-filmes');
    lista.innerHTML = '';
    dados.forEach(filme => {
        const li = document.createElement('li');
        li.innerHTML = `${filme.titulo} (${filme.ano}) 
            <button onclick="remover(${filme.id})">Remover</button>`;
        lista.appendChild(li);
    });
}

async function adicionarFilme(evento) {
    evento.preventDefault();
    const titulo = document.getElementById('titulo').value;
    const ano = document.getElementById('ano').value;
    await fetch(API, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ titulo, ano })
    });
    evento.target.reset();
    carregarFilmes();
}

async function remover(id) {
    await fetch(`${API}/${id}`, { method: 'DELETE' });
    carregarFilmes();
}

document.getElementById('form').addEventListener('submit', adicionarFilme);
carregarFilmes();
