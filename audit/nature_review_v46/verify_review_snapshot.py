"""Read-only reconstruction of the immutable self-review evidence packet."""
from pathlib import Path
from hashlib import sha256

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]

def main():
    count=0
    for line in (HERE/'packet_SHA256SUMS').read_text(encoding='utf-8').splitlines():
        digest,name=line.split('  ',1)
        relative=Path(name)
        if relative.is_absolute() or '..' in relative.parts:
            raise RuntimeError('Unsafe packet path')
        if name.startswith('archive/'):
            relative=Path(name[len('archive/'):])
            saved=HERE/'submitted'/relative
            path=saved if saved.is_file() else ROOT/relative
        else:
            path=HERE/relative
        if not path.is_file() or sha256(path.read_bytes()).hexdigest()!=digest:
            raise RuntimeError('Review source mismatch '+name)
        count+=1
    print('IMMUTABLE_REVIEW_PACKET_PASS',count)

if __name__=='__main__':
    main()
