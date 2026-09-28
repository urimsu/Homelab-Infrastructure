# Monitoring endpoint unreachable

## Problem

Prometheus cannot scrape an exporter, or a monitoring UI cannot be reached by an authorized operator.

## Symptoms

Target shows down, scrape errors, or the UI connection fails.

## Architecture / Context

Node Exporter → Prometheus → Grafana, with Uptime Kuma checking selected services. Typical example ports are 9100 and 9090; confirm actual settings locally.

## Hypotheses

Exporter stopped; wrong target address/port; bind address; route/firewall; scrape path; DNS mismatch; management access path missing.

## Investigation

Check process and listener on target, curl the metrics endpoint from Prometheus, inspect routes and firewall, then inspect scrape configuration and logs.

## Commands Used

```bash
systemctl status <EXPORTER_SERVICE>
ss -tulpn
curl -v http://<EXPORTER_IP>:9100/metrics
ip route
```

## Root Cause

Target-specific; distinguish scrape connectivity from dashboard availability.

## Solution

Correct the service, target, or private route/firewall policy. Keep metrics endpoints on trusted networks.

## Verification

Confirm target health in Prometheus and inspect a current sample; separately test the Grafana path over VPN.

## Security Considerations

Metrics can expose host details. Do not make exporter endpoints public.

## What I Learned

Monitoring itself has network dependencies and needs availability checks.
