# 🔍 MemInspector

Inspetor de Memória para macOS - Ferramenta para analisar o consumo de memória de aplicações e threads.

## 📋 Descrição

MemInspector é uma aplicação Python que permite inspecionar e analisar o consumo de memória das aplicações em execução no macOS. A ferramenta oferece:

- 📊 Lista dos processos que mais consomem memória
- 🧵 Análise detalhada das threads de cada processo
- 💻 Resumo do sistema (memória total, disponível, swap, etc.)
- 📈 Interface com barras de progresso usando tqdm
- 📉 Gráficos em tempo real
- 🔄 Modo de atualização contínua

## 🚀 Instalação

### Opção 1: Via Homebrew (Recomendado)

```bash
# Adicionar tap (após publicação)
brew tap yourusername/tap
brew install meminspector

# Executar
meminspector --help
```

Para instruções completas sobre como preparar o pacote Homebrew, veja [HOMEBREW_GUIDE.md](HOMEBREW_GUIDE.md).

### Opção 2: Via pip

```bash
# Instalar do repositório
pip install git+https://github.com/yourusername/meminspector.git

# Ou instalar localmente
git clone https://github.com/yourusername/meminspector.git
cd meminspector
pip install -e .
```

### Opção 3: Manual

### Opção 3: Manual

### Pré-requisitos

- Python 3.7 ou superior
- macOS (testado em macOS 10.15+)

### Passos de instalação

1. Clone ou faça download deste projeto

2. Instale as dependências:

```bash
pip install -r requirements.txt
```

Ou instale manualmente:

```bash
pip install psutil tqdm
```

## 📖 Como usar

### Instalado via Homebrew ou pip:

```bash
meminspector              # Lista todos os processos
meminspector --graph      # Mostra gráficos em tempo real
meminspector --refresh    # Atualização contínua no terminal
```

### Executando manualmente:

### Executando manualmente:

Execute o script principal:

```bash
python3 meminspector.py
```

Ou torne-o executável:

```bash
chmod +x meminspector.py
./meminspector.py
```

### Para usuários com permissões limitadas

Alguns processos do sistema podem requerer privilégios elevados. Para análise completa, execute com sudo:

```bash
sudo python meminspector.py
```

## 📊 Saída

A aplicação oferece três modos de operação:

### Modo Lista (--list ou padrão)
1. **Resumo do Sistema**: Informações sobre memória total, disponível, usada e swap
2. **Todos os Processos**: Lista completa dos processos ordenados por consumo de memória, incluindo:
   - PID (Process ID)
   - Nome do processo
   - Memória RSS (Resident Set Size)
   - Porcentagem de memória utilizada
   - Número de threads
   - Status do processo
3. **Análise de Threads**: Detalhamento das threads dos top 5 processos, mostrando:
   - Thread ID
   - Tempo de CPU do usuário
   - Tempo de CPU do sistema
   - Tempo total de CPU

### Modo Gráfico (--graph)
- Gráfico de linha mostrando uso de memória do sistema ao longo do tempo
- Gráfico de barras com os top N processos em tempo real
- Atualização automática em intervalos configuráveis

### Modo Refresh (--refresh)
- Atualização contínua no terminal
- Limpa a tela e mostra dados atualizados
- Ideal para monitoramento prolongado

## 🛠️ Funcionalidades

### Principais recursos

- ✅ Compatível com macOS
- ✅ Três modos de operação (lista, gráfico, refresh)
- ✅ Interface com barras de progresso (tqdm)
- ✅ Gráficos em tempo real com matplotlib
- ✅ Formatação legível de bytes (B, KB, MB, GB, TB)
- ✅ Ordenação automática por consumo de memória
- ✅ Análise de threads por processo
- ✅ Tratamento de erros para processos inacessíveis
- ✅ Interrupção segura (Ctrl+C)
- ✅ Argumentos de linha de comando configuráveis

### Opções de linha de comando

```
  -l, --list          Lista todos os processos (modo padrão)
  -g, --graph         Mostra gráficos em tempo real
  -r, --refresh       Atualização contínua no terminal
  -t, --top N         Número de processos a exibir (padrão: 10 para graph/refresh)
  -i, --interval N    Intervalo de atualização em segundos (padrão: 2.0)
  -a, --analyze N     Número de processos para análise de threads (padrão: 5)
```

### Exemplos de uso

```bash
# Lista todos os processos uma vez
meminspector
meminspector --list

# Gráficos em tempo real
meminspector --graph
meminspector -g -t 15 -i 1    # Top 15, atualiza a cada 1 segundo

# Refresh contínuo no terminal
meminspector --refresh
meminspector -r -t 20 -i 3    # Top 20, atualiza a cada 3 segundos

# Modo lista com mais análises
meminspector --list --analyze 10
```

## 📦 Dependências

- **psutil**: Biblioteca para obter informações de processos e sistema
- **tqdm**: Biblioteca para criar barras de progresso
- **matplotlib**: Biblioteca para criar gráficos em tempo real

## 🔧 Desenvolvimento

### Instalar em modo desenvolvimento

```bash
git clone https://github.com/yourusername/meminspector.git
cd meminspector
pip install -e .
```

### Criar distribuição

```bash
# Instalar ferramentas de build
pip install build twine

# Criar distribuição
python -m build

# Upload para PyPI (quando pronto)
twine upload dist/*
```

### Publicar no Homebrew

Veja o guia completo em [HOMEBREW_GUIDE.md](HOMEBREW_GUIDE.md)

## 🔧 Personalização

Você pode ajustar os parâmetros na linha de comando ou modificando o código:

```python
inspector.run(
    top_processes=None,      # None = todos, ou especifique um número
    analyze_threads_count=5  # Número de processos para análise de threads
)
```

## 📝 Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

- Alguns processos do sistema podem não ser acessíveis sem privilégios de administrador
- A análise pode levar alguns segundos dependendo do número de processos em execução
- O consumo de CPU durante a análise é mínimo devido aos delays implementados

## 🐛 Solução de Problemas

### Erro de permissão

Se você receber erros de "Access Denied", execute com sudo:

```bash
sudo python meminspector.py
```

### Módulos não encontrados

Certifique-se de que instalou todas as dependências:

```bash
pip install -r requirements.txt
```

## 📝 Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

## ⚠️ Avisos

## 🤝 Contribuições

Sugestões e melhorias são bem-vindas!

## 📧 Contato

Para questões ou sugestões, abra uma issue no repositório.

---

Desenvolvido com ❤️ para macOS
