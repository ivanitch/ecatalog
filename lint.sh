#!/bin/bash

# Останавливать выполнение, если любая команда завершилась с ошибкой
set -e

echo "--- Running flake8 ---"
flake8 catalog/

echo "--- Running black ---"
black catalog/

echo "--- Running isort ---"
isort catalog/

echo "--- Running mypy ---"
mypy catalog/

echo "--- All checks passed! ---"
