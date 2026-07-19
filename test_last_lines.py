import os
import tempfile
import unittest
from collections.abc import Iterator

from last_lines import last_lines


class TestLastLines(unittest.TestCase):

    def setUp(self):
        self._paths = []

    def tearDown(self):
        for path in self._paths:
            os.remove(path)

    def _write(self, content_bytes):
        """Cria um arquivo temporário com o conteúdo recebido e devolve o caminho."""
        fd, path = tempfile.mkstemp()
        with os.fdopen(fd, 'wb') as f:
            f.write(content_bytes)
        self._paths.append(path)
        return path

    def test_exemplo_enunciado(self):
        path = self._write(b"This is a file\nThis is line 2\nAnd this is line 3\n")

        resultado = list(last_lines(path))

        self.assertEqual(resultado, [
            'And this is line 3\n',
            'This is line 2\n',
            'This is a file\n',
        ])

    def test_next_explicito(self):
        path = self._write(b"This is a file\nThis is line 2\nAnd this is line 3\n")
        it = last_lines(path)
        self.assertEqual(next(it), 'And this is line 3\n')
        self.assertEqual(next(it), 'This is line 2\n')
        self.assertEqual(next(it), 'This is a file\n')
        it.close()

    def test_resultado_buffer_pequeno(self):
        path = self._write(b"This is a file\nThis is line 2\nAnd this is line 3\n")

        resultado = list(last_lines(path, buffer_size=3))

        self.assertEqual(resultado, [
            'And this is line 3\n',
            'This is line 2\n',
            'This is a file\n',
        ])

    def test_sem_newline_final(self):
        path = self._write(b"a\nb\nc")

        resultado = list(last_lines(path))

        self.assertEqual(resultado, ['c', 'b\n', 'a\n'])

    def test_arquivo_vazio(self):
        path = self._write(b"")

        resultado = list(last_lines(path))

        self.assertEqual(resultado, [])

    def test_retorna_iterator(self):
        path = self._write(b"This is a file\nThis is line 2\nAnd this is line 3\n")
        self.assertIsInstance(last_lines(path), Iterator)

    def test_utf8_multibyte(self):
        content = "café ☕\nfesta 🎉🎉\n".encode('utf-8')
        path = self._write(content)
        expected_result = [l.decode('utf-8') for l in reversed(content.splitlines(keepends=True))]
        self.assertEqual(list(last_lines(path, buffer_size=1)), expected_result)

if __name__ == '__main__':
    unittest.main()
