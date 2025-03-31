# OXONO - Jogo

Este jogo foi desenvolvido como parte dos requisitos da disciplina de Engenharia de Software I (INE5605) do Centro Tecnológico da Universidade Federal de Santa Catarina (UFSC).

## Descrição

OXONO é um jogo de tabuleiro estratégico para dois jogadores. O objetivo é alinhar quatro peças da mesma cor ou do mesmo símbolo (X ou O) em uma linha horizontal ou vertical.

## Regras do Jogo

1.  **Tabuleiro**: O jogo é jogado em um tabuleiro 6x6.
2.  **Peças**: Cada jogador tem oito peças de cada símbolo (X e O).
3.  **Totens**: Existem dois totens no tabuleiro, um "X" e um "O", posicionados inicialmente em casas aleatórias.
4.  **Turnos**: Os jogadores se alternam nos turnos. O jogador "Vermelho" começa.
5.  **Movimento do Totem**: No seu turno, o jogador deve mover um dos totens (X ou O) para uma casa livre adjacente (horizontal ou vertical).
6.  **Colocação da Peça**: Após mover o totem, o jogador deve colocar uma de suas peças com o mesmo símbolo do totem movido em uma casa livre adjacente à nova posição do totem.
7.  **Condição de Vitória**: O jogador que conseguir alinhar quatro peças da mesma cor ou do mesmo símbolo em uma linha horizontal ou vertical vence o jogo.
8.  **Empate**: Se todas as casas do tabuleiro forem preenchidas e nenhum jogador tiver vencido, o jogo termina em empate.
9.  **Reiniciar Partida**: A qualquer momento, é possível reiniciar a partida clicando no botão "Reiniciar Partida".

## Como Executar

Para executar o jogo, você precisará ter o Python 3 e a biblioteca Tkinter instalados. Siga os passos abaixo:

1.  **Clone o repositório (se aplicável)**: Se o código estiver em um repositório Git, clone-o para o seu computador.
2.  **Navegue até o diretório do jogo**: Abra o terminal e navegue até o diretório onde o arquivo `oxono_game.py` está localizado.
3.  **Execute o jogo**: Execute o seguinte comando no terminal:

    ```bash
    python oxono_game.py
    ```

4.  **Jogue**: A interface gráfica do jogo será aberta, e você poderá começar a jogar.

## Controles

* **Botões "Selecionar Totem X" e "Selecionar Totem O"**: Selecionam o totem a ser movido.
* **Clique nas casas do tabuleiro**: Movem o totem e colocam as peças.
* **Botão "Cancelar Ação"**: Cancela a ação de mover o totem ou colocar a peça.
* **Botão "Reiniciar Partida"**: Reinicia o jogo.

## Notas

* Este jogo foi desenvolvido com o objetivo de demonstrar os conceitos aprendidos na disciplina de Engenharia de Software I.
* O código está organizado em classes para melhor modularidade e legibilidade.
* A interface gráfica foi desenvolvida utilizando a biblioteca Tkinter.
* O jogo inclui validações para garantir que as regras sejam seguidas corretamente.
