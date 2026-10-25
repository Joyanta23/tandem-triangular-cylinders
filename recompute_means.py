"""Recompute means and fluctuation RMS from the archived report histories."""
from pathlib import Path
import csv
import json
import numpy as np

ROOT = Path(__file__).resolve().parent


def main():
    windows = json.loads((ROOT / 'windows.json').read_text())
    with (ROOT / 'summary_results.csv').open(newline='') as stream:
        expected = {(row['case'], row['quantity']): row
                    for row in csv.DictReader(stream)}
    count = 0
    for case, (start, end) in windows.items():
        paths = sorted((ROOT / 'data' / case).glob('*.csv.gz'))
        if not paths:
            raise FileNotFoundError(f'No report histories for {case}')
        for path in paths:
            values = np.loadtxt(path, delimiter=',', skiprows=1)
            if values.ndim != 2 or values.shape[1] != 3:
                raise ValueError(f'Expected three columns in {path}')
            if not np.isfinite(values).all():
                raise ValueError(f'Non-finite value in {path}')
            sample = values[(values[:, 0] >= start) & (values[:, 0] < end)]
            if len(sample) != end - start or not np.all(np.diff(sample[:, 0]) == 1):
                raise ValueError(f'Missing or repeated steps in {path}')
            quantity = path.name.removesuffix('.csv.gz')
            mean = float(sample[:, 1].mean())
            rms = float(sample[:, 1].std(ddof=0))
            reference = expected[(case, quantity)]
            if not np.isclose(mean, float(reference['mean']), rtol=0, atol=1e-10):
                raise ValueError(f'Mean does not match: {case}/{quantity}')
            if not np.isclose(rms, float(reference['fluctuation_rms']), rtol=0, atol=1e-10):
                raise ValueError(f'RMS does not match: {case}/{quantity}')
            print(f'{case:20s} {quantity:15s} mean={mean:.10g} fluctuation_rms={rms:.10g}')
            count += 1
    if count != len(expected):
        raise ValueError('Some summary rows have no corresponding history')
    print(f'Checked {count} signal summaries.')


if __name__ == '__main__':
    main()
