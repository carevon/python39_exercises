# Desafios de Programação

Solução dos três desafios técnicos de programação, implementados em **Python 3.9**
usando **apenas bibliotecas built-in**, o ambiente de execução está sendo
criado com o comando `conda create -n myenv python=3.9`, sem a adição de pacotes adicionais).

## Estrutura

| Arquivo | Descrição |
|---|---|
| `reconciliation.py` | Desafio 1 — `reconcile_accounts` |
| `last_lines.py` | Desafio 2 — `last_lines` |
| `computed_property.py` | Desafio 3 — `computed_property` |
| `test_*.py` | Suítes de teste correspondentes (27 testes no total) |
| `transactions1.csv`, `transactions2.csv`, `my_file.txt` | Fixtures de exemplo |

---

## Ambiente e execução

Para rodar toda a suíte de testes:

```bash
python -m unittest discover -p "test_*.py" -v
```


## Desafio 1 — `reconcile_accounts`

Faz a conciliação (batimento) entre dois grupos de transações financeiras, devolvendo
cópias das duas listas com uma coluna `FOUND`/`MISSING` acrescentada ao resultado do output.

**Decisões de projeto:**

- **Identidade da transação** o grupo `(departamento, valor, beneficiário)`;  a **data**
  pode diferir em ±1 dia (a mesma transação costuma ser registrada com um dia de defasagem
  entre sistemas). Por isso as datas são convertidas para `datetime.date` — comparar como
  string quebraria na virada de mês/ano (`31/12 ↔ 01/01`).
- **Valor comparado como string**, não como float: o enunciado trata tudo como string e a
  comparação exata evita erros de ponto flutuante.
- **Casamento como um problema de matching um-para-um por chave.** Agrupando por chave, o
  problema vira subproblemas independentes onde só a data varia. Uma **janela deslizante**
  (`deque`) percorre as transações em ordem de data e casa cada uma com a parceira
  disponível **mais antiga** dentro de `[data-1, data+1]`.
- A regra "preferir a data mais cedo" do enunciado não é só um desempate: ela **maximiza o
  número de batimentos** (ao ceder a parceira exata, libera datas posteriores para
  transações posteriores). Complexidade **O(n log n)**, dominada pela ordenação.
- A saída é montada com `linha + [rótulo]`, criando **listas novas** — a entrada não é
  mutada, como o enunciado pede ("devolver cópias").

## Desafio 2 — `last_lines`

Devolve um **iterator** com as linhas de um arquivo em ordem inversa (equivalente ao `tac`),
lendo em pedaços de no máximo `buffer_size` bytes.

**Decisões de projeto:**

- **Leitura binária de trás para frente, em blocos limitados.** O enunciado exige não ler
  mais que `buffer_size` bytes por vez; ler o arquivo inteiro (`readlines()`) ignoraria esse
  requisito. Como iterator preguiçoso, consumir só a última linha lê apenas o último bloco —
  relevante para arquivos grandes (ex.: logs).
- **Corte em `b'\n'` a nível de byte é seguro por construção.** Em UTF-8, o byte de nova
  linha (`0x0A`) nunca aparece dentro de um caractere multibyte, então separar linhas em
  bytes nunca parte um caractere. Cada linha completa é decodificada com `.decode('utf-8')`,
  atendendo ao requisito de não decodificar caractere pela metade.
- Linhas que atravessam a fronteira de dois blocos são costuradas por um `remainder`, e a
  primeira linha do arquivo é emitida ao final do laço.
- Implementado como **generator**, que já é um iterator (`next()` funciona nativamente) e
  mantém o arquivo aberto apenas enquanto está sendo consumido.

## Desafio 3 — `computed_property`

Um decorator análogo ao `property` que **cacheia** o valor calculado enquanto os atributos
dos quais ele depende não mudarem — recriando, em memória, o mecanismo de invalidação por
dependências do SecDB descrito no enunciado.

**Decisões de projeto:**

- **Classe descritora** (implementa `__get__`/`__set__`/`__delete__`), porque precisa de
  estado (dependências, getter/setter/deleter) e do protocolo de descritor. O nome é
  minúsculo para espelhar o `property` embutido (que também é uma classe minúscula).
- **Decorator com argumentos em duas fases:** `computed_property('x','y','z')` guarda as
  dependências no `__init__`; o `@` aplica à função via `__call__`, que guarda o getter.
- **Cache na própria instância**, sob uma chave derivada do nome do atributo (obtido via
  `__set_name__`). A cada leitura, tira-se uma "foto" das dependências; se bater com a
  guardada, devolve o valor cacheado, senão recomputa.
- **Dependência inexistente é tratada como inalterada** usando um sentinela
  (`getattr(obj, dep, _MISSING)`): como é sempre o mesmo objeto, um atributo ausente nunca
  provoca invalidação.
- **`__set__` e `__delete__` sempre definidos** (levantando `AttributeError` quando não há
  setter/deleter) tornam a classe um *data descriptor* — o que faz o atributo aparecer sob
  "Data descriptors" no `help()` e dá precedência ao descritor sobre o `__dict__` da
  instância. `setter`/`deleter` seguem o mesmo padrão encadeado do `property`.
