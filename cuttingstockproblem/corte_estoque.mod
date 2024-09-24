# Conjunto de barras disponíveis
set BARRAS_DISPONIVEIS;

# Conjunto de barras desejadas
set BARRAS_DESEJADAS;

# Tamanho das barras disponíveis
param Tamanho {BARRAS_DISPONIVEIS};

# Demanda das barras desejadas
param Demanda {BARRAS_DESEJADAS};

# Variável para indicar quantas barras de cada tamanho são usadas
var x {BARRAS_DISPONIVEIS} >= 0, integer;

# Variável para o desperdício total
var desperdicio >= 0;

# Função objetivo: minimizar o desperdício total
minimize Objetivo:
    desperdicio;

# Restrições para atender a demanda
s.t. AtendeDemanda {d in BARRAS_DESEJADAS}:
    sum {b in BARRAS_DISPONIVEIS: Tamanho[b] >= d} Tamanho[b] * x[b] >= Demanda[d];

# Calcular o desperdício total
s.t. DefinicaoDesperdicio:
    desperdicio = sum {b in BARRAS_DISPONIVEIS} (Tamanho[b] * x[b]) - sum {d in BARRAS_DESEJADAS} d * Demanda[d];
