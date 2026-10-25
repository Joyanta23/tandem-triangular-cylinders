# Tandem triangular cylinders

Report histories and analysis code for two heated triangular cylinders arranged in tandem in a channel.

**Data upload in progress.** Case folders are being added in separate commits.

## Study

The simulations use ANSYS Fluent 2023 R1 for two-dimensional transient laminar flow with heat transfer. The channel is 150 mm long and 20 mm high. Both cylinders have a transverse width of 5 mm and a fixed wall temperature of 302 K. Air enters at 300 K with a parabolic velocity profile.

Seven production cases vary one parameter at a time about the reference case:

| Parameter | Values | Other conditions |
| --- | --- | --- |
| Apex angle | 30, 60, 90 degrees | G/B = 3, Re_bulk = 120 |
| Clear gap G/B | 1, 3, 5 | Apex angle = 60 degrees, Re_bulk = 120 |
| Reynolds number | 80, 120, 160 | Apex angle = 60 degrees, G/B = 3 |

The reference case belongs to all three comparisons and was simulated once. This is not a full factorial dataset. G is the clear distance from the first triangle's rear base to the second triangle's upstream apex. Reynolds number for the tandem cases uses bulk inlet velocity and transverse width.

Coarse and fine mesh histories and a half-time-step comparison are included. `SINGLE_RE100` contains the separate single-cylinder comparison; its Reynolds number uses maximum inlet velocity.

## Files

- `data/`: gzip-compressed CSV report histories, organized by case.
- `windows.json`: averaging intervals, including the left endpoint and excluding the right endpoint.
- `summary_results.csv`: means and fluctuation RMS for all 63 signals.
- `recompute_means.py`: checks the averaging windows and reproduces the summary values.
- `data_manifest.json`: file sizes, SHA-256 hashes, row counts and saved time ranges.

Each report has three columns: `time_step`, `value`, and `flow_time_s`. Tandem cases contain drag coefficient, lift coefficient and area-averaged Nusselt number for each cylinder. The single-cylinder case contains three corresponding signals.

Fluctuation RMS is computed about the window mean, using the population standard deviation. It is not the RMS of the uncentered signal. Histories are supplied as saved samples; no interpolation or smoothing is applied by the calculation script.

## Reproduce the statistics

Use Python 3.9 or later. Download this repository, extract it, and run from its root directory:

```bash
python -m pip install -r requirements.txt
python recompute_means.py
```

The script reads `.csv.gz` directly. It reports a mismatch if a window has missing steps or if a calculated statistic differs from the supplied summary by more than 1e-10.

## Time and averaging

The tandem Re = 80 and Re = 120 production cases use a time step of 0.000142622294 s. Re = 160 and the half-step comparison use 0.000071311147 s. The single-cylinder comparison uses 0.0005 s.

Use the saved `flow_time_s` column. The half-step continuation retains an inherited time offset, so its full flow time is not its cumulative step index multiplied by the new time step.

The G/B = 5 averaging window covers a selected slow modulation interval. A single shedding frequency is not assigned to that case. Most other tandem windows follow three complete downstream lift cycles and are shared by all six signals. The single-cylinder window contains four lift cycles.

## Scope

These files contain scalar report histories. They do not contain Fluent case/data pairs or instantaneous velocity and temperature fields. Cell counts for the reference mesh comparison are 26,577, 44,734 and 71,749. The geometry variants use their own meshes.

Author: Joyanta Roy Chowdhury, Independent Researcher, Bangladesh.

The accompanying manuscript is in preparation. No journal publication or dataset DOI is claimed here. Citation details for this dataset are provided in `CITATION.cff`.
