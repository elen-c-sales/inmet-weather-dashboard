from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime, timedelta
import time
import os

# Define datas: últimos 30 dias até hoje
hoje = datetime.today()
inicio = hoje - timedelta(days=30)
DATA_INICIO = inicio.strftime("%d%m%Y")
DATA_FIM = hoje.strftime("%d%m%Y")

URL = "https://tempo.inmet.gov.br/TabelaEstacoes"
PASTA_DOWNLOADS = os.path.join(os.path.expanduser("~"), "Downloads")

# Configuração do navegador
options = webdriver.ChromeOptions()
prefs = {
    "download.default_directory": PASTA_DOWNLOADS,
    "download.prompt_for_download": False,
    "directory_upgrade": True
}
options.add_experimental_option("prefs", prefs)

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
wait = WebDriverWait(driver, 20)

try:
    driver.get(URL)

    # Clica no menu (três barras)
    wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "bars.icon.header-icon"))).click()
    time.sleep(1)

    # Clica no botão "Automáticas" (se necessário)
    tipo_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Automáticas']")))
    driver.execute_script("arguments[0].click();", tipo_btn)
    time.sleep(1)

    # Lista todos os campos de busca dos dropdowns
    inputs_busca = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//div[@role='combobox']//input[@class='search']")))

    # === ESTADO ===
    estado_input = inputs_busca[1]  # Segundo campo (índice 1) é Estado
    estado_input.send_keys("pa")
    time.sleep(1)
    estado_opcao = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@role='option']//span[contains(text(), 'Pará')]")))
    estado_opcao.click()
    print("Estado 'Pará' selecionado.")
    time.sleep(1)

    # === ESTAÇÃO ===
    estacao_input = inputs_busca[2]  # Terceiro campo (índice 2) é Estação
    estacao_input.send_keys("bra")
    time.sleep(1)
    estacao_opcao = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@role='option']//span[contains(text(), 'BRAGANCA (A226)')]")))
    estacao_opcao.click()
    print("Estação 'BRAGANCA (A226)' selecionada.")
    time.sleep(1)

    # Preenche as datas digitando diretamente nos inputs
    input_datas = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//input[@type='date']")))
    data_ini_input, data_fim_input = input_datas[0], input_datas[1]

    # Clica no ícone para focar no início do campo de data
    icone_data_ini = driver.find_element(By.XPATH, "(//i[@class='calendar icon'])[1]")
    driver.execute_script("arguments[0].click();", icone_data_ini)
    time.sleep(0.5)
    data_ini_input.send_keys(Keys.CONTROL, "a", Keys.BACKSPACE)
    data_ini_input.send_keys(DATA_INICIO)

    icone_data_fim = driver.find_element(By.XPATH, "(//i[@class='calendar icon'])[2]")
    driver.execute_script("arguments[0].click();", icone_data_fim)
    time.sleep(0.5)
    data_fim_input.send_keys(Keys.CONTROL, "a", Keys.BACKSPACE)
    data_fim_input.send_keys(DATA_FIM)


    # Clica em "Gerar Tabela"
    gerar = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Gerar Tabela']")))
    gerar.click()
    print("Tabela gerada...")
    time.sleep(5)

    # Clica em "Baixar CSV"
    baixar = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(),'Baixar CSV')]")))
    baixar.click()
    print("Download iniciado...")

    time.sleep(10)

finally:
    driver.quit()

print("Concluído.")
