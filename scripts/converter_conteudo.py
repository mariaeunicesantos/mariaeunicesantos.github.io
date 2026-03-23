#!/usr/bin/env python3
"""
Conversor de Conteúdo — Maria Eunice Santos
============================================
Converte os arquivos .doc da pasta mae_content em arquivos Markdown
compatíveis com Jekyll para o site.

Uso: python3 scripts/converter_conteudo.py

Categorias:
  - publicacoes: ensaios e artigos acadêmicos em português
  - textos_franceses: textos em francês
  - vidas_abertas: colunas do Correio da Bahia (parseadas individualmente)
"""

import subprocess
import os
import re
import unicodedata


# === Caminhos ===
PASTA_ORIGEM = os.path.join(os.path.dirname(__file__), '..', '..', 'mae_content')
PASTA_PUBLICACOES = os.path.join(os.path.dirname(__file__), '..', '_publicacoes')
PASTA_VIDAS_ABERTAS = os.path.join(os.path.dirname(__file__), '..', '_vidas_abertas')
PASTA_FRANCESES = os.path.join(os.path.dirname(__file__), '..', '_textos_franceses')


# === Classificação dos documentos ===

# Textos em francês
FRANCESES = [
    'AVANT-PROJET DE THESE POUR.doc',
    'Carta à Cher Monsieur.doc',
]

# Vidas Abertas (compilações — serão parseadas em artigos individuais)
VIDAS_ABERTAS = [
    'vidas abertas atualizada.doc',
    # 'Vidas Abertas -  Eunice Tabacof.doc',  # versão anterior, pular
]

# Publicações acadêmicas em português (todo o resto)
PUBLICACOES = [
    'A IMPERTINÊNCIA E ECCE HOMO.doc',
    'A PASSAGEM 3.doc',
    'Anteprojeto de pesquisa para a Pós.doc',
    'Bibliografia sobre o Temp1.doc',
    'BIBLIOGRAFIA SOBRE O TEMPO.doc',
    'DESTINAÇÃO.doc',
    'ECCE HOMO.doc',
    'Entre a Memória e o Olhar.doc',
    'LIVROS ESCRITO POR DRA EUNICE 1.doc',
    'Notas para uma critica do conceito de personalidade.doc',
    'O COTIDIANO DE UM ANALISTA.doc',
    'O Silêncio dos Inocentes.doc',
    'O tempo, o olhar, a ética.doc',
    'Observações sobre.doc',
    'Oh tanto riso.doc',
    'Palestra sobre a Perversão.doc',
    'Proposta de Investigação do Texto Freudiano.doc',
    'Proposta de investigação do tempo freudiano.doc',
    'RECÔNCAVO,RECÔNCAVO.meu medo.doc',
    'Tales de Mileto ( Nietzsche, Freud ).doc',
    'Tese para Doutorado O Tempo, O olhar, a Ética.doc',
    'Um Vidro Estilhaçado pela Janela.doc',
]

