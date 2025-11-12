#!/usr/bin/env python
import cmath, re, random

def fmt(z):
    a, b = round(z.real, 8), round(z.imag, 8)
    if abs(b) < 1e-9: return f"{a}"
    if abs(a) < 1e-9: return f"{b}i"
    return f"{a}{'+' if b>=0 else ''}{b}i"

def parse_complex(s: str) -> complex:
    s = s.replace('i', 'j')
    try:
        return complex(eval(s, {"__builtins__": {}}))
    except Exception:
        raise ValueError(f"Número complexo inválido: {s}")

def pedir_vars(expr):
    vars = sorted(set(re.findall(r'[a-zA-Z]+', expr)))
    vals = {}
    for v in vars:
        val = input(f"Valor de {v}: ")
        vals[v] = parse_complex(val)
    return vals

def substituir_vars(expr, vals):
    for v, z in vals.items():
        expr = re.sub(fr'\b{v}\b', f'({z})', expr)
    return expr

def avaliar(expr):
    expr = expr.replace('i','j')
    safe = {
        'sqrt': cmath.sqrt,
        'conj': lambda x: x.conjugate(),
        'root': lambda x,n: cmath.exp(cmath.log(x)/n)
    }
    try:
        return eval(expr, {"__builtins__": None}, safe)
    except ZeroDivisionError:
        raise ZeroDivisionError('Divisão por zero')
    except Exception as e:
        raise ValueError(f"Erro de sintaxe: {e}")

def comparar(expr1, expr2):
    vars = sorted(set(re.findall(r'[a-zA-Z]+', expr1 + expr2)))
    for _ in range(6):
        vals = {v: complex(random.uniform(-3,3), random.uniform(-3,3)) for v in vars}
        e1 = avaliar(substituir_vars(expr1, vals))
        e2 = avaliar(substituir_vars(expr2, vals))
        if abs(e1 - e2) > 1e-6:
            return False
    return True

def mostrar_arvore(expr, nivel=0):
    print('  '*nivel + expr)

def main():
    print('Calculadora complexa simples — digite * para Sair')
    ultima = None
    while True:
        s = input('> ').strip()
        if s in ('*',':quit'): break
        if not s: continue
        if s.startswith(':eq '):
            if not ultima: print('Nenhuma expressão anterior.'); continue
            expr2 = s[4:].strip()
            print('Iguais' if comparar(ultima, expr2) else 'Diferentes')
            continue
        if s == ':tree':
            if not ultima: print('Nenhuma expressão anterior.'); continue
            mostrar_arvore(ultima); continue
        try:
            ultima = s
            vals = pedir_vars(s)
            expr_ready = substituir_vars(s, vals)
            r = avaliar(expr_ready)
            print('Resultado:', fmt(r))
        except Exception as e:
            print('Erro:', e)

if __name__ == '__main__':
    main()
