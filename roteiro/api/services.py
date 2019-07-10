from datetime import datetime, date
import requests

def escalona_passeios(dados):
    disponibilidade = consulta_passeios_bonitour(dados['data_de_chegada'],
                                                 dados['data_de_saida'],
                                                 dados['passeios'],
                                                 dados['numero_de_pessoas'])
    agrupamentos_por_localizacao = agrupa_por_localizacao(disponibilidade)
    passeios_por_prioridade = define_prioridade(disponibilidade)

    agenda = {}
    for id in passeios_por_prioridade:
        agenda[id] = busca_horario_disponivel(disponibilidade[id], agenda)

    return agenda


def busca_horario_disponivel(info, agenda):

    for dia in info['availability']:
        for hora in info['availability'][dia]:
            if agenda.items().__len__() > 0:
                if not verifica_conflito(dia, hora, info['duration'], agenda):
                    return {
                        "dia": datetime.strptime(dia, '%Y-%m-%d').date(),
                        "horario": datetime.strptime(hora, '%H:%M').time(),
                        "duracao": info['duration']
                    }
            else:
                return {
                    "dia": datetime.strptime(dia, '%Y-%m-%d').date(),
                    "horario": datetime.strptime(hora, '%H:%M').time(),
                    "duracao": info['duration']
                }

    return {}


def verifica_conflito(dia, hora, duracao, agenda):
    dia = datetime.strptime(dia, '%Y-%m-%d').date()
    hora = datetime.strptime(hora, '%H:%M').time()
    for id in agenda:
        if dia == agenda[id]['dia']:
            delta_t = datetime.combine(date(1, 1, 1), agenda[id]['horario']) - datetime.combine(date(1, 1, 1), hora)
            delta_t = delta_t.total_seconds() / 60
            if (delta_t > 0 and duracao > delta_t.__abs__()) or\
                    (delta_t <= 0 and agenda[id]['duracao'] > delta_t.__abs__()):
                return True
    return False


def define_prioridade(disp):
    prio = {}
    for id in disp:
        cont = 0
        for dia in disp[id]['availability']:
            cont = cont+disp[id]['availability'][dia].__len__()
        prio[id] = cont

        ordenado = [i[0] for i in sorted(prio.items(), key=lambda kv:kv[1])]

    return ordenado

def agrupa_por_localizacao(disponibilidade):
    agrupamentos = []
    for i in disponibilidade:
        mesma_localizacao = [i]
        for j in disponibilidade:
            if (
                    i != j and
                    disponibilidade[i]['location']['lat'] == disponibilidade[j]['location']['lat'] and
                    disponibilidade[i]['location']['lat'] == disponibilidade[j]['location']['lat']
            ):
                mesma_localizacao.append(j)
                mesma_localizacao.sort()
        if mesma_localizacao.__len__() > 1 and mesma_localizacao not in agrupamentos:
            agrupamentos.append(mesma_localizacao)
    return agrupamentos


def consulta_passeios_bonitour(chegada, saida, passeios_id, n_pessoas):
    """
    Cria um dicionario contendo todos passeios passados como parametro
    com seus respectivos horarios disponiveis.
    """
    consulta_passeios = {}
    for id in passeios_id:
        url = "https://bonitour-test-api.herokuapp.com/attractions/" \
              "{}?start_date={}&end_date={}".format(id, chegada, saida)
        r = requests.get(url)
        consulta_passeios[id] = r.json()

    return verifica_disponibilidade(consulta_passeios, n_pessoas)


def verifica_disponibilidade(todos_passeios, numero_de_pessoas):
    disponibilidade = {}

    for p in todos_passeios:
        dias_disponiveis = {}
        for dia in todos_passeios[p]['availability']:
            horarios_disponiveis = []
            for horarios in list(dia.values()):
                for hora in horarios:
                    n_max = list(hora.values())[0]
                    if n_max >= numero_de_pessoas:
                        horarios_disponiveis.append(list(hora.keys())[0])
            dias_disponiveis[list(dia.keys())[0]] = horarios_disponiveis
        disponibilidade[p] = {
            'name': todos_passeios[p]['name'],
            'duration': todos_passeios[p]['duration'],
            'location': todos_passeios[p]['location'],
            'availability': dias_disponiveis
        }
    return disponibilidade
