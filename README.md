# The Lost Kingdom

Demo de RPG de acao 2D em Python e Pygame, implementada conforme o
[documento de game design](docs/game-design.md).

Parta de **START**, explore os caminhos e alcance o **santuario ao norte**.
Voce comeca com cinco coracoes. Cada orc tem um ponto de vida, e cada golpe
causa um ponto de dano. Colete moedas pelo caminho: elas sao opcionais para
vencer. Nao existe limite de tempo.

## Instalar e executar

Requisitos: Python 3.12 ou superior, um ambiente grafico e
[uv](https://docs.astral.sh/uv/). O projeto seleciona Python 3.12 em
[.python-version](.python-version) para usar os pacotes binarios do Pygame.
O uv pode baixar esse interpretador automaticamente.

```bash
uv sync --group dev
uv run python src/main.py
```

No VS Code, selecione o interpretador da pasta `.venv` e pressione **F5**
(configuracao **The Lost Kingdom**). Depois da instalacao, nao ha comandos
de terminal durante a partida: menus funcionam por teclado ou mouse.
Tambem e possivel executar [src/main.py](src/main.py) com o Python da `.venv`.

Mantenha a pasta [assets/](assets/) junto ao projeto. Os caminhos dos recursos
sao resolvidos a partir do codigo, nao do diretorio atual. Nao e necessario
baixar recursos nem acessar a internet para jogar.

## Controles

| Tecla | Acao |
| --- | --- |
| W / cima | Mover para cima |
| S / baixo | Mover para baixo |
| A / esquerda | Mover para a esquerda |
| D / direita | Mover para a direita |
| SPACE | Atacar na direcao atual; segurar repete apos o intervalo |
| ESC | Pausar / continuar; retornar ao menu nas telas finais |
| Setas / W / S + ENTER | Navegar e selecionar nos menus |
| Mouse | Selecionar botoes dos menus |

A janela pode ser redimensionada e mantem a proporcao da imagem. A camera
acompanha o jogador; o minimapa marca sua posicao em verde e o objetivo em
dourado. Perder o foco da janela pausa a partida automaticamente.

## Regras implementadas

- Movimento com velocidade independente do FPS e diagonais normalizadas.
- Agua, barrancos, paredes, arvores, pedras e monumentos bloqueiam os pes.
  A colisao e uma mascara separada do fundo, definida em coordenadas do mapa.
- Golpe direcional com alcance curto, duracao de 0,32 s e intervalo de 0,48 s.
  Obstaculos bloqueiam ataques e a deteccao dos inimigos.
- 13 orcs patrulham e perseguem o jogador quando ele esta proximo e visivel.
  Um golpe elimina um orc; contato causa um coracao de dano.
- Invulnerabilidade de 1,2 s apos dano, com indicacao visual.
- 26 moedas coletaveis, contador no HUD e total apresentado na tela de vitoria.
- Estados MENU, PLAYING, PAUSED, GAME_OVER e VICTORY.
- Pausa congela movimento, inimigos, ataques e invulnerabilidade.
  Uma nova partida reinicia vida, moedas, inimigos e todos os intervalos.
- Sprites animados em quatro direcoes, musica e efeitos dos assets fornecidos.
  Sem dispositivo de audio, o jogo mostra um aviso e continua sem som.
  Recursos ausentes ou invalidos geram erro explicito.

O efeito `life-increase.wav` nao e utilizado: recuperacao de vida nao faz
parte do escopo da demo. Nao ha inventario, salvamento, progressao ou outras fases.

## Organizacao e ajustes

| Arquivo | Responsabilidade |
| --- | --- |
| [src/main.py](src/main.py) | Entrada, tratamento de erros e encerramento |
| [game.py](src/lost_kingdom/game.py) | Janela, eventos, estados, camera e renderizacao |
| [world.py](src/lost_kingdom/world.py) | Simulacao, combate, coleta e condicoes de fim |
| [entities.py](src/lost_kingdom/entities.py) | Jogador, inimigos, moedas e direcoes |
| [level.py](src/lost_kingdom/level.py) | Terreno transitavel, obstaculos e posicionamento |
| [resources.py](src/lost_kingdom/resources.py) | Spritesheets, mapa, musica e efeitos |
| [ui.py](src/lost_kingdom/ui.py) | Botoes, menus, coracoes e HUD |
| [settings.py](src/lost_kingdom/settings.py) | Velocidades e parametros de combate |

Adicione inimigos e moedas em `ENEMY_SPAWNS` e `COIN_SPAWNS`.
As coordenadas usam o mapa original de **1086 x 1448** pixels. Ao alterar o
mapa, atualize tambem `LAND`, `SOLID_RECTS` e `SOLID_ELLIPSES`; as regioes
externas aos poligonos representam agua, barrancos ou areas decorativas
inacessiveis. O carregamento rejeita posicionamentos dentro de obstaculos.

Os spritesheets fornecidos usam celulas de 64 x 64 e quatro linhas.
No jogador, a ordem e baixo, esquerda, direita, cima; nos inimigos,
baixo, cima, esquerda, direita. `SPRITE_ROWS` em
[resources.py](src/lost_kingdom/resources.py) mapeia as direcoes para as
linhas de cada personagem. A renderizacao amplia os sprites com vizinho
mais proximo para preservar a pixel art.

## Validacao

```bash
uv run poe check
```

Executa Ruff, mypy estrito e pytest. Os testes usam os drivers SDL `dummy`
para video e audio, sem abrir janelas nem exigir dispositivos reais.
Cobrem combate, dano, coleta, pausa, reinicio, navegacao de menus,
carregamento dos assets e renderizacao de todos os estados.
Tambem verificam uma rota completa de START ao objetivo e a acessibilidade
de todas as moedas e inimigos.

```bash
uv run poe lint
uv run poe typecheck
uv run poe test
uv run pytest tests/test_world.py::test_start_to_goal_is_walkable
uv run poe format
```
