import sys
from plan import comparadorBTP, comparadorSBT


terminal_function = {
    'BTP': {'arquivo': 'BTP - 05 de setembro.csv',
            'function': comparadorBTP},
    'SBT': {'arquivo': '',
            'function': comparadorSBT},
}

if __name__ == '__main__':
    if len(sys.argv) == 1:
        print('Uso: python3 plan_test.py <terminal> <nomedoarquivo>')
    else:
        nome_arquivo = None
        if len(sys.argv) == 3:
            nome_arquivo = sys.argv[2]
        terminal = sys.argv[1]
        terminal_dict = terminal_function.get(terminal)
        if terminal_dict is None:
            print('Terminal não encontrado')
        the_function = terminal_dict.get('function')
        if nome_arquivo is None:
            nome_arquivo = terminal_dict.get('arquivo')
        result = the_function(nome_arquivo)
        print('Linhas com ocorrência: ', result)
        print(result)


def test_comparadorBTP():
    nome_arquivo = 'BTP - 05 de setembro.csv'
    linhas = comparadorBTP(nome_arquivo)
    assert len(linhas) == 336
    assert linhas[0].get('Nome-Motorista') is not None

def test_comparadorSBT():
    nome_arquivo = 'BTP - 05 de setembro.csv'
    linhas = comparadorBTP(nome_arquivo)
    assert len(linhas) == 336
    assert linhas[0].get('Motorista') is not None
