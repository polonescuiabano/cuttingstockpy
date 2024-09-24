import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication, QTableWidgetItem
from PyQt5.QtGui import QPen, QBrush
from PyQt5.QtCore import Qt
import logging
from amplpy import AMPL, add_to_path, Environment
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

# Configuração do logger
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Importando a classe Ui_MainWindow do arquivo gerado pelo Qt Designer
from ui.mainwindow import Ui_MainWindow


def gerar_arquivo_dat(barras_desejadas, barras_disponiveis):
    from collections import Counter
    demanda = Counter(barras_desejadas)

    with open('corte_estoque.dat', 'w') as f:
        # Conjunto de barras disponíveis
        f.write('# Conjunto de barras disponíveis\n')
        f.write(f'set BARRAS_DISPONIVEIS := {" ".join(map(str, barras_disponiveis))};\n\n')

        # Conjunto de barras desejadas
        f.write('# Conjunto de barras desejadas\n')
        f.write(f'set BARRAS_DESEJADAS := {" ".join(map(str, demanda.keys()))};\n\n')

        # Tamanho das barras disponíveis
        f.write('# Tamanho das barras disponíveis\n')
        f.write('param Tamanho :=\n')
        for barra in barras_disponiveis:
            f.write(f'    {barra} {barra}\n')
        f.write(';\n\n')

        # Demanda das barras desejadas
        f.write('# Demanda das barras desejadas\n')
        f.write('param Demanda :=\n')
        for barra, quantidade in demanda.items():
            f.write(f'    {barra} {quantidade}\n')
        f.write(';\n')


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Configurações e conexões
        self.ui.btn_adicionar.clicked.connect(self.adicionar_barra_desejada)
        self.ui.btn_resolver.clicked.connect(self.resolver_combinacoes)
        self.scene = QtWidgets.QGraphicsScene()
        self.ui.graphicsView.setScene(self.scene)

        # Configure o matplotlib para desenhar no QGraphicsView
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.ui.graphicsView.setScene(QtWidgets.QGraphicsScene())
        self.ui.graphicsView.scene().addWidget(self.canvas)

        # Atributos para armazenar a solução
        self.melhor_combinacao = []
        self.menor_desperdicio = None
        self.barras_disponiveis = []

    def adicionar_barra_desejada(self):
        try:
            tamanho = float(self.ui.lineEdit_tamanho.text().replace(',', '.'))
            quantidade = int(self.ui.lineEdit_quantidade.text())
        except ValueError:
            QtWidgets.QMessageBox.warning(self, 'Entrada Inválida', 'Por favor, insira valores válidos.')
            return

        # Adicionando a barra desejada na tabela
        row_count = self.ui.tableWidget_barras_desejadas.rowCount()
        self.ui.tableWidget_barras_desejadas.setRowCount(row_count + 1)

        self.ui.tableWidget_barras_desejadas.setItem(row_count, 0, QTableWidgetItem(f"{tamanho:.2f}"))
        self.ui.tableWidget_barras_desejadas.setItem(row_count, 1, QTableWidgetItem(str(quantidade)))

    def resolver_combinacoes(self):
        barras_desejadas = []
        for row in range(self.ui.tableWidget_barras_desejadas.rowCount()):
            try:
                tamanho = float(self.ui.tableWidget_barras_desejadas.item(row, 0).text().replace(',', '.'))
                quantidade = int(self.ui.tableWidget_barras_desejadas.item(row, 1).text())
                barras_desejadas.extend([tamanho] * quantidade)
            except ValueError:
                QtWidgets.QMessageBox.warning(self, 'Entrada Inválida', 'Por favor, insira valores válidos na tabela.')
                return

        barras_desejadas.sort(reverse=True)

        # Defina as barras disponíveis (ajuste conforme necessário)
        barras_disponiveis = [7, 8, 9, 10, 11, 12, 13, 15]

        # Gerar o arquivo .dat com as barras desejadas e disponíveis
        gerar_arquivo_dat(barras_desejadas, barras_disponiveis)

        self.calcular_melhor_combinacao(barras_desejadas)
        logger.debug("Chamando mostrar_resultado")
        self.mostrar_resultado()

    def calcular_melhor_combinacao(self, barras_desejadas):
        logger.debug("Iniciando cálculo da melhor combinação...")
        logger.debug(f"Barras desejadas: {barras_desejadas}")

        add_to_path(r"C:\Users\Dell\AMPL")
        ampl = AMPL(Environment())
        ampl.read('corte_estoque.mod')
        ampl.read_data('corte_estoque.dat')

        ampl.option['solver'] = 'cplex'

        try:
            ampl.solve()

            # Obter a solução
            x = ampl.get_variable('x').to_dict()
            desperdicio = ampl.get_variable('desperdicio').value()

            logger.debug(f"Solução x: {x}")
            logger.debug(f"Desperdício: {desperdicio}")

            # Ajustar a lógica para encontrar a melhor combinação
            self.barras_disponiveis = sorted([barra for barra in x.keys() if x[barra] > 0])
            self.melhor_combinacao = self.barras_disponiveis
            self.menor_desperdicio = desperdicio

            # Gerar a visualização das soluções
            self.desenhar_diagrama(barras_desejadas, x, desperdicio)

        except Exception as e:
            logger.error(f"Erro ao resolver o modelo: {e}")

    def mostrar_resultado(self):
        logger.debug(f"Mostrando resultado: {self.melhor_combinacao}, {self.menor_desperdicio}")

        if self.melhor_combinacao:
            resultado_texto = f"Melhor combinação:\n{self.melhor_combinacao}\nDesperdício: {self.menor_desperdicio} metros"
        else:
            resultado_texto = "Não foi possível encontrar uma combinação válida."

        self.ui.textEdit_combinacoes.setText(resultado_texto)

    def desenhar_diagrama(self, barras_desejadas, x, desperdicio):
        # Limpar o gráfico atual
        self.figure.clear()
        ax = self.figure.add_subplot(111)

        ax.set_xlim(0, max(self.barras_disponiveis) + 1)
        ax.set_ylim(0, len(self.barras_disponiveis) + 2)
        ax.set_xlabel('Comprimento (metros)')
        ax.set_ylabel('Índice da Solução')
        ax.set_title('Diagrama de Corte das Barras')

        color_map = plt.get_cmap('tab20')  # Usar uma paleta de cores com várias opções

        current_y = 0
        for barra_disponivel in self.barras_disponiveis:
            num_barras = x.get(barra_disponivel, 0)
            if num_barras > 0:
                # Adicionar a barra disponível
                for _ in range(int(num_barras)):
                    ax.add_patch(patches.Rectangle((0, current_y), barra_disponivel, 1, linewidth=1, edgecolor='black',
                                                   facecolor='lightgrey'))

                    # Desenhar as seções cortadas
                    barras_usadas = []
                    restante = barra_disponivel
                    for tamanho in barras_desejadas:
                        if tamanho <= restante:
                            barras_usadas.append(tamanho)
                            restante -= tamanho

                    x_start = 0
                    color_index = 0
                    for tamanho in barras_usadas:
                        ax.add_patch(patches.Rectangle((x_start, current_y), tamanho, 1, linewidth=1, edgecolor='black',
                                                       facecolor=color_map(color_index)))
                        ax.text(x_start + tamanho / 2, current_y + 0.5, f'{tamanho:.2f}', color='black', ha='center',
                                va='center')
                        x_start += tamanho
                        color_index += 1

                    # Adicionar desperdício se houver
                    if restante > 0:
                        ax.add_patch(
                            patches.Rectangle((x_start, current_y), restante, 1, linewidth=1, edgecolor='black',
                                              facecolor='red'))
                        ax.text(x_start + restante / 2, current_y + 0.5, f'{restante:.2f}', color='black', ha='center',
                                va='center')

                    current_y += 1

        # Mostrar o número de barras de cada tamanho utilizado
        for barra_disponivel in self.barras_disponiveis:
            num_barras = x.get(barra_disponivel, 0)
            if num_barras > 0:
                ax.text(barra_disponivel / 2, len(self.barras_disponiveis) - 0.5, f'{int(num_barras)}x', va='center',
                        ha='center')

        ax.grid(True)
        self.canvas.draw()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())