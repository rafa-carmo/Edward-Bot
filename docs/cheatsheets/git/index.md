---
title: Git Cheat Sheet
Author: Rafael do carmo
date: 2023-03-16
url_author: github.com/rafa-carmo
---

# Git Cheat Sheet

## Iniciar novo repositório
Passos para criação de um repositório
```

git init

git add .

git commit -m "first commit"

# Parametro
# -M: renomeia a branch atual para a nova selecionada
git branch -M main

git remote add origin <url do repositório>

#Parametro
# -u: Faz a branch main a upstream ( ou seja a principal para upload no remoto )
git push -u origin main

```
<br>
## Branches
Criar branch e trocar para ela
 
```
# Parametro
# -b: Após a criação ele troca para a branch criada

git checkout -b <branchname>
```
