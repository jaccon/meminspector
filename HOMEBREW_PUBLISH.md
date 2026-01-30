# Como Publicar no Homebrew

Este guia explica como publicar o MemInspector no Homebrew para que usuários possam instalar com `brew install`.

## 📋 Opções de Publicação

Existem duas formas principais:

### 1. **Criar um Tap Próprio** (Recomendado)
- Mais rápido e fácil
- Você mantém controle total
- Usuários instalam: `brew tap jaccon/tap && brew install meminspector`

### 2. **Submeter para Homebrew Core**
- Processo mais complexo e demorado
- Revisão pela equipe Homebrew
- Usuários instalam: `brew install meminspector` (direto)

---

## 🚀 Método 1: Criar Seu Próprio Tap (Recomendado)

### Passo 1: Criar Repositório do Tap no GitHub

1. Vá para GitHub e crie um novo repositório
2. **Nome obrigatório**: `homebrew-tap` (deve começar com `homebrew-`)
3. URL final: `https://github.com/jaccon/homebrew-tap`
4. Deixe público
5. Não inicialize com README (vamos criar localmente)

### Passo 2: Configurar o Tap Localmente

```bash
# Criar estrutura local
mkdir ~/homebrew-tap
cd ~/homebrew-tap

# Criar diretório Formula
mkdir Formula

# Copiar a fórmula
cp /Users/jaccon/Documents/meminspector/meminspector.rb Formula/

# Inicializar Git
git init
git add .
git commit -m "Add meminspector formula v1.1.0"

# Conectar com GitHub
git remote add origin https://github.com/jaccon/homebrew-tap.git
git branch -M main
git push -u origin main
```

### Passo 3: Atualizar o SHA256 na Fórmula

Você precisa calcular o SHA256 do arquivo da release:

```bash
# Baixar a release
curl -L https://github.com/jaccon/meminspector/archive/refs/tags/v1.1.0.tar.gz -o meminspector-1.1.0.tar.gz

# Calcular SHA256
shasum -a 256 meminspector-1.1.0.tar.gz
```

Edite `Formula/meminspector.rb` e substitua `YOUR_SHA256_HASH_HERE` pelo hash obtido.

```bash
# Commit a mudança
git add Formula/meminspector.rb
git commit -m "Update SHA256 hash"
git push origin main
```

### Passo 4: Testar Localmente

```bash
# Testar instalação do tap
brew tap jaccon/tap

# Verificar se a fórmula foi encontrada
brew info meminspector

# Instalar
brew install meminspector

# Testar
meminspector --help
meminspector --tui
```

### Passo 5: Compartilhar com Usuários

Usuários agora podem instalar com:

```bash
brew tap jaccon/tap
brew install meminspector
```

Ou em uma única linha:

```bash
brew install jaccon/tap/meminspector
```

---

## 🏆 Método 2: Submeter para Homebrew Core (Opcional)

Este método coloca seu pacote no repositório oficial do Homebrew.

### Requisitos

