---
name: tcpdump
title: tcpdump
area: tools
tags: [network, packets, debugging, dns, tls]
detect: []
related: [strace, curl-httpie, lsof, ngrok]
---
tcpdump: captures packets with BPF filters, to see what really crosses the wire (DNS, handshakes, resets, retransmits).

## Verify
- `sudo tcpdump -D`: interfaces available for capture.
- `sudo tcpdump -i any -nn port 53`: DNS queries and answers on any interface, no name resolution.
- `sudo tcpdump -i eth0 -nn host 10.0.0.5 and tcp port 443`: one host and port.
- `sudo tcpdump -i any -nn -c 50 -w /tmp/cap.pcap port 8080`: save 50 packets for later reading.
- `tcpdump -nn -r /tmp/cap.pcap`: read a saved capture without root.

## Test first
Generate the traffic while capturing, and confirm the packets of interest appear.
```
sudo tcpdump -i lo -nn -c 10 'tcp port 8080' &
curl -s http://127.0.0.1:8080/health >/dev/null
wait
# expect SYN, SYN-ACK, ACK, then data; [R.] means reset, no reply means filtered or down
```

## Do
- Always pass `-nn` to skip DNS and service lookups, which add noise and traffic.
- Choose the interface: `-i lo` for local, `-i any` when unsure, a named one for a bridge or VPN.
- Filter in the capture (BPF) so the file stays small: `host`, `port`, `net`, `tcp`, `udp`, joined with `and`, `or`, `not`.
- Use `-w file.pcap` and analyze later (tcpdump `-r`, or Wireshark), and bound the capture with `-c` or `-G`.
- Add `-A` to see ASCII payloads or `-X` for hex, only on traffic you may inspect.
- Read TCP flags: `[S]` SYN, `[S.]` SYN-ACK, `[.]` ACK, `[P.]` data, `[F.]` close, `[R]` reset.
- Compare the client side and server side captures to find where packets disappear.

## Avoid
- Capturing without a filter on a busy host: huge files and dropped packets. Filter by host and port.
- Expecting to read TLS payloads: they are encrypted. Check the handshake and SNI instead, or use app-level logging and keylog files.
- Forgetting `-s` expectations on old builds: modern tcpdump captures full packets, but if packets look truncated, set `-s 0`.
- Capturing on the wrong interface and seeing nothing: list with `-D`, and use `any`, then narrow.
- Leaving a capture running or leaving pcaps around: they may contain credentials and personal data. Delete them after use.
- Reading a missing reply as a server fault: firewalls and security groups drop silently. Capture on both ends.

## Review
- [ ] The capture command and filter are recorded, along with the observed flags and counts.
- [ ] The conclusion names where packets stop (client, network, server).
- [ ] Capture files with sensitive content are deleted or protected.
- [ ] The fix was confirmed with a second capture or a successful request.