# Metadados das publicações (título limpo, tipo, resumo)
METADADOS_PUBLICACOES = {
    'A IMPERTINÊNCIA E ECCE HOMO.doc': {
        'titulo': 'A Impertinência e Ecce Homo',
        'tipo': 'Ensaio',
        'resumo': 'Reflexão sobre a impertinência, o riso e a ironia a partir de Bergson e Nietzsche.',
    },
    'A PASSAGEM 3.doc': {
        'titulo': 'A Passagem: Cura e Autorização',
        'tipo': 'Ensaio',
        'resumo': 'Sobre o processo de cura e autorização na prática psicanalítica.',
    },
    'Anteprojeto de pesquisa para a Pós.doc': {
        'titulo': 'Anteprojeto de Pesquisa — Pós-Graduação em Letras e Linguística',
        'tipo': 'Pesquisa',
        'resumo': 'Projeto de pesquisa sobre sexualidades, a partir de Foucault e da psicanálise.',
    },
    'Bibliografia sobre o Temp1.doc': {
        'titulo': 'Bibliografia: O Tempo, O Olhar, a Ética',
        'tipo': 'Bibliografia',
        'resumo': 'Bibliografia comentada sobre tempo, olhar e ética na filosofia e na psicanálise.',
    },
    'BIBLIOGRAFIA SOBRE O TEMPO.doc': {
        'titulo': 'Bibliografia sobre o Tempo',
        'tipo': 'Bibliografia',
        'resumo': 'Referências bibliográficas sobre o conceito de tempo na psicanálise e filosofia.',
    },
    'DESTINAÇÃO.doc': {
        'titulo': 'Destinação',
        'tipo': 'Texto Literário',
        'resumo': 'Reflexão sobre o acaso, a repetição e os sinais que compõem o percurso de uma vida.',
    },
    'ECCE HOMO.doc': {
        'titulo': 'Ecce Homo',
        'tipo': 'Ensaio',
        'resumo': 'Leitura psicanalítica de Ecce Homo de Nietzsche — como alguém se torna o que é.',
    },
    'Entre a Memória e o Olhar.doc': {
        'titulo': 'Entre a Memória e o Olhar',
        'tipo': 'Ensaio',
        'resumo': 'Observações sobre "Um Distúrbio de Memória na Acrópole" de Freud, a carta a Romain Rolland.',
    },
    'LIVROS ESCRITO POR DRA EUNICE 1.doc': {
        'titulo': 'Nietzsche, Freud',
        'tipo': 'Livro',
        'resumo': 'Encontro inventado entre Nietzsche e Freud — aproximação sem totalização.',
    },
    'Notas para uma critica do conceito de personalidade.doc': {
        'titulo': 'Notas para uma Crítica do Conceito de Personalidade',
        'tipo': 'Ensaio',
        'resumo': 'Questionamento da eficácia epistemológica do conceito de personalidade em psicologia.',
    },
    'O COTIDIANO DE UM ANALISTA.doc': {
        'titulo': 'O Cotidiano de um Analista — O Diário Clínico de Ferenczi',
        'tipo': 'Ensaio',
        'resumo': 'Reflexão sobre a prática analítica a partir do Diário Clínico de Ferenczi.',
    },
    'O Silêncio dos Inocentes.doc': {
        'titulo': 'O Silêncio dos Inocentes',
        'tipo': 'Ensaio',
        'resumo': 'Leitura psicanalítica do filme — o médico como monstro e a ambiguidade de Hannibal Lecter.',
    },
    'O tempo, o olhar, a ética.doc': {
        'titulo': 'O Tempo, o Olhar, a Ética — Ante-Projeto de Tese',
        'tipo': 'Pesquisa',
        'resumo': 'Ante-projeto de tese doutoral sobre tempo e olhar como operadores teóricos na psicanálise.',
    },
    'Observações sobre.doc': {
        'titulo': 'Observações sobre "Um Distúrbio de Memória na Acrópole"',
        'tipo': 'Ensaio',
        'resumo': 'Análise da carta de Freud a Romain Rolland — criação e amor diante da doença e da velhice.',
    },
    'Oh tanto riso.doc': {
        'titulo': 'Oh Tanto Riso, Tanta Alegria!',
        'tipo': 'Ensaio',
        'resumo': 'Reflexão sobre os artistas internacionais que escolhem a Bahia e o fenômeno cultural que isso representa.',
    },
    'Palestra sobre a Perversão.doc': {
        'titulo': 'Palestra sobre a Perversão',
        'tipo': 'Conferência',
        'resumo': 'Palestra no Hospital Juliano Moreira sobre a perversão no interstício entre neurose e psicose.',
    },
    'Proposta de Investigação do Texto Freudiano.doc': {
        'titulo': 'Proposta de Investigação do Texto Freudiano — A Construção do Conceito de Sintoma',
        'tipo': 'Pesquisa',
        'resumo': 'Investigação sobre a construção do conceito de sintoma em Freud e a proposição do "sinthoma".',
    },
    'Proposta de investigação do tempo freudiano.doc': {
        'titulo': 'Proposta de Investigação do Tempo Freudiano',
        'tipo': 'Pesquisa',
        'resumo': 'A construção do conceito de sintoma e sua relação com o tempo na teoria freudiana.',
    },
    'RECÔNCAVO,RECÔNCAVO.meu medo.doc': {
        'titulo': 'Recôncavo, Recôncavo, Meu Medo — Presença do Feminino em Jorge Amado',
        'tipo': 'Ensaio',
        'resumo': 'A presença do feminino na obra de Jorge Amado, a partir do mito de Édipo e da civilização grega.',
    },
    'Tales de Mileto ( Nietzsche, Freud ).doc': {
        'titulo': 'Tales de Mileto — Nietzsche, Freud',
        'tipo': 'Ensaio',
        'resumo': 'Restos da palavra ouvida — de alunos, clientes, amigos — juntando sabedoria oral e escrita.',
    },
    'Tese para Doutorado O Tempo, O olhar, a Ética.doc': {
        'titulo': 'Tese para Doutorado — O Tempo, O Olhar, a Ética',
        'tipo': 'Pesquisa',
        'resumo': 'Projeto de tese doutoral sobre o tempo e o olhar como operadores teóricos silenciados na psicanálise.',
    },
    'Um Vidro Estilhaçado pela Janela.doc': {
        'titulo': 'Um Vidro Estilhaçado pela Janela',
        'tipo': 'Texto Literário',
        'resumo': 'Explosão silenciosa de fragmentos transparentes — paradoxo literário e instrumento psicanalítico.',
    },
}

