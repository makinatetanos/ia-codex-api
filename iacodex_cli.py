#!/usr/bin/env python3
"""
CLI universal para interactuar con la IA Codex API desde cualquier editor o terminal.
Permite autocompletar, corregir y convertir código usando la API local.
"""
import argparse
import sys
import requests
import json

API_URL = "http://127.0.0.1:5000"


def complete_code(prompt, max_tokens=100, num_suggestions=1):
    resp = requests.post(f"{API_URL}/complete", json={
        "prompt": prompt,
        "max_tokens": max_tokens,
        "num_suggestions": num_suggestions
    })
    resp.raise_for_status()
    return resp.json()["suggestions"][0]


def fix_code(code):
    resp = requests.post(f"{API_URL}/fix", json={"code": code})
    resp.raise_for_status()
    return resp.json()["fixed_code"]


def convert_code(code, target_language):
    resp = requests.post(f"{API_URL}/convert", json={
        "code": code,
        "target_language": target_language
    })
    resp.raise_for_status()
    return resp.json()["converted_code"]


def main():
    parser = argparse.ArgumentParser(description="CLI para IA Codex API")
    subparsers = parser.add_subparsers(dest="command", required=True)

    parser_complete = subparsers.add_parser("complete", help="Autocompletar código")
    parser_complete.add_argument("-p", "--prompt", required=False, help="Código de entrada (si no se pasa, se lee de stdin)")
    parser_complete.add_argument("-m", "--max_tokens", type=int, default=100, help="Tokens máximos")
    parser_complete.add_argument("-n", "--num_suggestions", type=int, default=1, help="Número de sugerencias")

    parser_fix = subparsers.add_parser("fix", help="Corregir código")
    parser_fix.add_argument("-c", "--code", required=False, help="Código a corregir (si no se pasa, se lee de stdin)")

    parser_convert = subparsers.add_parser("convert", help="Convertir código entre lenguajes")
    parser_convert.add_argument("-c", "--code", required=False, help="Código a convertir (si no se pasa, se lee de stdin)")
    parser_convert.add_argument("-t", "--target_language", required=True, help="Lenguaje de destino")

    args = parser.parse_args()

    # Leer código de stdin si no se pasa por argumento
    if args.command == "complete":
        prompt = args.prompt if args.prompt else sys.stdin.read()
        print(complete_code(prompt, args.max_tokens, args.num_suggestions))
    elif args.command == "fix":
        code = args.code if args.code else sys.stdin.read()
        print(fix_code(code))
    elif args.command == "convert":
        code = args.code if args.code else sys.stdin.read()
        print(convert_code(code, args.target_language))

if __name__ == "__main__":
    main()
