/**
 * Busca simples para a página Vidas Abertas
 * Filtra os cards de artigos pelo título conforme o usuário digita
 */
document.addEventListener('DOMContentLoaded', function() {
  const campoBusca = document.getElementById('campoBusca');
  const grade = document.getElementById('gradeArtigos');
  const contador = document.getElementById('contadorResultados');

  if (!campoBusca || !grade) return;

  const cards = Array.from(grade.querySelectorAll('.vidas-abertas-card'));
  const totalArtigos = cards.length;

  // Atualiza o contador
  function atualizarContador(visiveis) {
    if (!contador) return;
    if (visiveis === totalArtigos) {
      contador.textContent = totalArtigos + ' artigos no arquivo';
    } else {
      contador.textContent = visiveis + ' de ' + totalArtigos + ' artigos encontrados';
    }
  }

  // Exibe contagem inicial
  atualizarContador(totalArtigos);

  // Filtra conforme digita
  campoBusca.addEventListener('input', function() {
    var termo = this.value.toLowerCase().trim();

    // Remove acentos para busca mais flexível
    var termoNormalizado = termo.normalize('NFD').replace(/[\u0300-\u036f]/g, '');

    var visiveis = 0;

    cards.forEach(function(card) {
      var titulo = card.getAttribute('data-titulo') || '';
      var textoCard = card.textContent.toLowerCase();

      var tituloNormalizado = titulo.normalize('NFD').replace(/[\u0300-\u036f]/g, '');
      var textoNormalizado = textoCard.normalize('NFD').replace(/[\u0300-\u036f]/g, '');

      var encontrou = titulo.includes(termo) ||
                      textoCard.includes(termo) ||
                      tituloNormalizado.includes(termoNormalizado) ||
                      textoNormalizado.includes(termoNormalizado);

      if (termo === '' || encontrou) {
        card.style.display = '';
        visiveis++;
      } else {
        card.style.display = 'none';
      }
    });

    atualizarContador(visiveis);
  });
});
