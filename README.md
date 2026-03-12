# Plinko com Barreira

Jogo desktop em Python com Pygame inspirado em Plinko. Em cada rodada, o jogador escolhe de 1 a 5 bolas, acompanha a primeira queda ate a barreira, decide quais bolas manter e recebe a pontuacao final com base no slot onde cada bola termina.

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
python -m pip install -r requirements.txt
```

## Como executar

```powershell
python main.py
```

## Como jogar

1. Escolha a quantidade de bolas com os botoes `-` e `+`.
2. Clique em `Iniciar rodada`.
3. Espere todas as bolas chegarem ate a barreira.
4. Clique nas bolas que deseja manter.
5. Clique em `Confirmar`.
6. Veja o total da rodada e clique em `Nova rodada` para jogar novamente.

## Regras da rodada

- Cada rodada permite apostar de 1 a 5 bolas.
- Todas as bolas param obrigatoriamente na barreira.
- Bolas nao selecionadas sao abandonadas e nao pontuam.
- Os slots finais possuem os valores `0, 1, 2, 3, 2, 1, 5`.
- O premio final e a soma dos valores das bolas mantidas.

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

- A animacao usa uma simulacao simplificada, com deslocamentos laterais suaves em vez de fisica completa.
- O projeto foi organizado para facilitar evolucoes futuras, como efeitos sonoros, melhorias visuais e novas regras.