- Projeto deve ser estável e maduro
- Ter usuários significativos
- Código bem documentado
- Testes automatizados
- Licença open source
- Seguir as [diretrizes do Homebrew](https://docs.brew.sh/Acceptable-Formulae)

### Processo

#### 1. Fork do homebrew-core

```bash
# No GitHub, faça fork de:
# https://github.com/Homebrew/homebrew-core
```

#### 2. Clone e Configure

```bash
cd "$(brew --repository homebrew/core)"
git remote add jaccon https://github.com/jaccon/homebrew-core.git
```

#### 3. Criar Branch

```bash
git checkout -b meminspector
```

#### 4. Adicionar Fórmula

```bash
# Copiar fórmula para o local correto
cp /Users/jaccon/Documents/meminspector/meminspector.rb Formula/meminspector.rb

# Editar se necessário para seguir diretrizes
brew edit meminspector
```

#### 5. Testar Rigorosamente

```bash
# Audit completo
brew audit --new-formula meminspector

# Teste de instalação
brew install --build-from-source meminspector

# Executar testes
brew test meminspector

# Verificar estilo
brew style meminspector
```

#### 6. Commit e Push

```bash
git add Formula/meminspector.rb
git commit -m "meminspector 1.1.0 (new formula)"
git push jaccon meminspector
```

#### 7. Criar Pull Request

1. Vá para https://github.com/Homebrew/homebrew-core
2. Clique em "Pull requests"
3. "New pull request"
4. Compare: `homebrew:master` <- `jaccon:meminspector`
5. Título: `meminspector 1.1.0 (new formula)`
6. Descrição:
   ```markdown
   ## Description
   Memory Inspector for macOS - Analyze memory consumption of applications and threads with Docker support
   
   ## Features
   - Colored terminal interface (TUI)
   - Monitor system processes and memory usage
   - Docker container monitoring
   - Real-time graphs with matplotlib
   - Multiple operation modes
   
   ## License
   MIT
   
   ## Homepage
   https://github.com/jaccon/meminspector
   ```

#### 8. Aguardar Revisão

- Mantenedores do Homebrew vão revisar
- Podem pedir mudanças
- Processo pode levar dias/semanas
- Seja paciente e responda prontamente

---

## 📦 Estrutura do Tap

Seu repositório `homebrew-tap` deve ter esta estrutura:

```
homebrew-tap/
├── Formula/
│   └── meminspector.rb
└── README.md (opcional)
```

---

## 🔄 Atualizando a Fórmula

Quando lançar uma nova versão:

### 1. Criar Nova Release

```bash
cd /Users/jaccon/Documents/meminspector

# Atualizar versão em setup.py
# Atualizar CHANGELOG.md

git add .
git commit -m "Version 1.2.0"
git tag -a v1.2.0 -m "Version 1.2.0"
git push origin main
git push origin v1.2.0
```

### 2. Calcular Novo SHA256

```bash
curl -L https://github.com/jaccon/meminspector/archive/refs/tags/v1.2.0.tar.gz | shasum -a 256
```

### 3. Atualizar Fórmula no Tap

```bash
cd ~/homebrew-tap

# Editar Formula/meminspector.rb
# - Atualizar version
# - Atualizar url
# - Atualizar sha256

git add Formula/meminspector.rb
git commit -m "Update meminspector to v1.2.0"
git push origin main
```

### 4. Usuários Atualizam

```bash
brew update
brew upgrade meminspector
```

---

## ✅ Checklist de Publicação

### Antes de Publicar:

- [ ] Código está no GitHub (github.com/jaccon/meminspector)
- [ ] Release v1.1.0 criada
- [ ] SHA256 calculado
- [ ] Fórmula testada localmente (`brew install --build-from-source`)
- [ ] Todos os testes passam
- [ ] README atualizado com instruções de instalação

### Para Tap Próprio:

- [ ] Repositório `homebrew-tap` criado no GitHub
- [ ] Fórmula adicionada em `Formula/meminspector.rb`
- [ ] SHA256 correto na fórmula
- [ ] Push realizado
- [ ] Testado: `brew tap jaccon/tap && brew install meminspector`

### Para Homebrew Core (opcional):

- [ ] Fork de homebrew-core criado
- [ ] Branch criada
- [ ] Fórmula passa em `brew audit --strict`
- [ ] Fórmula passa em `brew test`
- [ ] Pull request criado
- [ ] Respondendo a revisões

---

## 🐛 Resolução de Problemas

### "SHA256 mismatch"

Recalcule o SHA256 e atualize a fórmula:

```bash
curl -L https://github.com/jaccon/meminspector/archive/refs/tags/v1.1.0.tar.gz | shasum -a 256
```

### "Formula not found"

Verifique se o tap foi adicionado:

```bash
brew tap jaccon/tap
brew tap  # Listar taps instalados
```

### "Build failed"

Teste localmente com mais detalhes:

```bash
brew install --build-from-source --verbose --debug meminspector
```

### Desinstalar e Reinstalar

```bash
brew uninstall meminspector
brew untap jaccon/tap
brew tap jaccon/tap
brew install meminspector
```

---

## 📚 Recursos Úteis

- [Homebrew Formula Cookbook](https://docs.brew.sh/Formula-Cookbook)
- [Python for Formula Authors](https://docs.brew.sh/Python-for-Formula-Authors)
- [How to Create a Tap](https://docs.brew.sh/How-to-Create-and-Maintain-a-Tap)
- [Acceptable Formulae](https://docs.brew.sh/Acceptable-Formulae)
- [Homebrew Pull Request Guide](https://docs.brew.sh/How-To-Open-a-Homebrew-Pull-Request)

---

## 🎯 Resumo Rápido

**Para usuários finais instalarem seu app:**

1. Crie repositório `homebrew-tap` no GitHub
2. Adicione fórmula em `Formula/meminspector.rb`
3. Usuários executam:
   ```bash
   brew tap jaccon/tap
   brew install meminspector
   ```

**É isso! Simples e direto.** 🚀
