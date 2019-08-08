from datetime import datetime, date
import requests

def escalona_passeios(dados):
    """
    Gerencia tratamentos e o escalonamento dos passeios.
    """

    disponibilidade = consulta_passeios(
                                            dados['data_de_chegada'],
                                            dados['data_de_saida'],
                                            dados['passeios']
                                        )

    # passeios_por_prioridade = define_prioridade(disponibilidade)
    #
    # agenda = {}
    # for id in passeios_por_prioridade:
    #     r = busca_horario_disponivel(disponibilidade[id], id, agenda)
    #     if r.items().__len__() > 0:
    #         agenda[id] = r
    #     else:
    #         agenda[id] = {
    #             "id_passeio": id,
    #             "nome": disponibilidade[id]['name'],
    #             "duracao": disponibilidade[id]['duration'],
    #             "mensagem": 'nao foi possivel alocar o passeio, horarios indisponiveis'}

    # return [agenda[id] for id in agenda]
    return disponibilidade


def consulta_passeios(chegada, saida, passeios_id):
    """
    Cria um dicionario contendo todos passeios passados como parametro
    com seus respectivos horarios disponiveis.
    """
    passeios_disponiveis = []
    for id in passeios_id:
        url = "http://127.0.0.1:8000/passeios/{}/?start_date={}&end_date={}".format(id, chegada, saida)
        r = requests.get(url)
        passeios_disponiveis.append(r.json())

    return passeios_disponiveis


def busca_horario_disponivel(info, id, agenda):
    """
    Dada as informações dos horarios disponiveis para um determinado passeio, a função retorna o primeiro horário
    disponivel que não possui conflito com outros passeios.
    """

    for dia in info['availability']:
        for hora in info['availability'][dia]:
            if agenda.items().__len__() > 0:
                if not verifica_conflito(dia, hora, info['duration'], agenda):
                    return {
                        "id_passeio": id,
                        "nome": info['name'],
                        "dia": datetime.strptime(dia, '%Y-%m-%d').date(),
                        "horario": datetime.strptime(hora, '%H:%M').time(),
                        "duracao": info['duration'],
                        "localizacao": info['location']
                    }
            else:
                return {
                    "id_passeio": id,
                    "nome": info['name'],
                    "dia": datetime.strptime(dia, '%Y-%m-%d').date(),
                    "horario": datetime.strptime(hora, '%H:%M').time(),
                    "duracao": info['duration'],
                    "localizacao": info['location']
                }

    return {}


def verifica_conflito(dia, hora, duracao, agenda):
    """
    A partir de um dia e uma hora, percorre todos os passeios agendados verificando conflitos.
    Caso haja conflitos retorna TRUE.
    """
    dia = datetime.strptime(dia, '%Y-%m-%d').date()
    hora = datetime.strptime(hora, '%H:%M').time()
    for id in agenda:
        if agenda[id].items().__len__() > 4 and dia == agenda[id]['dia']:
            delta_t = datetime.combine(date(1, 1, 1), agenda[id]['horario']) - datetime.combine(date(1, 1, 1), hora)
            delta_t = delta_t.total_seconds() / 60
            if (delta_t > 0 and duracao > delta_t.__abs__()) or\
                    (delta_t <= 0 and agenda[id]['duracao'] > delta_t.__abs__()):
                return True
    return False


def define_prioridade(disp):
    """
    Faz a contagem de horarios disponiveis para cada passeios e retorna uma lista ordenada
    pela contagem (disponibilidade).
    Considera menore contagem com maior prioridade de alocação.
    """
    prio = {}
    for id in disp:
        cont = 0
        for dia in disp[id]['availability']:
            cont = cont+disp[id]['availability'][dia].__len__()
        prio[id] = cont

        ordenado = [i[0] for i in sorted(prio.items(), key=lambda kv:kv[1])]

    return ordenado


def verifica_disponibilidade(todos_passeios, numero_de_pessoas):
    """
    Dado todos os horarios existentes para cada passeio, é realizada a filtragem dos horários
    pela quantidade de pessoas passadas no roteiro.
    """
    disponibilidade = {}

    for p in todos_passeios:
        dias_disponiveis = {}
        for dia in todos_passeios[p].get('availability'):
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
