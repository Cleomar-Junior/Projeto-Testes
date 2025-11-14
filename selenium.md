![Relatório de Cobertura de Testes](TDD.png)

# Testes usando Selenium

# Testes com Selenium

## Introdução ao Selenium
O **Selenium** é uma ferramenta de automação usada para realizar **testes em aplicações web**.  
Ele simula ações reais de um usuário — como cliques, preenchimento de formulários e navegação — diretamente no navegador.

### Vantagens
- Gratuito e **open source**  
- Suporte a vários **navegadores** e **sistemas operacionais**  
- Integração com frameworks de teste como **pytest** e **unittest**

### Limitações
- Não testa aplicações desktop  
- Pode ser sensível a mudanças no layout do site  
- Requer configuração de *WebDrivers* compatíveis com o navegador  

### Linguagens Suportadas
- **Python**, **Java**, **C#**, **Ruby**, **JavaScript**, entre outras.  

---

## Conceitos Fundamentais
O **WebDriver** é o componente principal do Selenium — ele é responsável por **controlar o navegador** e interagir com os elementos da página.

### Como o Selenium interage com o DOM
Ele acessa o **DOM (Document Object Model)** da página e identifica os elementos HTML através de seletores.

### Tipos de Seletores
- **ID** → `find_element(By.ID, "id_do_elemento")`  
- **Name** → `find_element(By.NAME, "nome")`  
- **CSS Selector** → `find_element(By.CSS_SELECTOR, ".classe")`  
- **XPath** → `find_element(By.XPATH, "//input[@type='text']")`  

### Diferença entre `find_element` e `find_elements`
- `find_element` → retorna **um único** elemento  
- `find_elements` → retorna **uma lista** de elementos correspondentes  

---

## Automação Básica de Navegação
O Selenium permite **abrir, fechar e navegar** entre páginas automaticamente.

- **Abrir página:** `driver.get("https://exemplo.com")`  
- **Navegar:** `driver.back()`, `driver.forward()`, `driver.refresh()`  
- **Capturar título e URL:** `driver.title`, `driver.current_url`  
- **Captura de tela:** `driver.save_screenshot("imagem.png")`  

---

## Interação com Elementos
O Selenium pode **interagir com qualquer elemento HTML** da página.

- **Preencher campos:** `element.send_keys("texto")`  
- **Clicar:** `element.click()`  
- **Selecionar opções:** via classe `Select` para `<select>`  
- **Alertas e pop-ups:** `driver.switch_to.alert.accept()`  
- **Enviar formulários:** `element.submit()`  

Essas ações simulam o comportamento real de um usuário navegando no site.

---

## Estrutura de Testes Automatizados
Para manter o código limpo e escalável, recomenda-se **separar o código de automação da lógica de teste**.

### Boas Práticas
- Centralizar funções repetidas (login, navegação, etc.)  
- Nomear testes de forma clara  
- Evitar esperas fixas com `sleep` — usar esperas explícitas  

### Page Object Model (POM)
Padrão que organiza o código em **classes representando páginas**, facilitando manutenção e reutilização.

---

## Integração com Frameworks de Teste
O Selenium pode ser integrado a frameworks para estruturar e automatizar execuções.

### Exemplos
- **unittest (Python)** → framework padrão da linguagem  
- **pytest** → mais moderno, simples e com geração automática de relatórios  

### Estrutura típica
- **Setup:** abre o navegador e prepara o ambiente  
- **Teste:** executa ações e faz validações  
- **Teardown:** fecha o navegador após o teste  

---

## 🚀 7. Exemplo Prático
```python
from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()
driver.get("https://www.google.com")

campo = driver.find_element(By.NAME, "q")
campo.send_keys("Selenium WebDriver\n")

print("Título da página:", driver.title)
driver.quit()
