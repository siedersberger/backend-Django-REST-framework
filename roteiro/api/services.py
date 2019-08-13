from datetime import datetime, date
import requests

def escalona_passeios(disponibilidade):
    """
    Gerencia tratamentos e o escalonamento dos passeios.
    """

    passeios_por_prioridade = define_prioridade(disponibilidade)


    agenda = {}
    for id in passeios_por_prioridade:
        r = busca_horario_disponivel(disponibilidade[id], id, agenda)
        if r.items().__len__() > 0:
            agenda[id] = r
        else:
            agenda[id] = {
                "passeio": id,
                "duracao": disponibilidade[id]['duracao'],
                "mensagem": 'nao foi possivel alocar o passeio, horarios indisponiveis'}

    return [agenda[id] for id in agenda]
    # return passeios_por_prioridade

def busca_horario_disponivel(info, id, agenda):
    """
    Dada as informações dos horarios disponiveis para um determinado passeio, a função retorna o primeiro horário
    disponivel que não possui conflito com outros passeios.
    """

    for dia in info['disponibilidade']:
        for hora in info['disponibilidade'][dia]:
            if agenda.items().__len__() > 0:
                if not verifica_conflito(dia, hora, info['duracao'], agenda):
                    return {
                        "passeio": id,
                        "dia": datetime.strptime(dia, '%Y-%m-%d').date(),
                        "horario": hora,
                        "duracao": info['duracao'],
                    }
            else:
                return {
                    "passeio": id,
                    "dia": datetime.strptime(dia, '%Y-%m-%d').date(),
                    "horario": hora,
                    "duracao": info['duracao'],
                }

    return {}


def verifica_conflito(dia, hora, duracao, agenda):
    """
    A partir de um dia e uma hora, percorre todos os passeios agendados verificando conflitos.
    Caso haja conflitos retorna TRUE.
    """
    dia = datetime.strptime(dia, '%Y-%m-%d').date()
    for id in agenda:
        if agenda[id].items().__len__() == 4 and dia == agenda[id]['dia']:
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
        for dia in disp[id]['disponibilidade']:
            cont = cont+disp[id]['disponibilidade'][dia].__len__()
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

def formata_agenda(agenda, dados):

    n_reservas = agenda.__len__()
    for r in range(n_reservas - 1, -1, -1):
        if agenda[r].__len__() < 4:
            agenda.pop(r)

    roteiro = {
        "data_de_chegada": dados['data_de_chegada'],
        "data_de_saida": dados['data_de_saida'],
        "numero_de_pessoas": dados['numero_de_pessoas'],
        "reservas": agenda
    }

    return roteiro