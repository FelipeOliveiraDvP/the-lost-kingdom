# Game Design Document — RPG 2D

## 1. Visão geral

**Nome provisório:** The Lost Kingdom

**Gênero:** RPG de ação 2D, com perspectiva top-down (visão de cima).

**Tecnologia:**

- Linguagem: Python 3
- Framework gráfico: Pygame
- Interface: 2D
- Estilo visual: Pixel Art, inspirado em jogos clássicos da franquia Zelda.

**Descrição:**

O jogo consiste em uma aventura 2D na qual o jogador precisa atravessar um mapa, partindo da região identificada como `START` até alcançar o objetivo localizado na parte superior do cenário.

Durante o percurso, o jogador encontrará inimigos que deverá enfrentar utilizando ataques. Também poderá coletar moedas distribuídas pelo mapa.

O jogador precisa administrar seus pontos de vida para conseguir chegar ao objetivo sem morrer.

---

## 2. Objetivo do jogo

O objetivo principal é conduzir o personagem desde o ponto inicial (`START`) até o destino final do mapa, enfrentando os inimigos encontrados pelo caminho.

Para concluir a partida, o jogador deverá:

1. Iniciar a aventura pela região START.
2. Explorar o mapa e percorrer os caminhos disponíveis.
3. Enfrentar os inimigos utilizando ataques.
4. Evitar receber danos excessivos.
5. Coletar moedas durante a exploração.
6. Alcançar o objetivo final para vencer a partida.

Não existe limite de tempo para concluir a aventura.

---

## 3. Mapa e cenário

O jogo utilizará como cenário principal a imagem de mapa em Pixel Art desenvolvida para o projeto.

O mapa possui:

- Região inicial na parte inferior, identificada como START.
- Caminhos que conectam as diferentes regiões.
- Áreas verdes com vegetação e obstáculos decorativos.
- Regiões com água.
- Árvores, pedras e outros elementos ambientais.
- Região superior representando o destino final.

### Regras de movimentação no mapa

- O personagem poderá caminhar pelas áreas transitáveis.
- Não será permitido atravessar regiões de água, paredes, árvores ou obstáculos sólidos.
- Os inimigos estarão distribuídos em diferentes regiões do mapa.
- As moedas estarão posicionadas em pontos estratégicos do percurso.
- O objetivo final será representado por uma estrutura na região superior.

**Requisito técnico:** a imagem do mapa será utilizada como camada visual de fundo. As colisões deverão ser implementadas separadamente, utilizando uma máscara de colisão ou áreas retangulares/poligonais definidas no código.

---

## 4. Personagem do jogador

O jogador controlará um personagem com capacidade de movimentação e ataque.

### Atributos

| Atributo        | Valor        |
| --------------- | ------------ |
| Vida inicial    | 5 corações   |
| Vida máxima     | 5 corações   |
| Dano por ataque | 1 ponto      |
| Moedas iniciais | 0            |
| Velocidade      | Configurável |

### Movimentação

O personagem poderá se movimentar em quatro direções:

- Cima.
- Baixo.
- Esquerda.
- Direita.

A movimentação deverá possuir animações básicas para representar o deslocamento do personagem.

### Ataque

O personagem poderá atacar os inimigos utilizando um ataque de curta distância.

Regras:

- Cada ataque causa 1 ponto de dano.
- O ataque deverá considerar a direção em que o personagem está olhando.
- O ataque deverá atingir somente inimigos dentro do alcance.
- O ataque deverá possuir um intervalo mínimo entre execuções para evitar ataques ilimitados por segundo.

### Sistema de vida

O jogador começa com 5 corações.

Cada ataque recebido de um inimigo remove 1 coração.

Quando a vida chegar a zero:

1. A partida será encerrada.
2. Será exibida a mensagem `GAME OVER`.
3. O jogador poderá retornar ao menu inicial.
4. Uma nova partida deverá reiniciar os atributos do personagem.

---

## 5. Inimigos

Os inimigos estarão distribuídos pelo mapa e representarão os principais desafios da aventura.

### Atributos

| Atributo        | Valor                   |
| --------------- | ----------------------- |
| Vida            | 1 coração               |
| Dano por ataque | 1 ponto                 |
| Velocidade      | Configurável            |
| Comportamento   | Patrulha ou perseguição |

### Regras de combate

- Cada inimigo começa com 1 coração de vida.
- Cada ataque do jogador causa 1 ponto de dano.
- Portanto, um único ataque bem-sucedido elimina um inimigo.
- Os inimigos poderão causar dano quando entrarem em contato com o jogador.
- Cada contato que efetivamente causar dano removerá 1 coração do jogador.
- Após receber um ataque, o inimigo deverá ser removido do cenário.

