# Gerenciamento de Aplicações

Este documento contém comandos para criar e gerenciar aplicações no OpenShift.

---

## Índice

1. [Índice](#índice)
2. [Criação de Aplicações](#criação-de-aplicações)
3. [Gerenciamento](#gerenciamento)
4. [Informações e Status](#informações-e-status)
5. [Atualização de Imagens](#atualização-de-imagens)
6. [Permissões e Validações](#permissões-e-validações)
7. [⏳ Aguardar Condições](#⏳-aguardar-condições)
8. [Documentação Oficial](#documentação-oficial)
9. [Navegação](#navegação)
---

## Criação de Aplicações

### A partir de Imagem Docker
```bash ignore-test
# Criar aplicação a partir de imagem
oc new-app <nome-da-imagem>
```

```bash ignore-test
# Exemplo com imagem pública
oc new-app nginx
```

```bash ignore-test
# Criar nova aplicação a partir de imagem ou código fonte
oc new-app myregistry.com/myapp:latest
```

```bash ignore-test
# Criar aplicação com nome customizado
oc new-app nginx --name=meu-nginx
```

```bash
# Exemplo com httpd
# oc new-app httpd:latest --name=test-app -n <namespace>
oc new-app httpd:latest --name=test-app -n development
```

### A partir de Repositório Git
```bash ignore-test
# Criar aplicação a partir de repositório Git
oc new-app <url-do-repositorio-git>
```

```bash ignore-test
# Especificando branch
oc new-app <url-do-repositorio-git>#<branch>
```

```bash
# Exemplo prático de new-app usando s2i
oc new-app https://github.com/lgchiaretto/s2i-chiaretto.git --name=s2i-chiaretto
```

### Com Variáveis de Ambiente
```bash ignore-test
# Criar aplicação com variáveis
oc new-app <imagem> -e VAR1=valor1 -e VAR2=valor2
```

```bash ignore-test
# Exemplo
oc new-app mysql -e MYSQL_USER=user -e MYSQL_PASSWORD=pass
```

### A partir de Template
```bash
# Listar templates disponíveis no namespace openshift
oc get templates -n openshift
```

```bash ignore-test
# Criar a partir de template
oc new-app --template=<nome-do-template>
```

```bash ignore-test
# Criar aplicação a partir de template
oc new-app --template=mysql-persistent -p MYSQL_USER=admin
```

### Com Estratégia de Build
```bash ignore-test
# Especificar estratégia de build
oc new-app <url-git> --strategy=docker
```
```bash  ignore
oc new-app <url-git> --strategy=source
```

```bash ignore-test
# Criar aplicação com nome customizado
oc new-app . --name=test-app
```

---

## Gerenciamento

### Listar Recursos
```bash
# Listar todos os recursos principais do namespace
oc get all
```

```bash
# Listar recurso filtrados por label
oc get all -l app=test-app
```

```bash
# Listar todos os deployments do namespace
oc get deployment
```

```bash
# Listar todos os services do namespace atual
oc get svc
```

```bash
# Listar todas as routes expostas no namespace
oc get routes
```

```bash
# Listar routes em um namespace específico
oc get routes -n development
```

```bash
# Listar todas as ImageStreams do projeto
oc get is
```

```bash
# Listar ImageStreams em um projeto
oc get is -n development
```

### Deletar Aplicações
```bash ignore-test
# Deletar recurso que correspondem ao seletor de label
oc delete all -l app=test-app
```

```bash ignore-test
# Deletar recurso que correspondem ao seletor de label
oc delete all --selector app=test-app
```

```bash ignore-test
# Deletar o recurso especificado
# oc delete deployment <deployment-name>
oc delete deployment test-app
```

### Expor Aplicação
```bash ignore-test
# Criar route para expor service externamente
# oc expose service <service-name>
oc expose service test-app
```

```bash ignore-test
# Criar route com hostname customizado para o service
# oc expose service <service-name> --hostname=app.example.com
oc expose service test-app --hostname=app.example.com
```

```bash
# Criar route com terminação TLS edge (TLS terminado no router)
# oc create route <route-name> --service=test-app
oc create route edge --service=test-app
```

---

## Informações e Status

### Status do Projeto
```bash
# Exibir visão geral dos recursos do projeto atual
oc status
```

```bash
# Status de um projeto específico
# oc status -n <namespace>
oc status -n development
```

### Descrever Recursos
```bash
# Exibir detalhes completos do recurso
# oc describe deployment <deployment-name>
oc describe deployment test-app
```

```bash
# Exibir detalhes completos do recurso
# oc describe deployment <deployment-name> -n <namespace>
oc describe deployment test-app -n development
```

---

## Atualização de Imagens

### Atualizar Imagem do Deployment
```bash
# Atualizar imagem do container no deployment/pod
# oc set image <resource-name>/test-app httpd=httpd:2.4 -n <namespace>
oc set image deployment/test-app httpd=httpd:2.4 -n development
```

```bash ignore-test
# Atualizar imagem do container no deployment/pod
# oc set image <resource-name>/test-app container1=image1:tag container2=image2:tag
oc set image deployment/test-app container1=image1:tag container2=image2:tag
```

### Patch de Deployment
```bash
# Aplicar merge patch ao recurso (mescla alterações)
# oc patch deployment <deployment-name> -n <namespace> --type=merge -p '{"spec":{"replicas":3}}'
oc patch deployment test-app -n development --type=merge -p '{"spec":{"replicas":3}}'
```

```bash
# Aplicar merge patch ao recurso (mescla alterações)
# oc patch deployment <deployment-name> -n <namespace> --type=merge -p '{"spec":{"template":{"spec":{"containers":[{"name":"httpd","image":"httpd:latest"}]}}}}'
oc patch deployment test-app -n development --type=merge -p '{"spec":{"template":{"spec":{"containers":[{"name":"httpd","image":"httpd:latest"}]}}}}'
```

---

## Permissões e Validações

### Verificar Permissões
```bash
# Verificar se usuário tem permissão para executar ação específica
oc auth can-i create deployments
```

```bash
# Verificar se usuário tem permissão para executar ação específica
# oc auth can-i create deployments -n <namespace>
oc auth can-i create deployments -n development
```

```bash
# Verificar se usuário tem permissão para executar ação específica
# oc auth can-i delete pods -n <namespace>
oc auth can-i delete pods -n development
# oc auth can-i get secrets -n <namespace>
oc auth can-i get secrets -n development
```

---

## ⏳ Aguardar Condições

### Wait para Deployment
```bash
# Aguardar deployment ficar disponível
# oc wait --for=condition=available deployment/<deployment-name>
oc wait --for=condition=available deployment/test-app
```

```bash
# Aguardar deployment ficar disponível
# oc wait --for=condition=available --timeout=60s deployment/<deployment-name>
oc wait --for=condition=available --timeout=60s deployment/test-app
```

```bash
# Aguardar deployment ficar disponível
# oc wait --for=condition=available --timeout=60s deployment/test-app -n <namespace>
oc wait --for=condition=available --timeout=60s deployment/test-app -n development
```
## Documentação Oficial

Consulte a documentação oficial do OpenShift 4.19 da Red Hat:

- <a href="https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/building_applications">Building applications</a>
- <a href="https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/cli_tools/developer-cli-odo">Developer CLI (odo)</a>
- <a href="https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/building_applications/deployments">Deployments</a>
- <a href="https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/images">Images - Using templates</a>
---

---

## Navegação

- [← Anterior: Projetos](02-projetos.md)
- [→ Próximo: Pods e Containers](04-pods-containers.md)
- [↑ Índice Principal](README.md)

---

**Última atualização**: Outubro 2025