METADADOS_FRANCESES = {
    'AVANT-PROJET DE THESE POUR.doc': {
        'titulo': 'Avant-Projet de Thèse — Le Temps, Le Regard, L\'Éthique',
        'tipo': 'Tese Doutoral',
        'resumo': 'Projeto de tese para doutorado na Université Paris VIII sobre o tempo, o olhar e a ética na psicanálise.',
    },
    'Carta à Cher Monsieur.doc': {
        'titulo': 'Carta ao Prof. Pierre Fédida',
        'tipo': 'Correspondência',
        'resumo': 'Carta organizando a visita do Prof. Pierre Fédida a Salvador para curso sobre Metapsicologia da Técnica e Contratransferência.',
    },
}


def criar_slug(texto):
    """Converte texto em slug para URL (sem acentos, lowercase, hífens)."""
    texto = unicodedata.normalize('NFD', texto)
    texto = texto.encode('ascii', 'ignore').decode('ascii')
    texto = texto.lower()
    texto = re.sub(r'[^a-z0-9\s-]', '', texto)
    texto = re.sub(r'[\s_]+', '-', texto)
    texto = re.sub(r'-+', '-', texto)
    texto = texto.strip('-')
    return texto[:80]


def converter_doc_para_texto(caminho_doc):
    """Converte .doc para texto puro usando textutil (macOS)."""
    resultado = subprocess.run(
        ['textutil', '-convert', 'txt', '-stdout', caminho_doc],
        capture_output=True, text=True
    )
    return resultado.stdout


def limpar_texto(texto):
    """Remove espaços excessivos e formata o texto para Markdown."""
    linhas = texto.splitlines()
    resultado = []
    em_branco_anterior = False

    for linha in linhas:
        linha = linha.rstrip()
        if not linha:
            if not em_branco_anterior:
                resultado.append('')
            em_branco_anterior = True
        else:
            em_branco_anterior = False
            resultado.append(linha)

    return '\n'.join(resultado).strip()


def criar_frontmatter(titulo, tipo='Ensaio', resumo='', autor='Maria Eunice Santos', categoria='publicacao'):
    """Gera o frontmatter YAML para Jekyll."""
    # Escapar aspas no título e resumo
    titulo_safe = titulo.replace('"', '\\"')
    resumo_safe = resumo.replace('"', '\\"')

    fm = f'---\n'
    fm += f'title: "{titulo_safe}"\n'
    fm += f'autor: "{autor}"\n'
    fm += f'tipo: "{tipo}"\n'
    if resumo:
        fm += f'resumo: "{resumo_safe}"\n'
    fm += f'---\n\n'
    return fm


