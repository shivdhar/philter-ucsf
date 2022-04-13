from flask import Flask, request, Response
import tempfile
import subprocess

from philter import Philter

app = Flask(__name__)
from pathlib import Path

OUT_FILE = Path('abc.txt')


@app.route('/get_phi', methods=['POST'])
def get_phi():
    data = request.data
    type_ = request.headers['format']

    assert type_ in ('asterisk', 'i2b2'), type_

    print('data is', data)

    out_text = _get_phi(data, type_)
    return Response(out_text, mimetype='text/xml')


def _get_phi(data: bytes, type_: str):
    with tempfile.TemporaryDirectory(
        prefix='input_'
    ) as in_dir, tempfile.TemporaryDirectory(
        prefix='output_'
    ) as out_dir, tempfile.NamedTemporaryFile(
        dir=in_dir, suffix='.txt'
    ) as in_f:
        # tempfile.NamedTemporaryFile(dir=out_dir) as out_f,:
        Path(in_f.name).write_bytes(data)
        in_f.flush()
        print(in_f.name)
        # assert isinstance(in_dir.name, str), in_dir.name
        run_phi_as_subprocess(inp_fname=in_dir, out_fname=out_dir, out_format=type_)
        print(list(Path(out_dir).rglob('*')))
        type_suffix = {'asterisk': '.txt', 'i2b2': '.xml'}[type_]
        out_filename = Path(out_dir, Path(in_f.name).with_suffix(type_suffix).name)
        assert out_filename.exists(), (Path(in_f.name).resolve(), out_filename)

        # out_f.flush()
        in_text = Path(in_f.name).read_text('utf-8')
        out_text = Path(out_filename).read_text('utf-8')
        assert isinstance(out_text, str), type(out_text)
    print(f'"{in_text}" "{out_text}"')
    return out_text

def run_phi_as_subprocess(inp_fname: str, out_fname: str, out_format: str):
    cp = subprocess.run(
        [
            'python3',
            'main.py',
            '-i',
            inp_fname,
            '-o',
            out_fname,
            '-f',
            './configs/philter_delta.json',
            '--outputformat',
            out_format,
            '--prod=True',
        ],
        check=True,
    )