### Comportamento dos inimigos

Para a primeira versão, os inimigos poderão utilizar comportamentos simples:

1. Patrulhar uma pequena região do mapa.
2. Identificar a proximidade do jogador.
3. Perseguir o jogador quando estiver dentro de um determinado alcance.
4. Causar dano quando entrar em contato com o personagem.

O sistema deverá possuir um intervalo de invulnerabilidade após o jogador receber dano, evitando que uma única colisão consuma todos os seus corações instantaneamente.

---

## 6. Sistema de moedas

O mapa terá moedas distribuídas pelo cenário para incentivar a exploração.

### Regras

- O jogador começa com zero moedas.
- Cada moeda coletada adiciona 1 unidade ao contador.
- A moeda desaparece do mapa após a coleta.
- O contador deverá ser atualizado imediatamente.
- As moedas coletadas permanecerão contabilizadas durante a partida.

As moedas não serão obrigatórias para alcançar a vitória na versão inicial.

---

## 7. Condições de vitória e derrota

### Vitória

<pre>
O jogador alcança o objetivo final
            |
            v
     Partida concluída
            |
            v
       Tela de vitória
</pre>

Quando o personagem alcançar a região do objetivo final, a partida será concluída com sucesso.

A tela de vitória deverá apresentar:

- Mensagem `YOU WIN!`.
- Quantidade de moedas coletadas.
- Opção para retornar ao menu inicial.

### Derrota

<pre>
Jogador recebe ataques
            |
            v
       Vida chega a 0
            |
            v
        GAME OVER
            |
            v
      Retornar ao menu
</pre>

Quando os cinco corações forem perdidos:

- A movimentação e os ataques serão interrompidos.
- A mensagem `GAME OVER` será apresentada.
- O jogador poderá retornar ao menu inicial.

Não haverá contagem regressiva, cronômetro ou limite de tempo.

---

## 8. Interface e HUD

Durante a partida, deverá existir uma interface gráfica (HUD) apresentando as informações essenciais.

### Elementos da interface

| Elemento   | Descrição                                   |
| ---------- | ------------------------------------------- |
| Vida       | Representação dos cinco corações do jogador |
| Moedas     | Contador de moedas coletadas                |
| Personagem | Sprite controlado pelo jogador              |
| Inimigos   | Sprites dos inimigos presentes no mapa      |

A interface deverá permanecer visível durante toda a partida.

---

## 9. Menu inicial

O jogo deverá apresentar um menu inicial antes de começar a aventura.

### Elementos obrigatórios

- Nome do jogo.
- Botão ou opção `START GAME`.
- Opção `EXIT`.
- Instruções de controle visíveis na própria tela.

### Comandos de controle

| Tecla | Ação                         |
| ----- | ---------------------------- |
| W / ↑ | Movimentar para cima         |
| S / ↓ | Movimentar para baixo        |
| A / ← | Movimentar para esquerda     |
| D / → | Movimentar para direita      |
| SPACE | Atacar                       |
| ESC   | Pausar / abrir menu de pausa |

Os comandos deverão estar visíveis no menu inicial.

---

## 10. Telas do jogo

O jogo deverá possuir os seguintes estados:

| Estado    | Descrição                            |
| --------- | ------------------------------------ |
| MENU      | Menu inicial com comandos            |
| PLAYING   | Partida em andamento                 |
| PAUSED    | Partida temporariamente interrompida |
| GAME_OVER | Jogador derrotado                    |
| VICTORY   | Objetivo alcançado                   |

### Fluxo de navegação

1. Ao executar o jogo, será apresentada a tela MENU.
2. Ao selecionar START GAME, uma nova partida será inicializada.
3. Durante a partida, o jogador poderá pausar o jogo.
4. Caso perca toda a vida, será apresentada a tela GAME_OVER.
5. Caso alcance o objetivo, será apresentada a tela VICTORY.
6. Nas telas de vitória e derrota, o jogador poderá retornar ao MENU.
7. A opção EXIT encerrará a aplicação.

---

## 11. Requisitos funcionais

