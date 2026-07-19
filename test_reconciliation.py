import unittest
from reconciliation import reconcile_accounts

def labels(rows):
    """ Extrair apenas a coluna de status (última) de cada linha, para asserts sucintos """
    return [row[-1] for row in rows]

class TestReconcileAccounts(unittest.TestCase):

    def test_exemplo_enunciado(self):
        t1 = [['2020-12-04', 'Tecnologia', '16.00', 'Bitbucket'],
              ['2020-12-04', 'Jurídico', '60.00', 'LinkSquares'],
              ['2020-12-05', 'Tecnologia', '50.00', 'AWS']]
        t2 = [['2020-12-04', 'Tecnologia', '16.00', 'Bitbucket'],
              ['2020-12-05', 'Tecnologia', '49.99', 'AWS'],
              ['2020-12-04', 'Jurídico', '60.00', 'LinkSquares']]
        
        out1, out2 = reconcile_accounts(t1, t2)
        self.assertEqual(labels(out1), ['FOUND', 'FOUND', 'MISSING'])
        self.assertEqual(labels(out2), ['FOUND', 'MISSING', 'FOUND'])

    def test_casa_dia_anterior(self):
        t1 = [['2020-12-25', 'Tecnologia', '16.00', 'Bitbucket'],
              ['2020-12-25', 'Jurídico', '60.00', 'LinkSquares'],
              ['2020-12-25', 'Tecnologia', '50.00', 'AWS']]
        t2 = [['2020-12-24', 'Tecnologia', '16.00', 'Bitbucket'],
              ['2020-12-24', 'Tecnologia', '49.99', 'AWS'],
              ['2020-12-24', 'Jurídico', '60.00', 'LinkSquares']]
        
        out1, out2 = reconcile_accounts(t1, t2)
        self.assertEqual(labels(out1), ['FOUND', 'FOUND', 'MISSING'])
        self.assertEqual(labels(out2), ['FOUND', 'MISSING', 'FOUND'])

    def test_casa_dia_posterior(self):
        t1 = [['2020-12-25', 'Tecnologia', '16.00', 'Bitbucket'],
              ['2020-12-25', 'Jurídico', '60.00', 'LinkSquares'],
              ['2020-12-25', 'Tecnologia', '50.00', 'AWS']]
        t2 = [['2020-12-26', 'Tecnologia', '16.00', 'Bitbucket'],
              ['2020-12-26', 'Tecnologia', '49.99', 'AWS'],
              ['2020-12-26', 'Jurídico', '60.00', 'LinkSquares']]
        
        out1, out2 = reconcile_accounts(t1, t2)
        self.assertEqual(labels(out1), ['FOUND', 'FOUND', 'MISSING'])
        self.assertEqual(labels(out2), ['FOUND', 'MISSING', 'FOUND'])

    def test_fora_da_janela(self):
        t1 = [['2020-12-20', 'Tecnologia', '16.00', 'Bitbucket'],
              ['2020-12-20', 'Jurídico', '60.00', 'LinkSquares'],
              ['2020-12-20', 'Tecnologia', '50.00', 'AWS']]
        t2 = [['2020-12-22', 'Tecnologia', '16.00', 'Bitbucket'],
              ['2020-12-22', 'Tecnologia', '49.99', 'AWS'],
              ['2020-12-22', 'Jurídico', '60.00', 'LinkSquares']]
        
        out1, out2 = reconcile_accounts(t1, t2)
        self.assertEqual(labels(out1), ['MISSING', 'MISSING', 'MISSING'])
        self.assertEqual(labels(out2), ['MISSING', 'MISSING', 'MISSING'])

    def test_colunas_diferentes(self):
        t1 = [['2020-12-25', 'Tecnologia', '16.00', 'Bitbucket']]
        t2 = [['2020-12-25', 'Tecnologia', '15.99', 'Bitbucket']]
        
        out1, out2 = reconcile_accounts(t1, t2)
        self.assertEqual(labels(out1), ['MISSING'])
        self.assertEqual(labels(out2), ['MISSING'])

    def test_virada_de_ano(self):
        t1 = [['2020-12-31', 'Tecnologia', '16.00', 'Bitbucket'],
              ['2020-12-31', 'Jurídico', '60.00', 'LinkSquares'],
              ['2020-12-31', 'Tecnologia', '50.00', 'AWS']]
        t2 = [['2021-01-01', 'Tecnologia', '16.00', 'Bitbucket'],
              ['2021-01-01', 'Tecnologia', '49.99', 'AWS'],
              ['2021-01-01', 'Jurídico', '60.00', 'LinkSquares']]
        
        out1, out2 = reconcile_accounts(t1, t2)
        self.assertEqual(labels(out1), ['FOUND', 'FOUND', 'MISSING'])
        self.assertEqual(labels(out2), ['FOUND', 'MISSING', 'FOUND'])

    def test_duplicata_sem_par(self):
        t1 = [['2020-12-31', 'Tecnologia', '16.00', 'Bitbucket'],
              ['2020-12-31', 'Jurídico', '60.00', 'LinkSquares'],
              ['2020-12-31', 'Tecnologia', '16.00', 'Bitbucket']]
        t2 = [['2021-01-01', 'Tecnologia', '16.00', 'Bitbucket'],
              ['2021-01-01', 'Tecnologia', '49.99', 'AWS'],
              ['2021-01-01', 'Jurídico', '60.00', 'LinkSquares']]
        
        out1, out2 = reconcile_accounts(t1, t2)
        self.assertEqual(labels(out1), ['FOUND', 'FOUND', 'MISSING'])
        self.assertEqual(labels(out2), ['FOUND', 'MISSING', 'FOUND'])

    def test_desempate_com_data_mais_cedo(self):
        t1 = [['2020-12-25', 'Tecnologia', '16.00', 'Bitbucket']]
        t2 = [['2020-12-24', 'Tecnologia', '16.00', 'Bitbucket'],
              ['2020-12-25', 'Tecnologia', '16.00', 'Bitbucket']]
        
        out1, out2 = reconcile_accounts(t1, t2)
        self.assertEqual(labels(out1), ['FOUND'])
        self.assertEqual(labels(out2), ['FOUND', 'MISSING'])

    def test_mais_cedo_maximizado(self):
        t1 = [['2020-12-24', 'Tecnologia', '16.00', 'Bitbucket'],
              ['2020-12-25', 'Tecnologia', '16.00', 'Bitbucket']]
        t2 = [['2020-12-23', 'Tecnologia', '16.00', 'Bitbucket'],
              ['2020-12-24', 'Tecnologia', '16.00', 'Bitbucket']]
        
        out1, out2 = reconcile_accounts(t1, t2)
        self.assertEqual(labels(out1), ['FOUND', 'FOUND'])
        self.assertEqual(labels(out2), ['FOUND', 'FOUND'])

    def test_nao_muta_entrada(self):
        t1 = [['2020-12-04', 'Tec', '16.00', 'Bitbucket']]
        t2 = [['2020-12-04', 'Tec', '16.00', 'Bitbucket']]
        reconcile_accounts(t1, t2)
        self.assertEqual(t1, [['2020-12-04', 'Tec', '16.00', 'Bitbucket']])  # 4 colunas, intacta
        self.assertEqual(len(t1[0]), 4)

    def test_listas_vazias(self):
        # Ambas vazias -> devolve duas listas vazias
        out1, out2 = reconcile_accounts([], [])
        self.assertEqual(out1, [])
        self.assertEqual(out2, [])

        # Uma vazia contra uma cheia -> tudo MISSING na cheia, vazia continua vazia
        t2 = [['2020-12-04', 'Tecnologia', '16.00', 'Bitbucket'],
              ['2020-12-05', 'Tecnologia', '50.00', 'AWS']]
        out1, out2 = reconcile_accounts([], t2)
        self.assertEqual(out1, [])
        self.assertEqual(labels(out2), ['MISSING', 'MISSING'])

if __name__ == '__main__':
    unittest.main()