# D4rkSploit

Framework personal de pruebas de penetración en Python, estilo Metasploit,
para tu propia máquina o un objetivo con permiso.

Consola tipo `msfconsole` con comandos `help`, `show modules`,
`use <modulo>`, `show options`, `set <opcion> <valor>`, `run`, `back` y `exit`.

## Módulos

- `vuln/http_headers` — revisa las cabeceras de seguridad de una web
  y dice cuáles faltan.

## Uso

```bash
python3 consola.py
```

```
darksploit> show modules
darksploit> use vuln/http_headers
darksploit(vuln/http_headers)> show options
darksploit(vuln/http_headers)> set URL https://example.com
darksploit(vuln/http_headers)> run
```

## Licencia

Licencia exclusiva y propietaria de Luis Antonio Angel Alencastro.
Ver `LICENSE`.
