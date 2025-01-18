# 🐍 Jogo da Cobrinha (Snake Game)

Uma versão moderna e aprimorada do clássico jogo da cobrinha, desenvolvido em Python usando Pygame.

![Python Version](https://img.shields.io/badge/python-3.12.3-blue.svg)
![Pygame Version](https://img.shields.io/badge/pygame-2.6.1-green.svg)

## 🎮 Funcionalidades

- 🌈 Interface gráfica moderna e colorida
- 👀 Cobra com detalhes visuais (olhos que seguem a direção)
- 🎲 Sistema de power-ups:
  - ⚡ Velocidade aumentada
  - 🐌 Velocidade reduzida
  - 💎 Pontos dobrados
- 🏆 Sistema de high score com armazenamento permanente
- ⏸️ Sistema de pause
- 🌀 Teletransporte nas bordas da tela
- 📊 Interface informativa com pontuação atual, recorde e velocidade

## 🚀 Como Jogar

### Pré-requisitos

- Python 3.12.3 ou superior
- Pygame 2.6.1 ou superior

### Instalação

1. Clone o repositório
```bash
git clone https://github.com/LuisT-ls/Jogo-da-Cobrinha.git
cd Jogo-da-Cobrinha
```

2. Instale as dependências
```bash
pip install pygame
```

3. Execute o jogo
```bash
python snake_game.py
```

### Controles

- ⬆️ Seta para cima: Move para cima
- ⬇️ Seta para baixo: Move para baixo
- ⬅️ Seta para esquerda: Move para esquerda
- ➡️ Seta para direita: Move para direita
- ESC: Pausa/Despausa o jogo
- ENTER: Inicia o jogo/Reinicia após game over

## 🎯 Objetivo

Controle a cobra para comer as maçãs vermelhas e crescer o máximo possível. Colete power-ups para ganhar vantagens temporárias, mas cuidado para não colidir com seu próprio corpo!

## 💾 Sistema de High Score

O jogo mantém registro da maior pontuação em um arquivo `high_score.json`. Este arquivo é criado automaticamente na primeira execução do jogo.

## 🛠️ Desenvolvido Com

- [Python](https://www.python.org/) - Linguagem de programação
- [Pygame](https://www.pygame.org/) - Biblioteca para desenvolvimento de jogos

## 👤 Autor

- **Luís Teixeira** - [LuisT-ls](https://github.com/LuisT-ls)

## 📜 Licença

Este projeto está licenciado sob a licença MIT - veja o arquivo [LICENSE](LICENSE) para mais detalhes.
