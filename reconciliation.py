import csv
from datetime import date, timedelta
from collections import defaultdict, deque
from pprint import pprint


FOUND = "FOUND"
MISSING = "MISSING"
ONE_DAY = timedelta(1)


def index_transactions_by_key(transactions):
    """ Agrupa as transações por (departamento, valor, beneficiario) e ordena cada bucket por (data, index) """
    entries_hash = defaultdict(list)
    for idx, transaction in enumerate(transactions):
        date_obj = date.fromisoformat(transaction[0])

        department = transaction[1]
        value = transaction[2]
        recipient = transaction[3]
        
        entries_hash[(department, value, recipient)].append((date_obj, idx))

    for entries in entries_hash.values():
        entries.sort()

    return entries_hash


def label_transactions(transactions, matched_indices):
    """Devolve cópias das linhas com FOUND ou MISSING acrescentado conforme o índice casou."""
    return [row + [FOUND if i in matched_indices else MISSING]
            for i, row in enumerate(transactions)]

def match_entries(primary_entries, secondary_entries):
    """Casa as entradas (data, índice) de uma mesma chave via janela deslizante de ±1 dia,
    devolvendo os pares (índice_primary, índice_secondary) casados."""
    matches = []
    window = deque()
    j = 0
    for a_date, a_idx in primary_entries:
        while j < len(secondary_entries) and secondary_entries[j][0] <= a_date + ONE_DAY:
            window.append(secondary_entries[j])
            j += 1
        while window and window[0][0] < a_date - ONE_DAY:
            window.popleft()
        if window:
            _, b_idx = window.popleft()
            matches.append((a_idx, b_idx))
    return matches


def reconcile_accounts(primary_transactions_list, secondary_transactions_list):
    """
    Concilia duas listas de transações, devolvendo cópias de cada uma com uma
    coluna FOUND/MISSING acrescentada à direita. Duas transações batem quando
    departamento, valor e beneficiário são iguais e as datas diferem em no máximo
    um dia; o casamento é um-para-um e prefere a parceira disponível mais antiga.
    """
    primary_hash = index_transactions_by_key(primary_transactions_list)
    secondary_hash = index_transactions_by_key(secondary_transactions_list)

    matched_primary = set()
    matched_secondary = set()
    for key, primary_entries in primary_hash.items():
        secondary_entries = secondary_hash.get(key)
        if not secondary_entries:
            continue
        
        for a_idx, b_idx in match_entries(primary_entries, secondary_entries):
            matched_primary.add(a_idx)
            matched_secondary.add(b_idx)
                
    primary_result_list = label_transactions(primary_transactions_list, matched_primary)
    secondary_result_list = label_transactions(secondary_transactions_list, matched_secondary)

    return primary_result_list, secondary_result_list



if __name__ == '__main__':

    with open('transactions1.csv', newline='') as f:
        transactions1 = list(csv.reader(f))
    
    with open('transactions2.csv', newline='') as f:
        transactions2 = list(csv.reader(f))

    out1, out2 = reconcile_accounts(transactions1, transactions2)

    pprint(out1)
    pprint(out2)