| ID   | Requisito                              | Prioridade             |
| ---- | -------------------------------------- | ---------------------- |
| RF01 | Apresentar menu inicial                | Obrigatório            |
| RF02 | Exibir comandos no menu                | Obrigatório            |
| RF03 | Permitir movimentação do jogador       | Obrigatório            |
| RF04 | Implementar sistema de ataque          | Obrigatório            |
| RF05 | Implementar sistema de vida do jogador | Obrigatório            |
| RF06 | Implementar inimigos com vida e dano   | Obrigatório            |
| RF07 | Implementar colisões entre personagens | Obrigatório            |
| RF08 | Implementar coleta de moedas           | Funcionalidade do jogo |
| RF09 | Apresentar contador de moedas          | Funcionalidade do jogo |
| RF10 | Implementar condição de vitória        | Obrigatório            |
| RF11 | Implementar condição de derrota        | Obrigatório            |
| RF12 | Exibir mensagem GAME OVER              | Obrigatório            |
| RF13 | Permitir retornar ao menu              | Obrigatório            |
| RF14 | Implementar cenário com obstáculos     | Funcionalidade do jogo |
| RF15 | Implementar sistema de pausa           | Complementar           |

## 12. Requisitos não funcionais

- O jogo deverá ser desenvolvido integralmente em Python.
- O framework gráfico utilizado será Pygame.
- A aplicação deverá possuir interface gráfica 2D.
- O jogo não poderá depender de interações via terminal para sua execução ou jogabilidade.
- Os elementos gráficos deverão seguir uma identidade visual consistente em Pixel Art.
- O código deverá ser organizado em módulos e classes.
- O sistema deverá permitir adicionar novos inimigos, moedas e elementos de cenário sem modificar excessivamente a estrutura existente.

---

## 13. Arquitetura do projeto

A implementação utiliza uma organização modular por responsabilidade, inspirada
nos limites de dependência da clean architecture. Os módulos de entidades e
sistemas não dependem de cenas, interface, carregamento de recursos ou do ciclo
principal do jogo.

Esta é uma abordagem pragmática: `pygame.Vector2`, `pygame.Rect` e as máscaras do
Pygame permanecem na geometria e na simulação. O domínio não é completamente
independente do framework, mas as regras do jogo ficam separadas da apresentação
e do acesso aos recursos.

### Estrutura adotada

```text
the-lost-kingdom/
│
├── assets/
│   ├── map.png
│   ├── player/
│   ├── enemy/
│   └── sound/
│
├── src/
│   ├── main.py
│   └── lost_kingdom/
│       ├── core/
│       │   ├── game.py
│       │   ├── settings.py
│       │   └── states.py
│       ├── entities/
│       │   ├── actor.py
│       │   ├── player.py
│       │   ├── enemy.py
│       │   └── coin.py
│       ├── systems/
│       │   ├── collision.py
│       │   ├── combat.py
│       │   ├── level.py
│       │   └── world.py
│       ├── scenes/
│       │   ├── menu.py
│       │   ├── game_scene.py
│       │   ├── pause.py
│       │   ├── game_over.py
│       │   └── victory.py
│       ├── ui/
│       │   ├── hud.py
│       │   ├── components.py
│       │   └── error.py
│       └── resources/
│           ├── assets.py
│           └── audio.py
│
├── docs/
│   └── game-design.md
├── tests/
├── pyproject.toml
├── uv.lock
├── .gitignore
└── README.md
```

Os arquivos `__init__.py` dos pacotes foram omitidos da árvore. Eles não
inicializam o Pygame nem carregam o coordenador gráfico. O namespace
`lost_kingdom` evita pacotes genéricos no nível de `src`, e os assets mantêm seus
nomes e caminhos atuais.

### Responsabilidades principais

- [main.py](../src/main.py): entrada, logging, tratamento de erros e encerramento.
- [core/game.py](../src/lost_kingdom/core/game.py): inicialização, composição das
  dependências, janela, eventos, navegação e ciclo principal.
- [core/settings.py](../src/lost_kingdom/core/settings.py): resolução, FPS,
  parâmetros de movimentação e combate e localização dos assets.
- [core/states.py](../src/lost_kingdom/core/states.py): estados da aplicação e
  ações de navegação.
- [entities/actor.py](../src/lost_kingdom/entities/actor.py): posição, direção e
  corpo de colisão compartilhados pelos personagens.
- [entities/player.py](../src/lost_kingdom/entities/player.py): vida, moedas,
  ataques e intervalos do jogador.
- [entities/enemy.py](../src/lost_kingdom/entities/enemy.py): atributos dos inimigos
  e dados dos inimigos derrotados para a animação de morte.