def processar_publicacoes():
    """Converte os artigos acadêmicos em Markdown."""
    os.makedirs(PASTA_PUBLICACOES, exist_ok=True)
    contagem = 0

    for arquivo in PUBLICACOES:
        caminho = os.path.join(PASTA_ORIGEM, arquivo)
        if not os.path.exists(caminho):
            print(f'  AVISO: Arquivo não encontrado: {arquivo}')
            continue

        meta = METADADOS_PUBLICACOES.get(arquivo, {})
        titulo = meta.get('titulo', arquivo.replace('.doc', ''))
        tipo = meta.get('tipo', 'Ensaio')
        resumo = meta.get('resumo', '')

        texto = converter_doc_para_texto(caminho)
        texto = limpar_texto(texto)

        slug = criar_slug(titulo)
        nome_arquivo = f'{slug}.md'
        caminho_saida = os.path.join(PASTA_PUBLICACOES, nome_arquivo)

        frontmatter = criar_frontmatter(titulo, tipo, resumo)

        with open(caminho_saida, 'w', encoding='utf-8') as f:
            f.write(frontmatter)
            f.write(texto)
            f.write('\n')

        print(f'  ✓ {nome_arquivo}')
        contagem += 1

    return contagem


def processar_franceses():
    """Converte os textos em francês."""
    os.makedirs(PASTA_FRANCESES, exist_ok=True)
    contagem = 0

    for arquivo in FRANCESES:
        caminho = os.path.join(PASTA_ORIGEM, arquivo)
        if not os.path.exists(caminho):
            print(f'  AVISO: Arquivo não encontrado: {arquivo}')
            continue

        meta = METADADOS_FRANCESES.get(arquivo, {})
        titulo = meta.get('titulo', arquivo.replace('.doc', ''))
        tipo = meta.get('tipo', 'Texto Acadêmico')
        resumo = meta.get('resumo', '')

        texto = converter_doc_para_texto(caminho)
        texto = limpar_texto(texto)

        slug = criar_slug(titulo)
        nome_arquivo = f'{slug}.md'
        caminho_saida = os.path.join(PASTA_FRANCESES, nome_arquivo)

        frontmatter = criar_frontmatter(titulo, tipo, resumo, autor='Maria Eunice Santos')

        with open(caminho_saida, 'w', encoding='utf-8') as f:
            f.write(frontmatter)
            f.write(texto)
            f.write('\n')

        print(f'  ✓ {nome_arquivo}')
        contagem += 1

    return contagem


def eh_saudacao_resposta(texto):
    """Verifica se a linha é uma saudação de resposta da Eunice (não um título)."""
    texto_lower = texto.lower().strip().rstrip(',').rstrip(':')
    prefixos = [
        'querida', 'querido', 'cara', 'caro', 'prezada', 'prezado',
        'minha querida', 'meu querido', 'minha cara', 'meu caro',
    ]
    for p in prefixos:
        if texto_lower.startswith(p):
            return True
    return False


def eh_assinatura(texto):
    """Verifica se a linha parece ser uma assinatura (nome curto do leitor)."""
    texto = texto.strip().rstrip('.')
    # Assinaturas: 1-3 palavras, sem pontuação complexa, curtas
    if len(texto) > 40:
        return False
    palavras = texto.split()
    if len(palavras) > 4:
        return False
    # Tem que parecer um nome (primeira letra maiúscula, sem verbos/artigos longos)
    if palavras and palavras[0][0].isupper() and len(texto) < 30:
        # Excluir frases que claramente não são nomes
        nao_nomes = ['eu ', 'um ', 'uma ', 'o ', 'a ', 'por ', 'para ', 'como ', 'que ']
        texto_lower = texto.lower()
        if any(texto_lower.startswith(n) for n in nao_nomes):
            return False
        # Excluir se termina com pontuação de frase
        if texto.endswith('?') or texto.endswith('!'):
            return False
        return True
    return False


