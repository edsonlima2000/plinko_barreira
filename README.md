# Plinko com Barreira

Jogo desktop em Python com Pygame inspirado em Plinko. Em cada rodada, o jogador escolhe de 1 a 5 bolas, acompanha a queda ate a barreira, decide quais bolas continuam e recebe o resultado com base nos multiplicadores das canaletas finais.

## Requisitos

- Python 3.12 ou superior
- Windows PowerShell

## Criacao e ativacao do ambiente virtual

Se o ambiente ainda nao estiver ativo:

```powershell
.\venv\Scripts\Activate.ps1
```

## Instalacao das dependencias

```powershell
py -3 -m pip install -r requirements.txt
```

## Como executar

```powershell
py -3 main.py
```

## Como jogar

1. Escolha a quantidade de bolas com os botoes `-` e `+`.
2. Clique em `Iniciar rodada`.
3. Espere todas as bolas chegarem ate a barreira.
4. Clique nas bolas que deseja manter.
5. Clique em `Confirmar`.
6. Veja o premio da rodada e o saldo exibido na interface.
7. Clique em `Nova rodada` para jogar novamente.

## Regras da rodada

- Cada rodada permite apostar de 1 a 5 bolas.
- Toda rodada comeca com `100 E$talecas`.
- Todas as bolas param obrigatoriamente na barreira.
- Bolas nao selecionadas sao abandonadas e nao pontuam.
- As bolas mantidas continuam pela metade inferior do tabuleiro, ainda atravessando pinos ate as canaletas.
- Os multiplicadores finais sao `-1x`, `-0.5x`, `0x`, `0.5x`, `10x`, `100x` e `100x`.
- O premio da rodada e a soma de `100 * multiplicador` para cada bola mantida que chega a uma canaleta.
- Ao iniciar uma nova rodada, o valor base volta para `100 E$talecas`.

## Interface atual

- Cabecalho com fase atual, bolas apostadas, bolas mantidas, premio da rodada e saldo mostrado em `E$talecas`.
- Placar da rodada logo abaixo do titulo, com o total e os multiplicadores obtidos.
- Piramide de pinos ocupando a parte superior e inferior do tabuleiro, com a barreira cortando a estrutura no meio.
- Canaletas finais exibindo apenas os multiplicadores, sem numeracao adicional.

## Estrutura do projeto

```text
plinko_barreira/
|- main.py
|- settings.py
|- requirements.txt
|- game/
|  |- game.py
|  |- board.py
|  |- ball.py
|  |- barrier.py
|  |- slot.py
|  |- round_manager.py
|  |- state_machine.py
|  `- ui.py
`- utils/
   |- colors.py
   `- helpers.py
```

## Componentes principais

- `main.py`: inicializa o Pygame e executa o loop principal.
- `settings.py`: centraliza resolucao, cores, limites e configuracoes da partida.
- `game/game.py`: coordena estados, eventos, atualizacao e renderizacao.
- `game/round_manager.py`: controla a rodada, selecao das bolas e pontuacao final.
- `game/board.py`: constroi a placa, os pinos e os slots de premio.
- `game/ball.py`: representa o movimento e os estados de cada bola.
- `game/ui.py`: desenha botoes, textos e resumo da rodada.

## Observacoes

- A animacao usa uma simulacao simplificada, com trajetorias guiadas e desvios nos pinos em vez de fisica completa.
- O projeto foi organizado para facilitar evolucoes futuras, como efeitos sonoros, melhorias visuais e novas regras.