- [entities/coin.py](../src/lost_kingdom/entities/coin.py): posição e corpo das moedas.
- [systems/collision.py](../src/lost_kingdom/systems/collision.py): máscara
  transitável, consultas de colisão, movimento com deslizamento e linha de visão.
- [systems/combat.py](../src/lost_kingdom/systems/combat.py): resolução dos ataques,
  dano por contato e efeitos do combate.
- [systems/level.py](../src/lost_kingdom/systems/level.py): geometria do mapa,
  obstáculos, objetivo, spawns e validação dos posicionamentos; compõe o sistema
  de colisão em `Level.collision`.
- [systems/world.py](../src/lost_kingdom/systems/world.py): entrada da simulação,
  movimentação, patrulha/perseguição, combate, coleta e condições de fim.
- [scenes/game_scene.py](../src/lost_kingdom/scenes/game_scene.py): mundo da partida,
  câmera, animações e renderização do cenário, personagens e HUD.
- [scenes/](../src/lost_kingdom/scenes/): menu inicial, pausa, derrota e vitória,
  com suas mensagens e opções de navegação.
- [ui/components.py](../src/lost_kingdom/ui/components.py): fontes, cores,
  primitivas visuais, molduras e desenho compartilhado de botões.
- [ui/hud.py](../src/lost_kingdom/ui/hud.py): apresentação dos corações, moedas
  e controles.
- [ui/error.py](../src/lost_kingdom/ui/error.py): apresentação gráfica de falhas.
- [resources/assets.py](../src/lost_kingdom/resources/assets.py): carregamento
  e validação do mapa visual e spritesheets.
- [resources/audio.py](../src/lost_kingdom/resources/audio.py): música, efeitos e
  aviso de indisponibilidade de áudio.

### Direção das dependências

Configurações e estados não importam o ciclo principal. Entidades não importam
sistemas nem apresentação; sistemas consomem entidades e não importam cenas,
UI ou recursos. Cenas utilizam a simulação e os componentes visuais, enquanto
o coordenador em `core/game.py` reúne as dependências externas e controla as
transições.

Apesar do nome `core`, escolhido para manter a organização original deste
documento, `core/game.py` é o coordenador externo: não deve ser importado pelas
entidades ou pelos sistemas. As regras ficam em `entities` e `systems`, não
nos módulos de telas ou nos carregadores de recursos.

Os imports utilizam os novos caminhos completos dos módulos. Não há fachadas
de compatibilidade para os arquivos antigos.

---

## 14. Critérios de aceitação

A versão demo será considerada funcional quando atender aos seguintes critérios:

- [ ] O jogo inicia em uma interface gráfica.
- [ ] O menu inicial apresenta as opções de início e saída.
- [ ] Os comandos de controle estão visíveis no menu.
- [ ] O jogador consegue se movimentar em quatro direções.
- [ ] O jogador não consegue atravessar obstáculos sólidos.
- [ ] O personagem começa com cinco corações.
- [ ] O jogador consegue atacar os inimigos.
- [ ] Cada ataque causa exatamente um ponto de dano.
- [ ] Os inimigos possuem um coração de vida.
- [ ] Os inimigos conseguem causar um ponto de dano.
- [ ] O jogador consegue coletar moedas.
- [ ] O contador de moedas é atualizado corretamente.
- [ ] A derrota acontece quando a vida chega a zero.
- [ ] A mensagem GAME OVER é apresentada após a derrota.
- [ ] O jogador consegue retornar ao menu após a derrota.
- [ ] A vitória acontece quando o jogador alcança o objetivo.
- [ ] A quantidade de moedas coletadas é apresentada na tela de vitória.
- [ ] O jogo não possui limite de tempo.
- [ ] A aplicação pode ser executada sem depender do terminal para interação.

---

## 15. Escopo da versão demo

O desenvolvimento será concentrado nas mecânicas fundamentais necessárias para entregar uma experiência jogável.

**Dentro do escopo:**

- Um mapa.
- Um personagem jogável.
- Inimigos com comportamento básico.
- Sistema de vida e combate.
- Sistema de moedas.
- Colisões com obstáculos.
- Menu inicial.
- HUD.
- Tela de vitória.
- Tela de derrota.

**Fora do escopo inicial:**

- Sistema de inventário.
- Evolução de personagem.
- Equipamentos e armas diferentes.
- Múltiplas fases.
- Sistema de salvamento.
- Multiplayer.
- Missões secundárias.
- Chefes com múltiplas fases.

O objetivo é entregar uma demonstração pequena, funcional e completa, priorizando as mecânicas obrigatórias da atividade e a consistência da experiência de jogo.