def nao_eh_titulo(texto):
    """Retorna True se a linha claramente NÃO é um título de coluna."""
    stripped = texto.strip()

    # Saudações de resposta
    if eh_saudacao_resposta(stripped):
        return True

    # Assinaturas
    if eh_assinatura(stripped):
        return True

    # Saudações de carta
    if stripped.lower().startswith('eunice'):
        return True

    # Despedidas
    despedidas = ['um abraço', 'abraço', 'beijos', 'obrigad', 'atenciosamente',
                  'afetuosamente', 'com carinho', 'até mais', 'um beijo']
    if any(stripped.lower().startswith(d) for d in despedidas):
        return True

    # Conectores (início de parágrafo, não de artigo)
    conectores = ['mas ', 'e ', 'ou ', 'porque ', 'pois ', 'então ', 'portanto ',
                  'assim ', 'porém ', 'todavia ', 'entretanto ', 'contudo ',
                  'no entanto ', 'nesse ', 'nessa ', 'desse ', 'dessa ',
                  'daí ', 'aí ']
    if any(stripped.lower().startswith(c) for c in conectores):
        return True

    # Continuação (termina com vírgula)
    if stripped.endswith(','):
        return True

    # Linhas que são claramente meios de frase (começa com minúscula)
    if stripped[0].islower():
        return True

    # Muito curto para ser título (provavelmente nome ou interjeição)
    if len(stripped) < 5:
        return True

    return False


def encontrar_proxima_nao_branca(linhas, inicio):
    """Encontra a próxima linha não-branca a partir de inicio."""
    for i in range(inicio, min(len(linhas), inicio + 5)):
        if linhas[i].strip():
            return i, linhas[i].strip()
    return None, None


