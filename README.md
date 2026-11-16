# D4rkSploit

Framework personal de pruebas de penetración en Python, estilo Metasploit,
para tu propia máquina o un objetivo con permiso.

Consola tipo `msfconsole`, con comandos en español
(también funcionan en inglés, como en Metasploit):
`ayuda`, `mostrar modulos`, `usar <modulo>`, `mostrar opciones`,
`poner <opcion> <valor>`, `correr`, `volver` y `salir`.

## Módulos

- `vuln/http_headers` — revisa las cabeceras de seguridad de una web
  y dice cuáles faltan.

## Uso

```bash
python3 consola.py
```

```
darksploit> mostrar modulos
darksploit> usar vuln/http_headers
darksploit(vuln/http_headers)> mostrar opciones
darksploit(vuln/http_headers)> poner URL https://example.com
darksploit(vuln/http_headers)> correr
```

## Licencia

Licencia exclusiva y propietaria de Luis Antonio Angel Alencastro.
Ver `LICENSE`.
