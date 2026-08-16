# Stockfish as a network service.
#
# Stockfish speaks UCI over stdin/stdout, so socat puts it on a TCP port. Every
# connection forks its own engine process: no shared state between requests, and
# a crashed search cannot take the service down with it.
FROM debian:trixie-slim

RUN apt-get update \
    && apt-get install -y --no-install-recommends stockfish socat \
    && rm -rf /var/lib/apt/lists/*

ENV ENGINE_PORT=23249

# Unprivileged: the engine never needs to write anything.
RUN useradd --system --no-create-home --shell /usr/sbin/nologin engine
USER engine

EXPOSE 23249

HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD printf 'uci\nquit\n' | socat -T3 - TCP:127.0.0.1:${ENGINE_PORT} | grep -q uciok

# `fork` gives each client its own process; `reuseaddr` lets the container
# restart without waiting for the socket to drain.
CMD ["sh", "-c", "exec socat TCP-LISTEN:${ENGINE_PORT},fork,reuseaddr EXEC:/usr/games/stockfish"]