def parsear_vidas_abertas():
    """
    Parseia a compilação de Vidas Abertas em artigos individuais.

    Cada coluna segue o padrão:
      Título (headline curta)
      [linha(s) em branco]
      Subtítulo/descrição (linha curta descrevendo o tema)
      [linha(s) em branco]
      Corpo (carta do leitor + resposta da Eunice)

    A detecção usa: linha curta + pelo menos 1 blank antes + NÃO é
    saudação/assinatura/conector.
    """
    os.makedirs(PASTA_VIDAS_ABERTAS, exist_ok=True)

    arquivo = VIDAS_ABERTAS[0]
    caminho = os.path.join(PASTA_ORIGEM, arquivo)
    if not os.path.exists(caminho):
        print(f'  ERRO: Arquivo não encontrado: {arquivo}')
        return 0

    texto = converter_doc_para_texto(caminho)
    linhas = texto.splitlines()

    # Fase 1: identificar todas as posições de títulos candidatos
    candidatos = []  # (indice_linha, titulo)

    linhas_em_branco = 0
    for i, linha in enumerate(linhas):
        stripped = linha.strip()

        if not stripped:
            linhas_em_branco += 1
            continue

        # Critérios para título:
        # 1. Pelo menos 1 linha em branco antes
        # 2. Tamanho de título (5-80 chars)
        # 3. Não é saudação/assinatura/conector
        if (linhas_em_branco >= 1 and
            5 <= len(stripped) <= 80 and
            not nao_eh_titulo(stripped)):

            # Verificação extra: a linha seguinte (pulando brancos)
            # deve ser outra linha curta (subtítulo) OU o início da carta
            prox_idx, prox_texto = encontrar_proxima_nao_branca(linhas, i + 1)
            if prox_texto:
                # Se a próxima linha não-branca é curta (subtítulo)
                # ou começa com formato de carta, confirma como título
                eh_subtitulo = len(prox_texto) < 150
                if eh_subtitulo:
                    candidatos.append((i, stripped))

        linhas_em_branco = 0

    # Fase 2: filtrar candidatos — manter apenas os que têm conteúdo
    # suficiente entre eles (mínimo ~10 linhas de conteúdo)
    titulos_finais = []
    for idx, (pos, titulo) in enumerate(candidatos):
        if idx == 0:
            titulos_finais.append((pos, titulo))
            continue
        pos_anterior = titulos_finais[-1][0]
        linhas_entre = pos - pos_anterior
        if linhas_entre >= 10:
            titulos_finais.append((pos, titulo))

    print(f'  Títulos detectados: {len(titulos_finais)}')

    # Fase 3: extrair artigos entre os títulos
    artigos = []
    for idx, (pos, titulo) in enumerate(titulos_finais):
        inicio_conteudo = pos + 1
        if idx + 1 < len(titulos_finais):
            fim_conteudo = titulos_finais[idx + 1][0]
        else:
            fim_conteudo = len(linhas)

        corpo_linhas = linhas[inicio_conteudo:fim_conteudo]
        corpo = '\n'.join(corpo_linhas)

        artigos.append({
            'titulo': titulo,
            'linhas': corpo_linhas,
        })

    # Filtrar artigos muito curtos (provavelmente fragmentos)
    artigos_validos = [a for a in artigos if len('\n'.join(a['linhas'])) > 200]

    print(f'  Artigos encontrados: {len(artigos)} (válidos: {len(artigos_validos)})')

    contagem = 0
    for idx, artigo in enumerate(artigos_validos, 1):
        titulo = artigo['titulo']
        # Limpar título
        titulo = titulo.strip()
        if len(titulo) > 100:
            titulo = titulo[:97] + '...'

        conteudo = limpar_texto('\n'.join(artigo['linhas']))

        # Gerar resumo a partir das primeiras linhas
        primeiro_paragrafo = ''
        for linha in conteudo.split('\n'):
            if linha.strip() and len(linha.strip()) > 20:
                primeiro_paragrafo = linha.strip()
                break
        resumo = primeiro_paragrafo[:150] + '...' if len(primeiro_paragrafo) > 150 else primeiro_paragrafo

        slug = criar_slug(titulo)
        if not slug:
            slug = f'artigo-{idx}'
        nome_arquivo = f'{idx:03d}-{slug}.md'
        caminho_saida = os.path.join(PASTA_VIDAS_ABERTAS, nome_arquivo)

        titulo_safe = titulo.replace('"', '\\"')
        resumo_safe = resumo.replace('"', '\\"')

        fm = f'---\n'
        fm += f'title: "{titulo_safe}"\n'
        fm += f'autor: "Maria Eunice Santos"\n'
        fm += f'numero: {idx}\n'
        fm += f'resumo: "{resumo_safe}"\n'
        fm += f'---\n\n'

        with open(caminho_saida, 'w', encoding='utf-8') as f:
            f.write(fm)
            f.write(conteudo)
            f.write('\n')

        contagem += 1

    return contagem


def main():
    print('=' * 60)
    print('Conversor de Conteúdo — Maria Eunice Santos')
    print('=' * 60)

    print('\n📚 Processando publicações acadêmicas...')
    n_pub = processar_publicacoes()
    print(f'   Total: {n_pub} publicações convertidas\n')

    print('🇫🇷 Processando textos em francês...')
    n_fr = processar_franceses()
    print(f'   Total: {n_fr} textos convertidos\n')

    print('📰 Processando Vidas Abertas...')
    n_va = parsear_vidas_abertas()
    print(f'   Total: {n_va} artigos convertidos\n')

    print('=' * 60)
    print(f'Conversão concluída!')
    print(f'  Publicações:     {n_pub}')
    print(f'  Textos franceses: {n_fr}')
    print(f'  Vidas Abertas:   {n_va}')
    print(f'  TOTAL:           {n_pub + n_fr + n_va} arquivos')
    print('=' * 60)


if __name__ == '__main__':
    main()
