import io


def last_lines(filename, buffer_size=io.DEFAULT_BUFFER_SIZE):
    """Devolve um iterator com as linhas do arquivo em ordem inversa (como o `tac`),
    mantendo o terminador de cada linha. Lê o arquivo de trás para frente em blocos
    de no máximo `buffer_size` bytes e só decodifica linhas completas, de modo que
    caracteres UTF-8 multibyte nunca são partidos.
    """
    with open(filename, 'rb') as f:
        f.seek(0, io.SEEK_END)
        position = f.tell()
        remainder = b''

        while position > 0:
            read_size = min(buffer_size, position)
            position -= read_size
            f.seek(position)
            chunk = f.read(read_size)
            buffer = chunk + remainder
            lines = buffer.splitlines(keepends=True)
            remainder = lines.pop(0)  # segura a ponta esquerda (caso incompleta)
            for line in reversed(lines):
                yield line.decode('utf-8')
            
        if remainder:
            yield remainder.decode('utf-8')

if __name__ == '__main__':
    lines = last_lines('my_file.txt')
    # next(lines)
    # next(lines)
    # next(lines)