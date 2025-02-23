import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from pathlib import Path

def setup_chrome_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Executar em modo headless
    chrome_options.add_argument("--window-size=390,844")  # Tamanho da janela
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    return webdriver.Chrome(options=chrome_options)

def create_print_directory():
    print_dir = Path("print")
    print_dir.mkdir(exist_ok=True)
    return print_dir

def capture_full_page_screenshot(driver, output_file):
    # Obter a altura total do documento
    total_height = driver.execute_script("return document.body.scrollHeight")
    
    # Definir o tamanho da janela para a altura total
    driver.set_window_size(390, total_height)

    # Capturar o screenshot da página inteira
    driver.save_screenshot(str(output_file))

def capture_screenshots():
    # Criar diretório para os screenshots
    print_dir = create_print_directory()
    
    try:
        # Inicializar o driver
        driver = setup_chrome_driver()
        
        # Encontrar todos os arquivos HTML no diretório atual
        html_files = [f for f in Path().glob("*.html") if f.is_file()]
        
        print(f"Encontrados {len(html_files)} arquivos HTML para processar.")
        
        for html_file in html_files:
            try:
                # Converter para URL absoluta
                file_url = f"file:///{os.path.abspath(html_file)}"
                print(f"Processando: {html_file.name}")
                
                # Carregar a página
                driver.get(file_url)
                
                # Aguardar um pouco para garantir que a página carregue completamente
                time.sleep(2)
                
                # Definir o nome do arquivo de saída
                output_file = print_dir / f"{html_file.stem}.png"
                
                # Capturar screenshot da página inteira
                capture_full_page_screenshot(driver, output_file)
                print(f"Screenshot salvo: {output_file}")
                
            except Exception as e:
                print(f"Erro ao processar {html_file}: {str(e)}")
                
        print("\nProcesso concluído!")
        
    except Exception as e:
        print(f"Erro ao inicializar o driver: {str(e)}")
        
    finally:
        try:
            driver.quit()
        except:
            pass

if __name__ == "__main__":
    capture_screenshots()
