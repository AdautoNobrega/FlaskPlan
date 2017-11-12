import csv
from collections import OrderedDict
import os
from jinja2 import Template
from config import portos_seguros
from covapp import UPLOAD_FOLDER

import pandas as pd
import openpyxl

BASEPATH = 'Notebooks\\'
ARQRISCO = os.path.join(BASEPATH, 'Matriz Risco.csv')
CAMPOS_RISCO = ['Nome Motorista', 'Mercadoria', 'TRANSPORTADORA', 'Operador de escâner', 'Cnh Motorista',
                'Nome Exportador', 'CNPJ DA TRANSPORTADORA (separado)']
CAMPOS_SBT = ['Motorista', 'Mercadoria', 'Transportadora', 'Login', 'CNH', 'Exportador importador', 'Cnpj']
CAMPOS_BTP = ['Nome Motorista', 'Descricao Ncm', 'Transportadora', 'Nome Operador Scanner', 'Cpf Motorista',
              'Cpf Motorista', 'Razão Social Exportador / Importador', 'CNPJ Transportadora']


def comparador(plan, campos_risco, campos_terminal, terminal):
    with open(ARQRISCO, 'rt') as csvrisco:
        reader = csv.DictReader(csvrisco)
        read_risco = []
        for row in reader:
            read_risco.append(row)
    linhas_com_risco = []
    linhas_com_risco_ordenadas = []
    with open(plan, 'rt') as csvplan:
        reader_plan = csv.DictReader(csvplan)
        field_names = reader_plan.fieldnames
        for row in reader_plan:
            if terminal.find('BTP') != -1:
                if row['Porto Destino Final'] in portos_seguros():
                    continue
                if not ((row['Categoria'] == "CS_EXP") or (row['CH/VZ'] == "F" or "FULL")):
                    continue
            if terminal.find('SBT') != -1:
                if row['Porto final'] in portos_seguros():
                    continue
                if (not (row['Missao'] == "Exportação FCL")) or (not (row['Chvz'] == "Cheio" or "CHEIO")):
                    continue

            parametros_encontrados = {}
            for risco_row in read_risco:
                for nome_parametro_risco, nome_parametro_terminal in zip(campos_risco, campos_terminal):
                    search = risco_row[nome_parametro_risco].strip()
                    if search and (row[nome_parametro_terminal].find(search) != -1):
                        parametros_encontrados[nome_parametro_terminal] = True
            if len(parametros_encontrados) > 0:
                linha_com_risco = {}
                for key, value in row.items():
                    risco_key = parametros_encontrados.get(key, False)
                    linha_com_risco[key] = (value, risco_key)
                linhas_com_risco.append(linha_com_risco)

        with open(plan[:-4] + '[Resultado].csv', 'w') as outfile:
            writer = csv.writer(outfile)
            writer.writerow(reader_plan.fieldnames)
            for row in linhas_com_risco:
                ordered_row = []
                ordered_dict = OrderedDict()
                for name in field_names:
                    ordered_row.append(row[name][0])
                    ordered_dict[name] = row[name]
                if ordered_row:
                    writer.writerow(ordered_row)
                if ordered_dict:
                    linhas_com_risco_ordenadas.append(ordered_dict)
        return field_names, linhas_com_risco_ordenadas


def recebe_plan(planilha):
    if planilha.find('SBT') != -1:
        result = comparador(planilha, CAMPOS_RISCO, CAMPOS_SBT, terminal='SBT')
        plan = True
    else:
        result = comparador(planilha, CAMPOS_RISCO, CAMPOS_BTP, terminal='BTP')
        plan = True
    if plan:
        escreve_plan(planilha)
    return result

def color(val):
    lista_valores = []
    with open(ARQRISCO, 'rt', encoding='latin-1') as csvrisco:
        reader = csv.reader(csvrisco)
        for row in reader:
            for value in row:
                if value is not '':
                    lista_valores.append(value)
    words = [l.replace('\xa0', '') for l in lista_valores]
    words = [l.replace('\n', '') for l in words]
    for item in lista_valores:
        words.append(item)
    color = 'yellow' if val in words else 'white'
    return 'background-color: %s' % color

def escreve_plan(planilha):
    planilha_filtrada = planilha[:-4] + '[Resultado].csv'
    # DEST = os.path.join(plan)
    df = pd.read_csv(planilha_filtrada, sep=',', encoding='latin-1')
    df.style.applymap(color).to_excel(planilha_filtrada[:-4] + '.xlsx', engine='openpyxl')

def geraHTML(target, result_dict, fieldnames):
    '''Usage:
    result = comparadorXXX()
    geraHTML('result.html', result)
    '''
    with open('table.html', 'r') as f:
        text = f.read()
        template = Template(text)
        html = template.render(fieldnames=fieldnames, result_dict=result_dict)
    with open(target, 'w') as outfile:
        outfile.write(html)
    return target

    '''outfile.write('<div class="table-responsive">')
        outfile.write('<div class="w3-col m4 l3">')
        outfile.write('<table class="table table-condensed;">')
        outfile.write('<tr>')
        for name in fieldnames:
            campo = '<b>' + name + '</b>'
            style = 'style'
            outfile.write('<td>' + campo + '</td>')
        outfile.write('</tr>')
        for linha in result_dict:
            outfile.write('<tr>')
            for key, value in linha.items():
                for values in value:
                    campo = values[0]
                    if values[1] == True:
                        campo = '<b>' + campo + '</b>'
                        style = 'style="background-color:yellow;"'
                    outfile.write('<td class="mycell">' + campo + '</td>')
            outfile.write('</tr>')
        outfile.write('</table>')
        outfile.write('</div>')
        outfile.write('</div>')'''
