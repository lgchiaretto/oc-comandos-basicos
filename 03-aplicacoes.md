# 🚀 Gerenciamento de Aplicações

Este documento contém comandos para criar e gerenciar aplicações no OpenShift.

---

## 📋 Índice

1. [Criação de Aplicações](#criação-de-aplicações)
2. [Gerenciamento](#gerenciamento)
3. [Estratégias de Deploy](#estratégias-de-deploy)
4. [Exemplos Práticos](#exemplos-práticos)

---

## 🆕 Criação de Aplicações

### A partir de Imagem Docker
```bash
# Criar aplicação a partir de imagem
oc new-app <nome-da-imagem>

# Exemplo com imagem pública
oc new-app nginx

# Imagem de registry customizado
oc new-app myregistry.com/myapp:latest

# Com nome personalizado
oc new-app nginx --name=meu-nginx
```

### A partir de Repositório Git
```bash
# Criar aplicação a partir de repositório Git
oc new-app <url-do-repositorio-git>

# Especificando branch
oc new-app <url-do-repositorio-git>#<branch>

# Exemplo prático
oc new-app https://github.com/sclorg/django-ex

# Branch específica
oc new-app https://github.com/sclorg/django-ex#develop
```

### Com Variáveis de Ambiente
```bash
# Criar aplicação com variáveis
oc new-app <imagem> -e VAR1=valor1 -e VAR2=valor2

# Exemplo
oc new-app mysql -e MYSQL_USER=user -e MYSQL_PASSWORD=pass
```

### A partir de Template
```bash
# Listar templates disponíveis
oc get templates -n openshift

# Criar a partir de template
oc new-app --template=<nome-do-template>

# Com parâmetros
oc new-app --template=mysql-persistent -p MYSQL_USER=admin
```

### Com Estratégia de Build
```bash
# Especificar estratégia de build
oc new-app <url-git> --strategy=docker
oc new-app <url-git> --strategy=source

# A partir de código local
oc new-app . --name=<nome-da-app>
```

---

## 🔧 Gerenciamento

### Listar Recursos
```bash
# Listar todas as aplicações
oc get all

# Listar recursos com labels
oc get all -l app=<nome-da-app>

# Listar apenas deployments
oc get deployment

# Listar services
oc get svc
```

### Deletar Aplicações
```bash
# Deletar aplicação e recursos relacionados
oc delete all -l app=<nome-da-app>

# Deletar por seletor
oc delete all --selector app=<nome-da-app>

# Deletar deployment específico
oc delete deployment <nome>
```

### Expor Aplicação
```bash
# Expor service como route
oc expose service <nome-do-service>

# Com hostname customizado
oc expose service <nome> --hostname=app.example.com

# Com TLS
oc create route edge --service=<nome>
```

---

## 📖 Navegação

- [← Anterior: Projetos](02-projetos.md)
- [→ Próximo: Pods e Containers](04-pods-containers.md)
- [↑ Índice Principal](README.md)

---

**Última atualização**: Outubro 2025
