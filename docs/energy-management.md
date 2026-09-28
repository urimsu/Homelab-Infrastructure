# Energy management

Observed server draw was around 156 W with peaks around 236 W. Temperature observations included CPU cores around 27–34 °C and another sensor near 51 °C. These are historical observations under particular, undocumented measurement conditions, not guaranteed operating ranges.

## Performance, availability, and energy

Always-on availability is convenient but consumes power. Scheduled shutdown and Wake-on-LAN can reduce runtime, while adding boot delay and recovery dependencies. CPU frequency governors such as `performance` and `schedutil` express different scaling policies. Dynamic governors can lower frequency at low demand and allow higher frequency when workload requires it, subject to kernel and hardware policy; they do not permanently cap maximum performance.

Investigations used `cpupower frequency-info` and `cpupower frequency-set -g schedutil`. Confirm supported governors and measure workload, temperature, and wall power before drawing conclusions. BIOS settings and automatic startup behavior also affect results.

Annual energy estimate:

```text
kWh/year = average watts × hours powered per day × 365 ÷ 1000
```

Use measured average consumption and actual runtime. Peak draw is not the same as average draw.
